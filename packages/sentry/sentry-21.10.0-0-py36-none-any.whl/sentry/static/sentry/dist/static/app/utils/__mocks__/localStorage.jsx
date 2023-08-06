Object.defineProperty(exports, "__esModule", { value: true });
const localStorageMock = function () {
    let store = {};
    return {
        getItem: jest.fn(key => store[key]),
        setItem: jest.fn((key, value) => {
            store[key] = value.toString();
        }),
        clear: jest.fn(() => {
            store = {};
        }),
    };
};
exports.default = localStorageMock();
//# sourceMappingURL=localStorage.jsx.map