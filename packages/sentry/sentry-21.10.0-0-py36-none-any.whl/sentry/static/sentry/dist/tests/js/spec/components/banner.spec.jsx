Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reactTestingLibrary_1 = require("sentry-test/reactTestingLibrary");
const banner_1 = (0, tslib_1.__importDefault)(require("app/components/banner"));
describe('Banner', function () {
    it('can be dismissed', function () {
        (0, reactTestingLibrary_1.mountWithTheme)(<banner_1.default dismissKey="test" title="test"/>);
        expect(reactTestingLibrary_1.screen.getByText('test')).toBeInTheDocument();
        reactTestingLibrary_1.fireEvent.click(reactTestingLibrary_1.screen.getByLabelText('Close'));
        expect(reactTestingLibrary_1.screen.queryByText('test')).toBeNull();
        expect(localStorage.getItem('test-banner-dismissed')).toBe('true');
    });
    it('is not dismissable', function () {
        (0, reactTestingLibrary_1.mountWithTheme)(<banner_1.default isDismissable={false}/>);
        expect(reactTestingLibrary_1.screen.queryByLabelText('Close')).toBeNull();
    });
});
//# sourceMappingURL=banner.spec.jsx.map