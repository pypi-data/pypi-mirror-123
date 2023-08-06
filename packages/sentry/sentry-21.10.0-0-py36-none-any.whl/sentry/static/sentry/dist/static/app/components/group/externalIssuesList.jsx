Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const alertLink_1 = (0, tslib_1.__importDefault)(require("app/components/alertLink"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const errorBoundary_1 = (0, tslib_1.__importDefault)(require("app/components/errorBoundary"));
const externalIssueActions_1 = (0, tslib_1.__importDefault)(require("app/components/group/externalIssueActions"));
const pluginActions_1 = (0, tslib_1.__importDefault)(require("app/components/group/pluginActions"));
const sentryAppExternalIssueActions_1 = (0, tslib_1.__importDefault)(require("app/components/group/sentryAppExternalIssueActions"));
const issueSyncListElement_1 = (0, tslib_1.__importDefault)(require("app/components/issueSyncListElement"));
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const externalIssueStore_1 = (0, tslib_1.__importDefault)(require("app/stores/externalIssueStore"));
const sentryAppComponentsStore_1 = (0, tslib_1.__importDefault)(require("app/stores/sentryAppComponentsStore"));
const sentryAppInstallationsStore_1 = (0, tslib_1.__importDefault)(require("app/stores/sentryAppInstallationsStore"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const sidebarSection_1 = (0, tslib_1.__importDefault)(require("./sidebarSection"));
class ExternalIssueList extends asyncComponent_1.default {
    constructor(props) {
        super(props, {});
        this.unsubscribables = [];
        this.onSentryAppInstallationChange = (sentryAppInstallations) => {
            this.setState({ sentryAppInstallations });
        };
        this.onExternalIssueChange = (externalIssues) => {
            this.setState({ externalIssues });
        };
        this.onSentryAppComponentsChange = (sentryAppComponents) => {
            const components = sentryAppComponents.filter(c => c.type === 'issue-link');
            this.setState({ components });
        };
        this.state = Object.assign({}, this.state, {
            components: sentryAppComponentsStore_1.default.getInitialState(),
            sentryAppInstallations: sentryAppInstallationsStore_1.default.getInitialState(),
            externalIssues: externalIssueStore_1.default.getInitialState(),
        });
    }
    getEndpoints() {
        const { group } = this.props;
        return [['integrations', `/groups/${group.id}/integrations/`]];
    }
    UNSAFE_componentWillMount() {
        super.UNSAFE_componentWillMount();
        this.unsubscribables = [
            sentryAppInstallationsStore_1.default.listen(this.onSentryAppInstallationChange, this),
            externalIssueStore_1.default.listen(this.onExternalIssueChange, this),
            sentryAppComponentsStore_1.default.listen(this.onSentryAppComponentsChange, this),
        ];
        this.fetchSentryAppData();
    }
    componentWillUnmount() {
        super.componentWillUnmount();
        this.unsubscribables.forEach(unsubscribe => unsubscribe());
    }
    // We want to do this explicitly so that we can handle errors gracefully,
    // instead of the entire component not rendering.
    //
    // Part of the API request here is fetching data from the Sentry App, so
    // we need to be more conservative about error cases since we don't have
    // control over those services.
    //
    fetchSentryAppData() {
        const { group, project, organization } = this.props;
        if (project && project.id && organization) {
            this.api
                .requestPromise(`/groups/${group.id}/external-issues/`)
                .then(data => {
                externalIssueStore_1.default.load(data);
                this.setState({ externalIssues: data });
            })
                .catch(_error => { });
        }
    }
    updateIntegrations(onSuccess = () => { }, onError = () => { }) {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            try {
                const { group } = this.props;
                const integrations = yield this.api.requestPromise(`/groups/${group.id}/integrations/`);
                this.setState({ integrations }, () => onSuccess());
            }
            catch (error) {
                onError();
            }
        });
    }
    renderIntegrationIssues(integrations = []) {
        const { group } = this.props;
        const activeIntegrations = integrations.filter(integration => integration.status === 'active');
        const activeIntegrationsByProvider = activeIntegrations.reduce((acc, curr) => {
            const items = acc.get(curr.provider.key);
            if (!!items) {
                acc.set(curr.provider.key, [...items, curr]);
            }
            else {
                acc.set(curr.provider.key, [curr]);
            }
            return acc;
        }, new Map());
        return activeIntegrations.length
            ? [...activeIntegrationsByProvider.entries()].map(([provider, configurations]) => (<externalIssueActions_1.default key={provider} configurations={configurations} group={group} onChange={this.updateIntegrations.bind(this)}/>))
            : null;
    }
    renderSentryAppIssues() {
        const { externalIssues, sentryAppInstallations, components } = this.state;
        const { group } = this.props;
        if (components.length === 0) {
            return null;
        }
        return components.map(component => {
            const { sentryApp } = component;
            const installation = sentryAppInstallations.find(i => i.app.uuid === sentryApp.uuid);
            // should always find a match but TS complains if we don't handle this case
            if (!installation) {
                return null;
            }
            const issue = (externalIssues || []).find(i => i.serviceType === sentryApp.slug);
            return (<errorBoundary_1.default key={sentryApp.slug} mini>
          <sentryAppExternalIssueActions_1.default key={sentryApp.slug} group={group} event={this.props.event} sentryAppComponent={component} sentryAppInstallation={installation} externalIssue={issue}/>
        </errorBoundary_1.default>);
        });
    }
    renderPluginIssues() {
        const { group, project } = this.props;
        return group.pluginIssues && group.pluginIssues.length
            ? group.pluginIssues.map((plugin, i) => (<pluginActions_1.default group={group} project={project} plugin={plugin} key={i}/>))
            : null;
    }
    renderPluginActions() {
        const { group } = this.props;
        return group.pluginActions && group.pluginActions.length
            ? group.pluginActions.map((plugin, i) => (<issueSyncListElement_1.default externalIssueLink={plugin[1]} key={i}>
            {plugin[0]}
          </issueSyncListElement_1.default>))
            : null;
    }
    renderLoading() {
        return (<sidebarSection_1.default data-test-id="linked-issues" title={(0, locale_1.t)('Linked Issues')}>
        <placeholder_1.default height="120px"/>
      </sidebarSection_1.default>);
    }
    renderBody() {
        const sentryAppIssues = this.renderSentryAppIssues();
        const integrationIssues = this.renderIntegrationIssues(this.state.integrations);
        const pluginIssues = this.renderPluginIssues();
        const pluginActions = this.renderPluginActions();
        const showSetup = !sentryAppIssues && !integrationIssues && !pluginIssues && !pluginActions;
        return (<sidebarSection_1.default data-test-id="linked-issues" title={(0, locale_1.t)('Linked Issues')}>
        {showSetup && (<alertLink_1.default icon={<icons_1.IconGeneric />} priority="muted" size="small" to={`/settings/${this.props.organization.slug}/integrations`}>
            {(0, locale_1.t)('Set up Issue Tracking')}
          </alertLink_1.default>)}
        {sentryAppIssues && <Wrapper>{sentryAppIssues}</Wrapper>}
        {integrationIssues && <Wrapper>{integrationIssues}</Wrapper>}
        {pluginIssues && <Wrapper>{pluginIssues}</Wrapper>}
        {pluginActions && <Wrapper>{pluginActions}</Wrapper>}
      </sidebarSection_1.default>);
    }
}
const Wrapper = (0, styled_1.default)('div') `
  margin-bottom: ${(0, space_1.default)(2)};
`;
exports.default = (0, withOrganization_1.default)(ExternalIssueList);
//# sourceMappingURL=externalIssuesList.jsx.map