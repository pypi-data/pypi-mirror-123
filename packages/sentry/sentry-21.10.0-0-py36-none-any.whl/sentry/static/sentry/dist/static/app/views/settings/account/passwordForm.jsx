Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const panels_1 = require("app/components/panels");
const accountPassword_1 = (0, tslib_1.__importDefault)(require("app/data/forms/accountPassword"));
const locale_1 = require("app/locale");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const jsonForm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/jsonForm"));
function PasswordForm() {
    function handleSubmitSuccess(_change, model) {
        // Reset form on success
        model.resetForm();
        (0, indicator_1.addSuccessMessage)('Password has been changed');
    }
    function handleSubmitError() {
        (0, indicator_1.addErrorMessage)('Error changing password');
    }
    const user = configStore_1.default.get('user');
    return (<form_1.default apiMethod="PUT" apiEndpoint="/users/me/password/" initialData={{}} onSubmitSuccess={handleSubmitSuccess} onSubmitError={handleSubmitError} hideFooter>
      <jsonForm_1.default forms={accountPassword_1.default} additionalFieldProps={{ user }} renderFooter={() => (<Actions>
            <button_1.default type="submit" priority="primary">
              {(0, locale_1.t)('Change password')}
            </button_1.default>
          </Actions>)} renderHeader={() => (<panels_1.PanelAlert type="info">
            {(0, locale_1.t)('Changing your password will invalidate all logged in sessions.')}
          </panels_1.PanelAlert>)}/>
    </form_1.default>);
}
const Actions = (0, styled_1.default)(panels_1.PanelItem) `
  justify-content: flex-end;
`;
exports.default = PasswordForm;
//# sourceMappingURL=passwordForm.jsx.map