Object.defineProperty(exports, "__esModule", { value: true });
const react_1 = require("react");
const isBrowser = typeof window !== 'undefined';
function useSessionStorage(key, initialValue) {
    if (!isBrowser) {
        return [initialValue, () => { }, () => { }];
    }
    const [state, setState] = (0, react_1.useState)(() => {
        try {
            // Get from session storage by key
            const sessionStorageValue = sessionStorage.getItem(key);
            if (sessionStorageValue === 'undefined') {
                return initialValue;
            }
            // Parse stored json or if none return initialValue
            return sessionStorageValue ? JSON.parse(sessionStorageValue) : initialValue;
        }
        catch (_a) {
            // If user is in private mode or has storage restriction
            // sessionStorage can throw. JSON.parse and JSON.stringify
            // can throw, too.
            return initialValue;
        }
    });
    (0, react_1.useEffect)(() => {
        try {
            const serializedState = JSON.stringify(state);
            sessionStorage.setItem(key, serializedState);
        }
        catch (_a) {
            // If user is in private mode or has storage restriction
            // sessionStorage can throw. Also JSON.stringify can throw.
        }
    }, [state]);
    function removeItem() {
        sessionStorage.removeItem(key);
        setState(undefined);
    }
    return [state, setState, removeItem];
}
exports.default = useSessionStorage;
//# sourceMappingURL=useSessionStorage.jsx.map