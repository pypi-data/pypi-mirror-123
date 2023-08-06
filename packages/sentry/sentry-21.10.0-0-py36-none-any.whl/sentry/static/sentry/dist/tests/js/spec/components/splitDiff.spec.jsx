Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reactTestingLibrary_1 = require("sentry-test/reactTestingLibrary");
const splitDiff_1 = (0, tslib_1.__importDefault)(require("app/components/splitDiff"));
describe('SplitDiff', function () {
    beforeEach(function () { });
    afterEach(function () { });
    it('renders', function () {
        const { container } = (0, reactTestingLibrary_1.mountWithTheme)(<splitDiff_1.default base="restaurant" target="aura"/>);
        expect(container).toSnapshot();
    });
    it('renders with newlines', function () {
        const base = `this is my restaurant
    and restaurant
    common`;
        const target = `aura
    and your aura
    common`;
        const { container } = (0, reactTestingLibrary_1.mountWithTheme)(<splitDiff_1.default base={base} target={target}/>);
        expect(container).toSnapshot();
    });
});
//# sourceMappingURL=splitDiff.spec.jsx.map