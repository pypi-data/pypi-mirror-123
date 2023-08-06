Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_hooks_1 = require("@testing-library/react-hooks");
const organizationStore_1 = (0, tslib_1.__importDefault)(require("app/stores/organizationStore"));
const teamStore_1 = (0, tslib_1.__importDefault)(require("app/stores/teamStore"));
const useTeams_1 = (0, tslib_1.__importDefault)(require("app/utils/useTeams"));
describe('useTeams', function () {
    // @ts-expect-error
    const org = TestStubs.Organization();
    // @ts-expect-error
    const mockTeams = [TestStubs.Team()];
    it('provides teams from the team store', function () {
        (0, react_hooks_1.act)(() => void teamStore_1.default.loadInitialData(mockTeams));
        const { result } = (0, react_hooks_1.renderHook)(() => (0, useTeams_1.default)());
        const { teams } = result.current;
        expect(teams).toBe(mockTeams);
    });
    it('loads more teams when using onSearch', function () {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            (0, react_hooks_1.act)(() => void teamStore_1.default.loadInitialData(mockTeams));
            (0, react_hooks_1.act)(() => void organizationStore_1.default.onUpdate(org, { replace: true }));
            // @ts-expect-error
            const newTeam2 = TestStubs.Team({ id: '2', slug: 'test-team2' });
            // @ts-expect-error
            const newTeam3 = TestStubs.Team({ id: '3', slug: 'test-team3' });
            // @ts-expect-error
            const mockRequest = MockApiClient.addMockResponse({
                url: `/organizations/${org.slug}/teams/`,
                method: 'GET',
                query: { query: 'test' },
                body: [newTeam2, newTeam3],
            });
            const { result, waitFor } = (0, react_hooks_1.renderHook)(() => (0, useTeams_1.default)());
            const { onSearch } = result.current;
            // Works with append
            const onSearchPromise = (0, react_hooks_1.act)(() => onSearch('test'));
            expect(result.current.fetching).toBe(true);
            yield onSearchPromise;
            expect(result.current.fetching).toBe(false);
            // Wait for state to be reflected from the store
            yield waitFor(() => result.current.teams.length === 3);
            expect(mockRequest).toHaveBeenCalled();
            expect(result.current.teams).toEqual([...mockTeams, newTeam2, newTeam3]);
            // de-duplicates itesm in the query results
            mockRequest.mockClear();
            yield (0, react_hooks_1.act)(() => onSearch('test'));
            // No new items have been added
            expect(mockRequest).toHaveBeenCalled();
            expect(result.current.teams).toEqual([...mockTeams, newTeam2, newTeam3]);
        });
    });
    it('provides only the users teams', function () {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            // @ts-expect-error
            const userTeams = [TestStubs.Team({ isMember: true })];
            // @ts-expect-error
            const nonUserTeams = [TestStubs.Team({ isMember: false })];
            (0, react_hooks_1.act)(() => void teamStore_1.default.loadInitialData([...userTeams, ...nonUserTeams]));
            const { result } = (0, react_hooks_1.renderHook)(props => (0, useTeams_1.default)(props), {
                initialProps: { provideUserTeams: true },
            });
            const { teams } = result.current;
            expect(teams.length).toBe(1);
            expect(teams).toEqual(expect.arrayContaining(userTeams));
        });
    });
    it('provides only the specified slugs', function () {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            (0, react_hooks_1.act)(() => void teamStore_1.default.loadInitialData(mockTeams));
            // @ts-expect-error
            const teamFoo = TestStubs.Team({ slug: 'foo' });
            // @ts-expect-error
            const mockRequest = MockApiClient.addMockResponse({
                url: `/organizations/${org.slug}/teams/`,
                method: 'GET',
                query: { slug: 'foo' },
                body: [teamFoo],
            });
            const { result, waitFor } = (0, react_hooks_1.renderHook)(props => (0, useTeams_1.default)(props), {
                initialProps: { slugs: ['foo'] },
            });
            expect(result.current.initiallyLoaded).toBe(false);
            expect(mockRequest).toHaveBeenCalled();
            yield waitFor(() => expect(result.current.teams.length).toBe(1));
            const { teams } = result.current;
            expect(teams).toEqual(expect.arrayContaining([teamFoo]));
        });
    });
    it('only loads slugs when needed', function () {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            (0, react_hooks_1.act)(() => void teamStore_1.default.loadInitialData(mockTeams));
            const { result } = (0, react_hooks_1.renderHook)(props => (0, useTeams_1.default)(props), {
                initialProps: { slugs: [mockTeams[0].slug] },
            });
            const { teams, initiallyLoaded } = result.current;
            expect(initiallyLoaded).toBe(true);
            expect(teams).toEqual(expect.arrayContaining(mockTeams));
        });
    });
});
//# sourceMappingURL=useTeams.spec.jsx.map