Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const locale_1 = require("app/locale");
const organization_1 = require("app/styles/organization");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const data_1 = require("./data");
const detail_1 = (0, tslib_1.__importDefault)(require("./detail"));
const types_1 = require("./types");
const utils_1 = require("./utils");
function CreateDashboard(props) {
    const { organization, location } = props;
    const [newWidget, setNewWidget] = (0, react_1.useState)();
    function renderDisabled() {
        return (<organization_1.PageContent>
        <alert_1.default type="warning">{(0, locale_1.t)("You don't have access to this feature")}</alert_1.default>
      </organization_1.PageContent>);
    }
    const dashboard = (0, utils_1.cloneDashboard)(data_1.EMPTY_DASHBOARD);
    (0, react_1.useEffect)(() => {
        const constructedWidget = (0, utils_1.constructWidgetFromQuery)(location.query);
        setNewWidget(constructedWidget);
        if (constructedWidget) {
            react_router_1.browserHistory.replace(location.pathname);
        }
    }, [organization.slug]);
    return (<feature_1.default features={['dashboards-edit']} organization={props.organization} renderDisabled={renderDisabled}>
      <detail_1.default {...props} initialState={types_1.DashboardState.CREATE} dashboard={dashboard} dashboards={[]} newWidget={newWidget}/>
    </feature_1.default>);
}
exports.default = (0, withOrganization_1.default)(CreateDashboard);
//# sourceMappingURL=create.jsx.map