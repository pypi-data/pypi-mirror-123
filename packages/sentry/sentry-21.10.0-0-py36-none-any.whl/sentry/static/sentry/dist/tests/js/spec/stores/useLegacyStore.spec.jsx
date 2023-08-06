Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_hooks_1 = require("@testing-library/react-hooks");
const teamStore_1 = (0, tslib_1.__importDefault)(require("app/stores/teamStore"));
const useLegacyStore_1 = require("app/stores/useLegacyStore");
describe('useLegacyStore', () => {
    // @ts-expect-error
    const team = TestStubs.Team();
    beforeEach(() => void teamStore_1.default.reset());
    it('should update on change to store', () => {
        const { result } = (0, react_hooks_1.renderHook)(() => (0, useLegacyStore_1.useLegacyStore)(teamStore_1.default));
        expect(result.current.teams).toEqual([]);
        (0, react_hooks_1.act)(() => teamStore_1.default.loadInitialData([team]));
        expect(result.current.teams).toEqual([team]);
    });
});
//# sourceMappingURL=useLegacyStore.spec.jsx.map