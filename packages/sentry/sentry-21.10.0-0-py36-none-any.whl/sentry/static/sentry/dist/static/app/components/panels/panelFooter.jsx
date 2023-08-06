Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const PanelFooter = (0, styled_1.default)('div') `
  border-top: 1px solid ${p => p.theme.border};
  color: ${p => p.theme.subText};
  font-size: 14px;
`;
exports.default = PanelFooter;
//# sourceMappingURL=panelFooter.jsx.map