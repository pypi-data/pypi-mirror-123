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
const fields_1 = require("app/utils/discover/fields");
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const useApi_1 = (0, tslib_1.__importDefault)(require("app/utils/useApi"));
const overview_1 = require("app/views/releases/detail/overview");
const QUERY_KEYS = [
    'environment',
    'project',
    'query',
    'start',
    'end',
    'statsPeriod',
];
const YAXIS_VALUES = [
    'p75(measurements.fp)',
    'p75(measurements.fcp)',
    'p75(measurements.lcp)',
    'p75(measurements.fid)',
];
function VitalsChart({ project, environment, location, organization, query, statsPeriod, router, queryExtra, withoutZerofill, start: propsStart, end: propsEnd, }) {
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
        top: 0,
        selected: (0, utils_1.getSeriesSelection)(location),
        formatter: seriesName => {
            const arg = (0, fields_1.getAggregateArg)(seriesName);
            if (arg !== null) {
                const slug = (0, fields_1.getMeasurementSlug)(arg);
                if (slug !== null) {
                    seriesName = slug.toUpperCase();
                }
            }
            return seriesName;
        },
    };
    const datetimeSelection = {
        start,
        end,
        period: statsPeriod,
    };
    return (<react_1.Fragment>
      <styles_1.HeaderTitleLegend>
        {(0, locale_1.t)('Web Vitals Breakdown')}
        <questionTooltip_1.default size="sm" position="top" title={(0, locale_1.t)(`Web Vitals Breakdown reflects the 75th percentile of web vitals over time.`)}/>
      </styles_1.HeaderTitleLegend>
      <chartZoom_1.default router={router} period={statsPeriod} start={start} end={end} utc={utc === 'true'}>
        {zoomRenderProps => (<eventsRequest_1.default api={api} organization={organization} period={statsPeriod} project={project} environment={environment} start={start} end={end} interval={(0, utils_1.getInterval)(datetimeSelection, 'high')} showLoading={false} query={query} includePrevious={false} yAxis={YAXIS_VALUES} partial withoutZerofill={withoutZerofill} referrer="api.performance.transaction-summary.vitals-chart">
            {({ results, errored, loading, reloading, timeframe }) => {
                if (errored) {
                    return (<errorPanel_1.default>
                    <icons_1.IconWarning color="gray500" size="lg"/>
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
                            // p75(measurements.fcp) coerces the axis to be time based
                            formatter: (value) => (0, charts_1.axisLabelFormatter)(value, 'p75(measurements.fcp)'),
                        },
                    },
                };
                const colors = (results && theme.charts.getColorPalette(results.length - 2)) || [];
                // Create a list of series based on the order of the fields,
                const series = results
                    ? results.map((values, i) => (Object.assign(Object.assign({}, values), { color: colors[i] })))
                    : [];
                return (<releaseSeries_1.default start={start} end={end} queryExtra={Object.assign(Object.assign({}, queryExtra), { showTransactions: overview_1.TransactionsListOption.SLOW_LCP })} period={statsPeriod} utc={utc === 'true'} projects={project} environments={environment}>
                  {({ releaseSeries }) => (<transitionChart_1.default loading={loading} reloading={reloading}>
                      <transparentLoadingMask_1.default visible={reloading}/>
                      {(0, getDynamicText_1.default)({
                            value: (<lineChart_1.default {...zoomRenderProps} {...chartOptions} legend={legend} onLegendSelectChanged={handleLegendSelectChanged} series={[...series, ...releaseSeries]}/>),
                            fixed: <placeholder_1.default height="200px" testId="skeleton-ui"/>,
                        })}
                    </transitionChart_1.default>)}
                </releaseSeries_1.default>);
            }}
          </eventsRequest_1.default>)}
      </chartZoom_1.default>
    </react_1.Fragment>);
}
exports.default = (0, react_router_1.withRouter)(VitalsChart);
//# sourceMappingURL=vitalsChart.jsx.map