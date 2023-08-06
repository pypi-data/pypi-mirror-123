Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const featureDisabled_1 = (0, tslib_1.__importDefault)(require("app/components/acl/featureDisabled"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const miniBarChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/miniBarChart"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const panels_1 = require("app/components/panels");
const pluginList_1 = (0, tslib_1.__importDefault)(require("app/components/pluginList"));
const sentryDocumentTitle_1 = (0, tslib_1.__importDefault)(require("app/components/sentryDocumentTitle"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const textBlock_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/text/textBlock"));
const permissionAlert_1 = (0, tslib_1.__importDefault)(require("app/views/settings/project/permissionAlert"));
class DataForwardingStats extends asyncComponent_1.default {
    getEndpoints() {
        const { orgId, projectId } = this.props.params;
        const until = Math.floor(new Date().getTime() / 1000);
        const since = until - 3600 * 24 * 30;
        const options = {
            query: {
                since,
                until,
                resolution: '1d',
                stat: 'forwarded',
            },
        };
        return [['stats', `/projects/${orgId}/${projectId}/stats/`, options]];
    }
    renderBody() {
        const { projectId } = this.props.params;
        const { stats } = this.state;
        const series = {
            seriesName: (0, locale_1.t)('Forwarded'),
            data: stats.map(([timestamp, value]) => ({ name: timestamp * 1000, value })),
        };
        const forwardedAny = series.data.some(({ value }) => value > 0);
        return (<panels_1.Panel>
        <sentryDocumentTitle_1.default title={(0, locale_1.t)('Data Forwarding')} projectSlug={projectId}/>
        <panels_1.PanelHeader>{(0, locale_1.t)('Forwarded events in the last 30 days (by day)')}</panels_1.PanelHeader>
        <panels_1.PanelBody withPadding>
          {forwardedAny ? (<miniBarChart_1.default isGroupedByDate showTimeInTooltip labelYAxisExtents series={[series]} height={150}/>) : (<emptyMessage_1.default title={(0, locale_1.t)('Nothing forwarded in the last 30 days.')} description={(0, locale_1.t)('Total events forwarded to third party integrations.')}/>)}
        </panels_1.PanelBody>
      </panels_1.Panel>);
    }
}
class ProjectDataForwarding extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.onEnablePlugin = (plugin) => this.updatePlugin(plugin, true);
        this.onDisablePlugin = (plugin) => this.updatePlugin(plugin, false);
    }
    getEndpoints() {
        const { orgId, projectId } = this.props.params;
        return [['plugins', `/projects/${orgId}/${projectId}/plugins/`]];
    }
    get forwardingPlugins() {
        return this.state.plugins.filter(p => p.type === 'data-forwarding' && p.hasConfiguration);
    }
    updatePlugin(plugin, enabled) {
        const plugins = this.state.plugins.map(p => (Object.assign(Object.assign({}, p), { enabled: p.id === plugin.id ? enabled : p.enabled })));
        this.setState({ plugins });
    }
    renderBody() {
        const { params, organization, project } = this.props;
        const plugins = this.forwardingPlugins;
        const hasAccess = organization.access.includes('project:write');
        const pluginsPanel = plugins.length > 0 ? (<pluginList_1.default organization={organization} project={project} pluginList={plugins} onEnablePlugin={this.onEnablePlugin} onDisablePlugin={this.onDisablePlugin}/>) : (<panels_1.Panel>
          <emptyMessage_1.default title={(0, locale_1.t)('There are no integrations available for data forwarding')}/>
        </panels_1.Panel>);
        return (<div data-test-id="data-forwarding-settings">
        <feature_1.default features={['projects:data-forwarding']} hookName="feature-disabled:data-forwarding">
          {({ hasFeature, features }) => (<react_1.Fragment>
              <settingsPageHeader_1.default title={(0, locale_1.t)('Data Forwarding')}/>
              <textBlock_1.default>
                {(0, locale_1.tct)(`Data Forwarding allows processed events to be sent to your
                favorite business intelligence tools. The exact payload and
                types of data depend on the integration you're using. Learn
                more about this functionality in our [link:documentation].`, {
                    link: (<externalLink_1.default href="https://docs.sentry.io/product/data-management-settings/data-forwarding/"/>),
                })}
              </textBlock_1.default>
              <permissionAlert_1.default />

              <alert_1.default icon={<icons_1.IconInfo size="md"/>}>
                {(0, locale_1.tct)(`Sentry forwards [em:all applicable events] to the provider, in
                some cases this may be a significant volume of data.`, {
                    em: <strong />,
                })}
              </alert_1.default>

              {!hasFeature && (<featureDisabled_1.default alert featureName="Data Forwarding" features={features}/>)}

              <DataForwardingStats params={params}/>
              {hasAccess && hasFeature && pluginsPanel}
            </react_1.Fragment>)}
        </feature_1.default>
      </div>);
    }
}
exports.default = (0, withOrganization_1.default)(ProjectDataForwarding);
//# sourceMappingURL=projectDataForwarding.jsx.map