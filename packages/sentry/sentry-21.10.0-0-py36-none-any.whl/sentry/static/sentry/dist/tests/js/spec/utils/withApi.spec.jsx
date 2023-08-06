Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reactTestingLibrary_1 = require("sentry-test/reactTestingLibrary");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
describe('withApi', function () {
    let apiInstance;
    const MyComponent = jest.fn((props) => {
        apiInstance = props.api;
        return <div />;
    });
    it('renders MyComponent with an api prop', function () {
        const MyComponentWithApi = (0, withApi_1.default)(MyComponent);
        (0, reactTestingLibrary_1.mountWithTheme)(<MyComponentWithApi />);
        expect(MyComponent).toHaveBeenCalledWith(expect.objectContaining({ api: apiInstance }), expect.anything());
    });
    it('cancels pending API requests when component is unmounted', function () {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const MyComponentWithApi = (0, withApi_1.default)(MyComponent);
            const wrapper = (0, reactTestingLibrary_1.mountWithTheme)(<MyComponentWithApi />);
            if (apiInstance === undefined) {
                throw new Error("apiInstance wasn't defined");
            }
            jest.spyOn(apiInstance, 'clear');
            expect(apiInstance === null || apiInstance === void 0 ? void 0 : apiInstance.clear).not.toHaveBeenCalled();
            wrapper.unmount();
            expect(apiInstance === null || apiInstance === void 0 ? void 0 : apiInstance.clear).toHaveBeenCalled();
        });
    });
});
//# sourceMappingURL=withApi.spec.jsx.map