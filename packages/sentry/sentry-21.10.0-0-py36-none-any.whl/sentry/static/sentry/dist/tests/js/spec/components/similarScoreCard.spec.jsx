Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reactTestingLibrary_1 = require("sentry-test/reactTestingLibrary");
const similarScoreCard_1 = (0, tslib_1.__importDefault)(require("app/components/similarScoreCard"));
describe('SimilarScoreCard', function () {
    beforeEach(function () { });
    afterEach(function () { });
    it('renders', function () {
        const { container } = (0, reactTestingLibrary_1.mountWithTheme)(<similarScoreCard_1.default />);
        expect(container.firstChild).toBeNull();
    });
    it('renders with score list', function () {
        const { container } = (0, reactTestingLibrary_1.mountWithTheme)(<similarScoreCard_1.default scoreList={[
                ['exception:message:character-shingles', null],
                ['exception:stacktrace:application-chunks', 0.8],
                ['exception:stacktrace:pairs', 1],
                ['message:message:character-shingles', 0.5],
                ['unknown:foo:bar', 0.5],
            ]}/>);
        expect(container).toSnapshot();
    });
});
//# sourceMappingURL=similarScoreCard.spec.jsx.map