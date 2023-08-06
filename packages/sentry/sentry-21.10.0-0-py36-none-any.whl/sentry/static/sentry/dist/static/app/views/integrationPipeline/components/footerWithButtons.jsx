Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/actions/button"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
function FooterWithButtons(_a) {
    var { buttonText } = _a, rest = (0, tslib_1.__rest)(_a, ["buttonText"]);
    return (<Footer>
      <button_1.default priority="primary" type="submit" size="xsmall" {...rest}>
        {buttonText}
      </button_1.default>
    </Footer>);
}
exports.default = FooterWithButtons;
// wrap in form so we can keep form submission behavior
const Footer = (0, styled_1.default)('form') `
  width: 100%;
  position: fixed;
  display: flex;
  justify-content: flex-end;
  bottom: 0;
  z-index: 100;
  background-color: ${p => p.theme.bodyBackground};
  border-top: 1px solid ${p => p.theme.innerBorder};
  padding: ${(0, space_1.default)(2)};
`;
//# sourceMappingURL=footerWithButtons.jsx.map