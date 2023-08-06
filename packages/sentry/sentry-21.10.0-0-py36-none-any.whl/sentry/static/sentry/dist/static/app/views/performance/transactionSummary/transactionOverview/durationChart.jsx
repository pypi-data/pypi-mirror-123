Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const react_2 = require("@emotion/react");
const areaChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/areaChart"));
const chartZoom_1 = (0, tslib_1.__importDefault)(require("app/components/charts/chartZoom"));
const errorPanel_1 = (0, tslib_1.__importDefault)(require("app/components/charts/errorPanel"));
const eventsRequest_1 = (0, tslib_1.__importDefault)(require("app/components/charts/eventsRequest"));
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
const filter_1 = require("../filter");
const QUERY_KEYS = [
    'environment',
    'project',
    'query',
    'start',
    'end',
    'statsPeriod',
];
function generateYAxisValues() {
    return ['p50()', 'p75()', 'p95()', 'p99()', 'p100()'];
}
/**
 * Fetch and render a stacked area chart that shows duration percentiles over
 * the past 7 days
 */
function DurationChart({ project, environment, location, organization, query, statsPeriod, router, queryExtra, currentFilter, withoutZerofill, start: propsStart, end: propsEnd, }) {
    const api = (0, useApi_1.default)();
    const theme = (0, react_2.useTheme)();
    const handleLegendSelectChanged = legendChange => {
        const { selected } = legendChange;
        const unselected = Object.keys(selected).filter(key => !selected[key]);
        const to = Object.assign(Object.assign({}, location), { query: Object.assign(Object.assign({}, location.query), { unselectedSeries: unselected }) });
        react_router_1.browserHistory.push(to);
    };
    const start = propsStart ? (0, dates_1.getUtcToLocalDateObject)(propsStart) : null;
    const end = propsEnd ? (0, dates_1.getUtcToLocalDateObject)(propsEnd) : null;
    const { utc } = (0, getParams_1.getParams)(location.query);
    const legend = {
        right: 10,
        top: 5,
        selected: (0, utils_1.getSeriesSelection)(location),
    };
    const datetimeSelection = {
        start,
        end,
        period: statsPeriod,
    };
    const headerTitle = currentFilter === filter_1.SpanOperationBreakdownFilter.None
        ? (0, locale_1.t)('Duration Breakdown')
        : (0, locale_1.tct)('Span Operation Breakdown - [operationName]', {
            operationName: currentFilter,
        });
    return (<react_1.Fragment>
      <styles_1.HeaderTitleLegend>
        {headerTitle}
        <questionTooltip_1.default size="sm" position="top" title={(0, locale_1.t)(`Duration Breakdown reflects transaction durations by percentile over time.`)}/>
      </styles_1.HeaderTitleLegend>
      <chartZoom_1.default router={router} period={statsPeriod} start={start} end={end} utc={utc === 'true'}>
        {zoomRenderProps => (<eventsRequest_1.default api={api} organization={organization} period={statsPeriod} project={project} environment={environment} start={start} end={end} interval={(0, utils_1.getInterval)(datetimeSelection, 'high')} showLoading={false} query={query} includePrevious={false} yAxis={generateYAxisValues()} partial withoutZerofill={withoutZerofill} referrer="api.performance.transaction-summary.duration-chart">
            {({ results, errored, loading, reloading, timeframe }) => {
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
                        valueFormatter: charts_1.tooltipFormatter,
                    },
                    xAxis: timeframe
                        ? {
                            min: timeframe.start,
                            max: timeframe.end,
                        }
                        : undefined,
                    yAxis: {
                        axisLabel: {
                            color: theme.chartLabel,
                            // p50() coerces the axis to be time based
                            formatter: (value) => (0, charts_1.axisLabelFormatter)(value, 'p50()'),
                        },
                    },
                };
                const colors = (results && theme.charts.getColorPalette(results.length - 2)) || [];
                // Create a list of series based on the order of the fields,
                // We need to flip it at the end to ensure the series stack right.
                const series = results
                    ? results
                        .map((values, i) => {
                        return Object.assign(Object.assign({}, values), { color: colors[i], lineStyle: {
                                opacity: 0,
                            } });
                    })
                        .reverse()
                    : [];
                return (<releaseSeries_1.default start={start} end={end} queryExtra={queryExtra} period={statsPeriod} utc={utc === 'true'} projects={project} environments={environment}>
                  {({ releaseSeries }) => (<transitionChart_1.default loading={loading} reloading={reloading}>
                      <transparentLoadingMask_1.default visible={reloading}/>
                      {(0, getDynamicText_1.default)({
                            value: (<areaChart_1.default {...zoomRenderProps} {...chartOptions} legend={legend} onLegendSelectChanged={handleLegendSelectChanged} series={[...series, ...releaseSeries]}/>),
                            fixed: <placeholder_1.default height="200px" testId="skeleton-ui"/>,
                        })}
                    </transitionChart_1.default>)}
                </releaseSeries_1.default>);
            }}
          </eventsRequest_1.default>)}
      </chartZoom_1.default>
    </react_1.Fragment>);
}
exports.default = (0, react_router_1.withRouter)(DurationChart);
//# sourceMappingURL=durationChart.jsx.map