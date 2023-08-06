Object.defineProperty(exports, "__esModule", { value: true });
const react_1 = require("react");
const api_1 = require("app/api");
/**
 * Returns an API client that will have it's requests canceled when the owning
 * React component is unmounted (may be disabled via options).
 */
function useApi({ persistInFlight, api: providedApi } = {}) {
    const localApi = (0, react_1.useRef)();
    // Lazily construct the client if we weren't provided with one
    if (localApi.current === undefined && providedApi === undefined) {
        localApi.current = new api_1.Client();
    }
    // Use the provided client if available
    const api = providedApi !== null && providedApi !== void 0 ? providedApi : localApi.current;
    function handleCleanup() {
        !persistInFlight && api.clear();
    }
    (0, react_1.useEffect)(() => handleCleanup, []);
    return api;
}
exports.default = useApi;
//# sourceMappingURL=useApi.jsx.map