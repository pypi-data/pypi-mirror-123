Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const enzyme_1 = require("sentry-test/enzyme");
const initializeOrg_1 = require("sentry-test/initializeOrg");
const notificationSettingsByOrganization_1 = (0, tslib_1.__importDefault)(require("app/views/settings/account/notifications/notificationSettingsByOrganization"));
const createWrapper = (notificationSettings) => {
    const { organization, routerContext } = (0, initializeOrg_1.initializeOrg)();
    return (0, enzyme_1.mountWithTheme)(<notificationSettingsByOrganization_1.default notificationType="alerts" notificationSettings={notificationSettings} organizations={[organization]} onChange={jest.fn()}/>, routerContext);
};
describe('NotificationSettingsByOrganization', function () {
    it('should render', function () {
        const wrapper = createWrapper({
            alerts: {
                user: { me: { email: 'always', slack: 'always' } },
                organization: { 1: { email: 'always', slack: 'always' } },
            },
        });
        expect(wrapper.find('Select')).toHaveLength(1);
    });
});
//# sourceMappingURL=notificationSettingsByOrganizations.spec.jsx.map