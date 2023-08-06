Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const narrowLayout_1 = (0, tslib_1.__importDefault)(require("app/components/narrowLayout"));
const locale_1 = require("app/locale");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const forms_1 = require("app/views/settings/components/forms");
class OrganizationCreate extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.onSubmitSuccess = data => {
            // redirect to project creation *(BYPASS REACT ROUTER AND FORCE PAGE REFRESH TO GRAB CSRF TOKEN)*
            // browserHistory.pushState(null, `/organizations/${data.slug}/projects/new/`);
            window.location.href = `/organizations/${data.slug}/projects/new/`;
        };
    }
    getEndpoints() {
        return [];
    }
    getTitle() {
        return (0, locale_1.t)('Create Organization');
    }
    renderBody() {
        const termsUrl = configStore_1.default.get('termsUrl');
        const privacyUrl = configStore_1.default.get('privacyUrl');
        return (<narrowLayout_1.default showLogout>
        <h3>{(0, locale_1.t)('Create a New Organization')}</h3>

        <p>
          {(0, locale_1.t)("Organizations represent the top level in your hierarchy. You'll be able to bundle a collection of teams within an organization as well as give organization-wide permissions to users.")}
        </p>

        <forms_1.ApiForm initialData={{ defaultTeam: true }} submitLabel={(0, locale_1.t)('Create Organization')} apiEndpoint="/organizations/" apiMethod="POST" onSubmitSuccess={this.onSubmitSuccess} requireChanges>
          <forms_1.TextField id="organization-name" name="name" label={(0, locale_1.t)('Organization Name')} placeholder={(0, locale_1.t)('e.g. My Company')} inline={false} flexibleControlStateSize stacked required/>

          {termsUrl && privacyUrl && (<forms_1.CheckboxField id="agreeTerms" name="agreeTerms" label={(0, locale_1.tct)('I agree to the [termsLink:Terms of Service] and the [privacyLink:Privacy Policy]', {
                    termsLink: <a href={termsUrl}/>,
                    privacyLink: <a href={privacyUrl}/>,
                })} inline={false} stacked required/>)}
        </forms_1.ApiForm>
      </narrowLayout_1.default>);
    }
}
exports.default = OrganizationCreate;
//# sourceMappingURL=organizationCreate.jsx.map