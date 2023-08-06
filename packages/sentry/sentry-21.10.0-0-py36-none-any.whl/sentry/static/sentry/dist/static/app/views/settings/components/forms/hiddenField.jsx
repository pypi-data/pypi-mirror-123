Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const inputField_1 = (0, tslib_1.__importDefault)(require("./inputField"));
function HiddenField(props) {
    return <HiddenInputField {...props} type="hidden"/>;
}
exports.default = HiddenField;
const HiddenInputField = (0, styled_1.default)(inputField_1.default) `
  display: none;
`;
//# sourceMappingURL=hiddenField.jsx.map