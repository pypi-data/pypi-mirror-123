Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const react_2 = require("@emotion/react");
const chartZoom_1 = (0, tslib_1.__importDefault)(require("app/components/charts/chartZoom"));
const errorPanel_1 = (0, tslib_1.__importDefault)(require("app/components/charts/errorPanel"));
const eventsRequest_1 = (0, tslib_1.__importDefault)(require("app/components/charts/eventsRequest"));
const lineChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/lineChart"));
const releaseSeries_1 = (0, tslib_1.__importDefault)(require("app/components/charts/releaseSeries"));
const styles_1 = require("app/components/charts/styles");
const transitionChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/transitionChart"));
const transparentLoadingMask_1 = (0, tslib_1.__importDefault)(require("app/components/charts/transparentLoadingMask"));
const utils_1 = require("app/components/charts/utils");
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const questionTooltip_1 = (0, tslib_1.__importDefault)(require("app/components/questionTooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const dates_1 = require("app/utils/dates");
const charts_1 = require("app/utils/discover/charts");
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const useApi_1 = (0, tslib_1.__importDefault)(require("app/utils/useApi"));
const utils_2 = require("../../trends/utils");
const QUERY_KEYS = [
    'environment',
    'project',
    'query',
    'start',
    'end',
    'statsPeriod',
];
function TrendChart({ project, environment, location, organization, query, statsPeriod, router, trendDisplay, queryExtra, withoutZerofill, start: propsStart, end: propsEnd, }) {
    const api = (0, useApi_1.default)();
    const theme = (0, react_2.useTheme)();
    const handleLegendSelectChanged = legendChange => {
        const { selected } = legendChange;
        const unselected = Object.keys(selected).filter(key => !selected[key]);
        const to = Object.assign(Object.assign({}, location), { query: Object.assign(Object.assign({}, location.query), { trendsUnselectedSeries: unselected }) });
        react_router_1.browserHistory.push(to);
    };
    const start = propsStart ? (0, dates_1.getUtcToLocalDateObject)(propsStart) : null;
    const end = propsEnd ? (0, dates_1.getUtcToLocalDateObject)(propsEnd) : null;
    const { utc } = (0, getParams_1.getParams)(location.query);
    const legend = {
        right: 10,
        top: 0,
        selected: (0, utils_1.getSeriesSelection)(location, 'trendsUnselectedSeries'),
    };
    const datetimeSelection = {
        start,
        end,
        period: statsPeriod,
    };
    return (<react_1.Fragment>
      <styles_1.HeaderTitleLegend>
        {(0, locale_1.t)('Trend')}
        <questionTooltip_1.default size="sm" position="top" title={(0, locale_1.t)(`Trends shows the smoothed value of an aggregate over time.`)}/>
      </styles_1.HeaderTitleLegend>
      <chartZoom_1.default router={router} period={statsPeriod} start={start} end={end} utc={utc === 'true'}>
        {zoomRenderProps => (<eventsRequest_1.default api={api} organization={organization} period={statsPeriod} project={project} environment={environment} start={start} end={end} interval={(0, utils_1.getInterval)(datetimeSelection, 'high')} showLoading={false} query={query} includePrevious={false} yAxis={trendDisplay} currentSeriesNames={[trendDisplay]} partial withoutZerofill={withoutZerofill} referrer="api.performance.transaction-summary.trends-chart">
            {({ errored, loading, reloading, timeseriesData, timeframe }) => {
                if (errored) {
                    return (<errorPanel_1.default>
                    <icons_1.IconWarning color="gray300" size="lg"/>
                  </errorPanel_1.default>);
                }
                const chartOptions = {
                    grid: {
                        left: '10px',
                        right: '10px',
                        top: '40px',
                        bottom: '0px',
                    },
                    seriesOptions: {
                        showSymbol: false,
                    },
                    tooltip: {
                        trigger: 'axis',
                        valueFormatter: value => (0, charts_1.tooltipFormatter)(value, 'p50()'),
                    },
                    xAxis: timeframe
                        ? {
                            min: timeframe.start,
                            max: timeframe.end,
                        }
                        : undefined,
                    yAxis: {
                        min: 0,
                        axisLabel: {
                            color: theme.chartLabel,
                            // p50() coerces the axis to be time based
                            formatter: (value) => (0, charts_1.axisLabelFormatter)(value, 'p50()'),
                        },
                    },
                };
                const series = timeseriesData
                    ? timeseriesData
                        .map(values => {
                        return Object.assign(Object.assign({}, values), { color: theme.purple300, lineStyle: {
                                opacity: 0.75,
                                width: 1,
                            } });
                    })
                        .reverse()
                    : [];
                const { smoothedResults } = (0, utils_2.transformEventStatsSmoothed)(timeseriesData, (0, locale_1.t)('Smoothed'));
                const smoothedSeries = smoothedResults
                    ? smoothedResults.map(values => {
                        return Object.assign(Object.assign({}, values), { color: theme.purple300, lineStyle: {
                                opacity: 1,
                            } });
                    })
                    : [];
                return (<releaseSeries_1.default start={start} end={end} queryExtra={queryExtra} period={statsPeriod} utc={utc === 'true'} projects={project} environments={environment}>
                  {({ releaseSeries }) => (<transitionChart_1.default loading={loading} reloading={reloading}>
                      <transparentLoadingMask_1.default visible={reloading}/>
                      {(0, getDynamicText_1.default)({
                            value: (<lineChart_1.default {...zoomRenderProps} {...chartOptions} legend={legend} onLegendSelectChanged={handleLegendSelectChanged} series={[...series, ...smoothedSeries, ...releaseSeries]}/>),
                            fixed: <placeholder_1.default height="200px" testId="skeleton-ui"/>,
                        })}
                    </transitionChart_1.default>)}
                </releaseSeries_1.default>);
            }}
          </eventsRequest_1.default>)}
      </chartZoom_1.default>
    </react_1.Fragment>);
}
exports.default = (0, react_router_1.withRouter)(TrendChart);
//# sourceMappingURL=trendChart.jsx.map