Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_router_1 = require("react-router");
const react_1 = require("@emotion/react");
const chartZoom_1 = (0, tslib_1.__importDefault)(require("app/components/charts/chartZoom"));
const lineChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/lineChart"));
const releaseSeries_1 = (0, tslib_1.__importDefault)(require("app/components/charts/releaseSeries"));
const transitionChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/transitionChart"));
const transparentLoadingMask_1 = (0, tslib_1.__importDefault)(require("app/components/charts/transparentLoadingMask"));
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const locale_1 = require("app/locale");
const dates_1 = require("app/utils/dates");
const charts_1 = require("app/utils/discover/charts");
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const queryString_1 = require("app/utils/queryString");
const utils_1 = require("./utils");
const QUERY_KEYS = [
    'environment',
    'project',
    'query',
    'start',
    'end',
    'statsPeriod',
];
function transformEventStats(data, seriesName) {
    return [
        {
            seriesName: seriesName || 'Current',
            data: data.map(([timestamp, countsForTimestamp]) => ({
                name: timestamp * 1000,
                value: countsForTimestamp.reduce((acc, { count }) => acc + count, 0),
            })),
        },
    ];
}
function getLegend(trendFunction) {
    return {
        right: 10,
        top: 0,
        itemGap: 12,
        align: 'left',
        data: [
            {
                name: 'Baseline',
                icon: 'path://M180 1000 l0 -40 200 0 200 0 0 40 0 40 -200 0 -200 0 0 -40z, M810 1000 l0 -40 200 0 200 0 0 40 0 40 -200 0 -200 0 0 -40zm, M1440 1000 l0 -40 200 0 200 0 0 40 0 40 -200 0 -200 0 0 -40z',
            },
            {
                name: 'Releases',
                icon: 'line',
            },
            {
                name: trendFunction,
                icon: 'line',
            },
        ],
    };
}
function getIntervalLine(theme, series, intervalRatio, transaction) {
    if (!transaction || !series.length || !series[0].data || !series[0].data.length) {
        return [];
    }
    const seriesStart = parseInt(series[0].data[0].name, 0);
    const seriesEnd = parseInt(series[0].data.slice(-1)[0].name, 0);
    if (seriesEnd < seriesStart) {
        return [];
    }
    const periodLine = {
        data: [],
        color: theme.textColor,
        markLine: {
            data: [],
            label: {},
            lineStyle: {
                normal: {
                    color: theme.textColor,
                    type: 'dashed',
                    width: 1,
                },
            },
            symbol: ['none', 'none'],
            tooltip: {
                show: false,
            },
        },
        seriesName: 'Baseline',
    };
    const periodLineLabel = {
        fontSize: 11,
        show: true,
    };
    const previousPeriod = Object.assign(Object.assign({}, periodLine), { markLine: Object.assign({}, periodLine.markLine), seriesName: 'Baseline' });
    const currentPeriod = Object.assign(Object.assign({}, periodLine), { markLine: Object.assign({}, periodLine.markLine), seriesName: 'Baseline' });
    const periodDividingLine = Object.assign(Object.assign({}, periodLine), { markLine: Object.assign({}, periodLine.markLine), seriesName: 'Period split' });
    const seriesDiff = seriesEnd - seriesStart;
    const seriesLine = seriesDiff * intervalRatio + seriesStart;
    previousPeriod.markLine.data = [
        [
            { value: 'Past', coord: [seriesStart, transaction.aggregate_range_1] },
            { coord: [seriesLine, transaction.aggregate_range_1] },
        ],
    ];
    previousPeriod.markLine.tooltip = {
        formatter: () => {
            return [
                '<div class="tooltip-series tooltip-series-solo">',
                '<div>',
                `<span class="tooltip-label"><strong>${(0, locale_1.t)('Past Baseline')}</strong></span>`,
                // p50() coerces the axis to be time based
                (0, charts_1.tooltipFormatter)(transaction.aggregate_range_1, 'p50()'),
                '</div>',
                '</div>',
                '<div class="tooltip-arrow"></div>',
            ].join('');
        },
    };
    currentPeriod.markLine.data = [
        [
            { value: 'Present', coord: [seriesLine, transaction.aggregate_range_2] },
            { coord: [seriesEnd, transaction.aggregate_range_2] },
        ],
    ];
    currentPeriod.markLine.tooltip = {
        formatter: () => {
            return [
                '<div class="tooltip-series tooltip-series-solo">',
                '<div>',
                `<span class="tooltip-label"><strong>${(0, locale_1.t)('Present Baseline')}</strong></span>`,
                // p50() coerces the axis to be time based
                (0, charts_1.tooltipFormatter)(transaction.aggregate_range_2, 'p50()'),
                '</div>',
                '</div>',
                '<div class="tooltip-arrow"></div>',
            ].join('');
        },
    };
    periodDividingLine.markLine = {
        data: [
            {
                value: 'Previous Period / This Period',
                xAxis: seriesLine,
            },
        ],
        label: { show: false },
        lineStyle: {
            normal: {
                color: theme.textColor,
                type: 'solid',
                width: 2,
            },
        },
        symbol: ['none', 'none'],
        tooltip: {
            show: false,
        },
    };
    previousPeriod.markLine.label = Object.assign(Object.assign({}, periodLineLabel), { formatter: 'Past', position: 'insideStartBottom' });
    currentPeriod.markLine.label = Object.assign(Object.assign({}, periodLineLabel), { formatter: 'Present', position: 'insideEndBottom' });
    const additionalLineSeries = [previousPeriod, currentPeriod, periodDividingLine];
    return additionalLineSeries;
}
function Chart({ trendChangeType, router, statsPeriod, project, environment, transaction, statsData, isLoading, location, projects, start: propsStart, end: propsEnd, }) {
    var _a, _b;
    const theme = (0, react_1.useTheme)();
    const handleLegendSelectChanged = legendChange => {
        const { selected } = legendChange;
        const unselected = Object.keys(selected).filter(key => !selected[key]);
        const query = Object.assign({}, location.query);
        const queryKey = (0, utils_1.getUnselectedSeries)(trendChangeType);
        query[queryKey] = unselected;
        const to = Object.assign(Object.assign({}, location), { query });
        react_router_1.browserHistory.push(to);
    };
    const lineColor = utils_1.trendToColor[trendChangeType || ''];
    const events = statsData && (transaction === null || transaction === void 0 ? void 0 : transaction.project) && (transaction === null || transaction === void 0 ? void 0 : transaction.transaction)
        ? statsData[[transaction.project, transaction.transaction].join(',')]
        : undefined;
    const data = (_a = events === null || events === void 0 ? void 0 : events.data) !== null && _a !== void 0 ? _a : [];
    const trendFunction = (0, utils_1.getCurrentTrendFunction)(location);
    const trendParameter = (0, utils_1.getCurrentTrendParameter)(location);
    const chartLabel = (0, utils_1.generateTrendFunctionAsString)(trendFunction.field, trendParameter.column);
    const results = transformEventStats(data, chartLabel);
    const { smoothedResults, minValue, maxValue } = (0, utils_1.transformEventStatsSmoothed)(results, chartLabel);
    const start = propsStart ? (0, dates_1.getUtcToLocalDateObject)(propsStart) : null;
    const end = propsEnd ? (0, dates_1.getUtcToLocalDateObject)(propsEnd) : null;
    const { utc } = (0, getParams_1.getParams)(location.query);
    const seriesSelection = (0, queryString_1.decodeList)(location.query[(0, utils_1.getUnselectedSeries)(trendChangeType)]).reduce((selection, metric) => {
        selection[metric] = false;
        return selection;
    }, {});
    const legend = Object.assign(Object.assign({}, getLegend(chartLabel)), { selected: seriesSelection });
    const loading = isLoading;
    const reloading = isLoading;
    const transactionProject = parseInt(((_b = projects.find(({ slug }) => (transaction === null || transaction === void 0 ? void 0 : transaction.project) === slug)) === null || _b === void 0 ? void 0 : _b.id) || '', 10);
    const yMax = Math.max(maxValue, (transaction === null || transaction === void 0 ? void 0 : transaction.aggregate_range_2) || 0, (transaction === null || transaction === void 0 ? void 0 : transaction.aggregate_range_1) || 0);
    const yMin = Math.min(minValue, (transaction === null || transaction === void 0 ? void 0 : transaction.aggregate_range_1) || Number.MAX_SAFE_INTEGER, (transaction === null || transaction === void 0 ? void 0 : transaction.aggregate_range_2) || Number.MAX_SAFE_INTEGER);
    const yDiff = yMax - yMin;
    const yMargin = yDiff * 0.1;
    const queryExtra = {
        showTransactions: trendChangeType,
        yAxis: 'countDuration',
    };
    const chartOptions = {
        tooltip: {
            valueFormatter: (value, seriesName) => {
                return (0, charts_1.tooltipFormatter)(value, seriesName);
            },
        },
        yAxis: {
            min: Math.max(0, yMin - yMargin),
            max: yMax + yMargin,
            axisLabel: {
                color: theme.chartLabel,
                // p50() coerces the axis to be time based
                formatter: (value) => (0, charts_1.axisLabelFormatter)(value, 'p50()'),
            },
        },
    };
    return (<chartZoom_1.default router={router} period={statsPeriod} start={start} end={end} utc={utc === 'true'}>
      {zoomRenderProps => {
            const smoothedSeries = smoothedResults
                ? smoothedResults.map(values => {
                    return Object.assign(Object.assign({}, values), { color: lineColor.default, lineStyle: {
                            opacity: 1,
                        } });
                })
                : [];
            const intervalSeries = getIntervalLine(theme, smoothedResults || [], 0.5, transaction);
            return (<releaseSeries_1.default start={start} end={end} queryExtra={queryExtra} period={statsPeriod} utc={utc === 'true'} projects={isNaN(transactionProject) ? project : [transactionProject]} environments={environment} memoized>
            {({ releaseSeries }) => (<transitionChart_1.default loading={loading} reloading={reloading}>
                <transparentLoadingMask_1.default visible={reloading}/>
                {(0, getDynamicText_1.default)({
                        value: (<lineChart_1.default {...zoomRenderProps} {...chartOptions} onLegendSelectChanged={handleLegendSelectChanged} series={[...smoothedSeries, ...releaseSeries, ...intervalSeries]} seriesOptions={{
                                showSymbol: false,
                            }} legend={legend} toolBox={{
                                show: false,
                            }} grid={{
                                left: '10px',
                                right: '10px',
                                top: '40px',
                                bottom: '0px',
                            }}/>),
                        fixed: 'Duration Chart',
                    })}
              </transitionChart_1.default>)}
          </releaseSeries_1.default>);
        }}
    </chartZoom_1.default>);
}
exports.default = (0, react_router_1.withRouter)(Chart);
//# sourceMappingURL=chart.jsx.map