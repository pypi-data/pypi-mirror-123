Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const sentryApps_1 = require("app/actionCreators/sentryApps");
const access_1 = (0, tslib_1.__importDefault)(require("app/components/acl/access"));
const alertLink_1 = (0, tslib_1.__importDefault)(require("app/components/alertLink"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const panels_1 = require("app/components/panels");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const routeTitle_1 = (0, tslib_1.__importDefault)(require("app/utils/routeTitle"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const sentryApplicationRow_1 = (0, tslib_1.__importDefault)(require("app/views/settings/organizationDeveloperSettings/sentryApplicationRow"));
class OrganizationDeveloperSettings extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.removeApp = (app) => {
            const apps = this.state.applications.filter(a => a.slug !== app.slug);
            (0, sentryApps_1.removeSentryApp)(this.api, app).then(() => {
                this.setState({ applications: apps });
            }, () => { });
        };
        this.renderApplicationRow = (app) => {
            const { organization } = this.props;
            return (<sentryApplicationRow_1.default key={app.uuid} app={app} organization={organization} onRemoveApp={this.removeApp}/>);
        };
    }
    getTitle() {
        const { orgId } = this.props.params;
        return (0, routeTitle_1.default)((0, locale_1.t)('Developer Settings'), orgId, false);
    }
    getEndpoints() {
        const { orgId } = this.props.params;
        return [['applications', `/organizations/${orgId}/sentry-apps/`]];
    }
    renderInternalIntegrations() {
        const { orgId } = this.props.params;
        const { organization } = this.props;
        const integrations = this.state.applications.filter((app) => app.status === 'internal');
        const isEmpty = integrations.length === 0;
        const permissionTooltipText = (0, locale_1.t)('Manager or Owner permissions required to add an internal integration.');
        const action = (<access_1.default organization={organization} access={['org:write']}>
        {({ hasAccess }) => (<button_1.default priority="primary" disabled={!hasAccess} title={!hasAccess ? permissionTooltipText : undefined} size="small" to={`/settings/${orgId}/developer-settings/new-internal/`} icon={<icons_1.IconAdd size="xs" isCircled/>}>
            {(0, locale_1.t)('New Internal Integration')}
          </button_1.default>)}
      </access_1.default>);
        return (<panels_1.Panel>
        <panels_1.PanelHeader hasButtons>
          {(0, locale_1.t)('Internal Integrations')}
          {action}
        </panels_1.PanelHeader>
        <panels_1.PanelBody>
          {!isEmpty ? (integrations.map(this.renderApplicationRow)) : (<emptyMessage_1.default>
              {(0, locale_1.t)('No internal integrations have been created yet.')}
            </emptyMessage_1.default>)}
        </panels_1.PanelBody>
      </panels_1.Panel>);
    }
    renderExernalIntegrations() {
        const { orgId } = this.props.params;
        const { organization } = this.props;
        const integrations = this.state.applications.filter(app => app.status !== 'internal');
        const isEmpty = integrations.length === 0;
        const permissionTooltipText = (0, locale_1.t)('Manager or Owner permissions required to add a public integration.');
        const action = (<access_1.default organization={organization} access={['org:write']}>
        {({ hasAccess }) => (<button_1.default priority="primary" disabled={!hasAccess} title={!hasAccess ? permissionTooltipText : undefined} size="small" to={`/settings/${orgId}/developer-settings/new-public/`} icon={<icons_1.IconAdd size="xs" isCircled/>}>
            {(0, locale_1.t)('New Public Integration')}
          </button_1.default>)}
      </access_1.default>);
        return (<panels_1.Panel>
        <panels_1.PanelHeader hasButtons>
          {(0, locale_1.t)('Public Integrations')}
          {action}
        </panels_1.PanelHeader>
        <panels_1.PanelBody>
          {!isEmpty ? (integrations.map(this.renderApplicationRow)) : (<emptyMessage_1.default>
              {(0, locale_1.t)('No public integrations have been created yet.')}
            </emptyMessage_1.default>)}
        </panels_1.PanelBody>
      </panels_1.Panel>);
    }
    renderBody() {
        return (<div>
        <settingsPageHeader_1.default title={(0, locale_1.t)('Developer Settings')}/>
        <alertLink_1.default href="https://docs.sentry.io/product/integrations/integration-platform/">
          {(0, locale_1.t)('Have questions about the Integration Platform? Learn more about it in our docs.')}
        </alertLink_1.default>
        {this.renderExernalIntegrations()}
        {this.renderInternalIntegrations()}
      </div>);
    }
}
exports.default = (0, withOrganization_1.default)(OrganizationDeveloperSettings);
//# sourceMappingURL=index.jsx.map