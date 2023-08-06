Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reactTestingLibrary_1 = require("sentry-test/reactTestingLibrary");
const checkboxFancy_1 = (0, tslib_1.__importDefault)(require("app/components/checkboxFancy/checkboxFancy"));
describe('CheckboxFancy', function () {
    it('renders', function () {
        const { container } = (0, reactTestingLibrary_1.mountWithTheme)(<checkboxFancy_1.default />);
        expect(container).toSnapshot();
    });
    it('isChecked', function () {
        (0, reactTestingLibrary_1.mountWithTheme)(<checkboxFancy_1.default isChecked/>);
        expect(reactTestingLibrary_1.screen.getByRole('checkbox', { checked: true })).toBeTruthy();
        expect(reactTestingLibrary_1.screen.getByTestId('icon-check-mark')).toBeInTheDocument();
        expect(reactTestingLibrary_1.screen.queryByTestId('icon-subtract')).toBeNull();
    });
    it('isIndeterminate', function () {
        (0, reactTestingLibrary_1.mountWithTheme)(<checkboxFancy_1.default isIndeterminate/>);
        expect(reactTestingLibrary_1.screen.getByRole('checkbox')).toHaveAttribute('aria-checked', 'mixed');
        expect(reactTestingLibrary_1.screen.queryByTestId('icon-check-mark')).toBeNull();
        expect(reactTestingLibrary_1.screen.getByTestId('icon-subtract')).toBeInTheDocument();
    });
    it('isDisabled', function () {
        (0, reactTestingLibrary_1.mountWithTheme)(<checkboxFancy_1.default isDisabled/>);
        expect(reactTestingLibrary_1.screen.getByRole('checkbox')).toHaveAttribute('aria-disabled', 'true');
        expect(reactTestingLibrary_1.screen.queryByTestId('icon-check-mark')).toBeNull();
        expect(reactTestingLibrary_1.screen.queryByTestId('icon-subtract')).toBeNull();
    });
});
//# sourceMappingURL=checkboxFancy.spec.jsx.map