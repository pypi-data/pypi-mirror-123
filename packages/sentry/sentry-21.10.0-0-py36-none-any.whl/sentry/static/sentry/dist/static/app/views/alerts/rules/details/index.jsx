Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const members_1 = require("app/actionCreators/members");
const dateTime_1 = (0, tslib_1.__importDefault)(require("app/components/dateTime"));
const locale_1 = require("app/locale");
const analytics_1 = require("app/utils/analytics");
const dates_1 = require("app/utils/dates");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const types_1 = require("app/views/alerts/incidentRules/types");
const row_1 = require("app/views/alerts/list/row");
const utils_1 = require("../../utils");
const body_1 = (0, tslib_1.__importDefault)(require("./body"));
const constants_1 = require("./constants");
const header_1 = (0, tslib_1.__importDefault)(require("./header"));
class AlertRuleDetails extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = { isLoading: false, hasError: false };
        this.fetchData = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, params: { orgId, ruleId }, location, } = this.props;
            this.setState({ isLoading: true, hasError: false });
            if (location.query.alert) {
                yield (0, utils_1.fetchIncident)(api, orgId, location.query.alert)
                    .then(incident => this.setState({ selectedIncident: incident }))
                    .catch(() => this.setState({ selectedIncident: null }));
            }
            else {
                this.setState({ selectedIncident: null });
            }
            try {
                const rule = yield (0, utils_1.fetchAlertRule)(orgId, ruleId);
                this.setState({ rule });
                const timePeriod = this.getTimePeriod();
                const { start, end } = timePeriod;
                const incidents = yield (0, utils_1.fetchIncidentsForRule)(orgId, ruleId, start, end);
                this.setState({ incidents });
                this.setState({ isLoading: false, hasError: false });
            }
            catch (_err) {
                this.setState({ isLoading: false, hasError: true });
            }
        });
        this.handleTimePeriodChange = (value) => {
            react_router_1.browserHistory.push({
                pathname: this.props.location.pathname,
                query: {
                    period: value,
                },
            });
        };
        this.handleZoom = (start, end) => {
            const { location } = this.props;
            react_router_1.browserHistory.push({
                pathname: location.pathname,
                query: {
                    start,
                    end,
                },
            });
        };
    }
    componentDidMount() {
        const { api, params } = this.props;
        (0, members_1.fetchOrgMembers)(api, params.orgId);
        this.fetchData();
        this.trackView();
    }
    componentDidUpdate(prevProps) {
        if (prevProps.location.search !== this.props.location.search ||
            prevProps.params.orgId !== this.props.params.orgId ||
            prevProps.params.ruleId !== this.props.params.ruleId) {
            this.fetchData();
            this.trackView();
        }
    }
    trackView() {
        var _a;
        const { params, organization, location } = this.props;
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey: 'alert_rule_details.viewed',
            eventName: 'Alert Rule Details: Viewed',
            organization_id: organization.id,
            rule_id: parseInt(params.ruleId, 10),
            alert: (_a = location.query.alert) !== null && _a !== void 0 ? _a : '',
        });
    }
    getTimePeriod() {
        var _a, _b;
        const { location } = this.props;
        const { rule } = this.state;
        const defaultPeriod = (rule === null || rule === void 0 ? void 0 : rule.timeWindow) && (rule === null || rule === void 0 ? void 0 : rule.timeWindow) > types_1.TimeWindow.ONE_HOUR
            ? types_1.TimePeriod.SEVEN_DAYS
            : types_1.TimePeriod.ONE_DAY;
        const period = (_a = location.query.period) !== null && _a !== void 0 ? _a : defaultPeriod;
        if (location.query.start && location.query.end) {
            return {
                start: location.query.start,
                end: location.query.end,
                period,
                label: (0, locale_1.t)('Custom time'),
                display: (<react_1.Fragment>
            <dateTime_1.default date={moment_1.default.utc(location.query.start)} timeAndDate/>
            {' — '}
            <dateTime_1.default date={moment_1.default.utc(location.query.end)} timeAndDate/>
          </react_1.Fragment>),
                custom: true,
            };
        }
        if (location.query.alert && this.state.selectedIncident) {
            const { start, end } = (0, row_1.makeRuleDetailsQuery)(this.state.selectedIncident);
            return {
                start,
                end,
                period,
                label: (0, locale_1.t)('Custom time'),
                display: (<react_1.Fragment>
            <dateTime_1.default date={moment_1.default.utc(start)} timeAndDate/>
            {' — '}
            <dateTime_1.default date={moment_1.default.utc(end)} timeAndDate/>
          </react_1.Fragment>),
                custom: true,
            };
        }
        const timeOption = (_b = constants_1.TIME_OPTIONS.find(item => item.value === period)) !== null && _b !== void 0 ? _b : constants_1.TIME_OPTIONS[1];
        const start = (0, dates_1.getUtcDateString)((0, moment_1.default)(moment_1.default.utc().diff(constants_1.TIME_WINDOWS[timeOption.value])));
        const end = (0, dates_1.getUtcDateString)(moment_1.default.utc());
        return {
            start,
            end,
            period,
            label: timeOption.label,
            display: timeOption.label,
        };
    }
    render() {
        const { rule, incidents, hasError, selectedIncident } = this.state;
        const { params } = this.props;
        const timePeriod = this.getTimePeriod();
        return (<react_1.Fragment>
        <header_1.default hasIncidentRuleDetailsError={hasError} params={params} rule={rule}/>
        <body_1.default {...this.props} rule={rule} incidents={incidents} timePeriod={timePeriod} selectedIncident={selectedIncident} handleTimePeriodChange={this.handleTimePeriodChange} handleZoom={this.handleZoom}/>
      </react_1.Fragment>);
    }
}
exports.default = (0, withApi_1.default)(AlertRuleDetails);
//# sourceMappingURL=index.jsx.map