Object.defineProperty(exports, "__esModule", { value: true });
exports.groupingComponentFilter = exports.shouldInlineComponentValue = exports.hasNonContributingComponent = void 0;
const tslib_1 = require("tslib");
const isObject_1 = (0, tslib_1.__importDefault)(require("lodash/isObject"));
function hasNonContributingComponent(component) {
    if (!(component === null || component === void 0 ? void 0 : component.contributes)) {
        return true;
    }
    for (const value of component.values) {
        if ((0, isObject_1.default)(value) && hasNonContributingComponent(value)) {
            return true;
        }
    }
    return false;
}
exports.hasNonContributingComponent = hasNonContributingComponent;
function shouldInlineComponentValue(component) {
    return component.values.every(value => !(0, isObject_1.default)(value));
}
exports.shouldInlineComponentValue = shouldInlineComponentValue;
function groupingComponentFilter(value, showNonContributing) {
    if ((0, isObject_1.default)(value)) {
        // no point rendering such nodes at all, we never show them
        if (!value.contributes && !value.hint && value.values.length === 0) {
            return false;
        }
        // non contributing values are otherwise optional
        if (!showNonContributing && !value.contributes) {
            return false;
        }
    }
    return true;
}
exports.groupingComponentFilter = groupingComponentFilter;
//# sourceMappingURL=utils.jsx.map