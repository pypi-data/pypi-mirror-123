Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const indicator_1 = require("app/actionCreators/indicator");
const organizations_1 = require("app/actionCreators/organizations");
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const locale_1 = require("app/locale");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const jsonForm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/jsonForm"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const permissionAlert_1 = (0, tslib_1.__importDefault)(require("app/views/settings/organization/permissionAlert"));
const fields = [
    {
        title: (0, locale_1.t)('General'),
        fields: [
            {
                name: 'apdexThreshold',
                type: 'number',
                required: true,
                label: (0, locale_1.t)('Response Time Threshold (Apdex)'),
                help: (0, locale_1.tct)(`Set a response time threshold in milliseconds to help define what satisfactory
                and tolerable response times are. This value will be reflected in the
                calculation of your [link:Apdex], a standard measurement in performance.`, {
                    link: (<externalLink_1.default href="https://docs.sentry.io/performance-monitoring/performance/metrics/#apdex"/>),
                }),
            },
        ],
    },
];
class OrganizationPerformance extends react_1.Component {
    constructor() {
        super(...arguments);
        this.handleSuccess = (data) => {
            (0, organizations_1.updateOrganization)(data);
        };
    }
    render() {
        const { location, organization } = this.props;
        const features = new Set(organization.features);
        const access = new Set(organization.access);
        const endpoint = `/organizations/${organization.slug}/`;
        const jsonFormSettings = {
            location,
            features,
            access,
            disabled: !(access.has('org:write') && features.has('performance-view')),
        };
        return (<react_1.Fragment>
        <settingsPageHeader_1.default title="Performance"/>
        <permissionAlert_1.default />

        <form_1.default data-test-id="organization-performance-settings" apiMethod="PUT" apiEndpoint={endpoint} saveOnBlur allowUndo initialData={organization} onSubmitSuccess={this.handleSuccess} onSubmitError={() => (0, indicator_1.addErrorMessage)('Unable to save changes')}>
          <jsonForm_1.default {...jsonFormSettings} forms={fields}/>
        </form_1.default>
      </react_1.Fragment>);
    }
}
exports.default = (0, withOrganization_1.default)(OrganizationPerformance);
//# sourceMappingURL=index.jsx.map