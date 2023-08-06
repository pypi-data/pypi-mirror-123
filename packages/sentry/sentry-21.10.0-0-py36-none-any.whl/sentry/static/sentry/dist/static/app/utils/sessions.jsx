Object.defineProperty(exports, "__esModule", { value: true });
exports.filterSessionsInTimeWindow = exports.getSessionsInterval = exports.initSessionsChart = exports.getCountSeries = exports.getAdoptionSeries = exports.getSessionP50Series = exports.getSessionStatusRateSeries = exports.getCrashFreeRateSeries = exports.getSessionStatusRate = exports.getSeriesAverage = exports.getCrashFreeRate = exports.getCount = void 0;
const tslib_1 = require("tslib");
const compact_1 = (0, tslib_1.__importDefault)(require("lodash/compact"));
const mean_1 = (0, tslib_1.__importDefault)(require("lodash/mean"));
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const utils_1 = require("app/components/charts/utils");
const types_1 = require("app/types");
const utils_2 = require("app/utils");
const utils_3 = require("app/views/releases/utils");
const sessionTerm_1 = require("app/views/releases/utils/sessionTerm");
function getCount(groups = [], field) {
    return groups.reduce((acc, group) => acc + group.totals[field], 0);
}
exports.getCount = getCount;
function getCrashFreeRate(groups = [], field) {
    const crashedRate = getSessionStatusRate(groups, field, types_1.SessionStatus.CRASHED);
    return (0, utils_2.defined)(crashedRate) ? (0, utils_3.getCrashFreePercent)(100 - crashedRate) : null;
}
exports.getCrashFreeRate = getCrashFreeRate;
function getSeriesAverage(groups = [], field) {
    const totalCount = getCount(groups, field);
    const dataPoints = groups.filter(group => !!group.totals[field]).length;
    return !(0, utils_2.defined)(totalCount) || dataPoints === null || totalCount === 0
        ? null
        : totalCount / dataPoints;
}
exports.getSeriesAverage = getSeriesAverage;
function getSessionStatusRate(groups = [], field, status) {
    const totalCount = getCount(groups, field);
    const crashedCount = getCount(groups.filter(({ by }) => by['session.status'] === status), field);
    return !(0, utils_2.defined)(totalCount) || totalCount === 0
        ? null
        : (0, utils_2.percent)(crashedCount !== null && crashedCount !== void 0 ? crashedCount : 0, totalCount !== null && totalCount !== void 0 ? totalCount : 0);
}
exports.getSessionStatusRate = getSessionStatusRate;
function getCrashFreeRateSeries(groups = [], intervals = [], field) {
    return (0, compact_1.default)(intervals.map((interval, i) => {
        var _a, _b;
        const intervalTotalSessions = groups.reduce((acc, group) => acc + group.series[field][i], 0);
        const intervalCrashedSessions = (_b = (_a = groups.find(group => group.by['session.status'] === types_1.SessionStatus.CRASHED)) === null || _a === void 0 ? void 0 : _a.series[field][i]) !== null && _b !== void 0 ? _b : 0;
        const crashedSessionsPercent = (0, utils_2.percent)(intervalCrashedSessions, intervalTotalSessions);
        if (intervalTotalSessions === 0) {
            return null;
        }
        return {
            name: interval,
            value: (0, utils_3.getCrashFreePercent)(100 - crashedSessionsPercent),
        };
    }));
}
exports.getCrashFreeRateSeries = getCrashFreeRateSeries;
function getSessionStatusRateSeries(groups = [], intervals = [], field, status) {
    return (0, compact_1.default)(intervals.map((interval, i) => {
        var _a, _b;
        const intervalTotalSessions = groups.reduce((acc, group) => acc + group.series[field][i], 0);
        const intervalStatusSessions = (_b = (_a = groups.find(group => group.by['session.status'] === status)) === null || _a === void 0 ? void 0 : _a.series[field][i]) !== null && _b !== void 0 ? _b : 0;
        const statusSessionsPercent = (0, utils_2.percent)(intervalStatusSessions, intervalTotalSessions);
        if (intervalTotalSessions === 0) {
            return null;
        }
        return {
            name: interval,
            value: (0, utils_3.getSessionStatusPercent)(statusSessionsPercent),
        };
    }));
}
exports.getSessionStatusRateSeries = getSessionStatusRateSeries;
function getSessionP50Series(groups = [], intervals = [], field, valueFormatter) {
    return (0, compact_1.default)(intervals.map((interval, i) => {
        const meanValue = (0, mean_1.default)(groups.map(group => group.series[field][i]).filter(v => !!v));
        if (!meanValue) {
            return null;
        }
        return {
            name: interval,
            value: typeof valueFormatter === 'function' ? valueFormatter(meanValue) : meanValue,
        };
    }));
}
exports.getSessionP50Series = getSessionP50Series;
function getAdoptionSeries(releaseGroups = [], allGroups = [], intervals = [], field) {
    return intervals.map((interval, i) => {
        const intervalReleaseSessions = releaseGroups.reduce((acc, group) => { var _a, _b; return acc + ((_b = (_a = group.series[field]) === null || _a === void 0 ? void 0 : _a[i]) !== null && _b !== void 0 ? _b : 0); }, 0);
        const intervalTotalSessions = allGroups.reduce((acc, group) => { var _a, _b; return acc + ((_b = (_a = group.series[field]) === null || _a === void 0 ? void 0 : _a[i]) !== null && _b !== void 0 ? _b : 0); }, 0);
        const intervalAdoption = (0, utils_2.percent)(intervalReleaseSessions, intervalTotalSessions);
        return {
            name: interval,
            value: Math.round(intervalAdoption),
        };
    });
}
exports.getAdoptionSeries = getAdoptionSeries;
function getCountSeries(field, group, intervals = []) {
    return intervals.map((interval, index) => {
        var _a;
        return ({
            name: interval,
            value: (_a = group === null || group === void 0 ? void 0 : group.series[field][index]) !== null && _a !== void 0 ? _a : 0,
        });
    });
}
exports.getCountSeries = getCountSeries;
function initSessionsChart(theme) {
    const colors = theme.charts.getColorPalette(14);
    return {
        [types_1.SessionStatus.HEALTHY]: {
            seriesName: sessionTerm_1.sessionTerm.healthy,
            data: [],
            color: theme.green300,
            areaStyle: {
                color: theme.green300,
                opacity: 1,
            },
            lineStyle: {
                opacity: 0,
                width: 0.4,
            },
        },
        [types_1.SessionStatus.ERRORED]: {
            seriesName: sessionTerm_1.sessionTerm.errored,
            data: [],
            color: colors[12],
            areaStyle: {
                color: colors[12],
                opacity: 1,
            },
            lineStyle: {
                opacity: 0,
                width: 0.4,
            },
        },
        [types_1.SessionStatus.ABNORMAL]: {
            seriesName: sessionTerm_1.sessionTerm.abnormal,
            data: [],
            color: colors[15],
            areaStyle: {
                color: colors[15],
                opacity: 1,
            },
            lineStyle: {
                opacity: 0,
                width: 0.4,
            },
        },
        [types_1.SessionStatus.CRASHED]: {
            seriesName: sessionTerm_1.sessionTerm.crashed,
            data: [],
            color: theme.red300,
            areaStyle: {
                color: theme.red300,
                opacity: 1,
            },
            lineStyle: {
                opacity: 0,
                width: 0.4,
            },
        },
    };
}
exports.initSessionsChart = initSessionsChart;
function getSessionsInterval(datetimeObj, { highFidelity } = {}) {
    const diffInMinutes = (0, utils_1.getDiffInMinutes)(datetimeObj);
    if ((0, moment_1.default)(datetimeObj.start).isSameOrBefore((0, moment_1.default)().subtract(30, 'days'))) {
        // we cannot use sub-hour session resolution on buckets older than 30 days
        highFidelity = false;
    }
    if (diffInMinutes > utils_1.TWO_WEEKS) {
        return '1d';
    }
    if (diffInMinutes > utils_1.ONE_WEEK) {
        return '6h';
    }
    // limit on backend for sub-hour session resolution is set to six hours
    if (highFidelity && diffInMinutes < 360) {
        if (diffInMinutes <= 30) {
            return '1m';
        }
        return '5m';
    }
    return '1h';
}
exports.getSessionsInterval = getSessionsInterval;
// Sessions API can only round intervals to the closest hour - this is especially problematic when using sub-hour resolution.
// We filter out results that are out of bounds on frontend and recalculate totals.
function filterSessionsInTimeWindow(sessions, start, end) {
    if (!start || !end) {
        return sessions;
    }
    const filteredIndexes = [];
    const intervals = sessions.intervals.filter((interval, index) => {
        const isBetween = moment_1.default
            .utc(interval)
            .isBetween(moment_1.default.utc(start), moment_1.default.utc(end), undefined, '[]');
        if (isBetween) {
            filteredIndexes.push(index);
        }
        return isBetween;
    });
    const groups = sessions.groups.map(group => {
        const series = {};
        const totals = {};
        Object.keys(group.series).forEach(field => {
            totals[field] = 0;
            series[field] = group.series[field].filter((value, index) => {
                var _a;
                const isBetween = filteredIndexes.includes(index);
                if (isBetween) {
                    totals[field] = ((_a = totals[field]) !== null && _a !== void 0 ? _a : 0) + value;
                }
                return isBetween;
            });
            if (field.startsWith('p50')) {
                totals[field] = (0, mean_1.default)(series[field]);
            }
            if (field.startsWith('count_unique')) {
                /* E.g. users
                We cannot sum here because users would not be unique anymore.
                User can be repeated and part of multiple buckets in series but it's still that one user so totals would be wrong.
                This operation is not 100% correct, because we are filtering series in time window but the total is for unfiltered series (it's the closest thing we can do right now) */
                totals[field] = group.totals[field];
            }
        });
        return Object.assign(Object.assign({}, group), { series, totals });
    });
    return {
        start: intervals[0],
        end: intervals[intervals.length - 1],
        query: sessions.query,
        intervals,
        groups,
    };
}
exports.filterSessionsInTimeWindow = filterSessionsInTimeWindow;
//# sourceMappingURL=sessions.jsx.map