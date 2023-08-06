Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const iconReturn_1 = require("app/icons/iconReturn");
const locale_1 = require("app/locale");
const SubmitButton = (0, styled_1.default)('div') `
  background: transparent;
  box-shadow: none;
  border: 1px solid transparent;
  border-radius: ${p => p.theme.borderRadius};
  transition: 0.2s all;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 1.4em;
  width: 1.4em;
`;
const ClickTargetStyled = (0, styled_1.default)('div') `
  height: 100%;
  width: 25%;
  max-width: 2.5em;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;

  &:hover ${SubmitButton} {
    background: ${p => p.theme.background};
    box-shadow: ${p => p.theme.dropShadowLight};
    border: 1px solid ${p => p.theme.border};
  }
`;
const ReturnButton = props => (<ClickTargetStyled {...props}>
    <tooltip_1.default title={(0, locale_1.t)('Save')}>
      <SubmitButton>
        <iconReturn_1.IconReturn />
      </SubmitButton>
    </tooltip_1.default>
  </ClickTargetStyled>);
exports.default = ReturnButton;
//# sourceMappingURL=returnButton.jsx.map