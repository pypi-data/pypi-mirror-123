Object.defineProperty(exports, "__esModule", { value: true });
exports.transformEventStatsSmoothed = exports.replaceSmoothedSeriesName = exports.replaceSeriesName = exports.smoothTrend = exports.movingAverage = exports.getUnselectedSeries = exports.getSelectedQueryKey = exports.normalizeTrends = exports.transformValueDelta = exports.modifyTrendsViewDefaultPeriod = exports.modifyTrendView = exports.getTrendProjectId = exports.transformDeltaSpread = exports.generateTrendFunctionAsString = exports.getCurrentTrendParameter = exports.getCurrentTrendFunction = exports.resetCursors = exports.trendCursorNames = exports.trendUnselectedSeries = exports.trendSelectedQueryKeys = exports.trendToColor = exports.TRENDS_PARAMETERS = exports.TRENDS_FUNCTIONS = exports.DEFAULT_MAX_DURATION = exports.DEFAULT_TRENDS_STATS_PERIOD = void 0;
const tslib_1 = require("tslib");
const ASAP_1 = require("downsample/methods/ASAP");
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const utils_1 = require("app/components/charts/utils");
const locale_1 = require("app/locale");
const fields_1 = require("app/utils/discover/fields");
const queryString_1 = require("app/utils/queryString");
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const tokenizeSearch_1 = require("app/utils/tokenizeSearch");
const types_1 = require("./types");
exports.DEFAULT_TRENDS_STATS_PERIOD = '14d';
exports.DEFAULT_MAX_DURATION = '15min';
exports.TRENDS_FUNCTIONS = [
    {
        label: 'p50',
        field: types_1.TrendFunctionField.P50,
        alias: 'percentile_range',
        legendLabel: 'p50',
    },
    {
        label: 'p75',
        field: types_1.TrendFunctionField.P75,
        alias: 'percentile_range',
        legendLabel: 'p75',
    },
    {
        label: 'p95',
        field: types_1.TrendFunctionField.P95,
        alias: 'percentile_range',
        legendLabel: 'p95',
    },
    {
        label: 'p99',
        field: types_1.TrendFunctionField.P99,
        alias: 'percentile_range',
        legendLabel: 'p99',
    },
    {
        label: 'average',
        field: types_1.TrendFunctionField.AVG,
        alias: 'avg_range',
        legendLabel: 'average',
    },
];
exports.TRENDS_PARAMETERS = [
    {
        label: 'Duration',
        column: types_1.TrendColumnField.DURATION,
    },
    {
        label: 'LCP',
        column: types_1.TrendColumnField.LCP,
    },
    {
        label: 'FCP',
        column: types_1.TrendColumnField.FCP,
    },
    {
        label: 'FID',
        column: types_1.TrendColumnField.FID,
    },
    {
        label: 'CLS',
        column: types_1.TrendColumnField.CLS,
    },
    {
        label: 'Spans (http)',
        column: types_1.TrendColumnField.SPANS_HTTP,
    },
    {
        label: 'Spans (db)',
        column: types_1.TrendColumnField.SPANS_DB,
    },
    {
        label: 'Spans (browser)',
        column: types_1.TrendColumnField.SPANS_BROWSER,
    },
    {
        label: 'Spans (resource)',
        column: types_1.TrendColumnField.SPANS_RESOURCE,
    },
];
exports.trendToColor = {
    [types_1.TrendChangeType.IMPROVED]: {
        lighter: theme_1.default.green200,
        default: theme_1.default.green300,
    },
    [types_1.TrendChangeType.REGRESSION]: {
        lighter: theme_1.default.red200,
        default: theme_1.default.red300,
    },
};
exports.trendSelectedQueryKeys = {
    [types_1.TrendChangeType.IMPROVED]: 'improvedSelected',
    [types_1.TrendChangeType.REGRESSION]: 'regressionSelected',
};
exports.trendUnselectedSeries = {
    [types_1.TrendChangeType.IMPROVED]: 'improvedUnselectedSeries',
    [types_1.TrendChangeType.REGRESSION]: 'regressionUnselectedSeries',
};
exports.trendCursorNames = {
    [types_1.TrendChangeType.IMPROVED]: 'improvedCursor',
    [types_1.TrendChangeType.REGRESSION]: 'regressionCursor',
};
function resetCursors() {
    const cursors = {};
    Object.values(exports.trendCursorNames).forEach(cursor => (cursors[cursor] = undefined)); // Resets both cursors
    return cursors;
}
exports.resetCursors = resetCursors;
function getCurrentTrendFunction(location) {
    var _a;
    const trendFunctionField = (0, queryString_1.decodeScalar)((_a = location === null || location === void 0 ? void 0 : location.query) === null || _a === void 0 ? void 0 : _a.trendFunction);
    const trendFunction = exports.TRENDS_FUNCTIONS.find(({ field }) => field === trendFunctionField);
    return trendFunction || exports.TRENDS_FUNCTIONS[0];
}
exports.getCurrentTrendFunction = getCurrentTrendFunction;
function getCurrentTrendParameter(location) {
    var _a;
    const trendParameterLabel = (0, queryString_1.decodeScalar)((_a = location === null || location === void 0 ? void 0 : location.query) === null || _a === void 0 ? void 0 : _a.trendParameter);
    const trendParameter = exports.TRENDS_PARAMETERS.find(({ label }) => label === trendParameterLabel);
    return trendParameter || exports.TRENDS_PARAMETERS[0];
}
exports.getCurrentTrendParameter = getCurrentTrendParameter;
function generateTrendFunctionAsString(trendFunction, trendParameter) {
    return (0, fields_1.generateFieldAsString)({
        kind: 'function',
        function: [trendFunction, trendParameter, undefined, undefined],
    });
}
exports.generateTrendFunctionAsString = generateTrendFunctionAsString;
function transformDeltaSpread(from, to) {
    const fromSeconds = from / 1000;
    const toSeconds = to / 1000;
    const showDigits = from > 1000 || to > 1000 || from < 10 || to < 10; // Show digits consistently if either has them
    return { fromSeconds, toSeconds, showDigits };
}
exports.transformDeltaSpread = transformDeltaSpread;
function getTrendProjectId(trend, projects) {
    if (!trend.project || !projects) {
        return undefined;
    }
    const transactionProject = projects.find(project => project.slug === trend.project);
    return transactionProject === null || transactionProject === void 0 ? void 0 : transactionProject.id;
}
exports.getTrendProjectId = getTrendProjectId;
function modifyTrendView(trendView, location, trendsType, isProjectOnly) {
    const trendFunction = getCurrentTrendFunction(location);
    const trendParameter = getCurrentTrendParameter(location);
    const transactionField = isProjectOnly ? [] : ['transaction'];
    const fields = [...transactionField, 'project'].map(field => ({
        field,
    }));
    const trendSort = {
        field: 'trend_percentage()',
        kind: 'asc',
    };
    trendView.trendType = trendsType;
    if (trendsType === types_1.TrendChangeType.REGRESSION) {
        trendSort.kind = 'desc';
    }
    if (trendFunction && trendParameter) {
        trendView.trendFunction = generateTrendFunctionAsString(trendFunction.field, trendParameter.column);
    }
    trendView.query = getLimitTransactionItems(trendView.query);
    trendView.interval = getQueryInterval(location, trendView);
    trendView.sorts = [trendSort];
    trendView.fields = fields;
}
exports.modifyTrendView = modifyTrendView;
function modifyTrendsViewDefaultPeriod(eventView, location) {
    const { query } = location;
    const hasStartAndEnd = query.start && query.end;
    if (!query.statsPeriod && !hasStartAndEnd) {
        eventView.statsPeriod = exports.DEFAULT_TRENDS_STATS_PERIOD;
    }
    return eventView;
}
exports.modifyTrendsViewDefaultPeriod = modifyTrendsViewDefaultPeriod;
function getQueryInterval(location, eventView) {
    var _a;
    const intervalFromQueryParam = (0, queryString_1.decodeScalar)((_a = location === null || location === void 0 ? void 0 : location.query) === null || _a === void 0 ? void 0 : _a.interval);
    const { start, end, statsPeriod } = eventView;
    const datetimeSelection = {
        start: start || null,
        end: end || null,
        period: statsPeriod,
    };
    const intervalFromSmoothing = (0, utils_1.getInterval)(datetimeSelection, 'high');
    return intervalFromQueryParam || intervalFromSmoothing;
}
function transformValueDelta(value, trendType) {
    const absoluteValue = Math.abs(value);
    const changeLabel = trendType === types_1.TrendChangeType.REGRESSION ? (0, locale_1.t)('slower') : (0, locale_1.t)('faster');
    const seconds = absoluteValue / 1000;
    const fixedDigits = absoluteValue > 1000 || absoluteValue < 10 ? 1 : 0;
    return { seconds, fixedDigits, changeLabel };
}
exports.transformValueDelta = transformValueDelta;
/**
 * This will normalize the trends transactions while the current trend function and current data are out of sync
 * To minimize extra renders with missing results.
 */
