Object.defineProperty(exports, "__esModule", { value: true });
exports.Dashboard = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_lazyload_1 = (0, tslib_1.__importDefault)(require("react-lazyload"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const react_2 = require("@sentry/react");
const flatten_1 = (0, tslib_1.__importDefault)(require("lodash/flatten"));
const uniqBy_1 = (0, tslib_1.__importDefault)(require("lodash/uniqBy"));
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const idBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const noProjectMessage_1 = (0, tslib_1.__importDefault)(require("app/components/noProjectMessage"));
const pageHeading_1 = (0, tslib_1.__importDefault)(require("app/components/pageHeading"));
const sentryDocumentTitle_1 = (0, tslib_1.__importDefault)(require("app/components/sentryDocumentTitle"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const projectsStatsStore_1 = (0, tslib_1.__importDefault)(require("app/stores/projectsStatsStore"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const withTeamsForUser_1 = (0, tslib_1.__importDefault)(require("app/utils/withTeamsForUser"));
const headerTabs_1 = (0, tslib_1.__importDefault)(require("app/views/teamInsights/headerTabs"));
const resources_1 = (0, tslib_1.__importDefault)(require("./resources"));
const teamSection_1 = (0, tslib_1.__importDefault)(require("./teamSection"));
function Dashboard({ teams, params, organization, loadingTeams, error }) {
    (0, react_1.useEffect)(() => {
        return function cleanup() {
            projectsStatsStore_1.default.reset();
        };
    }, []);
    if (loadingTeams) {
        return <loadingIndicator_1.default />;
    }
    if (error) {
        return <loadingError_1.default message={(0, locale_1.t)('An error occurred while fetching your projects')}/>;
    }
    const filteredTeams = teams.filter(team => team.projects.length);
    filteredTeams.sort((team1, team2) => team1.slug.localeCompare(team2.slug));
    const projects = (0, uniqBy_1.default)((0, flatten_1.default)(teams.map(teamObj => teamObj.projects)), 'id');
    const favorites = projects.filter(project => project.isBookmarked);
    const canCreateProjects = organization.access.includes('project:admin');
    const hasTeamAdminAccess = organization.access.includes('team:admin');
    const showEmptyMessage = projects.length === 0 && favorites.length === 0;
    const showResources = projects.length === 1 && !projects[0].firstEvent;
    if (showEmptyMessage) {
        return (<noProjectMessage_1.default organization={organization} superuserNeedsToBeProjectMember/>);
    }
    return (<react_1.Fragment>
      <sentryDocumentTitle_1.default title={(0, locale_1.t)('Projects Dashboard')} orgSlug={organization.slug}/>
      {projects.length > 0 && (<react_1.Fragment>
          <ProjectsHeader>
            <pageHeading_1.default>{(0, locale_1.t)('Projects')}</pageHeading_1.default>
            <button_1.default size="small" disabled={!canCreateProjects} title={!canCreateProjects
                ? (0, locale_1.t)('You do not have permission to create projects')
                : undefined} to={`/organizations/${organization.slug}/projects/new/`} icon={<icons_1.IconAdd size="xs" isCircled/>} data-test-id="create-project">
              {(0, locale_1.t)('Create Project')}
            </button_1.default>
          </ProjectsHeader>
          <feature_1.default organization={organization} features={['team-insights']}>
            <TabsWrapper>
              <headerTabs_1.default organization={organization} activeTab="projects"/>
            </TabsWrapper>
          </feature_1.default>
        </react_1.Fragment>)}

      {filteredTeams.map((team, index) => (<react_lazyload_1.default key={team.slug} once debounce={50} height={300} offset={300}>
          <teamSection_1.default orgId={params.orgId} team={team} showBorder={index !== teams.length - 1} title={hasTeamAdminAccess ? (<TeamLink to={`/settings/${organization.slug}/teams/${team.slug}/`}>
                  <idBadge_1.default team={team} avatarSize={22}/>
                </TeamLink>) : (<idBadge_1.default team={team} avatarSize={22}/>)} projects={(0, utils_1.sortProjects)(team.projects)} access={new Set(organization.access)}/>
        </react_lazyload_1.default>))}
      {showResources && <resources_1.default organization={organization}/>}
    </react_1.Fragment>);
}
exports.Dashboard = Dashboard;
const OrganizationDashboard = (props) => (<OrganizationDashboardWrapper>
    <Dashboard {...props}/>
  </OrganizationDashboardWrapper>);
const TeamLink = (0, styled_1.default)(link_1.default) `
  display: flex;
  align-items: center;
`;
const ProjectsHeader = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(3)} ${(0, space_1.default)(4)} 0 ${(0, space_1.default)(4)};
  display: flex;
  align-items: center;
  justify-content: space-between;
`;
const TabsWrapper = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(2)} ${(0, space_1.default)(4)} ${(0, space_1.default)(1)} ${(0, space_1.default)(4)};
`;
const OrganizationDashboardWrapper = (0, styled_1.default)('div') `
  display: flex;
  flex: 1;
  flex-direction: column;
`;
exports.default = (0, withApi_1.default)((0, withOrganization_1.default)((0, withTeamsForUser_1.default)((0, react_2.withProfiler)(OrganizationDashboard))));
//# sourceMappingURL=index.jsx.map