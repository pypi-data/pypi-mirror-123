Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = (0, tslib_1.__importDefault)(require("react"));
const alertLink_1 = (0, tslib_1.__importDefault)(require("app/components/alertLink"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const constants_1 = require("app/views/settings/account/notifications/constants");
const feedbackAlert_1 = (0, tslib_1.__importDefault)(require("app/views/settings/account/notifications/feedbackAlert"));
const fields2_1 = require("app/views/settings/account/notifications/fields2");
const utils_1 = require("app/views/settings/account/notifications/utils");
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const jsonForm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/jsonForm"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const textBlock_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/text/textBlock"));
class NotificationSettings extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.getStateToPutForDefault = (changedData, notificationType) => {
            /**
             * Update the current providers' parent-independent notification settings
             * with the new value. If the new value is "never", then also update all
             * parent-specific notification settings to "default". If the previous value
             * was "never", then assume providerList should be "email" only.
             */
            const { notificationSettings } = this.state;
            const updatedNotificationSettings = (0, utils_1.getStateToPutForDefault)(notificationType, notificationSettings, changedData, (0, utils_1.getParentIds)(notificationType, notificationSettings));
            this.setState({
                notificationSettings: (0, utils_1.mergeNotificationSettings)(notificationSettings, updatedNotificationSettings),
            });
            return updatedNotificationSettings;
        };
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { notificationSettings: {}, legacyData: {} });
    }
    getEndpoints() {
        return [
            ['notificationSettings', `/users/me/notification-settings/`],
            ['legacyData', '/users/me/notifications/'],
        ];
    }
    getInitialData() {
        const { notificationSettings } = this.state;
        return Object.fromEntries(constants_1.NOTIFICATION_SETTINGS_TYPES.map(notificationType => [
            notificationType,
            (0, utils_1.decideDefault)(notificationType, notificationSettings),
        ]));
    }
    getFields() {
        const { notificationSettings } = this.state;
        const fields = [];
        for (const notificationType of constants_1.NOTIFICATION_SETTINGS_TYPES) {
            const field = Object.assign({}, fields2_1.NOTIFICATION_SETTING_FIELDS[notificationType], {
                getData: data => this.getStateToPutForDefault(data, notificationType),
                help: (<react_1.default.Fragment>
            <p>
              {fields2_1.NOTIFICATION_SETTING_FIELDS[notificationType].help}
              &nbsp;
              <link_1.default data-test-id="fine-tuning" to={`/settings/account/notifications/${notificationType}`}>
                Fine tune
              </link_1.default>
            </p>
          </react_1.default.Fragment>),
            });
            if ((0, utils_1.isSufficientlyComplex)(notificationType, notificationSettings) &&
                typeof field !== 'function') {
                field.confirm = { never: constants_1.CONFIRMATION_MESSAGE };
            }
            fields.push(field);
        }
        return fields;
    }
    renderBody() {
        const { legacyData } = this.state;
        return (<react_1.default.Fragment>
        <settingsPageHeader_1.default title="Notifications"/>
        <textBlock_1.default>Personal notifications sent via email or an integration.</textBlock_1.default>
        <feedbackAlert_1.default />
        <form_1.default saveOnBlur apiMethod="PUT" apiEndpoint="/users/me/notification-settings/" initialData={this.getInitialData()}>
          <jsonForm_1.default title={(0, locale_1.t)('Notifications')} fields={this.getFields()}/>
        </form_1.default>
        <form_1.default initialData={legacyData} saveOnBlur apiMethod="PUT" apiEndpoint="/users/me/notifications/">
          <jsonForm_1.default title={(0, locale_1.t)('My Activity')} fields={constants_1.SELF_NOTIFICATION_SETTINGS_TYPES.map(type => fields2_1.NOTIFICATION_SETTING_FIELDS[type])}/>
        </form_1.default>
        <alertLink_1.default to="/settings/account/emails" icon={<icons_1.IconMail />}>
          {(0, locale_1.t)('Looking to add or remove an email address? Use the emails panel.')}
        </alertLink_1.default>
      </react_1.default.Fragment>);
    }
}
exports.default = NotificationSettings;
//# sourceMappingURL=notificationSettings.jsx.map