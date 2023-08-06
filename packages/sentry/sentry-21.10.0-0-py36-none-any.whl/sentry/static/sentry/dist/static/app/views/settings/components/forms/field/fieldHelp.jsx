Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const FieldHelp = (0, styled_1.default)('div') `
  color: ${p => p.theme.gray300};
  font-size: 14px;
  margin-top: ${p => (p.stacked && !p.inline ? 0 : (0, space_1.default)(1))};
  line-height: 1.4;
`;
exports.default = FieldHelp;
//# sourceMappingURL=fieldHelp.jsx.map