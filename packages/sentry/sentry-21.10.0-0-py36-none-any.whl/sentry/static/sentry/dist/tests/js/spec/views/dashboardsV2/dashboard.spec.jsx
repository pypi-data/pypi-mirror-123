Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const enzyme_1 = require("sentry-test/enzyme");
const initializeOrg_1 = require("sentry-test/initializeOrg");
const dashboard_1 = (0, tslib_1.__importDefault)(require("app/views/dashboardsV2/dashboard"));
const types_1 = require("app/views/dashboardsV2/types");
describe('Dashboards > Dashboard', () => {
    // @ts-expect-error
    const organization = TestStubs.Organization({
        features: ['dashboards-basic', 'dashboards-edit'],
    });
    const mockDashboard = {
        dateCreated: '2021-08-10T21:20:46.798237Z',
        id: '1',
        title: 'Test Dashboard',
        widgets: [],
    };
    const newWidget = {
        title: 'Test Query',
        displayType: types_1.DisplayType.LINE,
        interval: '5m',
        queries: [
            {
                name: '',
                conditions: '',
                fields: ['count()'],
                orderby: '',
            },
        ],
    };
    let initialData;
    beforeEach(() => {
        initialData = (0, initializeOrg_1.initializeOrg)({ organization, router: {}, project: 1, projects: [] });
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: `/organizations/org-slug/dashboards/widgets/`,
            method: 'POST',
            body: [],
        });
    });
    it('dashboard adds new widget if component is mounted with newWidget prop', () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const mock = jest.fn();
        const wrapper = (0, enzyme_1.mountWithTheme)(<dashboard_1.default paramDashboardId="1" dashboard={mockDashboard} organization={initialData.organization} isEditing={false} onUpdate={mock} onSetWidgetToBeUpdated={() => undefined} router={initialData.router} location={initialData.location} newWidget={newWidget}/>, initialData.routerContext);
        // @ts-expect-error
        yield tick();
        wrapper.update();
        expect(mock).toHaveBeenCalled();
    }));
    it('dashboard adds new widget if component updated with newWidget prop', () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const mock = jest.fn();
        const wrapper = (0, enzyme_1.mountWithTheme)(<dashboard_1.default paramDashboardId="1" dashboard={mockDashboard} organization={initialData.organization} isEditing={false} onUpdate={mock} onSetWidgetToBeUpdated={() => undefined} router={initialData.router} location={initialData.location}/>, initialData.routerContext);
        expect(mock).not.toHaveBeenCalled();
        wrapper.setProps({ newWidget });
        // @ts-expect-error
        yield tick();
        wrapper.update();
        expect(mock).toHaveBeenCalled();
    }));
});
//# sourceMappingURL=dashboard.spec.jsx.map