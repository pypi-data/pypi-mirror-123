Object.defineProperty(exports, "__esModule", { value: true });
exports.DashboardBasicFeature = void 0;
const tslib_1 = require("tslib");
const react_1 = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const dashboards_1 = require("app/actionCreators/dashboards");
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const notFound_1 = (0, tslib_1.__importDefault)(require("app/components/errors/notFound"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const locale_1 = require("app/locale");
const organization_1 = require("app/styles/organization");
const useApi_1 = (0, tslib_1.__importDefault)(require("app/utils/useApi"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const detail_1 = (0, tslib_1.__importDefault)(require("./detail"));
const orgDashboards_1 = (0, tslib_1.__importDefault)(require("./orgDashboards"));
const types_1 = require("./types");
const utils_1 = require("./utils");
function ViewEditDashboard(props) {
    const api = (0, useApi_1.default)();
    const { organization, params, location } = props;
    const dashboardId = params.dashboardId;
    const orgSlug = organization.slug;
    const [newWidget, setNewWidget] = (0, react_1.useState)();
    (0, react_1.useEffect)(() => {
        if (dashboardId && dashboardId !== 'default-overview') {
            (0, dashboards_1.updateDashboardVisit)(api, orgSlug, dashboardId);
        }
        const constructedWidget = (0, utils_1.constructWidgetFromQuery)(location.query);
        setNewWidget(constructedWidget);
        // Clean up url after constructing widget from query string
        if (constructedWidget) {
            react_router_1.browserHistory.replace(location.pathname);
        }
    }, [api, orgSlug, dashboardId]);
    return (<exports.DashboardBasicFeature organization={organization}>
      <orgDashboards_1.default api={api} location={location} params={params} organization={organization}>
        {({ dashboard, dashboards, error, reloadData }) => {
            return error ? (<notFound_1.default />) : dashboard ? (<detail_1.default {...props} initialState={newWidget ? types_1.DashboardState.EDIT : types_1.DashboardState.VIEW} dashboard={dashboard} dashboards={dashboards} reloadData={(...args) => {
                    if (newWidget) {
                        setNewWidget(undefined);
                    }
                    return reloadData(...args);
                }} newWidget={newWidget}/>) : (<loadingIndicator_1.default />);
        }}
      </orgDashboards_1.default>
    </exports.DashboardBasicFeature>);
}
exports.default = (0, withOrganization_1.default)(ViewEditDashboard);
const DashboardBasicFeature = ({ organization, children }) => {
    const renderDisabled = () => (<organization_1.PageContent>
      <alert_1.default type="warning">{(0, locale_1.t)("You don't have access to this feature")}</alert_1.default>
    </organization_1.PageContent>);
    return (<feature_1.default hookName="feature-disabled:dashboards-page" features={['organizations:dashboards-basic']} organization={organization} renderDisabled={renderDisabled}>
      {children}
    </feature_1.default>);
};
exports.DashboardBasicFeature = DashboardBasicFeature;
//# sourceMappingURL=view.jsx.map