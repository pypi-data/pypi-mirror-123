Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reactTestingLibrary_1 = require("sentry-test/reactTestingLibrary");
const checkbox_1 = (0, tslib_1.__importDefault)(require("app/components/checkbox"));
describe('Checkbox', function () {
    it('renders', function () {
        const { container } = (0, reactTestingLibrary_1.mountWithTheme)(<checkbox_1.default onChange={() => { }}/>);
        expect(container).toSnapshot();
    });
});
//# sourceMappingURL=checkbox.spec.jsx.map