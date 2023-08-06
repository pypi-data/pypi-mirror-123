Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = (0, tslib_1.__importDefault)(require("react"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const locale_1 = require("app/locale");
const withOrganizations_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganizations"));
const constants_1 = require("app/views/settings/account/notifications/constants");
const feedbackAlert_1 = (0, tslib_1.__importDefault)(require("app/views/settings/account/notifications/feedbackAlert"));
const fields_1 = require("app/views/settings/account/notifications/fields");
const fields2_1 = require("app/views/settings/account/notifications/fields2");
const notificationSettingsByOrganization_1 = (0, tslib_1.__importDefault)(require("app/views/settings/account/notifications/notificationSettingsByOrganization"));
const notificationSettingsByProjects_1 = (0, tslib_1.__importDefault)(require("app/views/settings/account/notifications/notificationSettingsByProjects"));
const unlinkedAlert_1 = (0, tslib_1.__importDefault)(require("app/views/settings/account/notifications/unlinkedAlert"));
const utils_1 = require("app/views/settings/account/notifications/utils");
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const jsonForm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/jsonForm"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const textBlock_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/text/textBlock"));
class NotificationSettingsByType extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        /* Methods responsible for updating state and hitting the API. */
        this.getStateToPutForProvider = (changedData) => {
            const { notificationType } = this.props;
            const { notificationSettings } = this.state;
            const updatedNotificationSettings = (0, utils_1.getStateToPutForProvider)(notificationType, notificationSettings, changedData);
            this.setState({
                notificationSettings: (0, utils_1.mergeNotificationSettings)(notificationSettings, updatedNotificationSettings),
            });
            return updatedNotificationSettings;
        };
        this.getStateToPutForDefault = (changedData) => {
            const { notificationType } = this.props;
            const { notificationSettings } = this.state;
            const updatedNotificationSettings = (0, utils_1.getStateToPutForDefault)(notificationType, notificationSettings, changedData, (0, utils_1.getParentIds)(notificationType, notificationSettings));
            this.setState({
                notificationSettings: (0, utils_1.mergeNotificationSettings)(notificationSettings, updatedNotificationSettings),
            });
            return updatedNotificationSettings;
        };
        this.getStateToPutForParent = (changedData, parentId) => {
            const { notificationType } = this.props;
            const { notificationSettings } = this.state;
            const updatedNotificationSettings = (0, utils_1.getStateToPutForParent)(notificationType, notificationSettings, changedData, parentId);
            this.setState({
                notificationSettings: (0, utils_1.mergeNotificationSettings)(notificationSettings, updatedNotificationSettings),
            });
            return updatedNotificationSettings;
        };
        this.getUnlinkedOrgs = () => {
            const { organizations } = this.props;
            const { identities, organizationIntegrations } = this.state;
            const integrationExternalIDsByOrganizationID = Object.fromEntries(organizationIntegrations.map(organizationIntegration => [
                organizationIntegration.organizationId,
                organizationIntegration.externalId,
            ]));
            const identitiesByExternalId = Object.fromEntries(identities.map(identity => { var _a; return [(_a = identity === null || identity === void 0 ? void 0 : identity.identityProvider) === null || _a === void 0 ? void 0 : _a.externalId, identity]; }));
            return organizations.filter(organization => {
                const externalID = integrationExternalIDsByOrganizationID[organization.id];
                const identity = identitiesByExternalId[externalID];
                return identity === undefined || identity === null;
            });
        };
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { notificationSettings: {}, identities: [], organizationIntegrations: [] });
    }
    getEndpoints() {
        const { notificationType } = this.props;
        return [
            [
                'notificationSettings',
                `/users/me/notification-settings/`,
                { query: { type: notificationType } },
            ],
            ['identities', `/users/me/identities/`, { query: { provider: 'slack' } }],
            [
                'organizationIntegrations',
                `/users/me/organization-integrations/`,
                { query: { provider: 'slack' } },
            ],
        ];
    }
    /* Methods responsible for rendering the page. */
    getInitialData() {
        const { notificationType } = this.props;
        const { notificationSettings } = this.state;
        const initialData = {
            [notificationType]: (0, utils_1.getCurrentDefault)(notificationType, notificationSettings),
        };
        if (!(0, utils_1.isEverythingDisabled)(notificationType, notificationSettings)) {
            initialData.provider = (0, utils_1.providerListToString)((0, utils_1.getCurrentProviders)(notificationType, notificationSettings));
        }
        return initialData;
    }
    getFields() {
        const { notificationType } = this.props;
        const { notificationSettings } = this.state;
        const defaultField = Object.assign({}, fields2_1.NOTIFICATION_SETTING_FIELDS[notificationType], {
            help: (0, locale_1.t)('This is the default for all projects.'),
            getData: data => this.getStateToPutForDefault(data),
        });
        if ((0, utils_1.isSufficientlyComplex)(notificationType, notificationSettings)) {
            defaultField.confirm = { never: constants_1.CONFIRMATION_MESSAGE };
        }
        const fields = [defaultField];
        if (!(0, utils_1.isEverythingDisabled)(notificationType, notificationSettings)) {
            fields.push(Object.assign({
                help: (0, locale_1.t)('Where personal notifications will be sent.'),
                getData: data => this.getStateToPutForProvider(data),
            }, fields2_1.NOTIFICATION_SETTING_FIELDS.provider));
        }
        return fields;
    }
    renderBody() {
        const { notificationType } = this.props;
        const { notificationSettings } = this.state;
        const hasSlack = (0, utils_1.getCurrentProviders)(notificationType, notificationSettings).includes('slack');
        const unlinkedOrgs = this.getUnlinkedOrgs();
        const { title, description } = fields_1.ACCOUNT_NOTIFICATION_FIELDS[notificationType];
        return (<react_1.default.Fragment>
        <settingsPageHeader_1.default title={title}/>
        {description && <textBlock_1.default>{description}</textBlock_1.default>}
        {hasSlack && unlinkedOrgs.length > 0 && (<unlinkedAlert_1.default organizations={unlinkedOrgs}/>)}
        <feedbackAlert_1.default />
        <form_1.default saveOnBlur apiMethod="PUT" apiEndpoint="/users/me/notification-settings/" initialData={this.getInitialData()}>
          <jsonForm_1.default title={(0, utils_1.isGroupedByProject)(notificationType)
                ? (0, locale_1.t)('All Projects')
                : (0, locale_1.t)('All Organizations')} fields={this.getFields()}/>
        </form_1.default>
        {!(0, utils_1.isEverythingDisabled)(notificationType, notificationSettings) &&
                ((0, utils_1.isGroupedByProject)(notificationType) ? (<notificationSettingsByProjects_1.default notificationType={notificationType} notificationSettings={notificationSettings} onChange={this.getStateToPutForParent}/>) : (<notificationSettingsByOrganization_1.default notificationType={notificationType} notificationSettings={notificationSettings} onChange={this.getStateToPutForParent}/>))}
      </react_1.default.Fragment>);
    }
}
exports.default = (0, withOrganizations_1.default)(NotificationSettingsByType);
//# sourceMappingURL=notificationSettingsByType.jsx.map