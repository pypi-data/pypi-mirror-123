Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const partition_1 = (0, tslib_1.__importDefault)(require("lodash/partition"));
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
const globalSelectionHeader_1 = (0, tslib_1.__importDefault)(require("./globalSelectionHeader"));
const initializeGlobalSelectionHeader_1 = (0, tslib_1.__importDefault)(require("./initializeGlobalSelectionHeader"));
function GlobalSelectionHeaderContainer(_a) {
    var { organization, projects, loadingProjects, location, router, routes, defaultSelection, forceProject, shouldForceProject, skipLoadLastUsed, specificProjectSlugs, showAbsolute } = _a, props = (0, tslib_1.__rest)(_a, ["organization", "projects", "loadingProjects", "location", "router", "routes", "defaultSelection", "forceProject", "shouldForceProject", "skipLoadLastUsed", "specificProjectSlugs", "showAbsolute"]);
    const { isSuperuser } = configStore_1.default.get('user');
    const isOrgAdmin = organization.access.includes('org:admin');
    const specifiedProjects = specificProjectSlugs
        ? projects.filter(project => specificProjectSlugs.includes(project.slug))
        : projects;
    const [memberProjects, otherProjects] = (0, partition_1.default)(specifiedProjects, project => project.isMember);
    const nonMemberProjects = isSuperuser || isOrgAdmin ? otherProjects : [];
    const enforceSingleProject = !organization.features.includes('global-views');
    // We can initialize before ProjectsStore is fully loaded if we don't need to enforce single project.
    return (<React.Fragment>
      {(!loadingProjects || (!shouldForceProject && !enforceSingleProject)) && (<initializeGlobalSelectionHeader_1.default location={location} skipLoadLastUsed={!!skipLoadLastUsed} router={router} organization={organization} defaultSelection={defaultSelection} forceProject={forceProject} shouldForceProject={!!shouldForceProject} shouldEnforceSingleProject={enforceSingleProject} memberProjects={memberProjects} showAbsolute={showAbsolute}/>)}
      <globalSelectionHeader_1.default {...props} loadingProjects={loadingProjects} location={location} organization={organization} router={router} routes={routes} projects={projects} shouldForceProject={!!shouldForceProject} defaultSelection={defaultSelection} forceProject={forceProject} memberProjects={memberProjects} nonMemberProjects={nonMemberProjects} showAbsolute={showAbsolute}/>
    </React.Fragment>);
}
exports.default = (0, withOrganization_1.default)((0, withProjects_1.default)((0, react_router_1.withRouter)(GlobalSelectionHeaderContainer)));
//# sourceMappingURL=index.jsx.map