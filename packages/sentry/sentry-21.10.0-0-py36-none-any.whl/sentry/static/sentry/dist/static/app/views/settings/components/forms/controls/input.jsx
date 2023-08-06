Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const is_prop_valid_1 = (0, tslib_1.__importDefault)(require("@emotion/is-prop-valid"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const input_1 = require("app/styles/input");
/**
 * Do not forward required to `input` to avoid default browser behavior
 */
const Input = (0, styled_1.default)('input', {
    shouldForwardProp: prop => typeof prop === 'string' && (0, is_prop_valid_1.default)(prop) && prop !== 'required',
}) `
  ${input_1.inputStyles};
`;
// Cast type to avoid exporting theme
exports.default = Input;
//# sourceMappingURL=input.jsx.map