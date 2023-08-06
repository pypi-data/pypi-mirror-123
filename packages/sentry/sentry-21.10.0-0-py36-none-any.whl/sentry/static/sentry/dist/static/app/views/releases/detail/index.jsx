Object.defineProperty(exports, "__esModule", { value: true });
exports.ReleasesDetailContainer = exports.ReleaseContext = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const noProjectMessage_1 = (0, tslib_1.__importDefault)(require("app/components/noProjectMessage"));
const globalSelectionHeader_1 = (0, tslib_1.__importDefault)(require("app/components/organizations/globalSelectionHeader"));
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const pickProjectToContinue_1 = (0, tslib_1.__importDefault)(require("app/components/pickProjectToContinue"));
const globalSelectionHeader_2 = require("app/constants/globalSelectionHeader");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const organization_1 = require("app/styles/organization");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const types_1 = require("app/types");
const formatters_1 = require("app/utils/formatters");
const routeTitle_1 = (0, tslib_1.__importDefault)(require("app/utils/routeTitle"));
const sessions_1 = require("app/utils/sessions");
const withGlobalSelection_1 = (0, tslib_1.__importDefault)(require("app/utils/withGlobalSelection"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const utils_1 = require("../utils");
const releaseHeader_1 = (0, tslib_1.__importDefault)(require("./releaseHeader"));
const ReleaseContext = (0, react_1.createContext)({});
exports.ReleaseContext = ReleaseContext;
class ReleasesDetail extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.shouldReload = true;
    }
    getTitle() {
        const { params, organization, selection } = this.props;
        const { release } = this.state;
        // The release details page will always have only one project selected
        const project = release === null || release === void 0 ? void 0 : release.projects.find(p => p.id === selection.projects[0]);
        return (0, routeTitle_1.default)((0, locale_1.t)('Release %s', (0, formatters_1.formatVersion)(params.release)), organization.slug, false, project === null || project === void 0 ? void 0 : project.slug);
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { deploys: [], sessions: null });
    }
    getEndpoints() {
        var _a;
        const { organization, location, params, releaseMeta } = this.props;
        const basePath = `/organizations/${organization.slug}/releases/${encodeURIComponent(params.release)}/`;
        const endpoints = [
            [
                'release',
                basePath,
                {
                    query: Object.assign({ adoptionStages: 1 }, (0, getParams_1.getParams)((0, pick_1.default)(location.query, [...Object.values(globalSelectionHeader_2.URL_PARAM)]))),
                },
            ],
        ];
        if (releaseMeta.deployCount > 0) {
            endpoints.push(['deploys', `${basePath}deploys/`]);
        }
        // Used to figure out if the release has any health data
        endpoints.push([
            'sessions',
            `/organizations/${organization.slug}/sessions/`,
            {
                query: {
                    project: location.query.project,
                    environment: (_a = location.query.environment) !== null && _a !== void 0 ? _a : [],
                    query: `release:"${params.release}"`,
                    field: 'sum(session)',
                    statsPeriod: '90d',
                    interval: '1d',
                },
            },
        ]);
        return endpoints;
    }
    renderError(...args) {
        const possiblyWrongProject = Object.values(this.state.errors).find(e => (e === null || e === void 0 ? void 0 : e.status) === 404 || (e === null || e === void 0 ? void 0 : e.status) === 403);
        if (possiblyWrongProject) {
            return (<organization_1.PageContent>
          <alert_1.default type="error" icon={<icons_1.IconWarning />}>
            {(0, locale_1.t)('This release may not be in your selected project.')}
          </alert_1.default>
        </organization_1.PageContent>);
        }
        return super.renderError(...args);
    }
    renderLoading() {
        return (<organization_1.PageContent>
        <loadingIndicator_1.default />
      </organization_1.PageContent>);
    }
    renderBody() {
        const { organization, location, selection, releaseMeta } = this.props;
        const { release, deploys, sessions, reloading } = this.state;
        const project = release === null || release === void 0 ? void 0 : release.projects.find(p => p.id === selection.projects[0]);
        const releaseBounds = (0, utils_1.getReleaseBounds)(release);
        if (!project || !release) {
            if (reloading) {
                return <loadingIndicator_1.default />;
            }
            return null;
        }
        return (<noProjectMessage_1.default organization={organization}>
        <StyledPageContent>
          <releaseHeader_1.default location={location} organization={organization} release={release} project={project} releaseMeta={releaseMeta} refetchData={this.fetchData}/>
          <ReleaseContext.Provider value={{
                release,
                project,
                deploys,
                releaseMeta,
                refetchData: this.fetchData,
                hasHealthData: (0, sessions_1.getCount)(sessions === null || sessions === void 0 ? void 0 : sessions.groups, types_1.SessionField.SESSIONS) > 0,
                releaseBounds,
            }}>
            {this.props.children}
          </ReleaseContext.Provider>
        </StyledPageContent>
      </noProjectMessage_1.default>);
    }
}
class ReleasesDetailContainer extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.shouldReload = true;
    }
    getEndpoints() {
        const { organization, params } = this.props;
        // fetch projects this release belongs to
        return [
            [
                'releaseMeta',
                `/organizations/${organization.slug}/releases/${encodeURIComponent(params.release)}/meta/`,
            ],
        ];
    }
    componentDidMount() {
        this.removeGlobalDateTimeFromUrl();
    }
    componentDidUpdate(prevProps, prevContext) {
        super.componentDidUpdate(prevProps, prevContext);
        this.removeGlobalDateTimeFromUrl();
    }
    removeGlobalDateTimeFromUrl() {
        const { router, location } = this.props;
        const _a = location.query, { start, end, statsPeriod, utc } = _a, restQuery = (0, tslib_1.__rest)(_a, ["start", "end", "statsPeriod", "utc"]);
        if (start || end || statsPeriod || utc) {
            router.replace(Object.assign(Object.assign({}, location), { query: restQuery }));
        }
    }
    renderError(...args) {
        const has404Errors = Object.values(this.state.errors).find(e => (e === null || e === void 0 ? void 0 : e.status) === 404);
        if (has404Errors) {
            // This catches a 404 coming from the release endpoint and displays a custom error message.
            return (<organization_1.PageContent>
          <alert_1.default type="error" icon={<icons_1.IconWarning />}>
            {(0, locale_1.t)('This release could not be found.')}
          </alert_1.default>
        </organization_1.PageContent>);
        }
        return super.renderError(...args);
    }
    isProjectMissingInUrl() {
        const projectId = this.props.location.query.project;
        return !projectId || typeof projectId !== 'string';
    }
    renderLoading() {
        return (<organization_1.PageContent>
        <loadingIndicator_1.default />
      </organization_1.PageContent>);
    }
    renderProjectsFooterMessage() {
        return (<ProjectsFooterMessage>
        <icons_1.IconInfo size="xs"/> {(0, locale_1.t)('Only projects with this release are visible.')}
      </ProjectsFooterMessage>);
    }
    renderBody() {
        const { organization, params, router } = this.props;
        const { releaseMeta } = this.state;
        if (!releaseMeta) {
            return null;
        }
        const { projects } = releaseMeta;
        if (this.isProjectMissingInUrl()) {
            return (<pickProjectToContinue_1.default projects={projects.map(({ id, slug }) => ({
                    id: String(id),
                    slug,
                }))} router={router} nextPath={{
                    pathname: `/organizations/${organization.slug}/releases/${encodeURIComponent(params.release)}/`,
                }} noProjectRedirectPath={`/organizations/${organization.slug}/releases/`}/>);
        }
        return (<globalSelectionHeader_1.default lockedMessageSubject={(0, locale_1.t)('release')} shouldForceProject={projects.length === 1} forceProject={projects.length === 1 ? Object.assign(Object.assign({}, projects[0]), { id: String(projects[0].id) }) : undefined} specificProjectSlugs={projects.map(p => p.slug)} disableMultipleProjectSelection showProjectSettingsLink projectsFooterMessage={this.renderProjectsFooterMessage()} showDateSelector={false}>
        <ReleasesDetail {...this.props} releaseMeta={releaseMeta}/>
      </globalSelectionHeader_1.default>);
    }
}
exports.ReleasesDetailContainer = ReleasesDetailContainer;
const StyledPageContent = (0, styled_1.default)(organization_1.PageContent) `
  padding: 0;
`;
const ProjectsFooterMessage = (0, styled_1.default)('div') `
  display: grid;
  align-items: center;
  grid-template-columns: min-content 1fr;
  grid-gap: ${(0, space_1.default)(1)};
`;
exports.default = (0, withGlobalSelection_1.default)((0, withOrganization_1.default)(ReleasesDetailContainer));
//# sourceMappingURL=index.jsx.map