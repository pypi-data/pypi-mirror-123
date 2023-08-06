Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const omit_1 = (0, tslib_1.__importDefault)(require("lodash/omit"));
const indicator_1 = require("app/actionCreators/indicator");
const utils_1 = require("app/components/charts/utils");
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const locale_1 = require("app/locale");
const types_1 = require("app/types");
const utils_2 = require("app/utils");
const getPeriod_1 = require("app/utils/getPeriod");
const sessions_1 = require("app/utils/sessions");
const utils_3 = require("app/views/releases/utils");
const projectCharts_1 = require("../projectCharts");
const utils_4 = require("../utils");
const omitIgnoredProps = (props) => (0, omit_1.default)(props, ['api', 'organization', 'children', 'selection.datetime.utc']);
class ProjectSessionsChartRequest extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            reloading: false,
            errored: false,
            timeseriesData: null,
            previousTimeseriesData: null,
            totalSessions: null,
        };
        this.unmounting = false;
        this.fetchData = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, selection, onTotalValuesChange, displayMode, disablePrevious } = this.props;
            const shouldFetchWithPrevious = !disablePrevious && (0, utils_4.shouldFetchPreviousPeriod)(selection.datetime);
            this.setState(state => ({
                reloading: state.timeseriesData !== null,
                errored: false,
            }));
            try {
                const response = yield api.requestPromise(this.path, {
                    query: this.queryParams({ shouldFetchWithPrevious }),
                });
                const { timeseriesData, previousTimeseriesData, totalSessions } = displayMode === projectCharts_1.DisplayModes.SESSIONS
                    ? this.transformSessionCountData(response)
                    : this.transformData(response, { fetchedWithPrevious: shouldFetchWithPrevious });
                if (this.unmounting) {
                    return;
                }
                this.setState({
                    reloading: false,
                    timeseriesData,
                    previousTimeseriesData,
                    totalSessions,
                });
                onTotalValuesChange(totalSessions);
            }
            catch (_a) {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Error loading chart data'));
                this.setState({
                    errored: true,
                    reloading: false,
                    timeseriesData: null,
                    previousTimeseriesData: null,
                    totalSessions: null,
                });
            }
        });
    }
    componentDidMount() {
        this.fetchData();
    }
    componentDidUpdate(prevProps) {
        if (!(0, isEqual_1.default)(omitIgnoredProps(this.props), omitIgnoredProps(prevProps))) {
            this.fetchData();
        }
    }
    componentWillUnmount() {
        this.unmounting = true;
    }
    get path() {
        const { organization } = this.props;
        return `/organizations/${organization.slug}/sessions/`;
    }
    queryParams({ shouldFetchWithPrevious = false }) {
        const { selection, query } = this.props;
        const { datetime, projects, environments: environment } = selection;
        const baseParams = {
            field: 'sum(session)',
            groupBy: 'session.status',
            interval: (0, utils_1.getSeriesApiInterval)(datetime),
            project: projects[0],
            environment,
            query,
        };
        if (!shouldFetchWithPrevious) {
            return Object.assign(Object.assign({}, baseParams), (0, getParams_1.getParams)(datetime));
        }
        const { period } = selection.datetime;
        const doubledPeriod = (0, getPeriod_1.getPeriod)({ period, start: undefined, end: undefined }, { shouldDoublePeriod: true }).statsPeriod;
        return Object.assign(Object.assign({}, baseParams), { statsPeriod: doubledPeriod });
    }
    transformData(responseData, { fetchedWithPrevious = false }) {
        const { theme } = this.props;
        // Take the floor just in case, but data should always be divisible by 2
        const dataMiddleIndex = Math.floor(responseData.intervals.length / 2);
        // calculate the total number of sessions for this period (exclude previous if there)
        const totalSessions = responseData.groups.reduce((acc, group) => acc +
            group.series['sum(session)']
                .slice(fetchedWithPrevious ? dataMiddleIndex : 0)
                .reduce((value, groupAcc) => groupAcc + value, 0), 0);
        const previousPeriodTotalSessions = fetchedWithPrevious
            ? responseData.groups.reduce((acc, group) => acc +
                group.series['sum(session)']
                    .slice(0, dataMiddleIndex)
                    .reduce((value, groupAcc) => groupAcc + value, 0), 0)
            : 0;
        // TODO(project-details): refactor this to avoid duplication as we add more session charts
        const timeseriesData = [
            {
                seriesName: (0, locale_1.t)('This Period'),
                color: theme.green300,
                data: responseData.intervals
                    .slice(fetchedWithPrevious ? dataMiddleIndex : 0)
                    .map((interval, i) => {
                    var _a, _b;
                    const totalIntervalSessions = responseData.groups.reduce((acc, group) => acc +
                        group.series['sum(session)'].slice(fetchedWithPrevious ? dataMiddleIndex : 0)[i], 0);
                    const intervalCrashedSessions = (_b = (_a = responseData.groups
                        .find(group => group.by['session.status'] === 'crashed')) === null || _a === void 0 ? void 0 : _a.series['sum(session)'].slice(fetchedWithPrevious ? dataMiddleIndex : 0)[i]) !== null && _b !== void 0 ? _b : 0;
                    const crashedSessionsPercent = (0, utils_2.percent)(intervalCrashedSessions, totalIntervalSessions);
                    return {
                        name: interval,
                        value: totalSessions === 0 && previousPeriodTotalSessions === 0
                            ? 0
                            : totalIntervalSessions === 0
                                ? null
                                : (0, utils_3.getCrashFreePercent)(100 - crashedSessionsPercent),
                    };
                }),
            },
        ]; // TODO(project-detail): Change SeriesDataUnit value to support null
        const previousTimeseriesData = fetchedWithPrevious
            ? {
                seriesName: (0, locale_1.t)('Previous Period'),
                data: responseData.intervals.slice(0, dataMiddleIndex).map((_interval, i) => {
                    var _a, _b;
                    const totalIntervalSessions = responseData.groups.reduce((acc, group) => acc + group.series['sum(session)'].slice(0, dataMiddleIndex)[i], 0);
                    const intervalCrashedSessions = (_b = (_a = responseData.groups
                        .find(group => group.by['session.status'] === 'crashed')) === null || _a === void 0 ? void 0 : _a.series['sum(session)'].slice(0, dataMiddleIndex)[i]) !== null && _b !== void 0 ? _b : 0;
                    const crashedSessionsPercent = (0, utils_2.percent)(intervalCrashedSessions, totalIntervalSessions);
                    return {
                        name: responseData.intervals[i + dataMiddleIndex],
                        value: totalSessions === 0 && previousPeriodTotalSessions === 0
                            ? 0
                            : totalIntervalSessions === 0
                                ? null
                                : (0, utils_3.getCrashFreePercent)(100 - crashedSessionsPercent),
                    };
                }),
            } // TODO(project-detail): Change SeriesDataUnit value to support null
            : null;
        return {
            totalSessions,
            timeseriesData,
            previousTimeseriesData,
        };
    }
    transformSessionCountData(responseData) {
        const { theme } = this.props;
        const sessionsChart = (0, sessions_1.initSessionsChart)(theme);
        const { intervals, groups } = responseData;
        const totalSessions = (0, sessions_1.getCount)(responseData.groups, types_1.SessionField.SESSIONS);
        const chartData = [
            Object.assign(Object.assign({}, sessionsChart[types_1.SessionStatus.HEALTHY]), { data: (0, sessions_1.getCountSeries)(types_1.SessionField.SESSIONS, groups.find(g => g.by['session.status'] === types_1.SessionStatus.HEALTHY), intervals) }),
            Object.assign(Object.assign({}, sessionsChart[types_1.SessionStatus.ERRORED]), { data: (0, sessions_1.getCountSeries)(types_1.SessionField.SESSIONS, groups.find(g => g.by['session.status'] === types_1.SessionStatus.ERRORED), intervals) }),
            Object.assign(Object.assign({}, sessionsChart[types_1.SessionStatus.ABNORMAL]), { data: (0, sessions_1.getCountSeries)(types_1.SessionField.SESSIONS, groups.find(g => g.by['session.status'] === types_1.SessionStatus.ABNORMAL), intervals) }),
            Object.assign(Object.assign({}, sessionsChart[types_1.SessionStatus.CRASHED]), { data: (0, sessions_1.getCountSeries)(types_1.SessionField.SESSIONS, groups.find(g => g.by['session.status'] === types_1.SessionStatus.CRASHED), intervals) }),
        ];
        return {
            timeseriesData: chartData,
            previousTimeseriesData: null,
            totalSessions,
        };
    }
    render() {
        const { children } = this.props;
        const { timeseriesData, reloading, errored, totalSessions, previousTimeseriesData } = this.state;
        const loading = timeseriesData === null;
        return children({
            loading,
            reloading,
            errored,
            totalSessions,
            previousTimeseriesData,
            timeseriesData: timeseriesData !== null && timeseriesData !== void 0 ? timeseriesData : [],
        });
    }
}
exports.default = (0, react_1.withTheme)(ProjectSessionsChartRequest);
//# sourceMappingURL=projectSessionsChartRequest.jsx.map