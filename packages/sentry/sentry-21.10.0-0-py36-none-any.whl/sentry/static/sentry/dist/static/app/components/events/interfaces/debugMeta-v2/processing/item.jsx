Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
function Item({ type, icon, className }) {
    function getLabel() {
        switch (type) {
            case 'stack_unwinding':
                return (0, locale_1.t)('Stack Unwinding');
            case 'symbolication':
                return (0, locale_1.t)('Symbolication');
            default: {
                Sentry.captureException(new Error('Unknown Images Loaded processing item type'));
                return null; // This shall not happen
            }
        }
    }
    return (<Wrapper className={className}>
      {icon}
      {getLabel()}
    </Wrapper>);
}
exports.default = Item;
const Wrapper = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: max-content 1fr;
  grid-column-gap: ${(0, space_1.default)(0.5)};
  align-items: center;
  font-size: ${p => p.theme.fontSizeSmall};
  white-space: nowrap;
`;
//# sourceMappingURL=item.jsx.map