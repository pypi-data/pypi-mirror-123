Object.defineProperty(exports, "__esModule", { value: true });
exports.callIfFunction = void 0;
// Checks if `fn` is a function and calls it with `args`
function callIfFunction(fn, ...args) {
    return typeof fn === 'function' && fn(...args);
}
exports.callIfFunction = callIfFunction;
//# sourceMappingURL=callIfFunction.jsx.map