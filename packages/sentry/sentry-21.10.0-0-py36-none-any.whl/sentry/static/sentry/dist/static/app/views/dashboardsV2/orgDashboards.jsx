Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const notFound_1 = (0, tslib_1.__importDefault)(require("app/components/errors/notFound"));
const sentryDocumentTitle_1 = (0, tslib_1.__importDefault)(require("app/components/sentryDocumentTitle"));
const locale_1 = require("app/locale");
const analytics_1 = require("app/utils/analytics");
class OrgDashboards extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.state = {
            // AsyncComponent state
            loading: true,
            reloading: false,
            error: false,
            errors: {},
            dashboards: [],
            selectedDashboard: null,
        };
    }
    componentDidUpdate(prevProps) {
        if (!(0, isEqual_1.default)(prevProps.params.dashboardId, this.props.params.dashboardId)) {
            this.remountComponent();
        }
    }
    getEndpoints() {
        const { organization, params } = this.props;
        const url = `/organizations/${organization.slug}/dashboards/`;
        const endpoints = [['dashboards', url]];
        if (params.dashboardId) {
            endpoints.push(['selectedDashboard', `${url}${params.dashboardId}/`]);
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'dashboards2.view',
                eventName: 'Dashboards2: View dashboard',
                organization_id: parseInt(this.props.organization.id, 10),
                dashboard_id: parseInt(params.dashboardId, 10),
            });
        }
        return endpoints;
    }
    getDashboards() {
        const { dashboards } = this.state;
        return Array.isArray(dashboards) ? dashboards : [];
    }
    onRequestSuccess({ stateKey, data }) {
        const { params, organization, location } = this.props;
        if (params.dashboardId || stateKey === 'selectedDashboard') {
            return;
        }
        // If we don't have a selected dashboard, and one isn't going to arrive
        // we can redirect to the first dashboard in the list.
        const dashboardId = data.length ? data[0].id : 'default-overview';
        const url = `/organizations/${organization.slug}/dashboard/${dashboardId}/`;
        react_router_1.browserHistory.replace({
            pathname: url,
            query: Object.assign({}, location.query),
        });
    }
    renderBody() {
        const { children } = this.props;
        const { selectedDashboard, error } = this.state;
        return children({
            error,
            dashboard: selectedDashboard,
            dashboards: this.getDashboards(),
            reloadData: this.reloadData.bind(this),
        });
    }
    renderError(error) {
        const notFound = Object.values(this.state.errors).find(resp => resp && resp.status === 404);
        if (notFound) {
            return <notFound_1.default />;
        }
        return super.renderError(error, true, true);
    }
    renderComponent() {
        const { organization, location } = this.props;
        if (!organization.features.includes('dashboards-basic')) {
            // Redirect to Dashboards v1
            react_router_1.browserHistory.replace({
                pathname: `/organizations/${organization.slug}/dashboards/`,
                query: Object.assign({}, location.query),
            });
            return null;
        }
        return (<sentryDocumentTitle_1.default title={(0, locale_1.t)('Dashboards')} orgSlug={organization.slug}>
        {super.renderComponent()}
      </sentryDocumentTitle_1.default>);
    }
}
exports.default = OrgDashboards;
//# sourceMappingURL=orgDashboards.jsx.map