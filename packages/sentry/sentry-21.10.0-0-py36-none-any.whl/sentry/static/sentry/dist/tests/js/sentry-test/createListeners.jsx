Object.defineProperty(exports, "__esModule", { value: true });
exports.createListeners = void 0;
function createListeners(type) {
    const eventTarget = type === 'window' ? window : document;
    let listeners = [];
    const handler = (eventData, event) => {
        var _a, _b, _c, _d;
        const filteredListeners = listeners.filter(listener => listener.hasOwnProperty(event));
        if ((eventData === null || eventData === void 0 ? void 0 : eventData.key) === 'Escape') {
            return (_b = (_a = filteredListeners[1]) === null || _a === void 0 ? void 0 : _a[event]) === null || _b === void 0 ? void 0 : _b.call(_a, eventData);
        }
        return (_d = (_c = filteredListeners[0]) === null || _c === void 0 ? void 0 : _c[event]) === null || _d === void 0 ? void 0 : _d.call(_c, eventData);
    };
    eventTarget.addEventListener = jest.fn((event, cb) => {
        listeners.push({
            [event]: cb,
        });
    });
    eventTarget.removeEventListener = jest.fn(event => {
        listeners = listeners.filter(listener => !listener.hasOwnProperty(event));
    });
    return {
        mouseDown: (domEl) => handler({ target: domEl }, 'mousedown'),
        keyDown: (key) => handler({ key }, 'keydown'),
    };
}
exports.createListeners = createListeners;
//# sourceMappingURL=createListeners.jsx.map