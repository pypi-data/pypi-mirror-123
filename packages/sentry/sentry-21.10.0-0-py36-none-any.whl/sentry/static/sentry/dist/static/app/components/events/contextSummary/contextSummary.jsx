Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const contextSummaryDevice_1 = (0, tslib_1.__importDefault)(require("./contextSummaryDevice"));
const contextSummaryGeneric_1 = (0, tslib_1.__importDefault)(require("./contextSummaryGeneric"));
const contextSummaryGPU_1 = (0, tslib_1.__importDefault)(require("./contextSummaryGPU"));
const contextSummaryOS_1 = (0, tslib_1.__importDefault)(require("./contextSummaryOS"));
const contextSummaryUser_1 = (0, tslib_1.__importDefault)(require("./contextSummaryUser"));
const filterContexts_1 = (0, tslib_1.__importDefault)(require("./filterContexts"));
const MIN_CONTEXTS = 3;
const MAX_CONTEXTS = 4;
const KNOWN_CONTEXTS = [
    { keys: ['user'], Component: contextSummaryUser_1.default },
    {
        keys: ['browser'],
        Component: contextSummaryGeneric_1.default,
        unknownTitle: (0, locale_1.t)('Unknown Browser'),
    },
    {
        keys: ['runtime'],
        Component: contextSummaryGeneric_1.default,
        unknownTitle: (0, locale_1.t)('Unknown Runtime'),
    },
    { keys: ['client_os', 'os'], Component: contextSummaryOS_1.default },
    { keys: ['device'], Component: contextSummaryDevice_1.default },
    { keys: ['gpu'], Component: contextSummaryGPU_1.default },
];
class ContextSummary extends React.Component {
    render() {
        const { event } = this.props;
        let contextCount = 0;
        // Add defined contexts in the declared order, until we reach the limit
        // defined by MAX_CONTEXTS.
        let contexts = KNOWN_CONTEXTS.filter(context => (0, filterContexts_1.default)(event, context)).map(({ keys, Component, unknownTitle }) => {
            if (contextCount >= MAX_CONTEXTS) {
                return null;
            }
            const [key, data] = keys
                .map(k => [k, event.contexts[k] || event[k]])
                .find(([_k, d]) => !(0, utils_1.objectIsEmpty)(d)) || [null, null];
            if (!key) {
                return null;
            }
            contextCount += 1;
            return <Component key={key} data={data} unknownTitle={unknownTitle}/>;
        });
        // Bail out if all contexts are empty or only the user context is set
        if (contextCount === 0 || (contextCount === 1 && contexts[0])) {
            return null;
        }
        if (contextCount < MIN_CONTEXTS) {
            // Add contents in the declared order until we have at least MIN_CONTEXTS
            // contexts in our list.
            contexts = KNOWN_CONTEXTS.filter(context => (0, filterContexts_1.default)(event, context)).map(({ keys, Component, unknownTitle }, index) => {
                if (contexts[index]) {
                    return contexts[index];
                }
                if (contextCount >= MIN_CONTEXTS) {
                    return null;
                }
                contextCount += 1;
                return <Component key={keys[0]} data={{}} unknownTitle={unknownTitle}/>;
            });
        }
        return <Wrapper className="context-summary">{contexts}</Wrapper>;
    }
}
exports.default = ContextSummary;
const Wrapper = (0, styled_1.default)('div') `
  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    display: flex;
    gap: ${(0, space_1.default)(3)};
    margin-bottom: ${(0, space_1.default)(2)};
  }
`;
//# sourceMappingURL=contextSummary.jsx.map