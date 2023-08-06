Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const breadcrumbs_1 = (0, tslib_1.__importDefault)(require("app/components/breadcrumbs"));
const idBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const isActiveSuperuser_1 = require("app/utils/isActiveSuperuser");
const recreateRoute_1 = (0, tslib_1.__importDefault)(require("app/utils/recreateRoute"));
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
const menuItem_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsBreadcrumb/menuItem"));
function BuilderBreadCrumbs(props) {
    const { orgSlug, title, alertName, projectSlug, projects, routes, canChangeProject, location, } = props;
    const project = projects.find(({ slug }) => projectSlug === slug);
    const isSuperuser = (0, isActiveSuperuser_1.isActiveSuperuser)();
    const projectCrumbLink = {
        to: `/organizations/${orgSlug}/alerts/rules/?project=${project === null || project === void 0 ? void 0 : project.id}`,
        label: <idBadge_1.default project={project} avatarSize={18} disableLink/>,
        preserveGlobalSelection: true,
    };
    const projectCrumbDropdown = {
        onSelect: ({ value }) => {
            react_router_1.browserHistory.push((0, recreateRoute_1.default)('', {
                routes,
                params: { orgId: orgSlug, projectId: value },
                location,
            }));
        },
        label: <idBadge_1.default project={project} avatarSize={18} disableLink/>,
        items: projects
            .filter(proj => proj.isMember || isSuperuser)
            .map((proj, index) => ({
            index,
            value: proj.slug,
            label: (<menuItem_1.default>
            <idBadge_1.default project={proj} avatarProps={{ consistentWidth: true }} avatarSize={18} disableLink/>
          </menuItem_1.default>),
            searchKey: proj.slug,
        })),
    };
    const projectCrumb = canChangeProject ? projectCrumbDropdown : projectCrumbLink;
    const crumbs = [
        {
            to: `/organizations/${orgSlug}/alerts/rules/`,
            label: (0, locale_1.t)('Alerts'),
            preserveGlobalSelection: true,
        },
        projectCrumb,
        Object.assign({ label: title }, (alertName
            ? {
                to: `/organizations/${orgSlug}/alerts/${projectSlug}/wizard`,
                preserveGlobalSelection: true,
            }
            : {})),
    ];
    if (alertName) {
        crumbs.push({ label: alertName });
    }
    return <StyledBreadcrumbs crumbs={crumbs}/>;
}
const StyledBreadcrumbs = (0, styled_1.default)(breadcrumbs_1.default) `
  font-size: 18px;
  margin-bottom: ${(0, space_1.default)(3)};
`;
exports.default = (0, withProjects_1.default)(BuilderBreadCrumbs);
//# sourceMappingURL=builderBreadCrumbs.jsx.map