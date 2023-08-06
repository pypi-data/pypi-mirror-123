Object.defineProperty(exports, "__esModule", { value: true });
exports.ProjectCrumb = void 0;
const tslib_1 = require("tslib");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const idBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const recreateRoute_1 = (0, tslib_1.__importDefault)(require("app/utils/recreateRoute"));
const replaceRouterParams_1 = (0, tslib_1.__importDefault)(require("app/utils/replaceRouterParams"));
const withLatestContext_1 = (0, tslib_1.__importDefault)(require("app/utils/withLatestContext"));
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
const breadcrumbDropdown_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsBreadcrumb/breadcrumbDropdown"));
const findFirstRouteWithoutRouteParam_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsBreadcrumb/findFirstRouteWithoutRouteParam"));
const menuItem_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsBreadcrumb/menuItem"));
const _1 = require(".");
const ProjectCrumb = (_a) => {
    var { organization: latestOrganization, project: latestProject, projects, params, routes, route } = _a, props = (0, tslib_1.__rest)(_a, ["organization", "project", "projects", "params", "routes", "route"]);
    const handleSelect = (item) => {
        // We have to make exceptions for routes like "Project Alerts Rule Edit" or "Client Key Details"
        // Since these models are project specific, we need to traverse up a route when switching projects
        //
        // we manipulate `routes` so that it doesn't include the current project's route
        // which, unlike the org version, does not start with a route param
        const returnTo = (0, findFirstRouteWithoutRouteParam_1.default)(routes.slice(routes.indexOf(route) + 1), route);
        if (returnTo === undefined) {
            return;
        }
        react_router_1.browserHistory.push((0, recreateRoute_1.default)(returnTo, { routes, params: Object.assign(Object.assign({}, params), { projectId: item.value }) }));
    };
    if (!latestOrganization) {
        return null;
    }
    if (!projects) {
        return null;
    }
    const hasMenu = projects && projects.length > 1;
    return (<breadcrumbDropdown_1.default hasMenu={hasMenu} route={route} name={<ProjectName>
          {!latestProject ? (<loadingIndicator_1.default mini/>) : (<_1.CrumbLink to={(0, replaceRouterParams_1.default)('/settings/:orgId/projects/:projectId/', {
                    orgId: latestOrganization.slug,
                    projectId: latestProject.slug,
                })}>
              <idBadge_1.default project={latestProject} avatarSize={18} disableLink/>
            </_1.CrumbLink>)}
        </ProjectName>} onSelect={handleSelect} items={projects.map((project, index) => ({
            index,
            value: project.slug,
            label: (<menuItem_1.default>
            <idBadge_1.default project={project} avatarProps={{ consistentWidth: true }} avatarSize={18} disableLink/>
          </menuItem_1.default>),
        }))} {...props}/>);
};
exports.ProjectCrumb = ProjectCrumb;
exports.default = (0, withProjects_1.default)((0, withLatestContext_1.default)(ProjectCrumb));
// Set height of crumb because of spinner
const SPINNER_SIZE = '24px';
const ProjectName = (0, styled_1.default)('div') `
  display: flex;

  .loading {
    width: ${SPINNER_SIZE};
    height: ${SPINNER_SIZE};
    margin: 0 ${(0, space_1.default)(0.25)} 0 0;
  }
`;
//# sourceMappingURL=projectCrumb.jsx.map