Object.defineProperty(exports, "__esModule", { value: true });
exports.ProjectReleaseTracking = void 0;
const tslib_1 = require("tslib");
const indicator_1 = require("app/actionCreators/indicator");
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const autoSelectText_1 = (0, tslib_1.__importDefault)(require("app/components/autoSelectText"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const panels_1 = require("app/components/panels");
const pluginList_1 = (0, tslib_1.__importDefault)(require("app/components/pluginList"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const routeTitle_1 = (0, tslib_1.__importDefault)(require("app/utils/routeTitle"));
const withPlugins_1 = (0, tslib_1.__importDefault)(require("app/utils/withPlugins"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const field_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field"));
const textCopyInput_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/textCopyInput"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const TOKEN_PLACEHOLDER = 'YOUR_TOKEN';
const WEBHOOK_PLACEHOLDER = 'YOUR_WEBHOOK_URL';
const placeholderData = {
    token: TOKEN_PLACEHOLDER,
    webhookUrl: WEBHOOK_PLACEHOLDER,
};
class ProjectReleaseTracking extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.handleRegenerateToken = () => {
            const { orgId, projectId } = this.props.params;
            this.api.request(`/projects/${orgId}/${projectId}/releases/token/`, {
                method: 'POST',
                data: { project: projectId },
                success: data => {
                    this.setState({
                        data: {
                            token: data.token,
                            webhookUrl: data.webhookUrl,
                        },
                    });
                    (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Your deploy token has been regenerated. You will need to update any existing deploy hooks.'));
                },
                error: () => {
                    (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to regenerate deploy token, please try again'));
                },
            });
        };
    }
    getTitle() {
        const { projectId } = this.props.params;
        return (0, routeTitle_1.default)((0, locale_1.t)('Releases'), projectId, false);
    }
    getEndpoints() {
        const { orgId, projectId } = this.props.params;
        // Allow 403s
        return [
            [
                'data',
                `/projects/${orgId}/${projectId}/releases/token/`,
                {},
                { allowError: err => err && err.status === 403 },
            ],
        ];
    }
    getReleaseWebhookIntructions() {
        const { webhookUrl } = this.state.data || placeholderData;
        return ('curl ' +
            webhookUrl +
            ' \\' +
            '\n  ' +
            '-X POST \\' +
            '\n  ' +
            "-H 'Content-Type: application/json' \\" +
            '\n  ' +
            '-d \'{"version": "abcdefg"}\'');
    }
    renderBody() {
        const { organization, project, plugins } = this.props;
        const hasWrite = organization.access.includes('project:write');
        if (plugins.loading) {
            return <loadingIndicator_1.default />;
        }
        const pluginList = plugins.plugins.filter((p) => p.type === 'release-tracking' && p.hasConfiguration);
        let { token, webhookUrl } = this.state.data || placeholderData;
        token = (0, getDynamicText_1.default)({ value: token, fixed: '__TOKEN__' });
        webhookUrl = (0, getDynamicText_1.default)({ value: webhookUrl, fixed: '__WEBHOOK_URL__' });
        return (<div>
        <settingsPageHeader_1.default title={(0, locale_1.t)('Release Tracking')}/>
        {!hasWrite && (<alert_1.default icon={<icons_1.IconFlag size="md"/>} type="warning">
            {(0, locale_1.t)('You do not have sufficient permissions to access Release tokens, placeholders are displayed below.')}
          </alert_1.default>)}
        <p>
          {(0, locale_1.t)('Configure release tracking for this project to automatically record new releases of your application.')}
        </p>

        <panels_1.Panel>
          <panels_1.PanelHeader>{(0, locale_1.t)('Client Configuration')}</panels_1.PanelHeader>
          <panels_1.PanelBody withPadding>
            <p>
              {(0, locale_1.tct)('Start by binding the [release] attribute in your application, take a look at [link] to see how to configure this for the SDK you are using.', {
                link: (<externalLink_1.default href="https://docs.sentry.io/platform-redirect/?next=/configuration/releases/">
                      our docs
                    </externalLink_1.default>),
                release: <code>release</code>,
            })}
            </p>
            <p>
              {(0, locale_1.t)("This will annotate each event with the version of your application, as well as automatically create a release entity in the system the first time it's seen.")}
            </p>
            <p>
              {(0, locale_1.t)('In addition you may configure a release hook (or use our API) to push a release and include additional metadata with it.')}
            </p>
          </panels_1.PanelBody>
        </panels_1.Panel>

        <panels_1.Panel>
          <panels_1.PanelHeader>{(0, locale_1.t)('Deploy Token')}</panels_1.PanelHeader>
          <panels_1.PanelBody>
            <field_1.default label={(0, locale_1.t)('Token')} help={(0, locale_1.t)('A unique secret which is used to generate deploy hook URLs')}>
              <textCopyInput_1.default>{token}</textCopyInput_1.default>
            </field_1.default>
            <field_1.default label={(0, locale_1.t)('Regenerate Token')} help={(0, locale_1.t)('If a service becomes compromised, you should regenerate the token and re-configure any deploy hooks with the newly generated URL.')}>
              <div>
                <confirm_1.default disabled={!hasWrite} priority="danger" onConfirm={this.handleRegenerateToken} message={(0, locale_1.t)('Are you sure you want to regenerate your token? Your current token will no longer be usable.')}>
                  <button_1.default type="button" priority="danger" disabled={!hasWrite}>
                    {(0, locale_1.t)('Regenerate Token')}
                  </button_1.default>
                </confirm_1.default>
              </div>
            </field_1.default>
          </panels_1.PanelBody>
        </panels_1.Panel>

        <panels_1.Panel>
          <panels_1.PanelHeader>{(0, locale_1.t)('Webhook')}</panels_1.PanelHeader>
          <panels_1.PanelBody withPadding>
            <p>
              {(0, locale_1.t)('If you simply want to integrate with an existing system, sometimes its easiest just to use a webhook.')}
            </p>

            <autoSelectText_1.default>
              <pre>{webhookUrl}</pre>
            </autoSelectText_1.default>

            <p>
              {(0, locale_1.t)('The release webhook accepts the same parameters as the "Create a new Release" API endpoint.')}
            </p>

            {(0, getDynamicText_1.default)({
                value: (<autoSelectText_1.default>
                  <pre>{this.getReleaseWebhookIntructions()}</pre>
                </autoSelectText_1.default>),
                fixed: (<pre>
                  {`curl __WEBHOOK_URL__ \\
  -X POST \\
  -H 'Content-Type: application/json' \\
  -d \'{"version": "abcdefg"}\'`}
                </pre>),
            })}
          </panels_1.PanelBody>
        </panels_1.Panel>

        <pluginList_1.default organization={organization} project={project} pluginList={pluginList}/>

        <panels_1.Panel>
          <panels_1.PanelHeader>{(0, locale_1.t)('API')}</panels_1.PanelHeader>
          <panels_1.PanelBody withPadding>
            <p>
              {(0, locale_1.t)('You can notify Sentry when you release new versions of your application via our HTTP API.')}
            </p>

            <p>
              {(0, locale_1.tct)('See the [link:releases documentation] for more information.', {
                link: <externalLink_1.default href="https://docs.sentry.io/workflow/releases/"/>,
            })}
            </p>
          </panels_1.PanelBody>
        </panels_1.Panel>
      </div>);
    }
}
exports.ProjectReleaseTracking = ProjectReleaseTracking;
exports.default = (0, withPlugins_1.default)(ProjectReleaseTracking);
//# sourceMappingURL=projectReleaseTracking.jsx.map