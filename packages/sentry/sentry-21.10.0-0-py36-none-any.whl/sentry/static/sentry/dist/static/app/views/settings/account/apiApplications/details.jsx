Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const indicator_1 = require("app/actionCreators/indicator");
const panels_1 = require("app/components/panels");
const apiApplication_1 = (0, tslib_1.__importDefault)(require("app/data/forms/apiApplication"));
const locale_1 = require("app/locale");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const formField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/formField"));
const jsonForm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/jsonForm"));
const textCopyInput_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/textCopyInput"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
class ApiApplicationsDetails extends asyncView_1.default {
    getEndpoints() {
        return [['app', `/api-applications/${this.props.params.appId}/`]];
    }
    getTitle() {
        return (0, locale_1.t)('Application Details');
    }
    renderBody() {
        const urlPrefix = configStore_1.default.get('urlPrefix');
        return (<div>
        <settingsPageHeader_1.default title={this.getTitle()}/>

        <form_1.default apiMethod="PUT" apiEndpoint={`/api-applications/${this.props.params.appId}/`} saveOnBlur allowUndo initialData={this.state.app} onSubmitError={() => (0, indicator_1.addErrorMessage)('Unable to save change')}>
          <jsonForm_1.default forms={apiApplication_1.default}/>

          <panels_1.Panel>
            <panels_1.PanelHeader>{(0, locale_1.t)('Credentials')}</panels_1.PanelHeader>

            <panels_1.PanelBody>
              <formField_1.default name="clientID" label="Client ID">
                {({ value }) => (<div>
                    <textCopyInput_1.default>
                      {(0, getDynamicText_1.default)({ value, fixed: 'CI_CLIENT_ID' })}
                    </textCopyInput_1.default>
                  </div>)}
              </formField_1.default>

              <formField_1.default name="clientSecret" label="Client Secret" help={(0, locale_1.t)(`Your secret is only available briefly after application creation. Make
                  sure to save this value!`)}>
                {({ value }) => value ? (<textCopyInput_1.default>
                      {(0, getDynamicText_1.default)({ value, fixed: 'CI_CLIENT_SECRET' })}
                    </textCopyInput_1.default>) : (<em>hidden</em>)}
              </formField_1.default>

              <formField_1.default name="" label="Authorization URL">
                {() => <textCopyInput_1.default>{`${urlPrefix}/oauth/authorize/`}</textCopyInput_1.default>}
              </formField_1.default>

              <formField_1.default name="" label="Token URL">
                {() => <textCopyInput_1.default>{`${urlPrefix}/oauth/token/`}</textCopyInput_1.default>}
              </formField_1.default>
            </panels_1.PanelBody>
          </panels_1.Panel>
        </form_1.default>
      </div>);
    }
}
exports.default = ApiApplicationsDetails;
//# sourceMappingURL=details.jsx.map