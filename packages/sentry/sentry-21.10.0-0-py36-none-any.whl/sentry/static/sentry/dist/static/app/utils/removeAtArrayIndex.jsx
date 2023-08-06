Object.defineProperty(exports, "__esModule", { value: true });
exports.removeAtArrayIndex = void 0;
/**
 * Remove item at `index` in `array` without mutating `array`
 */
function removeAtArrayIndex(array, index) {
    const newArray = [...array];
    newArray.splice(index, 1);
    return newArray;
}
exports.removeAtArrayIndex = removeAtArrayIndex;
//# sourceMappingURL=removeAtArrayIndex.jsx.map