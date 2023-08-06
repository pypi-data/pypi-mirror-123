Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_document_title_1 = (0, tslib_1.__importDefault)(require("react-document-title"));
const react_router_1 = require("react-router");
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const panels_1 = require("app/components/panels");
const constants_1 = require("app/constants");
const locale_1 = require("app/locale");
const apiForm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/apiForm"));
const multipleCheckbox_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/multipleCheckbox"));
const formField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/formField"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const textBlock_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/text/textBlock"));
const SORTED_DEFAULT_API_ACCESS_SCOPES = constants_1.DEFAULT_API_ACCESS_SCOPES.sort();
const API_CHOICES = constants_1.API_ACCESS_SCOPES.map(s => [s, s]);
const API_INDEX_ROUTE = '/settings/account/api/auth-tokens/';
class ApiNewToken extends react_1.Component {
    constructor() {
        super(...arguments);
        this.onCancel = () => {
            react_router_1.browserHistory.push(API_INDEX_ROUTE);
        };
        this.onSubmitSuccess = () => {
            react_router_1.browserHistory.push(API_INDEX_ROUTE);
        };
    }
    render() {
        return (<react_document_title_1.default title="Create API Token - Sentry">
        <div>
          <settingsPageHeader_1.default title={(0, locale_1.t)('Create New Token')}/>
          <textBlock_1.default>
            {(0, locale_1.t)("Authentication tokens allow you to perform actions against the Sentry API on behalf of your account. They're the easiest way to get started using the API.")}
          </textBlock_1.default>
          <textBlock_1.default>
            {(0, locale_1.tct)('For more information on how to use the web API, see our [link:documentation].', {
                link: <externalLink_1.default href="https://docs.sentry.io/api/"/>,
            })}
          </textBlock_1.default>
          <panels_1.Panel>
            <panels_1.PanelHeader>{(0, locale_1.t)('Create New Token')}</panels_1.PanelHeader>
            <apiForm_1.default apiMethod="POST" apiEndpoint="/api-tokens/" initialData={{ scopes: SORTED_DEFAULT_API_ACCESS_SCOPES }} onSubmitSuccess={this.onSubmitSuccess} onCancel={this.onCancel} footerStyle={{
                marginTop: 0,
                paddingRight: 20,
            }} submitLabel={(0, locale_1.t)('Create Token')}>
              <panels_1.PanelBody>
                <formField_1.default name="scopes" label={(0, locale_1.t)('Scopes')} inline={false} required>
                  {({ value, onChange }) => (<multipleCheckbox_1.default onChange={onChange} value={value} choices={API_CHOICES}/>)}
                </formField_1.default>
              </panels_1.PanelBody>
            </apiForm_1.default>
          </panels_1.Panel>
        </div>
      </react_document_title_1.default>);
    }
}
exports.default = ApiNewToken;
//# sourceMappingURL=apiNewToken.jsx.map