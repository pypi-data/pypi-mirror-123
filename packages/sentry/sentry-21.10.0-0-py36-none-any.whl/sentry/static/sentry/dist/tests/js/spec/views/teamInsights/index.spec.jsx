Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reactTestingLibrary_1 = require("sentry-test/reactTestingLibrary");
const projectsStore_1 = (0, tslib_1.__importDefault)(require("app/stores/projectsStore"));
const teamInsights_1 = (0, tslib_1.__importDefault)(require("app/views/teamInsights"));
describe('TeamInsightsContainer', () => {
    afterEach(() => {
        projectsStore_1.default.reset();
    });
    it('blocks access if org is missing flag', () => {
        // @ts-expect-error
        const organization = TestStubs.Organization();
        // @ts-expect-error
        const context = TestStubs.routerContext([{ organization }]);
        (0, reactTestingLibrary_1.mountWithTheme)(<teamInsights_1.default organization={organization}>
        <div>test</div>
      </teamInsights_1.default>, { context });
        expect(reactTestingLibrary_1.screen.queryByText('test')).toBeNull();
    });
    it('allows access for orgs with flag', () => {
        projectsStore_1.default.loadInitialData([
            // @ts-expect-error
            TestStubs.Project(),
        ]);
        // @ts-expect-error
        const organization = TestStubs.Organization({ features: ['team-insights'] });
        // @ts-expect-error
        const context = TestStubs.routerContext([{ organization }]);
        (0, reactTestingLibrary_1.mountWithTheme)(<teamInsights_1.default organization={organization}>
        <div>test</div>
      </teamInsights_1.default>, { context });
        expect(reactTestingLibrary_1.screen.getByText('test')).toBeTruthy();
    });
    it('shows message for users with no teams', () => {
        projectsStore_1.default.loadInitialData([]);
        // @ts-expect-error
        const organization = TestStubs.Organization({ features: ['team-insights'] });
        // @ts-expect-error
        const context = TestStubs.routerContext([{ organization }]);
        (0, reactTestingLibrary_1.mountWithTheme)(<teamInsights_1.default organization={organization}/>, { context });
        expect(reactTestingLibrary_1.screen.getByText('You need at least one project to use this view')).toBeTruthy();
    });
});
//# sourceMappingURL=index.spec.jsx.map