Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reactTestingLibrary_1 = require("sentry-test/reactTestingLibrary");
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
describe('ExternalLink', function () {
    it('renders', function () {
        const { container } = (0, reactTestingLibrary_1.mountWithTheme)(<externalLink_1.default href="https://www.sentry.io/">ExternalLink</externalLink_1.default>);
        expect(container).toSnapshot();
    });
});
//# sourceMappingURL=externalLink.spec.jsx.map