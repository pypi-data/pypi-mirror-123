Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const chartZoom_1 = (0, tslib_1.__importDefault)(require("app/components/charts/chartZoom"));
const errorPanel_1 = (0, tslib_1.__importDefault)(require("app/components/charts/errorPanel"));
const eventsRequest_1 = (0, tslib_1.__importDefault)(require("app/components/charts/eventsRequest"));
const lineChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/lineChart"));
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
const formatters_1 = require("app/utils/formatters");
const useApi_1 = (0, tslib_1.__importDefault)(require("app/utils/useApi"));
const data_1 = require("app/views/performance/data");
function SidebarCharts({ location, eventView, organization, router, isLoading, error, totals, }) {
    const api = (0, useApi_1.default)();
    const theme = (0, react_1.useTheme)();
    const statsPeriod = eventView.statsPeriod;
    const start = eventView.start ? (0, dates_1.getUtcToLocalDateObject)(eventView.start) : undefined;
    const end = eventView.end ? (0, dates_1.getUtcToLocalDateObject)(eventView.end) : undefined;
    const { utc } = (0, getParams_1.getParams)(location.query);
    const colors = theme.charts.getColorPalette(3);
    const axisLineConfig = {
        scale: true,
        axisLine: {
            show: false,
        },
        axisTick: {
            show: false,
        },
        splitLine: {
            show: false,
        },
    };
    const chartOptions = {
        height: 480,
        grid: [
            {
                top: '60px',
                left: '10px',
                right: '10px',
                height: '100px',
            },
            {
                top: '220px',
                left: '10px',
                right: '10px',
                height: '100px',
            },
            {
                top: '380px',
                left: '10px',
                right: '10px',
                height: '120px',
            },
        ],
        axisPointer: {
            // Link each x-axis together.
            link: [{ xAxisIndex: [0, 1, 2] }],
        },
        xAxes: Array.from(new Array(3)).map((_i, index) => ({
            gridIndex: index,
            type: 'time',
            show: false,
        })),
        yAxes: [
            Object.assign({ 
                // apdex
                gridIndex: 0, interval: 0.2, axisLabel: {
                    formatter: (value) => (0, formatters_1.formatFloat)(value, 1),
                    color: theme.chartLabel,
                } }, axisLineConfig),
            Object.assign({ 
                // failure rate
                gridIndex: 1, splitNumber: 4, interval: 0.5, max: 1.0, axisLabel: {
                    formatter: (value) => (0, formatters_1.formatPercentage)(value, 0),
                    color: theme.chartLabel,
                } }, axisLineConfig),
            Object.assign({ 
                // throughput
                gridIndex: 2, splitNumber: 4, axisLabel: {
                    formatter: formatters_1.formatAbbreviatedNumber,
                    color: theme.chartLabel,
                } }, axisLineConfig),
        ],
        utc: utc === 'true',
        isGroupedByDate: true,
        showTimeInTooltip: true,
        colors: [colors[0], colors[1], colors[2]],
        tooltip: {
            trigger: 'axis',
            truncate: 80,
            valueFormatter: charts_1.tooltipFormatter,
            nameFormatter(value) {
                return value === 'epm()' ? 'tpm()' : value;
            },
        },
    };
    const datetimeSelection = {
        start: start || null,
        end: end || null,
        period: statsPeriod,
    };
    const project = eventView.project;
    const environment = eventView.environment;
    return (<RelativeBox>
      <ChartLabel top="0px">
        <ChartTitle>
          {(0, locale_1.t)('Apdex')}
          <questionTooltip_1.default position="top" title={(0, data_1.getTermHelp)(organization, data_1.PERFORMANCE_TERM.APDEX_NEW)} size="sm"/>
        </ChartTitle>
        <ChartSummaryValue isLoading={isLoading} error={error} value={totals ? (0, formatters_1.formatFloat)(totals.apdex, 4) : null}/>
      </ChartLabel>

      <ChartLabel top="160px">
        <ChartTitle>
          {(0, locale_1.t)('Failure Rate')}
          <questionTooltip_1.default position="top" title={(0, data_1.getTermHelp)(organization, data_1.PERFORMANCE_TERM.FAILURE_RATE)} size="sm"/>
        </ChartTitle>
        <ChartSummaryValue isLoading={isLoading} error={error} value={totals ? (0, formatters_1.formatPercentage)(totals.failure_rate) : null}/>
      </ChartLabel>

      <ChartLabel top="320px">
        <ChartTitle>
          {(0, locale_1.t)('TPM')}
          <questionTooltip_1.default position="top" title={(0, data_1.getTermHelp)(organization, data_1.PERFORMANCE_TERM.TPM)} size="sm"/>
        </ChartTitle>
        <ChartSummaryValue isLoading={isLoading} error={error} value={totals ? (0, locale_1.tct)('[tpm] tpm', { tpm: (0, formatters_1.formatFloat)(totals.tpm, 4) }) : null}/>
      </ChartLabel>

      <chartZoom_1.default router={router} period={statsPeriod} start={start} end={end} utc={utc === 'true'} xAxisIndex={[0, 1, 2]}>
        {zoomRenderProps => (<eventsRequest_1.default api={api} organization={organization} period={statsPeriod} project={project} environment={environment} start={start} end={end} interval={(0, utils_1.getInterval)(datetimeSelection)} showLoading={false} query={eventView.query} includePrevious={false} yAxis={['apdex()', 'failure_rate()', 'epm()']} partial referrer="api.performance.transaction-summary.sidebar-chart">
            {({ results, errored, loading, reloading }) => {
                if (errored) {
                    return (<errorPanel_1.default height="580px">
                    <icons_1.IconWarning color="gray300" size="lg"/>
                  </errorPanel_1.default>);
                }
                const series = results
                    ? results.map((values, i) => (Object.assign(Object.assign({}, values), { yAxisIndex: i, xAxisIndex: i })))
                    : [];
                return (<transitionChart_1.default loading={loading} reloading={reloading} height="580px">
                  <transparentLoadingMask_1.default visible={reloading}/>
                  <lineChart_1.default {...zoomRenderProps} {...chartOptions} series={series}/>
                </transitionChart_1.default>);
            }}
          </eventsRequest_1.default>)}
      </chartZoom_1.default>
    </RelativeBox>);
}
function ChartSummaryValue({ error, isLoading, value }) {
    if (error) {
        return <div>{'\u2014'}</div>;
    }
    else if (isLoading) {
        return <placeholder_1.default height="24px"/>;
    }
    else {
        return <ChartValue>{value}</ChartValue>;
    }
}
const RelativeBox = (0, styled_1.default)('div') `
  position: relative;
`;
const ChartTitle = (0, styled_1.default)(styles_1.SectionHeading) `
  margin: 0;
`;
const ChartLabel = (0, styled_1.default)('div') `
  position: absolute;
  top: ${p => p.top};
  z-index: 1;
`;
const ChartValue = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeExtraLarge};
`;
exports.default = (0, react_router_1.withRouter)(SidebarCharts);
//# sourceMappingURL=sidebarCharts.jsx.map