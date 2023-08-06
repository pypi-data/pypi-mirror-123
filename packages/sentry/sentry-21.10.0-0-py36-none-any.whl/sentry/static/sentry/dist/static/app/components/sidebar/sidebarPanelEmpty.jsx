Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const SidebarPanelEmpty = (0, styled_1.default)('div') `
  flex-grow: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  color: ${p => p.theme.gray300};
  padding: 0 60px;
  text-align: center;
`;
exports.default = SidebarPanelEmpty;
//# sourceMappingURL=sidebarPanelEmpty.jsx.map