Object.defineProperty(exports, "__esModule", { value: true });
exports.ProjectInstallPlatform = void 0;
const tslib_1 = require("tslib");
require("prism-sentry/index.css");
const react_1 = require("react");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const projects_1 = require("app/actionCreators/projects");
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const notFound_1 = (0, tslib_1.__importDefault)(require("app/components/errors/notFound"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const sentryDocumentTitle_1 = (0, tslib_1.__importDefault)(require("app/components/sentryDocumentTitle"));
const platformCategories_1 = require("app/data/platformCategories");
const platforms_1 = (0, tslib_1.__importDefault)(require("app/data/platforms"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const organization_1 = require("app/styles/organization");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const projects_2 = (0, tslib_1.__importDefault)(require("app/utils/projects"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
class ProjectInstallPlatform extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            loading: true,
            error: false,
            html: '',
        };
        this.fetchData = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, params } = this.props;
            const { orgId, projectId, platform } = params;
            this.setState({ loading: true });
            try {
                const { html } = yield (0, projects_1.loadDocs)(api, orgId, projectId, platform);
                this.setState({ html });
            }
            catch (error) {
                this.setState({ error });
            }
            this.setState({ loading: false });
        });
    }
    componentDidMount() {
        this.fetchData();
        window.scrollTo(0, 0);
        const { platform } = this.props.params;
        // redirect if platform is not known.
        if (!platform || platform === 'other') {
            this.redirectToNeutralDocs();
        }
    }
    get isGettingStarted() {
        return window.location.href.indexOf('getting-started') > 0;
    }
    redirectToNeutralDocs() {
        const { orgId, projectId } = this.props.params;
        const url = `/organizations/${orgId}/projects/${projectId}/getting-started/`;
        react_router_1.browserHistory.push(url);
    }
    render() {
        var _a;
        const { params } = this.props;
        const { orgId, projectId } = params;
        const platform = platforms_1.default.find(p => p.id === params.platform);
        if (!platform) {
            return <notFound_1.default />;
        }
        const issueStreamLink = `/organizations/${orgId}/issues/`;
        const performanceOverviewLink = `/organizations/${orgId}/performance/`;
        const gettingStartedLink = `/organizations/${orgId}/projects/${projectId}/getting-started/`;
        const platformLink = (_a = platform.link) !== null && _a !== void 0 ? _a : undefined;
        return (<react_1.Fragment>
        <StyledPageHeader>
          <h2>{(0, locale_1.t)('Configure %(platform)s', { platform: platform.name })}</h2>
          <buttonBar_1.default gap={1}>
            <button_1.default size="small" to={gettingStartedLink}>
              {(0, locale_1.t)('< Back')}
            </button_1.default>
            <button_1.default size="small" href={platformLink} external>
              {(0, locale_1.t)('Full Documentation')}
            </button_1.default>
          </buttonBar_1.default>
        </StyledPageHeader>

        <div>
          <alert_1.default type="info" icon={<icons_1.IconInfo />}>
            {(0, locale_1.tct)(`
             This is a quick getting started guide. For in-depth instructions
             on integrating Sentry with [platform], view
             [docLink:our complete documentation].`, {
                platform: platform.name,
                docLink: <a href={platformLink}/>,
            })}
          </alert_1.default>

          {this.state.loading ? (<loadingIndicator_1.default />) : this.state.error ? (<loadingError_1.default onRetry={this.fetchData}/>) : (<react_1.Fragment>
              <sentryDocumentTitle_1.default title={`${(0, locale_1.t)('Configure')} ${platform.name}`} projectSlug={projectId}/>
              <DocumentationWrapper dangerouslySetInnerHTML={{ __html: this.state.html }}/>
            </react_1.Fragment>)}

          {this.isGettingStarted && (<projects_2.default key={`${orgId}-${projectId}`} orgId={orgId} slugs={[projectId]} passthroughPlaceholderProject={false}>
              {({ projects, initiallyLoaded, fetching, fetchError }) => {
                    const projectsLoading = !initiallyLoaded && fetching;
                    const projectFilter = !projectsLoading && !fetchError && projects.length
                        ? {
                            project: projects[0].id,
                        }
                        : {};
                    const showPerformancePrompt = platformCategories_1.performance.includes(platform.id);
                    return (<react_1.Fragment>
                    {showPerformancePrompt && (<feature_1.default features={['performance-view']} hookName="feature-disabled:performance-new-project">
                        {({ hasFeature }) => {
                                if (hasFeature) {
                                    return null;
                                }
                                return (<StyledAlert type="info" icon={<icons_1.IconInfo />}>
                              {(0, locale_1.t)(`Your selected platform supports performance, but your organization does not have performance enabled.`)}
                            </StyledAlert>);
                            }}
                      </feature_1.default>)}

                    <StyledButtonBar gap={1}>
                      <button_1.default priority="primary" busy={projectsLoading} to={{
                            pathname: issueStreamLink,
                            query: projectFilter,
                            hash: '#welcome',
                        }}>
                        {(0, locale_1.t)('Take me to Issues')}
                      </button_1.default>
                      <button_1.default busy={projectsLoading} to={{
                            pathname: performanceOverviewLink,
                            query: projectFilter,
                        }}>
                        {(0, locale_1.t)('Take me to Performance')}
                      </button_1.default>
                    </StyledButtonBar>
                  </react_1.Fragment>);
                }}
            </projects_2.default>)}
        </div>
      </react_1.Fragment>);
    }
}
exports.ProjectInstallPlatform = ProjectInstallPlatform;
const DocumentationWrapper = (0, styled_1.default)('div') `
  line-height: 1.5;

  .gatsby-highlight {
    margin-bottom: ${(0, space_1.default)(3)};

    &:last-child {
      margin-bottom: 0;
    }
  }

  .alert {
    margin-bottom: ${(0, space_1.default)(3)};
    border-radius: ${p => p.theme.borderRadius};
  }

  pre {
    word-break: break-all;
    white-space: pre-wrap;
  }
`;
const StyledButtonBar = (0, styled_1.default)(buttonBar_1.default) `
  margin-top: ${(0, space_1.default)(3)};
  width: max-content;

  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    width: auto;
    grid-row-gap: ${(0, space_1.default)(1)};
    grid-auto-flow: row;
  }
`;
const StyledPageHeader = (0, styled_1.default)(organization_1.PageHeader) `
  margin-bottom: ${(0, space_1.default)(3)};

  h2 {
    margin: 0;
  }

  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    flex-direction: column;
    align-items: flex-start;

    h2 {
      margin-bottom: ${(0, space_1.default)(2)};
    }
  }
`;
const StyledAlert = (0, styled_1.default)(alert_1.default) `
  margin-top: ${(0, space_1.default)(2)};
`;
exports.default = (0, withApi_1.default)((0, withOrganization_1.default)(ProjectInstallPlatform));
//# sourceMappingURL=platform.jsx.map