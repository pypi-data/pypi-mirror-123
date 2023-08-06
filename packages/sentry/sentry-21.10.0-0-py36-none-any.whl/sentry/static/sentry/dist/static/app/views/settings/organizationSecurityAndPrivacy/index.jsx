Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const indicator_1 = require("app/actionCreators/indicator");
const organizations_1 = require("app/actionCreators/organizations");
const sentryDocumentTitle_1 = (0, tslib_1.__importDefault)(require("app/components/sentryDocumentTitle"));
const organizationSecurityAndPrivacyGroups_1 = (0, tslib_1.__importDefault)(require("app/data/forms/organizationSecurityAndPrivacyGroups"));
const locale_1 = require("app/locale");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const jsonForm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/jsonForm"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const dataScrubbing_1 = (0, tslib_1.__importDefault)(require("../components/dataScrubbing"));
class OrganizationSecurityAndPrivacyContent extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.handleUpdateOrganization = (data) => {
            // This will update OrganizationStore (as well as OrganizationsStore
            // which is slightly incorrect because it has summaries vs a detailed org)
            (0, organizations_1.updateOrganization)(data);
        };
    }
    getEndpoints() {
        const { orgId } = this.props.params;
        return [['authProvider', `/organizations/${orgId}/auth-provider/`]];
    }
    renderBody() {
        const { organization } = this.props;
        const { orgId } = this.props.params;
        const initialData = organization;
        const endpoint = `/organizations/${orgId}/`;
        const access = new Set(organization.access);
        const features = new Set(organization.features);
        const relayPiiConfig = organization.relayPiiConfig;
        const { authProvider } = this.state;
        const title = (0, locale_1.t)('Security & Privacy');
        return (<react_1.Fragment>
        <sentryDocumentTitle_1.default title={title} orgSlug={organization.slug}/>
        <settingsPageHeader_1.default title={title}/>
        <form_1.default data-test-id="organization-settings-security-and-privacy" apiMethod="PUT" apiEndpoint={endpoint} initialData={initialData} additionalFieldProps={{ hasSsoEnabled: !!authProvider }} onSubmitSuccess={this.handleUpdateOrganization} onSubmitError={() => (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to save change'))} saveOnBlur allowUndo>
          <jsonForm_1.default features={features} forms={organizationSecurityAndPrivacyGroups_1.default} disabled={!access.has('org:write')}/>
        </form_1.default>
        <dataScrubbing_1.default additionalContext={(0, locale_1.t)('These rules can be configured for each project.')} endpoint={endpoint} relayPiiConfig={relayPiiConfig} disabled={!access.has('org:write')} organization={organization} onSubmitSuccess={this.handleUpdateOrganization}/>
      </react_1.Fragment>);
    }
}
exports.default = (0, withOrganization_1.default)(OrganizationSecurityAndPrivacyContent);
//# sourceMappingURL=index.jsx.map