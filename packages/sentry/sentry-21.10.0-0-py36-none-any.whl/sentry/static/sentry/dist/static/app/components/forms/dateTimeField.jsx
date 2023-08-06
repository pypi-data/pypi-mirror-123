Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const inputField_1 = (0, tslib_1.__importDefault)(require("app/components/forms/inputField"));
class DateTimeField extends inputField_1.default {
    getType() {
        return 'datetime-local';
    }
}
exports.default = DateTimeField;
//# sourceMappingURL=dateTimeField.jsx.map