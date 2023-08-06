Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const selectField_1 = (0, tslib_1.__importDefault)(require("app/components/forms/selectField"));
class MultiSelectField extends selectField_1.default {
    isMultiple() {
        return true;
    }
}
exports.default = MultiSelectField;
//# sourceMappingURL=multiSelectField.jsx.map