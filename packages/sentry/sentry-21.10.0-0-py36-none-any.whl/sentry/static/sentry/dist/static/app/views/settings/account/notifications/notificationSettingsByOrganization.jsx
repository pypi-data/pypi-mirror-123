Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = (0, tslib_1.__importDefault)(require("react"));
const locale_1 = require("app/locale");
const withOrganizations_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganizations"));
const utils_1 = require("app/views/settings/account/notifications/utils");
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const jsonForm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/jsonForm"));
class NotificationSettingsByOrganization extends react_1.default.Component {
    render() {
        const { notificationType, notificationSettings, onChange, organizations } = this.props;
        return (<form_1.default saveOnBlur apiMethod="PUT" apiEndpoint="/users/me/notification-settings/" initialData={(0, utils_1.getParentData)(notificationType, notificationSettings, organizations)}>
        <jsonForm_1.default title={(0, locale_1.t)('Organizations')} fields={organizations.map(organization => (0, utils_1.getParentField)(notificationType, notificationSettings, organization, onChange))}/>
      </form_1.default>);
    }
}
exports.default = (0, withOrganizations_1.default)(NotificationSettingsByOrganization);
//# sourceMappingURL=notificationSettingsByOrganization.jsx.map