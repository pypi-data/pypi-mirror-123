Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const omit_1 = (0, tslib_1.__importDefault)(require("lodash/omit"));
const radioBoolean_1 = (0, tslib_1.__importDefault)(require("./controls/radioBoolean"));
const inputField_1 = (0, tslib_1.__importDefault)(require("./inputField"));
function RadioBooleanField(props) {
    return (<inputField_1.default {...props} field={fieldProps => (<radioBoolean_1.default {...(0, omit_1.default)(fieldProps, ['onKeyDown', 'children'])}/>)}/>);
}
exports.default = RadioBooleanField;
//# sourceMappingURL=radioBooleanField.jsx.map