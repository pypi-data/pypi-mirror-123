Object.defineProperty(exports, "__esModule", { value: true });
exports.OrganizationCrumb = void 0;
const tslib_1 = require("tslib");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const idBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge"));
const recreateRoute_1 = (0, tslib_1.__importDefault)(require("app/utils/recreateRoute"));
const withLatestContext_1 = (0, tslib_1.__importDefault)(require("app/utils/withLatestContext"));
const breadcrumbDropdown_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsBreadcrumb/breadcrumbDropdown"));
const findFirstRouteWithoutRouteParam_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsBreadcrumb/findFirstRouteWithoutRouteParam"));
const menuItem_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsBreadcrumb/menuItem"));
const _1 = require(".");
const OrganizationCrumb = (_a) => {
    var { organization, organizations, params, routes, route } = _a, props = (0, tslib_1.__rest)(_a, ["organization", "organizations", "params", "routes", "route"]);
    const handleSelect = (item) => {
        // If we are currently in a project context, and we're attempting to switch organizations,
        // then we need to default to index route (e.g. `route`)
        //
        // Otherwise, find the last route without a router param
        // e.g. if you are on API details, we want the API listing
        // This fails if our route tree is not nested
        const hasProjectParam = !!params.projectId;
        let destination = hasProjectParam
            ? route
            : (0, findFirstRouteWithoutRouteParam_1.default)(routes.slice(routes.indexOf(route)));
        // It's possible there is no route without route params (e.g. organization settings index),
        // in which case, we can use the org settings index route (e.g. `route`)
        if (!hasProjectParam && typeof destination === 'undefined') {
            destination = route;
        }
        if (destination === undefined) {
            return;
        }
        react_router_1.browserHistory.push((0, recreateRoute_1.default)(destination, {
            routes,
            params: Object.assign(Object.assign({}, params), { orgId: item.value }),
        }));
    };
    if (!organization) {
        return null;
    }
    const hasMenu = organizations.length > 1;
    return (<breadcrumbDropdown_1.default name={<_1.CrumbLink to={(0, recreateRoute_1.default)(route, {
                routes,
                params: Object.assign(Object.assign({}, params), { orgId: organization.slug }),
            })}>
          <BadgeWrapper>
            <idBadge_1.default avatarSize={18} organization={organization}/>
          </BadgeWrapper>
        </_1.CrumbLink>} onSelect={handleSelect} hasMenu={hasMenu} route={route} items={organizations.map((org, index) => ({
            index,
            value: org.slug,
            label: (<menuItem_1.default>
            <idBadge_1.default organization={org}/>
          </menuItem_1.default>),
        }))} {...props}/>);
};
exports.OrganizationCrumb = OrganizationCrumb;
const BadgeWrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
`;
exports.default = (0, withLatestContext_1.default)(OrganizationCrumb);
//# sourceMappingURL=organizationCrumb.jsx.map