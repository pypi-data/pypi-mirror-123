Object.defineProperty(exports, "__esModule", { value: true });
const constants_1 = require("app/constants");
/**
 * Return a specified "fixed" string when we are in a testing environment
 * (more specifically, when `IS_ACCEPTANCE_TEST` is true)
 */
function getDynamicText({ value, fixed, }) {
    return constants_1.IS_ACCEPTANCE_TEST ? fixed : value;
}
exports.default = getDynamicText;
//# sourceMappingURL=getDynamicText.jsx.map