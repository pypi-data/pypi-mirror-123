Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reactTestingLibrary_1 = require("sentry-test/reactTestingLibrary");
const circleIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/circleIndicator"));
describe('CircleIndicator', function () {
    it('renders', function () {
        const { container } = (0, reactTestingLibrary_1.mountWithTheme)(<circleIndicator_1.default />);
        expect(container).toSnapshot();
    });
});
//# sourceMappingURL=circleIndicator.spec.jsx.map