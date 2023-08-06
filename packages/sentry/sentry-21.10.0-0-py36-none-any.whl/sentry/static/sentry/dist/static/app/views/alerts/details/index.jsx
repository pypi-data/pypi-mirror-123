Object.defineProperty(exports, "__esModule", { value: true });
exports.alertDetailsLink = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const analytics_1 = require("app/utils/analytics");
const useApi_1 = (0, tslib_1.__importDefault)(require("app/utils/useApi"));
const types_1 = require("../types");
const utils_1 = require("../utils");
const alertDetailsLink = (organization, incident) => `/organizations/${organization.slug}/alerts/rules/details/${incident.alertRule.status === types_1.AlertRuleStatus.SNAPSHOT &&
    incident.alertRule.originalAlertRuleId
    ? incident.alertRule.originalAlertRuleId
    : incident.alertRule.id}/`;
exports.alertDetailsLink = alertDetailsLink;
function IncidentDetails({ organization, params }) {
    const api = (0, useApi_1.default)();
    const [hasError, setHasError] = (0, react_1.useState)(false);
    const track = () => {
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey: 'alert_details.viewed',
            eventName: 'Alert Details: Viewed',
            organization_id: parseInt(organization.id, 10),
            alert_id: parseInt(params.alertId, 10),
        });
    };
    const fetchData = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        setHasError(false);
        try {
            const incident = yield (0, utils_1.fetchIncident)(api, params.orgId, params.alertId);
            react_router_1.browserHistory.replace({
                pathname: (0, exports.alertDetailsLink)(organization, incident),
                query: { alert: incident.identifier },
            });
        }
        catch (err) {
            setHasError(true);
        }
    });
    (0, react_1.useEffect)(() => {
        fetchData();
        track();
    }, []);
    if (hasError) {
        return <loadingError_1.default onRetry={fetchData}/>;
    }
    return <loadingIndicator_1.default />;
}
exports.default = IncidentDetails;
//# sourceMappingURL=index.jsx.map