Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_router_1 = require("react-router");
const enzyme_1 = require("sentry-test/enzyme");
const initializeOrg_1 = require("sentry-test/initializeOrg");
const api_1 = require("app/api");
const dashboardWidgetQuerySelectorModal_1 = (0, tslib_1.__importDefault)(require("app/components/modals/dashboardWidgetQuerySelectorModal"));
const locale_1 = require("app/locale");
const types_1 = require("app/views/dashboardsV2/types");
const stubEl = props => <div>{props.children}</div>;
const api = new api_1.Client();
function mountModal({ initialData, widget }) {
    return (0, enzyme_1.mountWithTheme)(<dashboardWidgetQuerySelectorModal_1.default Header={stubEl} 
    // @ts-expect-error
    Footer={stubEl} 
    // @ts-expect-error
    Body={stubEl} organization={initialData.organization} widget={widget} api={api}/>, initialData.routerContext);
}
describe('Modals -> AddDashboardWidgetModal', function () {
    const initialData = (0, initializeOrg_1.initializeOrg)({
        organization: {
            features: ['performance-view', 'discover-query'],
            apdexThreshold: 400,
        },
        router: {},
        project: 1,
        projects: [],
    });
    let mockQuery;
    let mockWidget;
    beforeEach(function () {
        mockQuery = {
            conditions: 'title:/organizations/:orgId/performance/summary/',
            fields: ['count()', 'failure_count()'],
            id: '1',
            name: 'Query Name',
            orderby: '',
        };
        mockWidget = {
            title: 'Test Widget',
            displayType: types_1.DisplayType.AREA,
            interval: '5m',
            queries: [mockQuery],
        };
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: '/organizations/org-slug/dashboards/widgets/',
            method: 'POST',
            statusCode: 200,
            body: [],
        });
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: '/organizations/org-slug/events-stats/',
            body: [],
        });
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: '/organizations/org-slug/eventsv2/',
            body: { data: [{ 'event.type': 'error' }], meta: { 'event.type': 'string' } },
        });
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: '/organizations/org-slug/events-geo/',
            body: { data: [], meta: {} },
        });
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: '/organizations/org-slug/recent-searches/',
            body: [],
        });
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: '/organizations/org-slug/dashboards/',
            body: [{ id: '1', title: (0, locale_1.t)('Test Dashboard') }],
        });
    });
    afterEach(() => {
        // @ts-expect-error
        MockApiClient.clearMockResponses();
    });
    it('renders a single query selection when the widget only has one query', function () {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const wrapper = mountModal({ initialData, widget: mockWidget });
            // @ts-expect-error
            yield tick();
            expect(wrapper.find('StyledInput').length).toEqual(1);
            expect(wrapper.find('StyledInput').props().value).toEqual('title:/organizations/:orgId/performance/summary/');
            expect(wrapper.find('OpenInDiscoverButton').length).toEqual(1);
            wrapper.unmount();
        });
    });
    it('renders a multiple query selections when the widget only has multiple queries', function () {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            mockWidget.queries.push(Object.assign(Object.assign({}, mockQuery), { conditions: 'title:/organizations/:orgId/performance/', id: '2' }));
            mockWidget.queries.push(Object.assign(Object.assign({}, mockQuery), { conditions: 'title:/organizations/:orgId/', id: '3' }));
            const wrapper = mountModal({ initialData, widget: mockWidget });
            // @ts-expect-error
            yield tick();
            expect(wrapper.find('StyledInput').length).toEqual(3);
            expect(wrapper.find('StyledInput').at(0).props().value).toEqual('title:/organizations/:orgId/performance/summary/');
            expect(wrapper.find('StyledInput').at(1).props().value).toEqual('title:/organizations/:orgId/performance/');
            expect(wrapper.find('StyledInput').at(2).props().value).toEqual('title:/organizations/:orgId/');
            expect(wrapper.find('OpenInDiscoverButton').length).toEqual(3);
            wrapper.unmount();
        });
    });
    it('links user to the query in discover when a query is selected from the modal', function () {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const wrapper = mountModal({ initialData, widget: mockWidget });
            // @ts-expect-error
            yield tick();
            wrapper.find('OpenInDiscoverButton').simulate('click');
            expect(react_router_1.browserHistory.push).toHaveBeenCalledWith(expect.objectContaining({
                pathname: '/organizations/org-slug/discover/results/',
                query: expect.objectContaining({
                    field: ['count()', 'failure_count()'],
                    name: 'Test Widget',
                    query: 'title:/organizations/:orgId/performance/summary/',
                    yAxis: ['count()', 'failure_count()'],
                }),
            }));
            wrapper.unmount();
        });
    });
    it('links user to the query in discover with additional field when a world map query is selected from the modal', function () {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            mockWidget.queries[0].fields = ['count()'];
            mockWidget.displayType = types_1.DisplayType.WORLD_MAP;
            const wrapper = mountModal({ initialData, widget: mockWidget });
            // @ts-expect-error
            yield tick();
            wrapper.find('OpenInDiscoverButton').simulate('click');
            expect(react_router_1.browserHistory.push).toHaveBeenCalledWith({
                pathname: '/organizations/org-slug/discover/results/',
                query: expect.objectContaining({
                    field: ['geo.country_code', 'count()'],
                    name: 'Test Widget',
                    query: 'title:/organizations/:orgId/performance/summary/ has:geo.country_code',
                    yAxis: ['count()'],
                }),
            });
            wrapper.unmount();
        });
    });
});
//# sourceMappingURL=dashboardWidgetQuerySelectorModal.spec.jsx.map