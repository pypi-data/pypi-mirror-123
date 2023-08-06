Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const indicator_1 = require("app/actionCreators/indicator");
const access_1 = (0, tslib_1.__importDefault)(require("app/components/acl/access"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const dateTime_1 = (0, tslib_1.__importDefault)(require("app/components/dateTime"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const panels_1 = require("app/components/panels");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const booleanField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/booleanField"));
const field_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field"));
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const selectField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/selectField"));
const textCopyInput_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/textCopyInput"));
const textField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/textField"));
const keyRateLimitsForm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/project/projectKeys/details/keyRateLimitsForm"));
const projectKeyCredentials_1 = (0, tslib_1.__importDefault)(require("app/views/settings/project/projectKeys/projectKeyCredentials"));
class KeySettings extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            loading: false,
            error: false,
        };
        this.handleRemove = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            if (this.state.loading) {
                return;
            }
            (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Revoking key\u2026'));
            const { api, onRemove, params } = this.props;
            const { keyId, orgId, projectId } = params;
            try {
                yield api.requestPromise(`/projects/${orgId}/${projectId}/keys/${keyId}/`, {
                    method: 'DELETE',
                });
                onRemove();
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Revoked key'));
            }
            catch (_err) {
                this.setState({
                    error: true,
                    loading: false,
                });
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to revoke key'));
            }
        });
    }
    render() {
        const { keyId, orgId, projectId } = this.props.params;
        const { data } = this.props;
        const apiEndpoint = `/projects/${orgId}/${projectId}/keys/${keyId}/`;
        const loaderLink = (0, getDynamicText_1.default)({
            value: data.dsn.cdn,
            fixed: '__JS_SDK_LOADER_URL__',
        });
        return (<access_1.default access={['project:write']}>
        {({ hasAccess }) => (<react_1.Fragment>
            <form_1.default saveOnBlur allowUndo apiEndpoint={apiEndpoint} apiMethod="PUT" initialData={data}>
              <panels_1.Panel>
                <panels_1.PanelHeader>{(0, locale_1.t)('Details')}</panels_1.PanelHeader>

                <panels_1.PanelBody>
                  <textField_1.default name="name" label={(0, locale_1.t)('Name')} disabled={!hasAccess} required={false} maxLength={64}/>
                  <booleanField_1.default name="isActive" label={(0, locale_1.t)('Enabled')} required={false} disabled={!hasAccess} help="Accept events from this key? This may be used to temporarily suspend a key."/>
                  <field_1.default label={(0, locale_1.t)('Created')}>
                    <div className="controls">
                      <dateTime_1.default date={data.dateCreated}/>
                    </div>
                  </field_1.default>
                </panels_1.PanelBody>
              </panels_1.Panel>
            </form_1.default>

            <keyRateLimitsForm_1.default params={this.props.params} data={data} disabled={!hasAccess}/>

            <form_1.default saveOnBlur apiEndpoint={apiEndpoint} apiMethod="PUT" initialData={data}>
              <panels_1.Panel>
                <panels_1.PanelHeader>{(0, locale_1.t)('JavaScript Loader')}</panels_1.PanelHeader>
                <panels_1.PanelBody>
                  <field_1.default help={(0, locale_1.tct)('Copy this script into your website to setup your JavaScript SDK without any additional configuration. [link]', {
                    link: (<externalLink_1.default href="https://docs.sentry.io/platforms/javascript/install/lazy-load-sentry/">
                            What does the script provide?
                          </externalLink_1.default>),
                })} inline={false} flexibleControlStateSize>
                    <textCopyInput_1.default>
                      {`<script src='${loaderLink}' crossorigin="anonymous"></script>`}
                    </textCopyInput_1.default>
                  </field_1.default>
                  <selectField_1.default name="browserSdkVersion" choices={data.browserSdk ? data.browserSdk.choices : []} placeholder={(0, locale_1.t)('4.x')} allowClear={false} disabled={!hasAccess} help={(0, locale_1.t)('Select the version of the SDK that should be loaded. Note that it can take a few minutes until this change is live.')}/>
                </panels_1.PanelBody>
              </panels_1.Panel>
            </form_1.default>

            <panels_1.Panel>
              <panels_1.PanelHeader>{(0, locale_1.t)('Credentials')}</panels_1.PanelHeader>
              <panels_1.PanelBody>
                <panels_1.PanelAlert type="info" icon={<icons_1.IconFlag size="md"/>}>
                  {(0, locale_1.t)('Your credentials are coupled to a public and secret key. Different clients will require different credentials, so make sure you check the documentation before plugging things in.')}
                </panels_1.PanelAlert>

                <projectKeyCredentials_1.default projectId={`${data.projectId}`} data={data} showPublicKey showSecretKey showProjectId/>
              </panels_1.PanelBody>
            </panels_1.Panel>

            <access_1.default access={['project:admin']}>
              <panels_1.Panel>
                <panels_1.PanelHeader>{(0, locale_1.t)('Revoke Key')}</panels_1.PanelHeader>
                <panels_1.PanelBody>
                  <field_1.default label={(0, locale_1.t)('Revoke Key')} help={(0, locale_1.t)('Revoking this key will immediately remove and suspend the credentials. This action is irreversible.')}>
                    <div>
                      <confirm_1.default priority="danger" message={(0, locale_1.t)('Are you sure you want to revoke this key? This will immediately remove and suspend the credentials.')} onConfirm={this.handleRemove} confirmText={(0, locale_1.t)('Revoke Key')}>
                        <button_1.default priority="danger">{(0, locale_1.t)('Revoke Key')}</button_1.default>
                      </confirm_1.default>
                    </div>
                  </field_1.default>
                </panels_1.PanelBody>
              </panels_1.Panel>
            </access_1.default>
          </react_1.Fragment>)}
      </access_1.default>);
    }
}
exports.default = KeySettings;
//# sourceMappingURL=keySettings.jsx.map