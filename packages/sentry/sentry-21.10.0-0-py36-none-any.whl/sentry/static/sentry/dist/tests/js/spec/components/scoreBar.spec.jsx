Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reactTestingLibrary_1 = require("sentry-test/reactTestingLibrary");
const scoreBar_1 = (0, tslib_1.__importDefault)(require("app/components/scoreBar"));
describe('ScoreBar', function () {
    beforeEach(function () { });
    afterEach(function () { });
    it('renders', function () {
        const { container } = (0, reactTestingLibrary_1.mountWithTheme)(<scoreBar_1.default size={60} thickness={2} score={3}/>);
        expect(container).toSnapshot();
    });
    it('renders vertically', function () {
        const { container } = (0, reactTestingLibrary_1.mountWithTheme)(<scoreBar_1.default size={60} thickness={2} vertical score={2}/>);
        expect(container).toSnapshot();
    });
    it('renders with score = 0', function () {
        const { container } = (0, reactTestingLibrary_1.mountWithTheme)(<scoreBar_1.default size={60} thickness={2} score={0}/>);
        expect(container).toSnapshot();
    });
    it('renders with score > max score', function () {
        const { container } = (0, reactTestingLibrary_1.mountWithTheme)(<scoreBar_1.default size={60} thickness={2} score={10}/>);
        expect(container).toSnapshot();
    });
    it('renders with < 0 score', function () {
        const { container } = (0, reactTestingLibrary_1.mountWithTheme)(<scoreBar_1.default size={60} thickness={2} score={-2}/>);
        expect(container).toSnapshot();
    });
    it('has custom palette', function () {
        const { container } = (0, reactTestingLibrary_1.mountWithTheme)(<scoreBar_1.default vertical size={60} thickness={2} score={7} palette={['white', 'red', 'red', 'pink', 'pink', 'purple', 'purple', 'black']}/>);
        expect(container).toSnapshot();
    });
});
//# sourceMappingURL=scoreBar.spec.jsx.map