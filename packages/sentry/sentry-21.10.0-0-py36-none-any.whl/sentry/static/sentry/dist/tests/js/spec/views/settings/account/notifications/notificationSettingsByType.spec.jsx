Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const enzyme_1 = require("sentry-test/enzyme");
const initializeOrg_1 = require("sentry-test/initializeOrg");
const notificationSettingsByType_1 = (0, tslib_1.__importDefault)(require("app/views/settings/account/notifications/notificationSettingsByType"));
const addMockResponses = (notificationSettings, identities = [], organizationIntegrations = []) => {
    // @ts-expect-error
    MockApiClient.addMockResponse({
        url: '/users/me/notification-settings/',
        method: 'GET',
        body: notificationSettings,
    });
    // @ts-expect-error
    MockApiClient.addMockResponse({
        url: '/users/me/identities/',
        method: 'GET',
        body: identities,
    });
    // @ts-expect-error
    MockApiClient.addMockResponse({
        url: '/users/me/organization-integrations/',
        method: 'GET',
        body: organizationIntegrations,
    });
};
const createWrapper = (notificationSettings, identities = [], organizationIntegrations = []) => {
    const { routerContext } = (0, initializeOrg_1.initializeOrg)();
    // @ts-expect-error
    const org = TestStubs.Organization();
    addMockResponses(notificationSettings, identities, organizationIntegrations);
    return (0, enzyme_1.mountWithTheme)(<notificationSettingsByType_1.default notificationType="alerts" organizations={[org]}/>, routerContext);
};
describe('NotificationSettingsByType', function () {
    it('should render when everything is disabled', function () {
        const wrapper = createWrapper({
            alerts: { user: { me: { email: 'never', slack: 'never' } } },
        });
        // There is only one field and it is the default and it is set to "off".
        const fields = wrapper.find('Field');
        expect(fields).toHaveLength(1);
        expect(fields.at(0).find('FieldLabel').text()).toEqual('Issue Alerts');
        expect(fields.at(0).find('Select').text()).toEqual('Off');
    });
    it('should render when notification settings are enabled', function () {
        const wrapper = createWrapper({
            alerts: { user: { me: { email: 'always', slack: 'always' } } },
        });
        const fields = wrapper.find('Field');
        expect(fields).toHaveLength(2);
        expect(fields.at(0).find('FieldLabel').text()).toEqual('Issue Alerts');
        expect(fields.at(0).find('Select').text()).toEqual('On');
        expect(fields.at(1).find('FieldLabel').text()).toEqual('Delivery Method');
        expect(fields.at(1).find('Select').text()).toEqual('Send to Email and Slack');
    });
    it('should render warning modal when identity not linked', function () {
        // @ts-expect-error
        const org = TestStubs.Organization();
        const wrapper = createWrapper({
            alerts: { user: { me: { email: 'always', slack: 'always' } } },
        }, [], 
        // @ts-expect-error
        [TestStubs.OrganizationIntegrations()]);
        const alert = wrapper.find('StyledAlert');
        expect(alert).toHaveLength(2);
        const organizationSlugs = alert.at(0).find('li');
        expect(organizationSlugs).toHaveLength(1);
        expect(organizationSlugs.at(0).text()).toEqual(org.slug);
    });
    it('should not render warning modal when identity is linked', function () {
        // @ts-expect-error
        const org = TestStubs.Organization();
        const wrapper = createWrapper({
            alerts: { user: { me: { email: 'always', slack: 'always' } } },
        }, 
        // @ts-expect-error
        [TestStubs.UserIdentity()], 
        // @ts-expect-error
        [TestStubs.OrganizationIntegrations(org.id)]);
        const alert = wrapper.find('StyledAlert');
        expect(alert).toHaveLength(1);
    });
});
//# sourceMappingURL=notificationSettingsByType.spec.jsx.map