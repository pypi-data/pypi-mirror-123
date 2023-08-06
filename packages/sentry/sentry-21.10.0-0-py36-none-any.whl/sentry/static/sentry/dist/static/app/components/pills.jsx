Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Pills = (0, styled_1.default)('div') `
  display: flex;
  flex-wrap: wrap;
  font-size: ${p => p.theme.fontSizeSmall};
`;
exports.default = Pills;
//# sourceMappingURL=pills.jsx.map