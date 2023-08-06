Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const indicator_1 = require("app/actionCreators/indicator");
const organizations_1 = require("app/actionCreators/organizations");
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const avatarChooser_1 = (0, tslib_1.__importDefault)(require("app/components/avatarChooser"));
const organizationGeneralSettings_1 = (0, tslib_1.__importDefault)(require("app/data/forms/organizationGeneralSettings"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const jsonForm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/jsonForm"));
class OrganizationSettingsForm extends asyncComponent_1.default {
    getEndpoints() {
        const { organization } = this.props;
        return [['authProvider', `/organizations/${organization.slug}/auth-provider/`]];
    }
    render() {
        const { initialData, organization, onSave, access } = this.props;
        const { authProvider } = this.state;
        const endpoint = `/organizations/${organization.slug}/`;
        const jsonFormSettings = {
            additionalFieldProps: { hasSsoEnabled: !!authProvider },
            features: new Set(organization.features),
            access,
            location: this.props.location,
            disabled: !access.has('org:write'),
        };
        return (<form_1.default data-test-id="organization-settings" apiMethod="PUT" apiEndpoint={endpoint} saveOnBlur allowUndo initialData={initialData} onSubmitSuccess={(_resp, model) => {
                // Special case for slug, need to forward to new slug
                if (typeof onSave === 'function') {
                    onSave(initialData, model.initialData);
                }
            }} onSubmitError={() => (0, indicator_1.addErrorMessage)('Unable to save change')}>
        <jsonForm_1.default {...jsonFormSettings} forms={organizationGeneralSettings_1.default}/>
        <avatarChooser_1.default type="organization" allowGravatar={false} endpoint={`${endpoint}avatar/`} model={initialData} onSave={organizations_1.updateOrganization} disabled={!access.has('org:write')}/>
      </form_1.default>);
    }
}
exports.default = (0, withOrganization_1.default)(OrganizationSettingsForm);
//# sourceMappingURL=organizationSettingsForm.jsx.map