Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const list_1 = (0, tslib_1.__importDefault)(require("app/components/list"));
const listItem_1 = (0, tslib_1.__importDefault)(require("app/components/list/listItem"));
const navTabs_1 = (0, tslib_1.__importDefault)(require("app/components/navTabs"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const integrationUtil_1 = require("app/utils/integrationUtil");
const marked_1 = require("app/utils/marked");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const addIntegration_1 = (0, tslib_1.__importDefault)(require("app/views/organizationIntegrations/addIntegration"));
const integrationAlertRules_1 = (0, tslib_1.__importDefault)(require("app/views/organizationIntegrations/integrationAlertRules"));
const integrationCodeMappings_1 = (0, tslib_1.__importDefault)(require("app/views/organizationIntegrations/integrationCodeMappings"));
const integrationExternalTeamMappings_1 = (0, tslib_1.__importDefault)(require("app/views/organizationIntegrations/integrationExternalTeamMappings"));
const integrationExternalUserMappings_1 = (0, tslib_1.__importDefault)(require("app/views/organizationIntegrations/integrationExternalUserMappings"));
const integrationItem_1 = (0, tslib_1.__importDefault)(require("app/views/organizationIntegrations/integrationItem"));
const integrationMainSettings_1 = (0, tslib_1.__importDefault)(require("app/views/organizationIntegrations/integrationMainSettings"));
const integrationRepos_1 = (0, tslib_1.__importDefault)(require("app/views/organizationIntegrations/integrationRepos"));
const integrationServerlessFunctions_1 = (0, tslib_1.__importDefault)(require("app/views/organizationIntegrations/integrationServerlessFunctions"));
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const jsonForm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/jsonForm"));
const breadcrumbTitle_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsBreadcrumb/breadcrumbTitle"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
class ConfigureIntegration extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.onTabChange = (value) => {
            this.setState({ tab: value });
        };
        this.onUpdateIntegration = () => {
            this.setState(this.getDefaultState(), this.fetchData);
        };
        this.getAction = (provider) => {
            const { integration } = this.state;
            const action = provider && provider.key === 'pagerduty' ? (<addIntegration_1.default provider={provider} onInstall={this.onUpdateIntegration} account={integration.domainName} organization={this.props.organization}>
          {onClick => (<button_1.default priority="primary" size="small" icon={<icons_1.IconAdd size="xs" isCircled/>} onClick={() => onClick()}>
              {(0, locale_1.t)('Add Services')}
            </button_1.default>)}
        </addIntegration_1.default>) : null;
            return action;
        };
    }
    getEndpoints() {
        const { orgId, integrationId } = this.props.params;
        return [
            ['config', `/organizations/${orgId}/config/integrations/`],
            ['integration', `/organizations/${orgId}/integrations/${integrationId}/`],
        ];
    }
    componentDidMount() {
        const { location } = this.props;
        const value = ['codeMappings', 'userMappings', 'teamMappings'].find(tab => tab === location.query.tab) || 'repos';
        // eslint-disable-next-line react/no-did-mount-set-state
        this.setState({ tab: value });
    }
    onRequestSuccess({ stateKey, data }) {
        if (stateKey !== 'integration') {
            return;
        }
        (0, integrationUtil_1.trackIntegrationAnalytics)('integrations.details_viewed', {
            integration: data.provider.key,
            integration_type: 'first_party',
            organization: this.props.organization,
        });
    }
    getTitle() {
        return this.state.integration
            ? this.state.integration.provider.name
            : 'Configure Integration';
    }
    hasStacktraceLinking(provider) {
        // CodeOwners will only work if the provider has StackTrace Linking
        return (provider.features.includes('stacktrace-link') &&
            this.props.organization.features.includes('integrations-stacktrace-link'));
    }
    hasCodeOwners() {
        return this.props.organization.features.includes('integrations-codeowners');
    }
    isCustomIntegration() {
        const { integration } = this.state;
        const { organization } = this.props;
        return (organization.features.includes('integrations-custom-scm') &&
            integration.provider.key === 'custom_scm');
    }
    get tab() {
        return this.state.tab || 'repos';
    }
    // TODO(Steve): Refactor components into separate tabs and use more generic tab logic
    renderMainTab(provider) {
        var _a, _b, _c, _d;
        const { orgId } = this.props.params;
        const { integration } = this.state;
        const instructions = (_b = (_a = integration.dynamicDisplayInformation) === null || _a === void 0 ? void 0 : _a.configure_integration) === null || _b === void 0 ? void 0 : _b.instructions;
        return (<react_1.Fragment>
        <breadcrumbTitle_1.default routes={this.props.routes} title={integration.provider.name}/>

        {integration.configOrganization.length > 0 && (<form_1.default hideFooter saveOnBlur allowUndo apiMethod="POST" initialData={integration.configData || {}} apiEndpoint={`/organizations/${orgId}/integrations/${integration.id}/`}>
            <jsonForm_1.default fields={integration.configOrganization} title={((_c = integration.provider.aspects.configure_integration) === null || _c === void 0 ? void 0 : _c.title) ||
                    (0, locale_1.t)('Organization Integration Settings')}/>
          </form_1.default>)}

        {instructions && instructions.length > 0 && (<alert_1.default type="info">
            {(instructions === null || instructions === void 0 ? void 0 : instructions.length) === 1 ? (<span dangerouslySetInnerHTML={{ __html: (0, marked_1.singleLineRenderer)(instructions[0]) }}/>) : (<list_1.default symbol={<icons_1.IconArrow size="xs" direction="right"/>}>
                {(_d = instructions === null || instructions === void 0 ? void 0 : instructions.map((instruction, i) => (<listItem_1.default key={i}>
                    <span dangerouslySetInnerHTML={{ __html: (0, marked_1.singleLineRenderer)(instruction) }}/>
                  </listItem_1.default>))) !== null && _d !== void 0 ? _d : []}
              </list_1.default>)}
          </alert_1.default>)}

        {provider.features.includes('alert-rule') && <integrationAlertRules_1.default />}

        {provider.features.includes('commits') && (<integrationRepos_1.default {...this.props} integration={integration}/>)}

        {provider.features.includes('serverless') && (<integrationServerlessFunctions_1.default integration={integration}/>)}
      </react_1.Fragment>);
    }
    renderBody() {
        const { integration } = this.state;
        const provider = this.state.config.providers.find(p => p.key === integration.provider.key);
        if (!provider) {
            return null;
        }
        const title = <integrationItem_1.default integration={integration}/>;
        const header = (<settingsPageHeader_1.default noTitleStyles title={title} action={this.getAction(provider)}/>);
        return (<react_1.Fragment>
        {header}
        {this.renderMainContent(provider)}
      </react_1.Fragment>);
    }
    // renders everything below header
    renderMainContent(provider) {
        // if no code mappings, render the single tab
        if (!this.hasStacktraceLinking(provider)) {
            return this.renderMainTab(provider);
        }
        // otherwise render the tab view
        const tabs = [
            ['repos', (0, locale_1.t)('Repositories')],
            ['codeMappings', (0, locale_1.t)('Code Mappings')],
            ...(this.hasCodeOwners() ? [['userMappings', (0, locale_1.t)('User Mappings')]] : []),
            ...(this.hasCodeOwners() ? [['teamMappings', (0, locale_1.t)('Team Mappings')]] : []),
        ];
        if (this.isCustomIntegration()) {
            tabs.unshift(['settings', (0, locale_1.t)('Settings')]);
        }
        return (<react_1.Fragment>
        <navTabs_1.default underlined>
          {tabs.map(tabTuple => (<li key={tabTuple[0]} className={this.tab === tabTuple[0] ? 'active' : ''} onClick={() => this.onTabChange(tabTuple[0])}>
              <CapitalizedLink>{tabTuple[1]}</CapitalizedLink>
            </li>))}
        </navTabs_1.default>
        {this.renderTabContent(this.tab, provider)}
      </react_1.Fragment>);
    }
    renderTabContent(tab, provider) {
        const { integration } = this.state;
        const { organization } = this.props;
        switch (tab) {
            case 'codeMappings':
                return <integrationCodeMappings_1.default integration={integration}/>;
            case 'repos':
                return this.renderMainTab(provider);
            case 'userMappings':
                return <integrationExternalUserMappings_1.default integration={integration}/>;
            case 'teamMappings':
                return <integrationExternalTeamMappings_1.default integration={integration}/>;
            case 'settings':
                return (<integrationMainSettings_1.default onUpdate={this.onUpdateIntegration} organization={organization} integration={integration}/>);
            default:
                return this.renderMainTab(provider);
        }
    }
}
exports.default = (0, withOrganization_1.default)(ConfigureIntegration);
const CapitalizedLink = (0, styled_1.default)('a') `
  text-transform: capitalize;
`;
//# sourceMappingURL=configureIntegration.jsx.map