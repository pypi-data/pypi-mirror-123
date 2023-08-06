Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const is_prop_valid_1 = (0, tslib_1.__importDefault)(require("@emotion/is-prop-valid"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const shouldForwardProp = p => p !== 'disabled' && (0, is_prop_valid_1.default)(p);
const FieldLabel = (0, styled_1.default)('div', { shouldForwardProp }) `
  color: ${p => (!p.disabled ? p.theme.textColor : p.theme.disabled)};
  display: flex;
  gap: ${(0, space_1.default)(0.5)};
  line-height: 16px;
`;
exports.default = FieldLabel;
//# sourceMappingURL=fieldLabel.jsx.map