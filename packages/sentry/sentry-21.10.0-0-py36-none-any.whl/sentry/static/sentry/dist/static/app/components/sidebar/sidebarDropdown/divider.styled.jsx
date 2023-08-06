Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Divider = (0, styled_1.default)('div') `
  height: 0;
  border-bottom: 1px solid ${p => p.theme.innerBorder};
  margin: 5px 0;
`;
exports.default = Divider;
//# sourceMappingURL=divider.styled.jsx.map