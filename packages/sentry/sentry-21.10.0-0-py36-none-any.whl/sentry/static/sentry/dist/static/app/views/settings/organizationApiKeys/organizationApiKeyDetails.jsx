Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_router_1 = require("react-router");
const indicator_1 = require("app/actionCreators/indicator");
const panels_1 = require("app/components/panels");
const constants_1 = require("app/constants");
const locale_1 = require("app/locale");
const recreateRoute_1 = (0, tslib_1.__importDefault)(require("app/utils/recreateRoute"));
const routeTitle_1 = (0, tslib_1.__importDefault)(require("app/utils/routeTitle"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const apiForm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/apiForm"));
const multipleCheckbox_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/multipleCheckbox"));
const formField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/formField"));
const textareaField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/textareaField"));
const textField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/textField"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const API_CHOICES = constants_1.API_ACCESS_SCOPES.map(s => [s, s]);
class OrganizationApiKeyDetails extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.handleSubmitSuccess = () => {
            (0, indicator_1.addSuccessMessage)('Saved changes');
            // Go back to API list
            react_router_1.browserHistory.push((0, recreateRoute_1.default)('', {
                stepBack: -1,
                routes: this.props.routes,
                params: this.props.params,
            }));
        };
        this.handleSubmitError = () => {
            (0, indicator_1.addErrorMessage)('Unable to save changes. Please try again.');
        };
    }
    getEndpoints() {
        return [
            [
                'apiKey',
                `/organizations/${this.props.params.orgId}/api-keys/${this.props.params.apiKey}/`,
            ],
        ];
    }
    getTitle() {
        return (0, routeTitle_1.default)((0, locale_1.t)('Edit API Key'), this.props.organization.slug, false);
    }
    renderBody() {
        return (<div>
        <settingsPageHeader_1.default title={(0, locale_1.t)('Edit API Key')}/>

        <panels_1.Panel>
          <panels_1.PanelHeader>{(0, locale_1.t)('API Key')}</panels_1.PanelHeader>
          <apiForm_1.default apiMethod="PUT" apiEndpoint={`/organizations/${this.props.params.orgId}/api-keys/${this.props.params.apiKey}/`} initialData={this.state.apiKey} onSubmitSuccess={this.handleSubmitSuccess} onSubmitError={this.handleSubmitError} onCancel={() => react_router_1.browserHistory.push((0, recreateRoute_1.default)('', {
                stepBack: -1,
                routes: this.props.routes,
                params: this.props.params,
            }))}>
            <panels_1.PanelBody>
              <textField_1.default label={(0, locale_1.t)('Label')} name="label"/>
              <textField_1.default label={(0, locale_1.t)('API Key')} name="key" disabled/>

              <formField_1.default name="scope_list" label={(0, locale_1.t)('Scopes')} inline={false} required>
                {({ value, onChange }) => (<multipleCheckbox_1.default value={value} onChange={onChange} choices={API_CHOICES}/>)}
              </formField_1.default>

              <textareaField_1.default label={(0, locale_1.t)('Allowed Domains')} name="allowed_origins" placeholder="e.g. example.com or https://example.com" help="Separate multiple entries with a newline"/>
            </panels_1.PanelBody>
          </apiForm_1.default>
        </panels_1.Panel>
      </div>);
    }
}
exports.default = (0, withOrganization_1.default)(OrganizationApiKeyDetails);
//# sourceMappingURL=organizationApiKeyDetails.jsx.map