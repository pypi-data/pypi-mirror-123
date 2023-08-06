Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reactTestingLibrary_1 = require("sentry-test/reactTestingLibrary");
const queryCount_1 = (0, tslib_1.__importDefault)(require("app/components/queryCount"));
describe('QueryCount', function () {
    it('displays count when no max', function () {
        const { container } = (0, reactTestingLibrary_1.mountWithTheme)(<queryCount_1.default count={5}/>);
        expect(container).toSnapshot();
    });
    it('displays count when count < max', function () {
        const { container } = (0, reactTestingLibrary_1.mountWithTheme)(<queryCount_1.default count={5} max={500}/>);
        expect(container).toSnapshot();
    });
    it('does not render if count is 0', function () {
        const { container } = (0, reactTestingLibrary_1.mountWithTheme)(<queryCount_1.default count={0}/>);
        expect(container.firstChild).toBeNull();
    });
    it('can render when count is 0 when `hideIfEmpty` is false', function () {
        const { container } = (0, reactTestingLibrary_1.mountWithTheme)(<queryCount_1.default count={0} hideIfEmpty={false}/>);
        expect(container).toSnapshot();
    });
    it('displays max count if count >= max', function () {
        const { container } = (0, reactTestingLibrary_1.mountWithTheme)(<queryCount_1.default count={500} max={500}/>);
        expect(container).toSnapshot();
    });
});
//# sourceMappingURL=queryCount.spec.jsx.map