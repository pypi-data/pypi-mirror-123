Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = (0, tslib_1.__importDefault)(require("react"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const forms_1 = require("app/views/settings/components/forms");
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const alert_1 = (0, tslib_1.__importDefault)(require("./alert"));
class RepositoryEditForm extends react_1.default.Component {
    get initialData() {
        const { repository } = this.props;
        return {
            name: repository.name,
            url: repository.url || '',
        };
    }
    get formFields() {
        const fields = [
            {
                name: 'name',
                type: 'string',
                required: true,
                label: (0, locale_1.t)('Name of your repository.'),
            },
            {
                name: 'url',
                type: 'string',
                required: false,
                label: (0, locale_1.t)('Full URL to your repository.'),
                placeholder: (0, locale_1.t)('https://github.com/my-org/my-repo/'),
            },
        ];
        return fields;
    }
    render() {
        const { onCancel, orgSlug, repository } = this.props;
        const endpoint = `/organizations/${orgSlug}/repos/${repository.id}/`;
        return (<form_1.default initialData={this.initialData} onSubmitSuccess={data => {
                this.props.onSubmitSuccess(data);
                this.props.closeModal();
            }} apiEndpoint={endpoint} apiMethod="PUT" onCancel={onCancel}>
        <alert_1.default type="warning" icon={<icons_1.IconWarning />}>
          {(0, locale_1.tct)('Changing the [name:repo name] may have consequences if it no longer matches the repo name used when [link:sending commits with releases].', {
                link: (<externalLink_1.default href="https://docs.sentry.io/product/cli/releases/#sentry-cli-commit-integration"/>),
                name: <strong>repo name</strong>,
            })}
        </alert_1.default>
        {this.formFields.map(field => (<forms_1.FieldFromConfig key={field.name} field={field} inline={false} stacked flexibleControlStateSize/>))}
      </form_1.default>);
    }
}
exports.default = RepositoryEditForm;
//# sourceMappingURL=repositoryEditForm.jsx.map