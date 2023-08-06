Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const enzyme_1 = require("sentry-test/enzyme");
const initializeOrg_1 = require("sentry-test/initializeOrg");
const notificationSettings_1 = (0, tslib_1.__importDefault)(require("app/views/settings/account/notifications/notificationSettings"));
const createWrapper = (notificationSettings) => {
    const { routerContext } = (0, initializeOrg_1.initializeOrg)();
    // @ts-expect-error
    MockApiClient.addMockResponse({
        url: '/users/me/notification-settings/',
        method: 'GET',
        body: notificationSettings,
    });
    // @ts-expect-error
    MockApiClient.addMockResponse({
        url: '/users/me/notifications/',
        method: 'GET',
        body: {
            personalActivityNotifications: true,
            selfAssignOnResolve: true,
            weeklyReports: true,
        },
    });
    return (0, enzyme_1.mountWithTheme)(<notificationSettings_1.default />, routerContext);
};
describe('NotificationSettings', function () {
    it('should render', function () {
        const wrapper = createWrapper({
            alerts: { user: { me: { email: 'never', slack: 'never' } } },
            deploy: { user: { me: { email: 'never', slack: 'never' } } },
            workflow: { user: { me: { email: 'never', slack: 'never' } } },
        });
        // There are 7 notification setting Selects/Toggles.
        const fields = wrapper.find('Field');
        expect(fields).toHaveLength(7);
    });
});
//# sourceMappingURL=notificationSettings.spec.jsx.map