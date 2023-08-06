Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/actions/button"));
const logoSentry_1 = (0, tslib_1.__importDefault)(require("app/components/logoSentry"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
function HeaderWithHelp({ docsUrl }) {
    return (<Header>
      <StyledLogoSentry />
      <button_1.default external href={docsUrl} size="xsmall">
        {(0, locale_1.t)('Need Help?')}
      </button_1.default>
    </Header>);
}
exports.default = HeaderWithHelp;
const Header = (0, styled_1.default)('div') `
  width: 100%;
  position: fixed;
  display: flex;
  justify-content: space-between;
  top: 0;
  z-index: 100;
  padding: ${(0, space_1.default)(2)};
  background: ${p => p.theme.background};
  border-bottom: 1px solid ${p => p.theme.innerBorder};
`;
const StyledLogoSentry = (0, styled_1.default)(logoSentry_1.default) `
  width: 130px;
  height: 30px;
  color: ${p => p.theme.textColor};
`;
//# sourceMappingURL=headerWithHelp.jsx.map