Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reactTestingLibrary_1 = require("sentry-test/reactTestingLibrary");
const tagDeprecated_1 = (0, tslib_1.__importDefault)(require("app/components/tagDeprecated"));
describe('Tag', function () {
    it('renders', function () {
        const { container } = (0, reactTestingLibrary_1.mountWithTheme)(<tagDeprecated_1.default priority="info" border size="small">
        Text to Copy
      </tagDeprecated_1.default>);
        expect(container).toSnapshot();
    });
});
//# sourceMappingURL=tagDeprecated.spec.jsx.map