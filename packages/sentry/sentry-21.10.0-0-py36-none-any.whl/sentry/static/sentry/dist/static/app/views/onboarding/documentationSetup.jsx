Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
require("prism-sentry/index.css");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const framer_motion_1 = require("framer-motion");
const projects_1 = require("app/actionCreators/projects");
const alert_1 = (0, tslib_1.__importStar)(require("app/components/alert"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const platforms_1 = (0, tslib_1.__importDefault)(require("app/data/platforms"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const trackAdvancedAnalyticsEvent_1 = (0, tslib_1.__importDefault)(require("app/utils/analytics/trackAdvancedAnalyticsEvent"));
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const firstEventFooter_1 = (0, tslib_1.__importDefault)(require("./components/firstEventFooter"));
const fullIntroduction_1 = (0, tslib_1.__importDefault)(require("./components/fullIntroduction"));
/**
 * The documentation will include the following string should it be missing the
 * verification example, which currently a lot of docs are.
 */
const INCOMPLETE_DOC_FLAG = 'TODO-ADD-VERIFICATION-EXAMPLE';
class DocumentationSetup extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            platformDocs: null,
            loadedPlatform: null,
            hasError: false,
        };
        this.fetchData = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, project, organization, platform } = this.props;
            if (!project || !platform) {
                return;
            }
            try {
                const platformDocs = yield (0, projects_1.loadDocs)(api, organization.slug, project.slug, platform);
                this.setState({ platformDocs, loadedPlatform: platform, hasError: false });
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
    /**
     * TODO(epurkhiser): This can be removed once all documentation has an
     * example for sending the users first event.
     */
    get missingExampleWarning() {
        var _a;
        const { loadedPlatform, platformDocs } = this.state;
        const missingExample = platformDocs && platformDocs.html.includes(INCOMPLETE_DOC_FLAG);
        if (!missingExample) {
            return null;
        }
        return (<alert_1.default type="warning" icon={<icons_1.IconInfo size="md"/>}>
        {(0, locale_1.tct)(`Looks like this getting started example is still undergoing some
           work and doesn't include an example for triggering an event quite
           yet. If you have trouble sending your first event be sure to consult
           the [docsLink:full documentation] for [platform].`, {
                docsLink: <externalLink_1.default href={platformDocs === null || platformDocs === void 0 ? void 0 : platformDocs.link}/>,
                platform: (_a = platforms_1.default.find(p => p.id === loadedPlatform)) === null || _a === void 0 ? void 0 : _a.name,
            })}
      </alert_1.default>);
    }
    render() {
        var _a;
        const { organization, project, platform } = this.props;
        const { loadedPlatform, platformDocs, hasError } = this.state;
        const currentPlatform = (_a = loadedPlatform !== null && loadedPlatform !== void 0 ? loadedPlatform : platform) !== null && _a !== void 0 ? _a : 'other';
        const docs = platformDocs !== null && (<DocsWrapper key={platformDocs.html}>
        <Content dangerouslySetInnerHTML={{ __html: platformDocs.html }}/>
        {this.missingExampleWarning}

        {project && (<firstEventFooter_1.default project={project} organization={organization} docsLink={platformDocs === null || platformDocs === void 0 ? void 0 : platformDocs.link} docsOnClick={this.handleFullDocsClick}/>)}
      </DocsWrapper>);
        const loadingError = (<loadingError_1.default message={(0, locale_1.t)('Failed to load documentation for the %s platform.', platform)} onRetry={this.fetchData}/>);
        const testOnlyAlert = (<alert_1.default type="warning">
        Platform documentation is not rendered in for tests in CI
      </alert_1.default>);
        return (<React.Fragment>
        <fullIntroduction_1.default currentPlatform={currentPlatform}/>
        {(0, getDynamicText_1.default)({
                value: !hasError ? docs : loadingError,
                fixed: testOnlyAlert,
            })}
      </React.Fragment>);
    }
}
const getAlertSelector = (type) => type === 'muted' ? null : `.alert[level="${type}"], .alert-${type}`;
const mapAlertStyles = (p, type) => (0, react_1.css) `
    ${getAlertSelector(type)} {
      ${(0, alert_1.alertStyles)({ theme: p.theme, type })};
      display: block;
    }
  `;
const Content = (0, styled_1.default)(framer_motion_1.motion.div) `
  h1,
  h2,
  h3,
  h4,
  h5,
  h6,
  p {
    margin-bottom: 18px;
  }

  div[data-language] {
    margin-bottom: ${(0, space_1.default)(2)};
  }

  code {
    font-size: 87.5%;
    color: ${p => p.theme.pink300};
  }

  pre code {
    color: inherit;
    font-size: inherit;
    white-space: pre;
  }

  h2 {
    font-size: 1.4em;
  }

  .alert h5 {
    font-size: 1em;
    margin-bottom: 1rem;
  }

  /**
   * XXX(epurkhiser): This comes from the doc styles and avoids bottom margin issues in alerts
   */
  .content-flush-bottom *:last-child {
    margin-bottom: 0;
  }

  ${p => Object.keys(p.theme.alert).map(type => mapAlertStyles(p, type))}
`;
const DocsWrapper = (0, styled_1.default)(framer_motion_1.motion.div) ``;
DocsWrapper.defaultProps = {
    initial: { opacity: 0, y: 40 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0 },
};
exports.default = (0, withOrganization_1.default)((0, withApi_1.default)(DocumentationSetup));
//# sourceMappingURL=documentationSetup.jsx.map