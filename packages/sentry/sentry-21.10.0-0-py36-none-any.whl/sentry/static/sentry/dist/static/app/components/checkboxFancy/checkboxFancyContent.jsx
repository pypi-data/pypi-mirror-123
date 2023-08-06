Object.defineProperty(exports, "__esModule", { value: true });
const icons_1 = require("app/icons");
const CheckboxFancyContent = ({ isChecked, isIndeterminate }) => {
    if (isIndeterminate) {
        return <icons_1.IconSubtract size="70%" color="white"/>;
    }
    if (isChecked) {
        return <icons_1.IconCheckmark size="70%" color="white"/>;
    }
    return null;
};
exports.default = CheckboxFancyContent;
//# sourceMappingURL=checkboxFancyContent.jsx.map