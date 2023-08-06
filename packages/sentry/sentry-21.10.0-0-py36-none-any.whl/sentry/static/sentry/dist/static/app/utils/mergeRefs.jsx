Object.defineProperty(exports, "__esModule", { value: true });
/**
 * Combine refs to allow assignment to all passed refs
 */
function mergeRefs(refs) {
    return value => {
        refs.forEach(ref => {
            if (typeof ref === 'function') {
                ref(value);
            }
            else if (ref !== null && ref !== undefined) {
                ref.current = value;
            }
        });
    };
}
exports.default = mergeRefs;
//# sourceMappingURL=mergeRefs.jsx.map