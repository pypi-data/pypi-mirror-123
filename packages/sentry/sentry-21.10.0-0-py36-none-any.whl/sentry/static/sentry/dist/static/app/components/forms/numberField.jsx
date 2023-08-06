Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const inputField_1 = (0, tslib_1.__importDefault)(require("app/components/forms/inputField"));
class NumberField extends inputField_1.default {
    coerceValue(value) {
        const intValue = parseInt(value, 10);
        // return previous value if new value is NaN, otherwise, will get recursive error
        const isNewCoercedNaN = isNaN(intValue);
        if (!isNewCoercedNaN) {
            return intValue;
        }
        return '';
    }
    getType() {
        return 'number';
    }
    getAttributes() {
        return {
            min: this.props.min || undefined,
            max: this.props.max || undefined,
        };
    }
}
exports.default = NumberField;
//# sourceMappingURL=numberField.jsx.map