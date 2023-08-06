Object.defineProperty(exports, "__esModule", { value: true });
exports.ProjectPluginDetails = void 0;
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const plugins_1 = require("app/actionCreators/plugins");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const pluginConfig_1 = (0, tslib_1.__importDefault)(require("app/components/pluginConfig"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const integrationUtil_1 = require("app/utils/integrationUtil");
const withPlugins_1 = (0, tslib_1.__importDefault)(require("app/utils/withPlugins"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
/**
 * There are currently two sources of truths for plugin details:
 *
 * 1) PluginsStore has a list of plugins, and this is where ENABLED state lives
 * 2) We fetch "plugin details" via API and save it to local state as `pluginDetails`.
 *    This is because "details" call contains form `config` and the "list" endpoint does not.
 *    The more correct way would be to pass `config` to PluginConfig and use plugin from
 *    PluginsStore
 */
class ProjectPluginDetails extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.handleReset = () => {
            const { projectId, orgId, pluginId } = this.props.params;
            (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Saving changes\u2026'));
            (0, integrationUtil_1.trackIntegrationAnalytics)('integrations.uninstall_clicked', {
                integration: pluginId,
                integration_type: 'plugin',
                view: 'plugin_details',
                organization: this.props.organization,
            });
            this.api.request(`/projects/${orgId}/${projectId}/plugins/${pluginId}/`, {
                method: 'POST',
                data: { reset: true },
                success: pluginDetails => {
                    this.setState({ pluginDetails });
                    (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Plugin was reset'));
                    (0, integrationUtil_1.trackIntegrationAnalytics)('integrations.uninstall_completed', {
                        integration: pluginId,
                        integration_type: 'plugin',
                        view: 'plugin_details',
                        organization: this.props.organization,
                    });
                },
                error: () => {
                    (0, indicator_1.addErrorMessage)((0, locale_1.t)('An error occurred'));
                },
            });
        };
        this.handleEnable = () => {
            (0, plugins_1.enablePlugin)(this.props.params);
            this.analyticsChangeEnableStatus(true);
        };
        this.handleDisable = () => {
            (0, plugins_1.disablePlugin)(this.props.params);
            this.analyticsChangeEnableStatus(false);
        };
        this.analyticsChangeEnableStatus = (enabled) => {
            const { pluginId } = this.props.params;
            const eventKey = enabled ? 'integrations.enabled' : 'integrations.disabled';
            (0, integrationUtil_1.trackIntegrationAnalytics)(eventKey, {
                integration: pluginId,
                integration_type: 'plugin',
                view: 'plugin_details',
                organization: this.props.organization,
            });
        };
    }
    componentDidUpdate(prevProps, prevContext) {
        super.componentDidUpdate(prevProps, prevContext);
        if (prevProps.params.pluginId !== this.props.params.pluginId) {
            this.recordDetailsViewed();
        }
    }
    componentDidMount() {
        this.recordDetailsViewed();
    }
    recordDetailsViewed() {
        const { pluginId } = this.props.params;
        (0, integrationUtil_1.trackIntegrationAnalytics)('integrations.details_viewed', {
            integration: pluginId,
            integration_type: 'plugin',
            view: 'plugin_details',
            organization: this.props.organization,
        });
    }
    getTitle() {
        const { plugin } = this.state;
        if (plugin && plugin.name) {
            return plugin.name;
        }
        else {
            return 'Sentry';
        }
    }
    getEndpoints() {
        const { projectId, orgId, pluginId } = this.props.params;
        return [['pluginDetails', `/projects/${orgId}/${projectId}/plugins/${pluginId}/`]];
    }
    trimSchema(value) {
        return value.split('//')[1];
    }
    // Enabled state is handled via PluginsStore and not via plugins detail
    getEnabled() {
        const { pluginDetails } = this.state;
        const { plugins } = this.props;
        const plugin = plugins &&
            plugins.plugins &&
            plugins.plugins.find(({ slug }) => slug === this.props.params.pluginId);
        return plugin ? plugin.enabled : pluginDetails && pluginDetails.enabled;
    }
    renderActions() {
        const { pluginDetails } = this.state;
        if (!pluginDetails) {
            return null;
        }
        const enabled = this.getEnabled();
        const enable = (<StyledButton size="small" onClick={this.handleEnable}>
        {(0, locale_1.t)('Enable Plugin')}
      </StyledButton>);
        const disable = (<StyledButton size="small" priority="danger" onClick={this.handleDisable}>
        {(0, locale_1.t)('Disable Plugin')}
      </StyledButton>);
        const toggleEnable = enabled ? disable : enable;
        return (<div className="pull-right">
        {pluginDetails.canDisable && toggleEnable}
        <button_1.default size="small" onClick={this.handleReset}>
          {(0, locale_1.t)('Reset Configuration')}
        </button_1.default>
      </div>);
    }
    renderBody() {
        var _a, _b;
        const { organization, project } = this.props;
        const { pluginDetails } = this.state;
        if (!pluginDetails) {
            return null;
        }
        return (<div>
        <settingsPageHeader_1.default title={pluginDetails.name} action={this.renderActions()}/>
        <div className="row">
          <div className="col-md-7">
            <pluginConfig_1.default organization={organization} project={project} data={pluginDetails} enabled={this.getEnabled()} onDisablePlugin={this.handleDisable}/>
          </div>
          <div className="col-md-4 col-md-offset-1">
            <div className="pluginDetails-meta">
              <h4>{(0, locale_1.t)('Plugin Information')}</h4>

              <dl className="flat">
                <dt>{(0, locale_1.t)('Name')}</dt>
                <dd>{pluginDetails.name}</dd>
                <dt>{(0, locale_1.t)('Author')}</dt>
                <dd>{(_a = pluginDetails.author) === null || _a === void 0 ? void 0 : _a.name}</dd>
                {((_b = pluginDetails.author) === null || _b === void 0 ? void 0 : _b.url) && (<div>
                    <dt>{(0, locale_1.t)('URL')}</dt>
                    <dd>
                      <externalLink_1.default href={pluginDetails.author.url}>
                        {this.trimSchema(pluginDetails.author.url)}
                      </externalLink_1.default>
                    </dd>
                  </div>)}
                <dt>{(0, locale_1.t)('Version')}</dt>
                <dd>{pluginDetails.version}</dd>
              </dl>

              {pluginDetails.description && (<div>
                  <h4>{(0, locale_1.t)('Description')}</h4>
                  <p className="description">{pluginDetails.description}</p>
                </div>)}

              {pluginDetails.resourceLinks && (<div>
                  <h4>{(0, locale_1.t)('Resources')}</h4>
                  <dl className="flat">
                    {pluginDetails.resourceLinks.map(({ title, url }) => (<dd key={url}>
                        <externalLink_1.default href={url}>{title}</externalLink_1.default>
                      </dd>))}
                  </dl>
                </div>)}
            </div>
          </div>
        </div>
      </div>);
    }
}
exports.ProjectPluginDetails = ProjectPluginDetails;
exports.default = (0, withPlugins_1.default)(ProjectPluginDetails);
const StyledButton = (0, styled_1.default)(button_1.default) `
  margin-right: ${(0, space_1.default)(0.75)};
`;
//# sourceMappingURL=details.jsx.map