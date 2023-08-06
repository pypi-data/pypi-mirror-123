Object.defineProperty(exports, "__esModule", { value: true });
exports.useLegacyStore = void 0;
const react_1 = require("react");
/**
 * Returns the state of a reflux store. Automatically unsubscribes when destroyed
 *
 * ```
 * const teams = useLegacyStore(TeamStore);
 * ```
 */
function useLegacyStore(store) {
    const [state, setState] = (0, react_1.useState)(store.getState());
    // Not all stores emit the new state, call get on change
    const callback = () => setState(store.getState());
    (0, react_1.useEffect)(() => store.listen(callback, undefined), []);
    return state;
}
exports.useLegacyStore = useLegacyStore;
//# sourceMappingURL=useLegacyStore.jsx.map