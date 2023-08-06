Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const annotatedText_1 = (0, tslib_1.__importDefault)(require("app/components/events/meta/annotatedText"));
const metaProxy_1 = require("app/components/events/meta/metaProxy");
const textOverflow_1 = (0, tslib_1.__importDefault)(require("app/components/textOverflow"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const contextSummaryNoSummary_1 = (0, tslib_1.__importDefault)(require("./contextSummaryNoSummary"));
const generateClassName_1 = (0, tslib_1.__importDefault)(require("./generateClassName"));
const item_1 = (0, tslib_1.__importDefault)(require("./item"));
const ContextSummaryOS = ({ data }) => {
    if (Object.keys(data).length === 0 || !data.name) {
        return <contextSummaryNoSummary_1.default title={(0, locale_1.t)('Unknown OS')}/>;
    }
    const renderName = () => {
        const meta = (0, metaProxy_1.getMeta)(data, 'name');
        return <annotatedText_1.default value={data.name} meta={meta}/>;
    };
    const getVersionElement = () => {
        if (data.version) {
            return {
                subject: (0, locale_1.t)('Version:'),
                value: data.version,
                meta: (0, metaProxy_1.getMeta)(data, 'version'),
            };
        }
        if (data.kernel_version) {
            return {
                subject: (0, locale_1.t)('Kernel:'),
                value: data.kernel_version,
                meta: (0, metaProxy_1.getMeta)(data, 'kernel_version'),
            };
        }
        return {
            subject: (0, locale_1.t)('Version:'),
            value: (0, locale_1.t)('Unknown'),
        };
    };
    const versionElement = getVersionElement();
    const className = (0, generateClassName_1.default)(data.name);
    return (<item_1.default className={className} icon={<span className="context-item-icon"/>}>
      <h3>{renderName()}</h3>
      <textOverflow_1.default isParagraph data-test-id="context-sub-title">
        <Subject>{versionElement.subject}</Subject>
        <annotatedText_1.default value={versionElement.value} meta={versionElement.meta}/>
      </textOverflow_1.default>
    </item_1.default>);
};
exports.default = ContextSummaryOS;
const Subject = (0, styled_1.default)('strong') `
  margin-right: ${(0, space_1.default)(0.5)};
`;
//# sourceMappingURL=contextSummaryOS.jsx.map