Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const ToolbarHeader = (0, styled_1.default)('div') `
  font-size: 12px;
  text-transform: uppercase;
  font-weight: bold;
  color: ${p => p.theme.subText};
`;
exports.default = ToolbarHeader;
//# sourceMappingURL=toolbarHeader.jsx.map