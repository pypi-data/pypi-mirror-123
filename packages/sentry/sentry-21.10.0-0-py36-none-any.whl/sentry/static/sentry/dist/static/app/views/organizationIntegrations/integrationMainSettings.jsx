Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = (0, tslib_1.__importDefault)(require("react"));
const indicator_1 = require("app/actionCreators/indicator");
const locale_1 = require("app/locale");
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const jsonForm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/jsonForm"));
class IntegrationMainSettings extends react_1.default.Component {
    constructor() {
        super(...arguments);
        this.state = {
            integration: this.props.integration,
        };
        this.handleSubmitSuccess = (data) => {
            (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Integration updated.'));
            this.props.onUpdate();
            this.setState({ integration: data });
        };
    }
    get initialData() {
        const { integration } = this.props;
        return {
            name: integration.name,
            domain: integration.domainName || '',
        };
    }
    get formFields() {
        const fields = [
            {
                name: 'name',
                type: 'string',
                required: false,
                label: (0, locale_1.t)('Integration Name'),
            },
            {
                name: 'domain',
                type: 'string',
                required: false,
                label: (0, locale_1.t)('Full URL'),
            },
        ];
        return fields;
    }
    render() {
        const { integration } = this.state;
        const { organization } = this.props;
        return (<form_1.default initialData={this.initialData} apiMethod="PUT" apiEndpoint={`/organizations/${organization.slug}/integrations/${integration.id}/`} onSubmitSuccess={this.handleSubmitSuccess} submitLabel={(0, locale_1.t)('Save Settings')}>
        <jsonForm_1.default fields={this.formFields}/>
      </form_1.default>);
    }
}
exports.default = IntegrationMainSettings;
//# sourceMappingURL=integrationMainSettings.jsx.map