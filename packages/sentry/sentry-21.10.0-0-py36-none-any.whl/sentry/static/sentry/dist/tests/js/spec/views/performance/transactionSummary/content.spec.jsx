Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const enzyme_1 = require("sentry-test/enzyme");
const initializeOrg_1 = require("sentry-test/initializeOrg");
const eventView_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/eventView"));
const filter_1 = require("app/views/performance/transactionSummary/filter");
const content_1 = (0, tslib_1.__importDefault)(require("app/views/performance/transactionSummary/transactionOverview/content"));
function initialize(projects, query, additionalFeatures = []) {
    const features = ['transaction-event', 'performance-view', ...additionalFeatures];
    // @ts-expect-error
    const organization = TestStubs.Organization({
        features,
        projects,
    });
    const initialOrgData = {
        organization,
        router: {
            location: {
                query: Object.assign({}, query),
            },
        },
        project: 1,
        projects: [],
    };
    const initialData = (0, initializeOrg_1.initializeOrg)(initialOrgData);
    const eventView = eventView_1.default.fromNewQueryWithLocation({
        id: undefined,
        version: 2,
        name: 'test-transaction',
        fields: ['id', 'user.display', 'transaction.duration', 'trace', 'timestamp'],
        projects: [],
    }, initialData.router.location);
    const spanOperationBreakdownFilter = filter_1.SpanOperationBreakdownFilter.None;
    const transactionName = 'example-transaction';
    return Object.assign(Object.assign({}, initialData), { spanOperationBreakdownFilter,
        transactionName, location: initialData.router.location, eventView });
}
describe('Transaction Summary Content', function () {
    beforeEach(function () {
        // @ts-expect-error
        MockApiClient.addMockResponse({
            method: 'GET',
            url: '/prompts-activity/',
            body: {},
        });
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: '/organizations/org-slug/sdk-updates/',
            body: [],
        });
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: '/organizations/org-slug/eventsv2/',
            body: { data: [{ 'event.type': 'error' }], meta: { 'event.type': 'string' } },
        });
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: '/organizations/org-slug/users/',
            body: [],
        });
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: '/organizations/org-slug/issues/?limit=5&query=is%3Aunresolved%20transaction%3Aexample-transaction&sort=new&statsPeriod=14d',
            body: [],
        });
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: '/organizations/org-slug/events-facets/',
            body: [],
        });
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: '/organizations/org-slug/releases/stats/',
            body: [],
        });
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: '/organizations/org-slug/events-stats/',
            body: [],
        });
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: '/organizations/org-slug/events-has-measurements/',
            body: { measurements: false },
        });
    });
    afterEach(function () {
        // @ts-expect-error
        MockApiClient.clearMockResponses();
    });
    it('Basic Rendering', function () {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            // @ts-expect-error
            const projects = [TestStubs.Project()];
            const { organization, location, eventView, spanOperationBreakdownFilter, transactionName, } = initialize(projects, {});
            // @ts-expect-error
            const routerContext = TestStubs.routerContext([{ organization }]);
            const wrapper = (0, enzyme_1.mountWithTheme)(<content_1.default location={location} organization={organization} eventView={eventView} transactionName={transactionName} isLoading={false} totalValues={null} spanOperationBreakdownFilter={spanOperationBreakdownFilter} error={null} onChangeFilter={() => { }}/>, routerContext);
            // @ts-expect-error
            yield tick();
            wrapper.update();
            expect(wrapper.find('Filter')).toHaveLength(1);
            expect(wrapper.find('StyledSearchBar')).toHaveLength(1);
            expect(wrapper.find('TransactionSummaryCharts')).toHaveLength(1);
            expect(wrapper.find('TransactionsList')).toHaveLength(1);
            expect(wrapper.find('UserStats')).toHaveLength(1);
            expect(wrapper.find('StatusBreakdown')).toHaveLength(1);
            expect(wrapper.find('SidebarCharts')).toHaveLength(1);
            expect(wrapper.find('DiscoverQuery')).toHaveLength(2);
            const transactionListProps = wrapper.find('TransactionsList').first().props();
            expect(transactionListProps.generateDiscoverEventView).toBeDefined();
            expect(transactionListProps.handleOpenInDiscoverClick).toBeDefined();
            expect(transactionListProps.generatePerformanceTransactionEventsView).toBeUndefined();
            expect(transactionListProps.handleOpenAllEventsClick).toBeUndefined();
        });
    });
    it('Renders with generatePerformanceTransactionEventsView instead when feature flagged', function () {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            // @ts-expect-error
            const projects = [TestStubs.Project()];
            const { organization, location, eventView, spanOperationBreakdownFilter, transactionName, } = initialize(projects, {}, ['performance-events-page']);
            // @ts-expect-error
            const routerContext = TestStubs.routerContext([{ organization }]);
            const wrapper = (0, enzyme_1.mountWithTheme)(<content_1.default location={location} organization={organization} eventView={eventView} transactionName={transactionName} isLoading={false} totalValues={null} spanOperationBreakdownFilter={spanOperationBreakdownFilter} error={null} onChangeFilter={() => { }}/>, routerContext);
            // @ts-expect-error
            yield tick();
            wrapper.update();
            expect(wrapper.find('Filter')).toHaveLength(1);
            expect(wrapper.find('StyledSearchBar')).toHaveLength(1);
            expect(wrapper.find('TransactionSummaryCharts')).toHaveLength(1);
            expect(wrapper.find('TransactionsList')).toHaveLength(1);
            expect(wrapper.find('UserStats')).toHaveLength(1);
            expect(wrapper.find('StatusBreakdown')).toHaveLength(1);
            expect(wrapper.find('SidebarCharts')).toHaveLength(1);
            expect(wrapper.find('DiscoverQuery')).toHaveLength(2);
            const transactionListProps = wrapper.find('TransactionsList').first().props();
            expect(transactionListProps.generateDiscoverEventView).toBeUndefined();
            expect(transactionListProps.handleOpenInDiscoverClick).toBeUndefined();
            expect(transactionListProps.generatePerformanceTransactionEventsView).toBeDefined();
            expect(transactionListProps.handleOpenAllEventsClick).toBeDefined();
        });
    });
    it('Renders TransactionSummaryCharts withoutZerofill when feature flagged', function () {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            // @ts-expect-error
            const projects = [TestStubs.Project()];
            const { organization, location, eventView, spanOperationBreakdownFilter, transactionName, } = initialize(projects, {}, [
                'performance-events-page',
                'performance-chart-interpolation',
            ]);
            // @ts-expect-error
            const routerContext = TestStubs.routerContext([{ organization }]);
            const wrapper = (0, enzyme_1.mountWithTheme)(<content_1.default location={location} organization={organization} eventView={eventView} transactionName={transactionName} isLoading={false} totalValues={null} spanOperationBreakdownFilter={spanOperationBreakdownFilter} error={null} onChangeFilter={() => { }}/>, routerContext);
            // @ts-expect-error
            yield tick();
            wrapper.update();
            expect(wrapper.find('TransactionSummaryCharts')).toHaveLength(1);
            const transactionSummaryChartsProps = wrapper
                .find('TransactionSummaryCharts')
                .first()
                .props();
            expect(transactionSummaryChartsProps.withoutZerofill).toEqual(true);
        });
    });
});
//# sourceMappingURL=content.spec.jsx.map