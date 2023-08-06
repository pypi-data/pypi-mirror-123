Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const FieldRequiredBadge = (0, styled_1.default)('div') `
  display: inline-block;
  background: ${p => p.theme.red300};
  opacity: 0.6;
  width: 5px;
  height: 5px;
  border-radius: 5px;
  text-indent: -9999em;
  vertical-align: super;
  margin-left: ${(0, space_1.default)(0.5)};
`;
exports.default = FieldRequiredBadge;
//# sourceMappingURL=fieldRequiredBadge.jsx.map