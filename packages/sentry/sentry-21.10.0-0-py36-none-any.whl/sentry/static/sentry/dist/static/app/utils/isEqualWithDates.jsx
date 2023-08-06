Object.defineProperty(exports, "__esModule", { value: true });
exports.isEqualWithDates = void 0;
const tslib_1 = require("tslib");
const isDate_1 = (0, tslib_1.__importDefault)(require("lodash/isDate"));
const isEqualWith_1 = (0, tslib_1.__importDefault)(require("lodash/isEqualWith"));
// `lodash.isEqual` does not compare date objects
function dateComparator(value, other) {
    if ((0, isDate_1.default)(value) && (0, isDate_1.default)(other)) {
        return +value === +other;
    }
    // Loose checking
    if (!value && !other) {
        return true;
    }
    // returning undefined will use default comparator
    return undefined;
}
const isEqualWithDates = (a, b) => (0, isEqualWith_1.default)(a, b, dateComparator);
exports.isEqualWithDates = isEqualWithDates;
//# sourceMappingURL=isEqualWithDates.jsx.map