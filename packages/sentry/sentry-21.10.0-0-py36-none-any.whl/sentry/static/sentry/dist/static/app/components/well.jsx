Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Well = (0, styled_1.default)('div') `
  border: 1px solid ${p => p.theme.border};
  box-shadow: none;
  background: ${p => p.theme.backgroundSecondary};
  padding: ${p => (p.hasImage ? '80px 30px' : '15px 20px')};
  margin-bottom: 20px;
  border-radius: 3px;
  ${p => p.centered && 'text-align: center'};
`;
exports.default = Well;
//# sourceMappingURL=well.jsx.map