Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const PageAlertBar = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  justify-content: center;
  color: ${p => p.theme.headerBackground};
  background-color: ${p => p.theme.bannerBackground};
  padding: 6px 30px;
  font-size: 14px;
`;
exports.default = PageAlertBar;
//# sourceMappingURL=pageAlertBar.jsx.map