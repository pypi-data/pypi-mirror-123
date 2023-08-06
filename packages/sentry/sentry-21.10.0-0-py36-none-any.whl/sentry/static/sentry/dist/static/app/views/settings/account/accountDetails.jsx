Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const account_1 = require("app/actionCreators/account");
const avatarChooser_1 = (0, tslib_1.__importDefault)(require("app/components/avatarChooser"));
const accountDetails_1 = (0, tslib_1.__importDefault)(require("app/data/forms/accountDetails"));
const accountPreferences_1 = (0, tslib_1.__importDefault)(require("app/data/forms/accountPreferences"));
const locale_1 = require("app/locale");
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const jsonForm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/jsonForm"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const ENDPOINT = '/users/me/';
class AccountDetails extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.handleSubmitSuccess = (user) => {
            // the updateUser method updates our Config Store
            // No components listen to the ConfigStore, they just access it directly
            (0, account_1.updateUser)(user);
            // We need to update the state, because AvatarChooser is using it,
            // otherwise it will flick
            this.setState({
                user,
            });
        };
    }
    getEndpoints() {
        // local state is NOT updated when the form saves
        return [['user', ENDPOINT]];
    }
    renderBody() {
        const user = this.state.user;
        const formCommonProps = {
            apiEndpoint: ENDPOINT,
            apiMethod: 'PUT',
            allowUndo: true,
            saveOnBlur: true,
            onSubmitSuccess: this.handleSubmitSuccess,
        };
        return (<div>
        <settingsPageHeader_1.default title={(0, locale_1.t)('Account Details')}/>
        <form_1.default initialData={user} {...formCommonProps}>
          <jsonForm_1.default forms={accountDetails_1.default} additionalFieldProps={{ user }}/>
        </form_1.default>
        <form_1.default initialData={user.options} {...formCommonProps}>
          <jsonForm_1.default forms={accountPreferences_1.default} additionalFieldProps={{ user }}/>
        </form_1.default>
        <avatarChooser_1.default endpoint="/users/me/avatar/" model={user} onSave={resp => {
                this.handleSubmitSuccess(resp);
            }} isUser/>
      </div>);
    }
}
exports.default = AccountDetails;
//# sourceMappingURL=accountDetails.jsx.map