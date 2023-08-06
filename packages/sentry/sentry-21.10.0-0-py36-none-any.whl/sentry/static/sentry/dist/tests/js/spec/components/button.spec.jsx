Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reactTestingLibrary_1 = require("sentry-test/reactTestingLibrary");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
describe('Button', function () {
    // @ts-expect-error
    const routerContext = TestStubs.routerContext();
    it('renders', function () {
        const { container } = (0, reactTestingLibrary_1.mountWithTheme)(<button_1.default priority="primary">Button</button_1.default>);
        expect(container).toSnapshot();
    });
    it('renders react-router link', function () {
        const { container } = (0, reactTestingLibrary_1.mountWithTheme)(<button_1.default to="/some/route">Router Link</button_1.default>, {
            context: routerContext,
        });
        expect(container).toSnapshot();
    });
    it('renders normal link', function () {
        const { container } = (0, reactTestingLibrary_1.mountWithTheme)(<button_1.default href="/some/relative/url">Normal Link</button_1.default>, { context: routerContext });
        expect(container).toSnapshot();
    });
    it('renders disabled normal link', function () {
        const { container } = (0, reactTestingLibrary_1.mountWithTheme)(<button_1.default href="/some/relative/url">Normal Link</button_1.default>, { context: routerContext });
        expect(container).toSnapshot();
    });
    it('calls `onClick` callback', function () {
        const spy = jest.fn();
        (0, reactTestingLibrary_1.mountWithTheme)(<button_1.default onClick={spy}>Click me</button_1.default>, {
            context: routerContext,
        });
        reactTestingLibrary_1.fireEvent.click(reactTestingLibrary_1.screen.getByText('Click me'));
        expect(spy).toHaveBeenCalled();
    });
    it('does not call `onClick` on disabled buttons', function () {
        const spy = jest.fn();
        (0, reactTestingLibrary_1.mountWithTheme)(<button_1.default onClick={spy} disabled>
        Click me
      </button_1.default>, { context: routerContext });
        reactTestingLibrary_1.fireEvent.click(reactTestingLibrary_1.screen.getByText('Click me'));
        expect(spy).not.toHaveBeenCalled();
    });
});
//# sourceMappingURL=button.spec.jsx.map