Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reactTestingLibrary_1 = require("sentry-test/reactTestingLibrary");
const similarSpectrum_1 = (0, tslib_1.__importDefault)(require("app/components/similarSpectrum"));
describe('SimilarSpectrum', function () {
    beforeEach(function () { });
    afterEach(function () { });
    it('renders', function () {
        const { container } = (0, reactTestingLibrary_1.mountWithTheme)(<similarSpectrum_1.default />);
        expect(container).toSnapshot();
    });
});
//# sourceMappingURL=similarSpectrum.spec.jsx.map