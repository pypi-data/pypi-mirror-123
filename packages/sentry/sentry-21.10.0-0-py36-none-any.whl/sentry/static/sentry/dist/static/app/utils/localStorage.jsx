Object.defineProperty(exports, "__esModule", { value: true });
function createLocalStorage() {
    try {
        const localStorage = window.localStorage;
        const mod = 'sentry';
        localStorage.setItem(mod, mod);
        localStorage.removeItem(mod);
        return {
            setItem: localStorage.setItem.bind(localStorage),
            getItem: localStorage.getItem.bind(localStorage),
            removeItem: localStorage.removeItem.bind(localStorage),
        };
    }
    catch (e) {
        return {
            setItem() {
                return;
            },
            // Returns null if key doesn't exist:
            // https://developer.mozilla.org/en-US/docs/Web/API/Storage/getItem
            getItem() {
                return null;
            },
            removeItem() {
                return null;
            },
        };
    }
}
const functions = createLocalStorage();
exports.default = functions;
//# sourceMappingURL=localStorage.jsx.map