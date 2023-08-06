Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const locale_1 = require("app/locale");
const integrationUtil_1 = require("app/utils/integrationUtil");
const forms_1 = require("app/views/settings/components/forms");
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
class RepositoryProjectPathConfigForm extends react_1.Component {
    get initialData() {
        const { existingConfig, integration } = this.props;
        return Object.assign({ defaultBranch: 'master', stackRoot: '', sourceRoot: '', repositoryId: existingConfig === null || existingConfig === void 0 ? void 0 : existingConfig.repoId, integrationId: integration.id }, (0, pick_1.default)(existingConfig, ['projectId', 'defaultBranch', 'stackRoot', 'sourceRoot']));
    }
    get formFields() {
        const { projects, repos } = this.props;
        const repoChoices = repos.map(({ name, id }) => ({ value: id, label: name }));
        return [
            {
                name: 'projectId',
                type: 'sentry_project_selector',
                required: true,
                label: (0, locale_1.t)('Project'),
                projects,
            },
            {
                name: 'repositoryId',
                type: 'select',
                required: true,
                label: (0, locale_1.t)('Repo'),
                placeholder: (0, locale_1.t)('Choose repo'),
                options: repoChoices,
            },
            {
                name: 'defaultBranch',
                type: 'string',
                required: true,
                label: (0, locale_1.t)('Branch'),
                placeholder: (0, locale_1.t)('Type your branch'),
                showHelpInTooltip: true,
                help: (0, locale_1.t)('If an event does not have a release tied to a commit, we will use this branch when linking to your source code.'),
            },
            {
                name: 'stackRoot',
                type: 'string',
                required: false,
                label: (0, locale_1.t)('Stack Trace Root'),
                placeholder: (0, locale_1.t)('Type root path of your stack traces'),
                showHelpInTooltip: true,
                help: (0, locale_1.t)('Any stack trace starting with this path will be mapped with this rule. An empty string will match all paths.'),
            },
            {
                name: 'sourceRoot',
                type: 'string',
                required: false,
                label: (0, locale_1.t)('Source Code Root'),
                placeholder: (0, locale_1.t)('Type root path of your source code, e.g. `src/`.'),
                showHelpInTooltip: true,
                help: (0, locale_1.t)('When a rule matches, the stack trace root is replaced with this path to get the path in your repository. Leaving this empty means replacing the stack trace root with an empty string.'),
            },
        ];
    }
    handlePreSubmit() {
        (0, integrationUtil_1.trackIntegrationAnalytics)('integrations.stacktrace_submit_config', {
            setup_type: 'manual',
            view: 'integration_configuration_detail',
            provider: this.props.integration.provider.key,
            organization: this.props.organization,
        });
    }
    render() {
        const { organization, onSubmitSuccess, onCancel, existingConfig } = this.props;
        // endpoint changes if we are making a new row or updating an existing one
        const baseEndpoint = `/organizations/${organization.slug}/code-mappings/`;
        const endpoint = existingConfig
            ? `${baseEndpoint}${existingConfig.id}/`
            : baseEndpoint;
        const apiMethod = existingConfig ? 'PUT' : 'POST';
        return (<form_1.default onSubmitSuccess={onSubmitSuccess} onPreSubmit={() => this.handlePreSubmit()} initialData={this.initialData} apiEndpoint={endpoint} apiMethod={apiMethod} onCancel={onCancel}>
        {this.formFields.map(field => (<forms_1.FieldFromConfig key={field.name} field={field} inline={false} stacked flexibleControlStateSize/>))}
      </form_1.default>);
    }
}
exports.default = RepositoryProjectPathConfigForm;
//# sourceMappingURL=repositoryProjectPathConfigForm.jsx.map