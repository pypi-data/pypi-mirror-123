Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const HeaderSeparator = (0, styled_1.default)('div') `
  width: 1px;
  background-color: ${p => p.theme.border};
  margin: ${(0, space_1.default)(2)} 0;
`;
exports.default = HeaderSeparator;
//# sourceMappingURL=headerSeparator.jsx.map