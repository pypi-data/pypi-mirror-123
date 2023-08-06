Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const inputField_1 = (0, tslib_1.__importDefault)(require("app/components/forms/inputField"));
class TextField extends inputField_1.default {
    getAttributes() {
        return {
            spellCheck: this.props.spellCheck,
        };
    }
    getType() {
        return 'text';
    }
}
exports.default = TextField;
//# sourceMappingURL=textField.jsx.map