function normalizeTrends(data) {
    const received_at = (0, moment_1.default)(); // Adding the received time for the transaction so calls to get baseline always line up with the transaction
    return data.map(row => {
        return Object.assign(Object.assign({}, row), { received_at, transaction: row.transaction });
    });
}
exports.normalizeTrends = normalizeTrends;
function getSelectedQueryKey(trendChangeType) {
    return exports.trendSelectedQueryKeys[trendChangeType];
}
exports.getSelectedQueryKey = getSelectedQueryKey;
function getUnselectedSeries(trendChangeType) {
    return exports.trendUnselectedSeries[trendChangeType];
}
exports.getUnselectedSeries = getUnselectedSeries;
function movingAverage(data, index, size) {
    return (data
        .slice(index - size, index)
        .map(a => a.value)
        .reduce((a, b) => a + b, 0) / size);
}
exports.movingAverage = movingAverage;
/**
 * This function applies defaults for trend and count percentage, and adds the confidence limit to the query
 */
function getLimitTransactionItems(query) {
    const limitQuery = new tokenizeSearch_1.MutableSearch(query);
    if (!limitQuery.hasFilter('count_percentage()')) {
        limitQuery.addFilterValues('count_percentage()', ['>0.25', '<4']);
    }
    if (!limitQuery.hasFilter('trend_percentage()')) {
        limitQuery.addFilterValues('trend_percentage()', ['>0%']);
    }
    if (!limitQuery.hasFilter('confidence()')) {
        limitQuery.addFilterValues('confidence()', ['>6']);
    }
    return limitQuery.formatString();
}
const smoothTrend = (data, resolution = 100) => {
    return (0, ASAP_1.ASAP)(data, resolution);
};
exports.smoothTrend = smoothTrend;
const replaceSeriesName = (seriesName) => {
    return ['p50', 'p75'].find(aggregate => seriesName.includes(aggregate));
};
exports.replaceSeriesName = replaceSeriesName;
const replaceSmoothedSeriesName = (seriesName) => {
    return `Smoothed ${['p50', 'p75'].find(aggregate => seriesName.includes(aggregate))}`;
};
exports.replaceSmoothedSeriesName = replaceSmoothedSeriesName;
function transformEventStatsSmoothed(data, seriesName) {
    let minValue = Number.MAX_SAFE_INTEGER;
    let maxValue = 0;
    if (!data) {
        return {
            maxValue,
            minValue,
            smoothedResults: undefined,
        };
    }
    const smoothedResults = [];
    for (const current of data) {
        const currentData = current.data;
        const resultData = [];
        const smoothed = (0, exports.smoothTrend)(currentData.map(({ name, value }) => [Number(name), value]));
        for (let i = 0; i < smoothed.length; i++) {
            const point = smoothed[i];
            const value = point.y;
            resultData.push({
                name: point.x,
                value,
            });
            if (!isNaN(value)) {
                const rounded = Math.round(value);
                minValue = Math.min(rounded, minValue);
                maxValue = Math.max(rounded, maxValue);
            }
        }
        smoothedResults.push({
            seriesName: seriesName || current.seriesName || 'Current',
            data: resultData,
            lineStyle: current.lineStyle,
            color: current.color,
        });
    }
    return {
        minValue,
        maxValue,
        smoothedResults,
    };
}
exports.transformEventStatsSmoothed = transformEventStatsSmoothed;
//# sourceMappingURL=utils.jsx.map