Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const projects_1 = require("app/actionCreators/projects");
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const styles_1 = require("app/components/charts/styles");
const dateTime_1 = (0, tslib_1.__importDefault)(require("app/components/dateTime"));
const emptyStateWarning_1 = (0, tslib_1.__importDefault)(require("app/components/emptyStateWarning"));
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const textOverflow_1 = (0, tslib_1.__importDefault)(require("app/components/textOverflow"));
const version_1 = (0, tslib_1.__importDefault)(require("app/components/version"));
const globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const releasePromo_1 = require("app/views/releases/list/releasePromo");
const missingReleasesButtons_1 = (0, tslib_1.__importDefault)(require("./missingFeatureButtons/missingReleasesButtons"));
const styles_2 = require("./styles");
const utils_1 = require("./utils");
const PLACEHOLDER_AND_EMPTY_HEIGHT = '160px';
class ProjectLatestReleases extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.handleTourAdvance = (index) => {
            const { organization, projectId } = this.props;
            (0, analytics_1.analytics)('releases.landing_card_clicked', {
                org_id: parseInt(organization.id, 10),
                project_id: projectId && parseInt(projectId, 10),
                step_id: index,
                step_title: releasePromo_1.RELEASES_TOUR_STEPS[index].title,
            });
        };
        this.renderReleaseRow = (release) => {
            const { projectId } = this.props;
            const { lastDeploy, dateCreated } = release;
            return (<react_1.Fragment key={release.version}>
        <dateTime_1.default date={(lastDeploy === null || lastDeploy === void 0 ? void 0 : lastDeploy.dateFinished) || dateCreated} seconds={false}/>
        <textOverflow_1.default>
          <StyledVersion version={release.version} tooltipRawVersion projectId={projectId}/>
        </textOverflow_1.default>
      </react_1.Fragment>);
        };
    }
    shouldComponentUpdate(nextProps, nextState) {
        const { location, isProjectStabilized } = this.props;
        // TODO(project-detail): we temporarily removed refetching based on timeselector
        if (this.state !== nextState ||
            (0, utils_1.didProjectOrEnvironmentChange)(location, nextProps.location) ||
            isProjectStabilized !== nextProps.isProjectStabilized) {
            return true;
        }
        return false;
    }
    componentDidUpdate(prevProps) {
        const { location, isProjectStabilized } = this.props;
        if ((0, utils_1.didProjectOrEnvironmentChange)(prevProps.location, location) ||
            prevProps.isProjectStabilized !== isProjectStabilized) {
            this.remountComponent();
        }
    }
    getEndpoints() {
        const { location, organization, projectSlug, isProjectStabilized } = this.props;
        if (!isProjectStabilized) {
            return [];
        }
        const query = Object.assign(Object.assign({}, (0, pick_1.default)(location.query, Object.values(globalSelectionHeader_1.URL_PARAM))), { per_page: 5 });
        // TODO(project-detail): this does not filter releases for the given time
        return [
            ['releases', `/projects/${organization.slug}/${projectSlug}/releases/`, { query }],
        ];
    }
    /**
     * If our releases are empty, determine if we had a release in the last 90 days (empty message differs then)
     */
    onLoadAllEndpointsSuccess() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { releases } = this.state;
            const { organization, projectId, isProjectStabilized } = this.props;
            if (!isProjectStabilized) {
                return;
            }
            if ((releases !== null && releases !== void 0 ? releases : []).length !== 0 || !projectId) {
                this.setState({ hasOlderReleases: true });
                return;
            }
            this.setState({ loading: true });
            const hasOlderReleases = yield (0, projects_1.fetchAnyReleaseExistence)(this.api, organization.slug, projectId);
            this.setState({ hasOlderReleases, loading: false });
        });
    }
    get releasesLink() {
        const { organization } = this.props;
        // as this is a link to latest releases, we want to only preserve project and environment
        return {
            pathname: `/organizations/${organization.slug}/releases/`,
            query: {
                statsPeriod: undefined,
                start: undefined,
                end: undefined,
                utc: undefined,
            },
        };
    }
    renderInnerBody() {
        const { organization, projectId, isProjectStabilized } = this.props;
        const { loading, releases, hasOlderReleases } = this.state;
        const checkingForOlderReleases = !(releases !== null && releases !== void 0 ? releases : []).length && hasOlderReleases === undefined;
        const showLoadingIndicator = loading || checkingForOlderReleases || !isProjectStabilized;
        if (showLoadingIndicator) {
            return <placeholder_1.default height={PLACEHOLDER_AND_EMPTY_HEIGHT}/>;
        }
        if (!hasOlderReleases) {
            return <missingReleasesButtons_1.default organization={organization} projectId={projectId}/>;
        }
        if (!releases || releases.length === 0) {
            return (<StyledEmptyStateWarning small>{(0, locale_1.t)('No releases found')}</StyledEmptyStateWarning>);
        }
        return <ReleasesTable>{releases.map(this.renderReleaseRow)}</ReleasesTable>;
    }
    renderLoading() {
        return this.renderBody();
    }
    renderBody() {
        return (<styles_2.SidebarSection>
        <styles_2.SectionHeadingWrapper>
          <styles_1.SectionHeading>{(0, locale_1.t)('Latest Releases')}</styles_1.SectionHeading>
          <styles_2.SectionHeadingLink to={this.releasesLink}>
            <icons_1.IconOpen />
          </styles_2.SectionHeadingLink>
        </styles_2.SectionHeadingWrapper>
        <div>{this.renderInnerBody()}</div>
      </styles_2.SidebarSection>);
    }
}
const ReleasesTable = (0, styled_1.default)('div') `
  display: grid;
  font-size: ${p => p.theme.fontSizeMedium};
  white-space: nowrap;
  grid-template-columns: 1fr auto;
  margin-bottom: ${(0, space_1.default)(2)};

  & > * {
    padding: ${(0, space_1.default)(0.5)} ${(0, space_1.default)(1)};
    height: 32px;
  }

  & > *:nth-child(2n + 2) {
    text-align: right;
  }

  & > *:nth-child(4n + 1),
  & > *:nth-child(4n + 2) {
    background-color: ${p => p.theme.rowBackground};
  }
`;
const StyledVersion = (0, styled_1.default)(version_1.default) `
  ${overflowEllipsis_1.default}
  line-height: 1.6;
  font-variant-numeric: tabular-nums;
`;
const StyledEmptyStateWarning = (0, styled_1.default)(emptyStateWarning_1.default) `
  height: ${PLACEHOLDER_AND_EMPTY_HEIGHT};
  justify-content: center;
`;
exports.default = ProjectLatestReleases;
//# sourceMappingURL=projectLatestReleases.jsx.map