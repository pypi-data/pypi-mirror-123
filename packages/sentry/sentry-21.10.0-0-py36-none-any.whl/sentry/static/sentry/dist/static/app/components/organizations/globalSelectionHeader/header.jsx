Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Header = (0, styled_1.default)('div') `
  position: relative;
  display: flex;
  width: 100%;
  height: 60px;

  border-bottom: 1px solid ${p => p.theme.border};
  box-shadow: ${p => p.theme.dropShadowLight};
  z-index: ${p => p.theme.zIndex.globalSelectionHeader};

  background: ${p => p.theme.headerBackground};
  font-size: ${p => p.theme.fontSizeExtraLarge};
  @media (min-width: ${props => props.theme.breakpoints[0]} and max-width: ${props => props.theme.breakpoints[1]}) {
    margin-top: 54px;
  }
  @media (max-width: calc(${props => props.theme.breakpoints[0]} - 1px)) {
    margin-top: 0;
  }
`;
exports.default = Header;
//# sourceMappingURL=header.jsx.map