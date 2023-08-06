Object.defineProperty(exports, "__esModule", { value: true });
// hook from https://usehooks.com/useOnClickOutside/
const react_1 = require("react");
function useOnClickOutside(ref, handler) {
    (0, react_1.useEffect)(() => {
        const listener = (event) => {
            const el = ref === null || ref === void 0 ? void 0 : ref.current;
            // Do nothing if clicking ref's element or descendent elements
            if (!el || el.contains(event.target)) {
                return;
            }
            handler(event);
        };
        document.addEventListener('mousedown', listener);
        document.addEventListener('touchstart', listener);
        return () => {
            document.removeEventListener('mousedown', listener);
            document.removeEventListener('touchstart', listener);
        };
    }, 
    // Reload only if ref or handler changes
    [ref, handler]);
}
exports.default = useOnClickOutside;
//# sourceMappingURL=useOnClickOutside.jsx.map