Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
require("prism-sentry/index.css");
const react_1 = require("react");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const platforms_1 = (0, tslib_1.__importDefault)(require("app/data/platforms"));
const locale_1 = require("app/locale");
const organization_1 = require("app/styles/organization");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const trackAdvancedAnalyticsEvent_1 = (0, tslib_1.__importDefault)(require("app/utils/analytics/trackAdvancedAnalyticsEvent"));
const integrationUtil_1 = require("app/utils/integrationUtil");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const firstEventFooter_1 = (0, tslib_1.__importDefault)(require("app/views/onboarding/components/firstEventFooter"));
const addInstallationInstructions_1 = (0, tslib_1.__importDefault)(require("app/views/onboarding/components/integrations/addInstallationInstructions"));
const postInstallCodeSnippet_1 = (0, tslib_1.__importDefault)(require("app/views/onboarding/components/integrations/postInstallCodeSnippet"));
const addIntegrationButton_1 = (0, tslib_1.__importDefault)(require("app/views/organizationIntegrations/addIntegrationButton"));
const platformHeaderButtonBar_1 = (0, tslib_1.__importDefault)(require("./components/platformHeaderButtonBar"));
class PlatformIntegrationSetup extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.handleFullDocsClick = () => {
            const { organization } = this.props;
            (0, trackAdvancedAnalyticsEvent_1.default)('growth.onboarding_view_full_docs', { organization });
        };
        this.handleAddIntegration = () => {
            this.setState({ installed: true });
        };
        this.trackSwitchToManual = () => {
            const { organization, integrationSlug } = this.props;
            (0, integrationUtil_1.trackIntegrationAnalytics)('integrations.switch_manual_sdk_setup', {
                integration_type: 'first_party',
                integration: integrationSlug,
                view: 'project_creation',
                organization,
            });
        };
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { installed: false, integrations: { providers: [] }, project: null });
    }
    componentDidMount() {
        window.scrollTo(0, 0);
        const { platform } = this.props.params;
        // redirect if platform is not known.
        if (!platform || platform === 'other') {
            this.redirectToNeutralDocs();
        }
    }
    get provider() {
        const { providers } = this.state.integrations;
        return providers.length ? providers[0] : null;
    }
    getEndpoints() {
        const { organization, integrationSlug, params } = this.props;
        if (!integrationSlug) {
            return [];
        }
        return [
            [
                'integrations',
                `/organizations/${organization.slug}/config/integrations/?provider_key=${integrationSlug}`,
            ],
            ['project', `/projects/${organization.slug}/${params.projectId}/`],
        ];
    }
    redirectToNeutralDocs() {
        const { orgId, projectId } = this.props.params;
        const url = `/organizations/${orgId}/projects/${projectId}/getting-started/`;
        react_router_1.browserHistory.push(url);
    }
    render() {
        const { organization, params } = this.props;
        const { installed, project } = this.state;
        const { projectId, orgId, platform } = params;
        const provider = this.provider;
        const platformIntegration = platforms_1.default.find(p => p.id === platform);
        if (!provider || !platformIntegration || !project) {
            return null;
        }
        const gettingStartedLink = `/organizations/${orgId}/projects/${projectId}/getting-started/`;
        // TODO: make dynamic when adding more integrations
        const docsLink = 'https://docs.sentry.io/product/integrations/cloud-monitoring/aws-lambda/';
        return (<OuterWrapper>
        <StyledPageHeader>
          <StyledTitle>
            {(0, locale_1.t)('Automatically instrument %s', platformIntegration.name)}
          </StyledTitle>
          <platformHeaderButtonBar_1.default gettingStartedLink={gettingStartedLink} docsLink={docsLink}/>
        </StyledPageHeader>
        <InnerWrapper>
          {!installed ? (<react_1.Fragment>
              <addInstallationInstructions_1.default />
              <StyledButtonBar gap={1}>
                <addIntegrationButton_1.default provider={provider} onAddIntegration={this.handleAddIntegration} organization={organization} priority="primary" size="small" analyticsParams={{ view: 'project_creation', already_installed: false }} modalParams={{ projectId: project.id }}/>
                <button_1.default size="small" to={{
                    pathname: window.location.pathname,
                    query: { manual: '1' },
                }} onClick={this.trackSwitchToManual}>
                  {(0, locale_1.t)('Manual Setup')}
                </button_1.default>
              </StyledButtonBar>
            </react_1.Fragment>) : (<react_1.Fragment>
              <postInstallCodeSnippet_1.default provider={provider}/>
              <firstEventFooter_1.default project={project} organization={organization} docsLink={docsLink} docsOnClick={this.handleFullDocsClick}/>
            </react_1.Fragment>)}
        </InnerWrapper>
      </OuterWrapper>);
    }
}
const StyledButtonBar = (0, styled_1.default)(buttonBar_1.default) `
  margin-top: ${(0, space_1.default)(3)};
  width: max-content;

  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    width: auto;
    grid-row-gap: ${(0, space_1.default)(1)};
    grid-auto-flow: row;
  }
`;
const InnerWrapper = (0, styled_1.default)('div') `
  width: 850px;
`;
const OuterWrapper = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 50px;
`;
const StyledPageHeader = (0, styled_1.default)(organization_1.PageHeader) `
  margin-bottom: ${(0, space_1.default)(3)};
`;
const StyledTitle = (0, styled_1.default)('h2') `
  margin: 0 ${(0, space_1.default)(3)} 0 0;
`;
exports.default = (0, withOrganization_1.default)(PlatformIntegrationSetup);
//# sourceMappingURL=platformIntegrationSetup.jsx.map