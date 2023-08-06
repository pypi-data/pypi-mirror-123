Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const flatMap_1 = (0, tslib_1.__importDefault)(require("lodash/flatMap"));
function hasRootGroup(items) {
    var _a;
    return !!((_a = items[0]) === null || _a === void 0 ? void 0 : _a.items);
}
function filterItems(items, inputValue) {
    return items.filter(item => (item.searchKey || `${item.value} ${item.label}`)
        .toLowerCase()
        .indexOf(inputValue.toLowerCase()) > -1);
}
function filterGroupedItems(groups, inputValue) {
    return groups
        .map(group => (Object.assign(Object.assign({}, group), { items: filterItems(group.items, inputValue) })))
        .filter(group => group.items.length > 0);
}
function autoCompleteFilter(items, inputValue) {
    let itemCount = 0;
    if (!items) {
        return [];
    }
    if (hasRootGroup(items)) {
        // if the first item has children, we assume it is a group
        return (0, flatMap_1.default)(filterGroupedItems(items, inputValue), item => {
            const groupItems = item.items.map(groupedItem => (Object.assign(Object.assign({}, groupedItem), { index: itemCount++ })));
            // Make sure we don't add the group label to list of items
            // if we try to hide it, otherwise it will render if the list
            // is using virtualized rows (because of fixed row heights)
            if (item.hideGroupLabel) {
                return groupItems;
            }
            return [Object.assign(Object.assign({}, item), { groupLabel: true }), ...groupItems];
        });
    }
    return filterItems(items, inputValue).map((item, index) => (Object.assign(Object.assign({}, item), { index })));
}
exports.default = autoCompleteFilter;
//# sourceMappingURL=autoCompleteFilter.jsx.map