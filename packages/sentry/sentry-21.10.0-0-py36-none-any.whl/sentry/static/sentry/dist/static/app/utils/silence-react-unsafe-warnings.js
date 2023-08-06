Object.defineProperty(exports, "__esModule", { value: true });
exports.silencedWarn = exports.originalConsoleWarn = void 0;
// eslint-disable-next-line no-console
exports.originalConsoleWarn = console.warn;
const REACT_UNSAFE_WARNING_REGEX = /componentWill.* has been renamed, and is not recommended for use.*/;
const MOMENT_INVALID_INPUT_REGEX = /moment construction falls back/;
window.console.warn = (message, ...args) => {
    if (typeof message === 'string' &&
        (REACT_UNSAFE_WARNING_REGEX.test(message) || MOMENT_INVALID_INPUT_REGEX.test(message))) {
        return;
    }
    (0, exports.originalConsoleWarn)(message, ...args);
};
exports.silencedWarn = window.console.warn;
//# sourceMappingURL=silence-react-unsafe-warnings.js.map