Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const indicator_1 = require("app/actionCreators/indicator");
const projectActions_1 = (0, tslib_1.__importDefault)(require("app/actions/projectActions"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const sentryDocumentTitle_1 = (0, tslib_1.__importDefault)(require("app/components/sentryDocumentTitle"));
const projectSecurityAndPrivacyGroups_1 = (0, tslib_1.__importDefault)(require("app/data/forms/projectSecurityAndPrivacyGroups"));
const locale_1 = require("app/locale");
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const jsonForm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/jsonForm"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const dataScrubbing_1 = (0, tslib_1.__importDefault)(require("../components/dataScrubbing"));
class ProjectSecurityAndPrivacy extends react_1.Component {
    constructor() {
        super(...arguments);
        this.handleUpdateProject = (data) => {
            // This will update our project global state
            projectActions_1.default.updateSuccess(data);
        };
    }
    render() {
        const { organization, project } = this.props;
        const initialData = project;
        const projectSlug = project.slug;
        const endpoint = `/projects/${organization.slug}/${projectSlug}/`;
        const access = new Set(organization.access);
        const features = new Set(organization.features);
        const relayPiiConfig = project.relayPiiConfig;
        const apiMethod = 'PUT';
        const title = (0, locale_1.t)('Security & Privacy');
        return (<react_1.Fragment>
        <sentryDocumentTitle_1.default title={title} projectSlug={projectSlug}/>
        <settingsPageHeader_1.default title={title}/>
        <form_1.default saveOnBlur allowUndo initialData={initialData} apiMethod={apiMethod} apiEndpoint={endpoint} onSubmitSuccess={this.handleUpdateProject} onSubmitError={() => (0, indicator_1.addErrorMessage)('Unable to save change')}>
          <jsonForm_1.default additionalFieldProps={{ organization }} features={features} disabled={!access.has('project:write')} forms={projectSecurityAndPrivacyGroups_1.default}/>
        </form_1.default>
        <dataScrubbing_1.default additionalContext={<span>
              {(0, locale_1.tct)('These rules can be configured at the organization level in [linkToOrganizationSecurityAndPrivacy].', {
                    linkToOrganizationSecurityAndPrivacy: (<link_1.default to={`/settings/${organization.slug}/security-and-privacy/`}>
                      {title}
                    </link_1.default>),
                })}
            </span>} endpoint={endpoint} relayPiiConfig={relayPiiConfig} disabled={!access.has('project:write')} organization={organization} projectId={project.id} onSubmitSuccess={this.handleUpdateProject}/>
      </react_1.Fragment>);
    }
}
exports.default = ProjectSecurityAndPrivacy;
//# sourceMappingURL=index.jsx.map