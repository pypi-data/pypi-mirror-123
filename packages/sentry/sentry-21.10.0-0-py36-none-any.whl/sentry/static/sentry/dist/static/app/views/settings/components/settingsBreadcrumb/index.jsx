Object.defineProperty(exports, "__esModule", { value: true });
exports.CrumbLink = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const settingsBreadcrumbActions_1 = (0, tslib_1.__importDefault)(require("app/actions/settingsBreadcrumbActions"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const settingsBreadcrumbStore_1 = (0, tslib_1.__importDefault)(require("app/stores/settingsBreadcrumbStore"));
const getRouteStringFromRoutes_1 = (0, tslib_1.__importDefault)(require("app/utils/getRouteStringFromRoutes"));
const recreateRoute_1 = (0, tslib_1.__importDefault)(require("app/utils/recreateRoute"));
const crumb_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsBreadcrumb/crumb"));
const divider_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsBreadcrumb/divider"));
const organizationCrumb_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsBreadcrumb/organizationCrumb"));
const projectCrumb_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsBreadcrumb/projectCrumb"));
const teamCrumb_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsBreadcrumb/teamCrumb"));
const MENUS = {
    Organization: organizationCrumb_1.default,
    Project: projectCrumb_1.default,
    Team: teamCrumb_1.default,
};
class SettingsBreadcrumb extends react_1.Component {
    componentDidUpdate(prevProps) {
        if (this.props.routes === prevProps.routes) {
            return;
        }
        settingsBreadcrumbActions_1.default.trimMappings(this.props.routes);
    }
    render() {
        const { className, routes, params, pathMap } = this.props;
        const lastRouteIndex = routes.map(r => !!r.name).lastIndexOf(true);
        return (<Breadcrumbs className={className}>
        {routes.map((route, i) => {
                if (!route.name) {
                    return null;
                }
                const pathTitle = pathMap[(0, getRouteStringFromRoutes_1.default)(routes.slice(0, i + 1))];
                const isLast = i === lastRouteIndex;
                const createMenu = MENUS[route.name];
                const Menu = typeof createMenu === 'function' && createMenu;
                const hasMenu = !!Menu;
                const CrumbPicker = hasMenu
                    ? Menu
                    : () => (<crumb_1.default>
                  <CrumbLink to={(0, recreateRoute_1.default)(route, { routes, params })}>
                    {pathTitle || route.name}{' '}
                  </CrumbLink>
                  <divider_1.default isLast={isLast}/>
                </crumb_1.default>);
                return (<CrumbPicker key={`${route.name}:${route.path}`} routes={routes} params={params} route={route} isLast={isLast}/>);
            })}
      </Breadcrumbs>);
    }
}
SettingsBreadcrumb.defaultProps = {
    pathMap: {},
};
class ConnectedSettingsBreadcrumb extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = { pathMap: settingsBreadcrumbStore_1.default.getPathMap() };
        this.unsubscribe = settingsBreadcrumbStore_1.default.listen((pathMap) => this.setState({ pathMap }), undefined);
    }
    componentWillUnmount() {
        this.unsubscribe();
    }
    render() {
        return <SettingsBreadcrumb {...this.props} {...this.state}/>;
    }
}
exports.default = ConnectedSettingsBreadcrumb;
const CrumbLink = (0, styled_1.default)(link_1.default) `
  display: block;

  &.focus-visible {
    outline: none;
    box-shadow: ${p => p.theme.blue300} 0 2px 0;
  }

  color: ${p => p.theme.subText};
  &:hover {
    color: ${p => p.theme.textColor};
  }
`;
exports.CrumbLink = CrumbLink;
const Breadcrumbs = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
`;
//# sourceMappingURL=index.jsx.map