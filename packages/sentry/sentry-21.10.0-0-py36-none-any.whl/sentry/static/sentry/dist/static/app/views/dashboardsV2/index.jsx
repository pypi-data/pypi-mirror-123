Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const notFound_1 = (0, tslib_1.__importDefault)(require("app/components/errors/notFound"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const detail_1 = (0, tslib_1.__importDefault)(require("./detail"));
const orgDashboards_1 = (0, tslib_1.__importDefault)(require("./orgDashboards"));
const types_1 = require("./types");
const view_1 = require("./view");
function DashboardsV2Container(props) {
    const { organization, params, api, location, children } = props;
    if (organization.features.includes('dashboards-edit')) {
        return <react_1.Fragment>{children}</react_1.Fragment>;
    }
    return (<view_1.DashboardBasicFeature organization={organization}>
      <orgDashboards_1.default api={api} location={location} params={params} organization={organization}>
        {({ dashboard, dashboards, error, reloadData }) => {
            return error ? (<notFound_1.default />) : dashboard ? (<detail_1.default {...props} initialState={types_1.DashboardState.VIEW} dashboard={dashboard} dashboards={dashboards} reloadData={reloadData}/>) : (<loadingIndicator_1.default />);
        }}
      </orgDashboards_1.default>
    </view_1.DashboardBasicFeature>);
}
exports.default = (0, withApi_1.default)((0, withOrganization_1.default)(DashboardsV2Container));
//# sourceMappingURL=index.jsx.map