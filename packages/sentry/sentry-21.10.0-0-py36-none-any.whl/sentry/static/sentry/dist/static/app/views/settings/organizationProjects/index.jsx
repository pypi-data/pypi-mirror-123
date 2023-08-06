Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const panels_1 = require("app/components/panels");
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const queryString_1 = require("app/utils/queryString");
const routeTitle_1 = (0, tslib_1.__importDefault)(require("app/utils/routeTitle"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const settingsProjectItem_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsProjectItem"));
const projectStatsGraph_1 = (0, tslib_1.__importDefault)(require("./projectStatsGraph"));
const ITEMS_PER_PAGE = 50;
class OrganizationProjects extends asyncView_1.default {
    getEndpoints() {
        const { orgId } = this.props.params;
        const { location } = this.props;
        const query = (0, queryString_1.decodeScalar)(location.query.query);
        return [
            [
                'projectList',
                `/organizations/${orgId}/projects/`,
                {
                    query: {
                        query,
                        per_page: ITEMS_PER_PAGE,
                    },
                },
            ],
            [
                'projectStats',
                `/organizations/${orgId}/stats/`,
                {
                    query: {
                        since: new Date().getTime() / 1000 - 3600 * 24,
                        stat: 'generated',
                        group: 'project',
                        per_page: ITEMS_PER_PAGE,
                    },
                },
            ],
        ];
    }
    getTitle() {
        const { organization } = this.props;
        return (0, routeTitle_1.default)((0, locale_1.t)('Projects'), organization.slug, false);
    }
    renderLoading() {
        return this.renderBody();
    }
    renderBody() {
        const { projectList, projectListPageLinks, projectStats } = this.state;
        const { organization } = this.props;
        const canCreateProjects = new Set(organization.access).has('project:admin');
        const action = (<button_1.default priority="primary" size="small" disabled={!canCreateProjects} title={!canCreateProjects
                ? (0, locale_1.t)('You do not have permission to create projects')
                : undefined} to={`/organizations/${organization.slug}/projects/new/`} icon={<icons_1.IconAdd size="xs" isCircled/>}>
        {(0, locale_1.t)('Create Project')}
      </button_1.default>);
        return (<React.Fragment>
        <settingsPageHeader_1.default title="Projects" action={action}/>
        <SearchWrapper>
          {this.renderSearchInput({
                updateRoute: true,
                placeholder: (0, locale_1.t)('Search Projects'),
                className: 'search',
            })}
        </SearchWrapper>
        <panels_1.Panel>
          <panels_1.PanelHeader>{(0, locale_1.t)('Projects')}</panels_1.PanelHeader>
          <panels_1.PanelBody>
            {projectList ? ((0, utils_1.sortProjects)(projectList).map(project => (<GridPanelItem key={project.id}>
                  <ProjectListItemWrapper>
                    <settingsProjectItem_1.default project={project} organization={organization}/>
                  </ProjectListItemWrapper>
                  <ProjectStatsGraphWrapper>
                    {projectStats ? (<projectStatsGraph_1.default key={project.id} project={project} stats={projectStats[project.id]}/>) : (<placeholder_1.default height="25px"/>)}
                  </ProjectStatsGraphWrapper>
                </GridPanelItem>))) : (<loadingIndicator_1.default />)}
            {projectList && projectList.length === 0 && (<emptyMessage_1.default>{(0, locale_1.t)('No projects found.')}</emptyMessage_1.default>)}
          </panels_1.PanelBody>
        </panels_1.Panel>
        {projectListPageLinks && (<pagination_1.default pageLinks={projectListPageLinks} {...this.props}/>)}
      </React.Fragment>);
    }
}
exports.default = (0, withOrganization_1.default)(OrganizationProjects);
const SearchWrapper = (0, styled_1.default)('div') `
  margin-bottom: ${(0, space_1.default)(2)};
`;
const GridPanelItem = (0, styled_1.default)(panels_1.PanelItem) `
  display: flex;
  align-items: center;
  padding: 0;
`;
const ProjectListItemWrapper = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(2)};
  flex: 1;
`;
const ProjectStatsGraphWrapper = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(2)};
  width: 25%;
  margin-left: ${(0, space_1.default)(2)};
`;
//# sourceMappingURL=index.jsx.map