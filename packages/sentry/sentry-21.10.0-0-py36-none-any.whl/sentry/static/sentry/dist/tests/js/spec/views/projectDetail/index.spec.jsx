Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const initializeOrg_1 = require("sentry-test/initializeOrg");
const reactTestingLibrary_1 = require("sentry-test/reactTestingLibrary");
const utils_1 = require("sentry-test/utils");
const globalSelectionStore_1 = (0, tslib_1.__importDefault)(require("app/stores/globalSelectionStore"));
const projectsStore_1 = (0, tslib_1.__importDefault)(require("app/stores/projectsStore"));
const projectDetail_1 = (0, tslib_1.__importDefault)(require("app/views/projectDetail/projectDetail"));
describe('ProjectDetail', function () {
    const { routerContext, organization, project, router } = (0, initializeOrg_1.initializeOrg)();
    const params = Object.assign(Object.assign({}, router.params), { projectId: project.slug });
    beforeEach(() => {
        globalSelectionStore_1.default.reset();
        projectsStore_1.default.reset();
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: '/organizations/org-slug/sdk-updates/',
            body: [],
        });
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: '/prompts-activity/',
            body: {},
        });
    });
    describe('project low priority queue alert', function () {
        it('does not render alert', function () {
            return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
                const projects = [
                    Object.assign(Object.assign({}, project), { eventProcessing: {
                            symbolicationDegraded: false,
                        } }),
                ];
                // @ts-expect-error
                MockApiClient.addMockResponse({
                    url: '/organizations/org-slug/projects/',
                    body: projects,
                });
                // @ts-expect-error
                MockApiClient.addMockResponse({
                    url: '/projects/org-slug/project-slug/',
                    data: projects[0],
                });
                projectsStore_1.default.loadInitialData(projects);
                (0, reactTestingLibrary_1.mountWithTheme)(<projectDetail_1.default organization={organization} {...router} params={params}/>, { context: routerContext });
                yield (0, reactTestingLibrary_1.waitForElementToBeRemoved)(() => reactTestingLibrary_1.screen.getByText('Loading\u2026'));
                expect(reactTestingLibrary_1.screen.queryByText('Event Processing for this project is currently degraded. Events may appear with larger delays than usual or get dropped.', { exact: false })).toBe(null);
            });
        });
        it('renders alert', function () {
            return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
                const projects = [
                    Object.assign(Object.assign({}, project), { eventProcessing: {
                            symbolicationDegraded: true,
                        } }),
                ];
                projectsStore_1.default.loadInitialData(projects);
                // @ts-expect-error
                MockApiClient.addMockResponse({
                    url: '/organizations/org-slug/projects/',
                    body: projects,
                });
                // @ts-expect-error
                MockApiClient.addMockResponse({
                    url: '/projects/org-slug/project-slug/',
                    data: projects[0],
                });
                (0, reactTestingLibrary_1.mountWithTheme)(<projectDetail_1.default organization={organization} {...router} params={params}/>, { context: routerContext });
                yield (0, reactTestingLibrary_1.waitForElementToBeRemoved)(() => reactTestingLibrary_1.screen.getByText('Loading\u2026'));
                expect(yield (0, utils_1.findByTextContent)(reactTestingLibrary_1.screen, 'Event Processing for this project is currently degraded. Events may appear with larger delays than usual or get dropped. Please check the Status page for a potential outage.')).toBeInTheDocument();
            });
        });
    });
});
//# sourceMappingURL=index.spec.jsx.map