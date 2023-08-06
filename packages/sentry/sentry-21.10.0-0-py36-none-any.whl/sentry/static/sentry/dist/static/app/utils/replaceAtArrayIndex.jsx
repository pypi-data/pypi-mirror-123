Object.defineProperty(exports, "__esModule", { value: true });
exports.replaceAtArrayIndex = void 0;
/**
 * Replace item at `index` in `array` with `obj`
 */
function replaceAtArrayIndex(array, index, obj) {
    const newArray = [...array];
    newArray.splice(index, 1, obj);
    return newArray;
}
exports.replaceAtArrayIndex = replaceAtArrayIndex;
//# sourceMappingURL=replaceAtArrayIndex.jsx.map