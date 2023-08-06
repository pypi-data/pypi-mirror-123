Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const enzyme_1 = require("sentry-test/enzyme");
const initializeOrg_1 = require("sentry-test/initializeOrg");
const eventView_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/eventView"));
const header_1 = (0, tslib_1.__importDefault)(require("app/views/performance/transactionSummary/header"));
const tabs_1 = (0, tslib_1.__importDefault)(require("app/views/performance/transactionSummary/tabs"));
function initializeData(opts) {
    const { features, platform } = opts !== null && opts !== void 0 ? opts : {};
    // @ts-expect-error
    const project = TestStubs.Project({ platform });
    // @ts-expect-error
    const organization = TestStubs.Organization({
        projects: [project],
        features,
    });
    const initialData = (0, initializeOrg_1.initializeOrg)({
        organization,
        router: {
            location: {
                query: {
                    project: project.id,
                },
            },
        },
        project: project.id,
        projects: [],
    });
    const router = initialData.router;
    const eventView = eventView_1.default.fromSavedQuery({
        id: undefined,
        version: 2,
        name: '',
        fields: ['transaction.status'],
        projects: [parseInt(project.id, 10)],
    });
    return {
        project,
        organization,
        router,
        eventView,
    };
}
describe('Performance > Transaction Summary Header', function () {
    let wrapper;
    afterEach(function () {
        // @ts-expect-error
        MockApiClient.clearMockResponses();
        wrapper.unmount();
    });
    it('should render web vitals tab when yes', function () {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { project, organization, router, eventView } = initializeData();
            wrapper = (0, enzyme_1.mountWithTheme)(<header_1.default eventView={eventView} location={router.location} organization={organization} projects={[project]} projectId={project.id} transactionName="transaction_name" currentTab={tabs_1.default.TransactionSummary} hasWebVitals="yes" handleIncompatibleQuery={() => { }}/>);
            // @ts-expect-error
            yield tick();
            wrapper.update();
            expect(wrapper.find('ListLink[data-test-id="web-vitals-tab"]').exists()).toBeTruthy();
        });
    });
    it('should not render web vitals tab when no', function () {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { project, organization, router, eventView } = initializeData();
            wrapper = (0, enzyme_1.mountWithTheme)(<header_1.default eventView={eventView} location={router.location} organization={organization} projects={[project]} projectId={project.id} transactionName="transaction_name" currentTab={tabs_1.default.TransactionSummary} hasWebVitals="no" handleIncompatibleQuery={() => { }}/>);
            // @ts-expect-error
            yield tick();
            wrapper.update();
            expect(wrapper.find('ListLink[data-test-id="web-vitals-tab"]').exists()).toBeFalsy();
        });
    });
    it('should render web vitals tab when maybe and is frontend platform', function () {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { project, organization, router, eventView } = initializeData({
                platform: 'javascript',
            });
            wrapper = (0, enzyme_1.mountWithTheme)(<header_1.default eventView={eventView} location={router.location} organization={organization} projects={[project]} projectId={project.id} transactionName="transaction_name" currentTab={tabs_1.default.TransactionSummary} hasWebVitals="maybe" handleIncompatibleQuery={() => { }}/>);
            // @ts-expect-error
            yield tick();
            wrapper.update();
            expect(wrapper.find('ListLink[data-test-id="web-vitals-tab"]').exists()).toBeTruthy();
        });
    });
    it('should render web vitals tab when maybe and has measurements', function () {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            // @ts-expect-error
            MockApiClient.addMockResponse({
                url: '/organizations/org-slug/events-has-measurements/',
                body: { measurements: true },
            });
            const { project, organization, router, eventView } = initializeData();
            wrapper = (0, enzyme_1.mountWithTheme)(<header_1.default eventView={eventView} location={router.location} organization={organization} projects={[project]} projectId={project.id} transactionName="transaction_name" currentTab={tabs_1.default.TransactionSummary} hasWebVitals="maybe" handleIncompatibleQuery={() => { }}/>);
            // @ts-expect-error
            yield tick();
            wrapper.update();
            expect(wrapper.find('ListLink[data-test-id="web-vitals-tab"]').exists()).toBeTruthy();
        });
    });
    it('should not render web vitals tab when maybe and has no measurements', function () {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            // @ts-expect-error
            MockApiClient.addMockResponse({
                url: '/organizations/org-slug/events-has-measurements/',
                body: { measurements: false },
            });
            const { project, organization, router, eventView } = initializeData();
            wrapper = (0, enzyme_1.mountWithTheme)(<header_1.default eventView={eventView} location={router.location} organization={organization} projects={[project]} projectId={project.id} transactionName="transaction_name" currentTab={tabs_1.default.TransactionSummary} hasWebVitals="maybe" handleIncompatibleQuery={() => { }}/>);
            // @ts-expect-error
            yield tick();
            wrapper.update();
            expect(wrapper.find('ListLink[data-test-id="web-vitals-tab"]').exists()).toBeFalsy();
        });
    });
    it('should render spans tab with feature', function () {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { project, organization, router, eventView } = initializeData({
                features: ['performance-suspect-spans-view'],
            });
            wrapper = (0, enzyme_1.mountWithTheme)(<header_1.default eventView={eventView} location={router.location} organization={organization} projects={[project]} projectId={project.id} transactionName="transaction_name" currentTab={tabs_1.default.TransactionSummary} hasWebVitals="yes" handleIncompatibleQuery={() => { }}/>);
            // @ts-expect-error
            yield tick();
            wrapper.update();
            expect(wrapper.find('ListLink[data-test-id="spans-tab"]').exists()).toBeTruthy();
        });
    });
});
//# sourceMappingURL=header.spec.jsx.map