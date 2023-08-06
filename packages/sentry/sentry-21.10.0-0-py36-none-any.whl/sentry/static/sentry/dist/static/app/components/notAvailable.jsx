Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const utils_1 = require("app/utils");
function NotAvailable({ tooltip, className }) {
    return (<Wrapper className={className}>
      <tooltip_1.default title={tooltip} disabled={!(0, utils_1.defined)(tooltip)}>
        {'\u2014'}
      </tooltip_1.default>
    </Wrapper>);
}
const Wrapper = (0, styled_1.default)('div') `
  color: ${p => p.theme.gray200};
`;
exports.default = NotAvailable;
//# sourceMappingURL=notAvailable.jsx.map