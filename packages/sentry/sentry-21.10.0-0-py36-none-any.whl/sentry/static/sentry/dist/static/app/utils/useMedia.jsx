Object.defineProperty(exports, "__esModule", { value: true });
const react_1 = require("react");
/**
 * Hook that updates when a media query result changes
 */
function useMedia(query) {
    if (!window.matchMedia) {
        return false;
    }
    const [state, setState] = (0, react_1.useState)(() => window.matchMedia(query).matches);
    (0, react_1.useEffect)(() => {
        let mounted = true;
        const mql = window.matchMedia(query);
        const onChange = () => {
            if (!mounted) {
                return;
            }
            setState(!!mql.matches);
        };
        mql.addListener(onChange);
        setState(mql.matches);
        return () => {
            mounted = false;
            mql.removeListener(onChange);
        };
    }, [query]);
    return state;
}
exports.default = useMedia;
//# sourceMappingURL=useMedia.jsx.map