Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
require("prism-sentry/index.css");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const framer_motion_1 = require("framer-motion");
const modal_1 = require("app/actionCreators/modal");
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const platforms_1 = (0, tslib_1.__importDefault)(require("app/data/platforms"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const trackAdvancedAnalyticsEvent_1 = (0, tslib_1.__importDefault)(require("app/utils/analytics/trackAdvancedAnalyticsEvent"));
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const integrationUtil_1 = require("app/utils/integrationUtil");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const addIntegrationButton_1 = (0, tslib_1.__importDefault)(require("app/views/organizationIntegrations/addIntegrationButton"));
const firstEventFooter_1 = (0, tslib_1.__importDefault)(require("./components/firstEventFooter"));
const addInstallationInstructions_1 = (0, tslib_1.__importDefault)(require("./components/integrations/addInstallationInstructions"));
const postInstallCodeSnippet_1 = (0, tslib_1.__importDefault)(require("./components/integrations/postInstallCodeSnippet"));
const setupIntroduction_1 = (0, tslib_1.__importDefault)(require("./components/setupIntroduction"));
class IntegrationSetup extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            loadedPlatform: null,
            hasError: false,
            provider: null,
            installed: false,
        };
        this.fetchData = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, organization, platform, integrationSlug } = this.props;
            if (!integrationSlug) {
                return;
            }
            try {
                const endpoint = `/organizations/${organization.slug}/config/integrations/?provider_key=${integrationSlug}`;
                const integrations = yield api.requestPromise(endpoint);
                const provider = integrations.providers[0];
                this.setState({ provider, loadedPlatform: platform, hasError: false });
            }
            catch (error) {
                this.setState({ hasError: error });
                throw error;
            }
        });
        this.handleFullDocsClick = () => {
            const { organization } = this.props;
            (0, trackAdvancedAnalyticsEvent_1.default)('growth.onboarding_view_full_docs', { organization });
        };
        this.trackSwitchToManual = () => {
            const { organization, integrationSlug } = this.props;
            (0, integrationUtil_1.trackIntegrationAnalytics)('integrations.switch_manual_sdk_setup', {
                integration_type: 'first_party',
                integration: integrationSlug,
                view: 'onboarding',
                organization,
            });
        };
        this.handleAddIntegration = () => {
            this.setState({ installed: true });
        };
        this.renderSetupInstructions = () => {
            var _a, _b, _c;
            const { platform } = this.props;
            const { loadedPlatform } = this.state;
            const currentPlatform = (_a = loadedPlatform !== null && loadedPlatform !== void 0 ? loadedPlatform : platform) !== null && _a !== void 0 ? _a : 'other';
            return (<setupIntroduction_1.default stepHeaderText={(0, locale_1.t)('Automatically instrument %s', (_c = (_b = platforms_1.default.find(p => p.id === currentPlatform)) === null || _b === void 0 ? void 0 : _b.name) !== null && _c !== void 0 ? _c : '')} platform={currentPlatform}/>);
        };
    }
    componentDidMount() {
        this.fetchData();
    }
    componentDidUpdate(nextProps) {
        if (nextProps.platform !== this.props.platform ||
            nextProps.project !== this.props.project) {
            this.fetchData();
        }
    }
    get manualSetupUrl() {
        const { search } = window.location;
        // honor any existing query params
        const separator = search.includes('?') ? '&' : '?';
        return `${search}${separator}manual=1`;
    }
    get platformDocs() {
        // TODO: make dynamic based on the integration
        return 'https://docs.sentry.io/product/integrations/cloud-monitoring/aws-lambda/';
    }
    renderIntegrationInstructions() {
        const { organization, project } = this.props;
        const { provider } = this.state;
        if (!provider || !project) {
            return null;
        }
        return (<react_1.Fragment>
        {this.renderSetupInstructions()}
        <framer_motion_1.motion.p variants={{
                initial: { opacity: 0 },
                animate: { opacity: 1 },
                exit: { opacity: 0 },
            }}>
          {(0, locale_1.tct)("Don't have have permissions to create a Cloudformation stack? [link:Invite your team instead].", {
                link: (<button_1.default priority="link" onClick={() => {
                        (0, modal_1.openInviteMembersModal)();
                    }}/>),
            })}
        </framer_motion_1.motion.p>
        <framer_motion_1.motion.div variants={{
                initial: { opacity: 0 },
                animate: { opacity: 1 },
                exit: { opacity: 0 },
            }}>
          <addInstallationInstructions_1.default />
        </framer_motion_1.motion.div>

        <DocsWrapper>
          <StyledButtonBar gap={1}>
            <addIntegrationButton_1.default provider={provider} onAddIntegration={this.handleAddIntegration} organization={organization} priority="primary" size="small" analyticsParams={{ view: 'onboarding', already_installed: false }} modalParams={{ projectId: project.id }}/>
            <button_1.default size="small" to={{
                pathname: window.location.pathname,
                query: { manual: '1' },
            }} onClick={this.trackSwitchToManual}>
              {(0, locale_1.t)('Manual Setup')}
            </button_1.default>
          </StyledButtonBar>
        </DocsWrapper>
      </react_1.Fragment>);
    }
    renderPostInstallInstructions() {
        const { organization, project, platform } = this.props;
        const { provider } = this.state;
        if (!project || !provider || !platform) {
            return null;
        }
        return (<react_1.Fragment>
        {this.renderSetupInstructions()}
        <postInstallCodeSnippet_1.default provider={provider} platform={platform} isOnboarding/>
        <firstEventFooter_1.default project={project} organization={organization} docsLink={this.platformDocs} docsOnClick={this.handleFullDocsClick}/>
      </react_1.Fragment>);
    }
    render() {
        const { platform } = this.props;
        const { hasError } = this.state;
        const loadingError = (<loadingError_1.default message={(0, locale_1.t)('Failed to load the integration for the %s platform.', platform)} onRetry={this.fetchData}/>);
        const testOnlyAlert = (<alert_1.default type="warning">
        Platform documentation is not rendered in for tests in CI
      </alert_1.default>);
        return (<react_1.Fragment>
        {this.state.installed
                ? this.renderPostInstallInstructions()
                : this.renderIntegrationInstructions()}
        {(0, getDynamicText_1.default)({
                value: !hasError ? null : loadingError,
                fixed: testOnlyAlert,
            })}
      </react_1.Fragment>);
    }
}
const DocsWrapper = (0, styled_1.default)(framer_motion_1.motion.div) ``;
DocsWrapper.defaultProps = {
    initial: { opacity: 0, y: 40 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0 },
};
const StyledButtonBar = (0, styled_1.default)(buttonBar_1.default) `
  margin-top: ${(0, space_1.default)(3)};
  width: max-content;

  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    width: auto;
    grid-row-gap: ${(0, space_1.default)(1)};
    grid-auto-flow: row;
  }
`;
exports.default = (0, withOrganization_1.default)((0, withApi_1.default)(IntegrationSetup));
//# sourceMappingURL=integrationSetup.jsx.map