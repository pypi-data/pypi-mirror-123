Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const enzyme_1 = require("sentry-test/enzyme");
const initializeOrg_1 = require("sentry-test/initializeOrg");
const locale_1 = require("app/locale");
const projectsStore_1 = (0, tslib_1.__importDefault)(require("app/stores/projectsStore"));
const eventView_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/eventView"));
const fields_1 = require("app/utils/discover/fields");
const eventsTable_1 = (0, tslib_1.__importDefault)(require("app/views/performance/transactionSummary/transactionEvents/eventsTable"));
function initializeData({ features: additionalFeatures = [] }) {
    const features = ['discover-basic', 'performance-view', ...additionalFeatures];
    // @ts-expect-error
    const organization = TestStubs.Organization({
        features,
        // @ts-expect-error
        projects: [TestStubs.Project()],
        apdexThreshold: 400,
    });
    const initialData = (0, initializeOrg_1.initializeOrg)({
        organization,
        router: {
            location: {
                query: {
                    transaction: '/performance',
                    project: 1,
                    transactionCursor: '1:0:0',
                },
            },
        },
        project: 1,
        projects: [],
    });
    projectsStore_1.default.loadInitialData(initialData.organization.projects);
    return initialData;
}
describe('Performance GridEditable Table', function () {
    let transactionsListTitles;
    let fields;
    let organization;
    let data;
    let transactionName;
    const query = 'transaction.duration:<15m event.type:transaction transaction:/api/0/organizations/{organization_slug}/eventsv2/';
    beforeEach(function () {
        transactionName = 'transactionName';
        transactionsListTitles = [
            (0, locale_1.t)('event id'),
            (0, locale_1.t)('user'),
            (0, locale_1.t)('operation duration'),
            (0, locale_1.t)('total duration'),
            (0, locale_1.t)('trace id'),
            (0, locale_1.t)('timestamp'),
        ];
        fields = [
            'id',
            'user.display',
            fields_1.SPAN_OP_RELATIVE_BREAKDOWN_FIELD,
            'transaction.duration',
            'trace',
            'timestamp',
            'spans.total.time',
            ...fields_1.SPAN_OP_BREAKDOWN_FIELDS,
        ];
        // @ts-expect-error
        organization = TestStubs.Organization();
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: '/organizations/org-slug/projects/',
            body: [],
        });
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: '/prompts-activity/',
            body: {},
        });
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: '/organizations/org-slug/sdk-updates/',
            body: [],
        });
        data = [
            {
                id: 'deadbeef',
                'user.display': 'uhoh@example.com',
                'transaction.duration': 400,
                'project.id': 1,
                timestamp: '2020-05-21T15:31:18+00:00',
                trace: '1234',
                'span_ops_breakdown.relative': '',
                'spans.browser': 100,
                'spans.db': 30,
                'spans.http': 170,
                'spans.resource': 100,
                'spans.total.time': 400,
            },
            {
                id: 'moredeadbeef',
                'user.display': 'moreuhoh@example.com',
                'transaction.duration': 600,
                'project.id': 1,
                timestamp: '2020-05-22T15:31:18+00:00',
                trace: '4321',
                'span_ops_breakdown.relative': '',
                'spans.browser': 100,
                'spans.db': 300,
                'spans.http': 100,
                'spans.resource': 100,
                'spans.total.time': 600,
            },
        ];
        // Transaction list response
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: '/organizations/org-slug/eventsv2/',
            headers: {
                Link: '<http://localhost/api/0/organizations/org-slug/eventsv2/?cursor=2:0:0>; rel="next"; results="true"; cursor="2:0:0",' +
                    '<http://localhost/api/0/organizations/org-slug/eventsv2/?cursor=1:0:0>; rel="previous"; results="false"; cursor="1:0:0"',
            },
            body: {
                meta: {
                    id: 'string',
                    'user.display': 'string',
                    'transaction.duration': 'duration',
                    'project.id': 'integer',
                    timestamp: 'date',
                },
                data,
            },
        }, {
            predicate: (url, options) => {
                var _a;
                return (url.includes('eventsv2') && ((_a = options.query) === null || _a === void 0 ? void 0 : _a.field.includes('user.display')));
            },
        });
    });
    afterEach(function () {
        // @ts-expect-error
        MockApiClient.clearMockResponses();
        projectsStore_1.default.reset();
        jest.clearAllMocks();
    });
    it('renders ops breakdown bar when querying for span_ops_breakdown.relative', function () {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const initialData = initializeData({ features: ['performance-events-page'] });
            const eventView = eventView_1.default.fromNewQueryWithLocation({
                id: undefined,
                version: 2,
                name: 'transactionName',
                fields,
                query,
                projects: [],
                orderby: '-timestamp',
            }, initialData.router.location);
            const wrapper = (0, enzyme_1.mountWithTheme)(<eventsTable_1.default eventView={eventView} organization={organization} location={initialData.router.location} setError={() => { }} columnTitles={transactionsListTitles} transactionName={transactionName}/>, initialData.routerContext);
            // @ts-expect-error
            yield tick();
            wrapper.update();
            expect(wrapper.find('GridHeadCell')).toHaveLength(6);
            expect(wrapper.find('GridHeadCellStatic')).toHaveLength(0);
            expect(wrapper.find('OperationSort')).toHaveLength(1);
            expect(wrapper.find('RelativeOpsBreakdown')).toHaveLength(2);
        });
    });
    it('renders basic columns without ops breakdown when not querying for span_ops_breakdown.relative', function () {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const initialData = initializeData({ features: ['performance-events-page'] });
            fields = [
                'id',
                'user.display',
                'transaction.duration',
                'trace',
                'timestamp',
                'spans.http',
            ];
            data.forEach(result => {
                delete result['span_ops_breakdown.relative'];
                delete result['spans.resource'];
                delete result['spans.browser'];
                delete result['spans.db'];
                delete result['spans.total.time'];
            });
            const eventView = eventView_1.default.fromNewQueryWithLocation({
                id: undefined,
                version: 2,
                name: 'transactionName',
                fields,
                query,
                projects: [],
                orderby: '-timestamp',
            }, initialData.router.location);
            const wrapper = (0, enzyme_1.mountWithTheme)(<eventsTable_1.default eventView={eventView} organization={organization} location={initialData.router.location} setError={() => { }} columnTitles={transactionsListTitles} transactionName={transactionName}/>, initialData.routerContext);
            // @ts-expect-error
            yield tick();
            wrapper.update();
            expect(wrapper.find('GridHeadCell')).toHaveLength(6);
            expect(wrapper.find('GridHeadCellStatic')).toHaveLength(0);
            expect(wrapper.find('OperationSort')).toHaveLength(0);
            expect(wrapper.find('RelativeOpsBreakdown')).toHaveLength(0);
        });
    });
});
//# sourceMappingURL=eventsTable.spec.jsx.map