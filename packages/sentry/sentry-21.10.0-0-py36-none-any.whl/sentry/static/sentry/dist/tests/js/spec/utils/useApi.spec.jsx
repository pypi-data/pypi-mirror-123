Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_hooks_1 = require("@testing-library/react-hooks");
const api_1 = require("app/api");
const useApi_1 = (0, tslib_1.__importDefault)(require("app/utils/useApi"));
describe('useApi', function () {
    it('provides an api client ', function () {
        const { result } = (0, react_hooks_1.renderHook)(() => (0, useApi_1.default)());
        expect(result.current).toBeInstanceOf(api_1.Client);
    });
    it('cancels pending API requests when unmounted', function () {
        const { result, unmount } = (0, react_hooks_1.renderHook)(() => (0, useApi_1.default)());
        jest.spyOn(result.current, 'clear');
        unmount();
        expect(result.current.clear).toHaveBeenCalled();
    });
    it('does not cancel inflights when persistInFlight is true', function () {
        const { result, unmount } = (0, react_hooks_1.renderHook)(() => (0, useApi_1.default)({ persistInFlight: true }));
        jest.spyOn(result.current, 'clear');
        unmount();
        expect(result.current.clear).not.toHaveBeenCalled();
    });
    it('uses pass through API when provided', function () {
        const myClient = new api_1.Client();
        const { unmount } = (0, react_hooks_1.renderHook)(() => (0, useApi_1.default)({ api: myClient }));
        jest.spyOn(myClient, 'clear');
        unmount();
        expect(myClient.clear).toHaveBeenCalled();
    });
});
//# sourceMappingURL=useApi.spec.jsx.map