Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const react_1 = require("@emotion/react");
const round_1 = (0, tslib_1.__importDefault)(require("lodash/round"));
const areaChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/areaChart"));
const chartZoom_1 = (0, tslib_1.__importDefault)(require("app/components/charts/chartZoom"));
const stackedAreaChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/stackedAreaChart"));
const styles_1 = require("app/components/charts/styles");
const transitionChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/transitionChart"));
const transparentLoadingMask_1 = (0, tslib_1.__importDefault)(require("app/components/charts/transparentLoadingMask"));
const questionTooltip_1 = (0, tslib_1.__importDefault)(require("app/components/questionTooltip"));
const locale_1 = require("app/locale");
const types_1 = require("app/types");
const utils_1 = require("app/utils");
const formatters_1 = require("app/utils/formatters");
const sessions_1 = require("app/utils/sessions");
const utils_2 = require("app/views/releases/utils");
const utils_3 = require("../../utils");
class ReleaseSessionsChart extends React.Component {
    constructor() {
        super(...arguments);
        this.formatTooltipValue = (value, label) => {
            if (label && Object.values(utils_3.releaseMarkLinesLabels).includes(label)) {
                return '';
            }
            const { chartType } = this.props;
            if (value === null) {
                return '\u2015';
            }
            switch (chartType) {
                case types_1.ReleaseComparisonChartType.CRASH_FREE_SESSIONS:
                case types_1.ReleaseComparisonChartType.HEALTHY_SESSIONS:
                case types_1.ReleaseComparisonChartType.ABNORMAL_SESSIONS:
                case types_1.ReleaseComparisonChartType.ERRORED_SESSIONS:
                case types_1.ReleaseComparisonChartType.CRASHED_SESSIONS:
                case types_1.ReleaseComparisonChartType.CRASH_FREE_USERS:
                case types_1.ReleaseComparisonChartType.HEALTHY_USERS:
                case types_1.ReleaseComparisonChartType.ABNORMAL_USERS:
                case types_1.ReleaseComparisonChartType.ERRORED_USERS:
                case types_1.ReleaseComparisonChartType.CRASHED_USERS:
                    return (0, utils_1.defined)(value) ? `${value}%` : '\u2015';
                case types_1.ReleaseComparisonChartType.SESSION_DURATION:
                    return (0, utils_1.defined)(value) && typeof value === 'number'
                        ? (0, formatters_1.getExactDuration)(value, true)
                        : '\u2015';
                case types_1.ReleaseComparisonChartType.SESSION_COUNT:
                case types_1.ReleaseComparisonChartType.USER_COUNT:
                default:
                    return typeof value === 'number' ? value.toLocaleString() : value;
            }
        };
    }
    getYAxis() {
        const { theme, chartType } = this.props;
        switch (chartType) {
            case types_1.ReleaseComparisonChartType.CRASH_FREE_SESSIONS:
            case types_1.ReleaseComparisonChartType.CRASH_FREE_USERS:
                return {
                    max: 100,
                    scale: true,
                    axisLabel: {
                        formatter: (value) => (0, utils_2.displayCrashFreePercent)(value),
                        color: theme.chartLabel,
                    },
                };
            case types_1.ReleaseComparisonChartType.HEALTHY_SESSIONS:
            case types_1.ReleaseComparisonChartType.ABNORMAL_SESSIONS:
            case types_1.ReleaseComparisonChartType.ERRORED_SESSIONS:
            case types_1.ReleaseComparisonChartType.CRASHED_SESSIONS:
            case types_1.ReleaseComparisonChartType.HEALTHY_USERS:
            case types_1.ReleaseComparisonChartType.ABNORMAL_USERS:
            case types_1.ReleaseComparisonChartType.ERRORED_USERS:
            case types_1.ReleaseComparisonChartType.CRASHED_USERS:
                return {
                    scale: true,
                    axisLabel: {
                        formatter: (value) => `${(0, round_1.default)(value, 2)}%`,
                        color: theme.chartLabel,
                    },
                };
            case types_1.ReleaseComparisonChartType.SESSION_DURATION:
                return {
                    scale: true,
                    axisLabel: {
                        formatter: (value) => (0, formatters_1.getDuration)(value, undefined, true),
                        color: theme.chartLabel,
                    },
                };
            case types_1.ReleaseComparisonChartType.SESSION_COUNT:
            case types_1.ReleaseComparisonChartType.USER_COUNT:
            default:
                return undefined;
        }
    }
    getChart() {
        const { chartType } = this.props;
        switch (chartType) {
            case types_1.ReleaseComparisonChartType.CRASH_FREE_SESSIONS:
            case types_1.ReleaseComparisonChartType.HEALTHY_SESSIONS:
            case types_1.ReleaseComparisonChartType.ABNORMAL_SESSIONS:
            case types_1.ReleaseComparisonChartType.ERRORED_SESSIONS:
            case types_1.ReleaseComparisonChartType.CRASHED_SESSIONS:
            case types_1.ReleaseComparisonChartType.CRASH_FREE_USERS:
            case types_1.ReleaseComparisonChartType.HEALTHY_USERS:
            case types_1.ReleaseComparisonChartType.ABNORMAL_USERS:
            case types_1.ReleaseComparisonChartType.ERRORED_USERS:
            case types_1.ReleaseComparisonChartType.CRASHED_USERS:
            default:
                return areaChart_1.default;
            case types_1.ReleaseComparisonChartType.SESSION_COUNT:
            case types_1.ReleaseComparisonChartType.SESSION_DURATION:
            case types_1.ReleaseComparisonChartType.USER_COUNT:
                return stackedAreaChart_1.default;
        }
    }
    getColors() {
        const { theme, chartType } = this.props;
        const colors = theme.charts.getColorPalette(14);
        switch (chartType) {
            case types_1.ReleaseComparisonChartType.CRASH_FREE_SESSIONS:
                return [colors[0]];
            case types_1.ReleaseComparisonChartType.HEALTHY_SESSIONS:
                return [theme.green300];
            case types_1.ReleaseComparisonChartType.ABNORMAL_SESSIONS:
                return [colors[15]];
            case types_1.ReleaseComparisonChartType.ERRORED_SESSIONS:
                return [colors[12]];
            case types_1.ReleaseComparisonChartType.CRASHED_SESSIONS:
                return [theme.red300];
            case types_1.ReleaseComparisonChartType.CRASH_FREE_USERS:
                return [colors[6]];
            case types_1.ReleaseComparisonChartType.HEALTHY_USERS:
                return [theme.green300];
            case types_1.ReleaseComparisonChartType.ABNORMAL_USERS:
                return [colors[15]];
            case types_1.ReleaseComparisonChartType.ERRORED_USERS:
                return [colors[12]];
            case types_1.ReleaseComparisonChartType.CRASHED_USERS:
                return [theme.red300];
            case types_1.ReleaseComparisonChartType.SESSION_COUNT:
            case types_1.ReleaseComparisonChartType.SESSION_DURATION:
            case types_1.ReleaseComparisonChartType.USER_COUNT:
            default:
                return undefined;
        }
    }
    getSeries(chartType) {
        const { releaseSessions, allSessions, release, location, project, theme } = this.props;
        const countCharts = (0, sessions_1.initSessionsChart)(theme);
        if (!releaseSessions) {
            return {};
        }
        const markLines = (0, utils_3.generateReleaseMarkLines)(release, project, theme, location);
        switch (chartType) {
            case types_1.ReleaseComparisonChartType.CRASH_FREE_SESSIONS:
                return {
                    series: [
                        {
                            seriesName: (0, locale_1.t)('This Release'),
                            connectNulls: true,
                            data: (0, sessions_1.getCrashFreeRateSeries)(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.intervals, types_1.SessionField.SESSIONS),
                        },
                    ],
                    previousSeries: [
                        {
                            seriesName: (0, locale_1.t)('All Releases'),
                            data: (0, sessions_1.getCrashFreeRateSeries)(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, allSessions === null || allSessions === void 0 ? void 0 : allSessions.intervals, types_1.SessionField.SESSIONS),
                        },
                    ],
                    markLines,
                };
            case types_1.ReleaseComparisonChartType.HEALTHY_SESSIONS:
                return {
                    series: [
                        {
                            seriesName: (0, locale_1.t)('This Release'),
                            connectNulls: true,
                            data: (0, sessions_1.getSessionStatusRateSeries)(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.intervals, types_1.SessionField.SESSIONS, types_1.SessionStatus.HEALTHY),
                        },
                    ],
                    previousSeries: [
                        {
                            seriesName: (0, locale_1.t)('All Releases'),
                            data: (0, sessions_1.getSessionStatusRateSeries)(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, allSessions === null || allSessions === void 0 ? void 0 : allSessions.intervals, types_1.SessionField.SESSIONS, types_1.SessionStatus.HEALTHY),
                        },
                    ],
                    markLines,
                };
            case types_1.ReleaseComparisonChartType.ABNORMAL_SESSIONS:
                return {
                    series: [
                        {
                            seriesName: (0, locale_1.t)('This Release'),
                            connectNulls: true,
                            data: (0, sessions_1.getSessionStatusRateSeries)(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.intervals, types_1.SessionField.SESSIONS, types_1.SessionStatus.ABNORMAL),
                        },
                    ],
                    previousSeries: [
                        {
                            seriesName: (0, locale_1.t)('All Releases'),
                            data: (0, sessions_1.getSessionStatusRateSeries)(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, allSessions === null || allSessions === void 0 ? void 0 : allSessions.intervals, types_1.SessionField.SESSIONS, types_1.SessionStatus.ABNORMAL),
                        },
                    ],
                    markLines,
                };
            case types_1.ReleaseComparisonChartType.ERRORED_SESSIONS:
                return {
                    series: [
                        {
                            seriesName: (0, locale_1.t)('This Release'),
                            connectNulls: true,
                            data: (0, sessions_1.getSessionStatusRateSeries)(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.intervals, types_1.SessionField.SESSIONS, types_1.SessionStatus.ERRORED),
                        },
                    ],
                    previousSeries: [
                        {
                            seriesName: (0, locale_1.t)('All Releases'),
                            data: (0, sessions_1.getSessionStatusRateSeries)(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, allSessions === null || allSessions === void 0 ? void 0 : allSessions.intervals, types_1.SessionField.SESSIONS, types_1.SessionStatus.ERRORED),
                        },
                    ],
                    markLines,
                };
            case types_1.ReleaseComparisonChartType.CRASHED_SESSIONS:
                return {
                    series: [
                        {
                            seriesName: (0, locale_1.t)('This Release'),
                            connectNulls: true,
                            data: (0, sessions_1.getSessionStatusRateSeries)(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.intervals, types_1.SessionField.SESSIONS, types_1.SessionStatus.CRASHED),
                        },
                    ],
                    previousSeries: [
                        {
                            seriesName: (0, locale_1.t)('All Releases'),
                            data: (0, sessions_1.getSessionStatusRateSeries)(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, allSessions === null || allSessions === void 0 ? void 0 : allSessions.intervals, types_1.SessionField.SESSIONS, types_1.SessionStatus.CRASHED),
                        },
                    ],
                    markLines,
                };
            case types_1.ReleaseComparisonChartType.CRASH_FREE_USERS:
                return {
                    series: [
                        {
                            seriesName: (0, locale_1.t)('This Release'),
                            connectNulls: true,
                            data: (0, sessions_1.getCrashFreeRateSeries)(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.intervals, types_1.SessionField.USERS),
                        },
                    ],
                    previousSeries: [
                        {
                            seriesName: (0, locale_1.t)('All Releases'),
                            data: (0, sessions_1.getCrashFreeRateSeries)(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, allSessions === null || allSessions === void 0 ? void 0 : allSessions.intervals, types_1.SessionField.USERS),
                        },
                    ],
                    markLines,
                };
            case types_1.ReleaseComparisonChartType.HEALTHY_USERS:
                return {
                    series: [
                        {
                            seriesName: (0, locale_1.t)('This Release'),
                            connectNulls: true,
                            data: (0, sessions_1.getSessionStatusRateSeries)(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.intervals, types_1.SessionField.USERS, types_1.SessionStatus.HEALTHY),
                        },
                    ],
                    previousSeries: [
                        {
                            seriesName: (0, locale_1.t)('All Releases'),
                            data: (0, sessions_1.getSessionStatusRateSeries)(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, allSessions === null || allSessions === void 0 ? void 0 : allSessions.intervals, types_1.SessionField.USERS, types_1.SessionStatus.HEALTHY),
                        },
                    ],
                    markLines,
                };
            case types_1.ReleaseComparisonChartType.ABNORMAL_USERS:
                return {
                    series: [
                        {
                            seriesName: (0, locale_1.t)('This Release'),
                            connectNulls: true,
                            data: (0, sessions_1.getSessionStatusRateSeries)(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.intervals, types_1.SessionField.USERS, types_1.SessionStatus.ABNORMAL),
                        },
                    ],
                    previousSeries: [
                        {
                            seriesName: (0, locale_1.t)('All Releases'),
                            data: (0, sessions_1.getSessionStatusRateSeries)(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, allSessions === null || allSessions === void 0 ? void 0 : allSessions.intervals, types_1.SessionField.USERS, types_1.SessionStatus.ABNORMAL),
                        },
                    ],
                    markLines,
                };
            case types_1.ReleaseComparisonChartType.ERRORED_USERS:
                return {
                    series: [
                        {
                            seriesName: (0, locale_1.t)('This Release'),
                            connectNulls: true,
                            data: (0, sessions_1.getSessionStatusRateSeries)(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.intervals, types_1.SessionField.USERS, types_1.SessionStatus.ERRORED),
                        },
                    ],
                    previousSeries: [
                        {
                            seriesName: (0, locale_1.t)('All Releases'),
                            data: (0, sessions_1.getSessionStatusRateSeries)(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, allSessions === null || allSessions === void 0 ? void 0 : allSessions.intervals, types_1.SessionField.USERS, types_1.SessionStatus.ERRORED),
                        },
                    ],
                    markLines,
                };
            case types_1.ReleaseComparisonChartType.CRASHED_USERS:
                return {
                    series: [
                        {
                            seriesName: (0, locale_1.t)('This Release'),
                            connectNulls: true,
                            data: (0, sessions_1.getSessionStatusRateSeries)(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.intervals, types_1.SessionField.USERS, types_1.SessionStatus.CRASHED),
                        },
                    ],
                    previousSeries: [
                        {
                            seriesName: (0, locale_1.t)('All Releases'),
                            data: (0, sessions_1.getSessionStatusRateSeries)(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, allSessions === null || allSessions === void 0 ? void 0 : allSessions.intervals, types_1.SessionField.USERS, types_1.SessionStatus.CRASHED),
                        },
                    ],
                    markLines,
                };
            case types_1.ReleaseComparisonChartType.SESSION_COUNT:
                return {
                    series: [
                        Object.assign(Object.assign({}, countCharts[types_1.SessionStatus.HEALTHY]), { data: (0, sessions_1.getCountSeries)(types_1.SessionField.SESSIONS, releaseSessions.groups.find(g => g.by['session.status'] === types_1.SessionStatus.HEALTHY), releaseSessions.intervals) }),
                        Object.assign(Object.assign({}, countCharts[types_1.SessionStatus.ERRORED]), { data: (0, sessions_1.getCountSeries)(types_1.SessionField.SESSIONS, releaseSessions.groups.find(g => g.by['session.status'] === types_1.SessionStatus.ERRORED), releaseSessions.intervals) }),
                        Object.assign(Object.assign({}, countCharts[types_1.SessionStatus.ABNORMAL]), { data: (0, sessions_1.getCountSeries)(types_1.SessionField.SESSIONS, releaseSessions.groups.find(g => g.by['session.status'] === types_1.SessionStatus.ABNORMAL), releaseSessions.intervals) }),
                        Object.assign(Object.assign({}, countCharts[types_1.SessionStatus.CRASHED]), { data: (0, sessions_1.getCountSeries)(types_1.SessionField.SESSIONS, releaseSessions.groups.find(g => g.by['session.status'] === types_1.SessionStatus.CRASHED), releaseSessions.intervals) }),
                    ],
                    markLines,
                };
            case types_1.ReleaseComparisonChartType.SESSION_DURATION:
                return {
                    series: [
                        {
                            seriesName: (0, locale_1.t)('This Release'),
                            connectNulls: true,
                            data: (0, sessions_1.getSessionP50Series)(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.intervals, types_1.SessionField.DURATION, duration => (0, utils_2.roundDuration)(duration / 1000)),
                        },
                    ],
                    previousSeries: [
                        {
                            seriesName: (0, locale_1.t)('All Releases'),
                            data: (0, sessions_1.getSessionP50Series)(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, allSessions === null || allSessions === void 0 ? void 0 : allSessions.intervals, types_1.SessionField.DURATION, duration => (0, utils_2.roundDuration)(duration / 1000)),
                        },
                    ],
                    markLines,
                };
            case types_1.ReleaseComparisonChartType.USER_COUNT:
                return {
                    series: [
                        Object.assign(Object.assign({}, countCharts[types_1.SessionStatus.HEALTHY]), { data: (0, sessions_1.getCountSeries)(types_1.SessionField.USERS, releaseSessions.groups.find(g => g.by['session.status'] === types_1.SessionStatus.HEALTHY), releaseSessions.intervals) }),
                        Object.assign(Object.assign({}, countCharts[types_1.SessionStatus.ERRORED]), { data: (0, sessions_1.getCountSeries)(types_1.SessionField.USERS, releaseSessions.groups.find(g => g.by['session.status'] === types_1.SessionStatus.ERRORED), releaseSessions.intervals) }),
                        Object.assign(Object.assign({}, countCharts[types_1.SessionStatus.ABNORMAL]), { data: (0, sessions_1.getCountSeries)(types_1.SessionField.USERS, releaseSessions.groups.find(g => g.by['session.status'] === types_1.SessionStatus.ABNORMAL), releaseSessions.intervals) }),
                        Object.assign(Object.assign({}, countCharts[types_1.SessionStatus.CRASHED]), { data: (0, sessions_1.getCountSeries)(types_1.SessionField.USERS, releaseSessions.groups.find(g => g.by['session.status'] === types_1.SessionStatus.CRASHED), releaseSessions.intervals) }),
                    ],
                    markLines,
                };
            default:
                return {};
        }
    }
    render() {
        const { chartType, router, period, start, end, utc, value, diff, loading, reloading } = this.props;
        const Chart = this.getChart();
        const { series, previousSeries, markLines } = this.getSeries(chartType);
        const legend = {
            right: 10,
            top: 0,
            data: [...(series !== null && series !== void 0 ? series : []), ...(previousSeries !== null && previousSeries !== void 0 ? previousSeries : [])].map(s => s.seriesName),
        };
        return (<transitionChart_1.default loading={loading} reloading={reloading} height="240px">
        <transparentLoadingMask_1.default visible={reloading}/>
        <styles_1.HeaderTitleLegend aria-label={(0, locale_1.t)('Chart Title')}>
          {utils_3.releaseComparisonChartTitles[chartType]}
          {utils_3.releaseComparisonChartHelp[chartType] && (<questionTooltip_1.default size="sm" position="top" title={utils_3.releaseComparisonChartHelp[chartType]}/>)}
        </styles_1.HeaderTitleLegend>

        <styles_1.HeaderValue aria-label={(0, locale_1.t)('Chart Value')}>
          {value} {diff}
        </styles_1.HeaderValue>

        <chartZoom_1.default router={router} period={period} utc={utc} start={start} end={end} usePageDate>
          {zoomRenderProps => (<Chart legend={legend} series={[...(series !== null && series !== void 0 ? series : []), ...(markLines !== null && markLines !== void 0 ? markLines : [])]} previousPeriod={previousSeries !== null && previousSeries !== void 0 ? previousSeries : []} {...zoomRenderProps} grid={{
                    left: '10px',
                    right: '10px',
                    top: '70px',
                    bottom: '0px',
                }} yAxis={this.getYAxis()} tooltip={{ valueFormatter: this.formatTooltipValue }} colors={this.getColors()} transformSinglePointToBar height={240}/>)}
        </chartZoom_1.default>
      </transitionChart_1.default>);
    }
}
exports.default = (0, react_1.withTheme)((0, react_router_1.withRouter)(ReleaseSessionsChart));
//# sourceMappingURL=releaseSessionsChart.jsx.map