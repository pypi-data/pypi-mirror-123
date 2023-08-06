Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const enzyme_1 = require("sentry-test/enzyme");
const initializeOrg_1 = require("sentry-test/initializeOrg");
const notificationSettingsByProjects_1 = (0, tslib_1.__importDefault)(require("app/views/settings/account/notifications/notificationSettingsByProjects"));
const createWrapper = (projects) => {
    const { routerContext } = (0, initializeOrg_1.initializeOrg)();
    // @ts-expect-error
    MockApiClient.addMockResponse({
        url: '/projects/',
        method: 'GET',
        body: projects,
    });
    const notificationSettings = {
        alerts: {
            user: { me: { email: 'always', slack: 'always' } },
            project: Object.fromEntries(projects.map(project => [project.id, { email: 'never', slack: 'never' }])),
        },
    };
    return (0, enzyme_1.mountWithTheme)(<notificationSettingsByProjects_1.default notificationType="alerts" notificationSettings={notificationSettings} onChange={jest.fn()}/>, routerContext);
};
describe('NotificationSettingsByProjects', function () {
    it('should render when there are no projects', function () {
        const wrapper = createWrapper([]);
        expect(wrapper.find('EmptyMessage').text()).toEqual('No projects found');
        expect(wrapper.find('AsyncComponentSearchInput')).toHaveLength(0);
        expect(wrapper.find('Pagination')).toHaveLength(0);
    });
    it('should show search bar when there are enough projects', function () {
        // @ts-expect-error
        const organization = TestStubs.Organization();
        const projects = [...Array(3).keys()].map(id => 
        // @ts-expect-error
        TestStubs.Project({ organization, id }));
        const wrapper = createWrapper(projects);
        expect(wrapper.find('AsyncComponentSearchInput')).toHaveLength(1);
    });
});
//# sourceMappingURL=notificationSettingsByProjects.spec.jsx.map