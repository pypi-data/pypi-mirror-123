Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reactTestingLibrary_1 = require("sentry-test/reactTestingLibrary");
const detailedError_1 = (0, tslib_1.__importDefault)(require("app/components/errors/detailedError"));
describe('DetailedError', function () {
    it('renders', function () {
        const { container } = (0, reactTestingLibrary_1.mountWithTheme)(<detailedError_1.default heading="Error heading" message={<div>Message</div>}/>);
        expect(container).toSnapshot();
    });
    it('renders with "Retry" button', function () {
        const { container } = (0, reactTestingLibrary_1.mountWithTheme)(<detailedError_1.default onRetry={() => { }} heading="Error heading" message={<div>Message</div>}/>);
        expect(container).toSnapshot();
    });
    it('can hide support links', function () {
        const { container } = (0, reactTestingLibrary_1.mountWithTheme)(<detailedError_1.default hideSupportLinks onRetry={() => { }} heading="Error heading" message={<div>Message</div>}/>);
        expect(container).toSnapshot();
    });
    it('hides footer when no "Retry" and no support links', function () {
        const { container } = (0, reactTestingLibrary_1.mountWithTheme)(<detailedError_1.default hideSupportLinks heading="Error heading" message={<div>Message</div>}/>);
        expect(container).toSnapshot();
    });
});
//# sourceMappingURL=detailedError.spec.jsx.map