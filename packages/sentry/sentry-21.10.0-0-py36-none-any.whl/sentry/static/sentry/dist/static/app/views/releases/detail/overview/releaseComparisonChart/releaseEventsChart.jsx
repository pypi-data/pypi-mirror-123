Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const react_2 = require("@emotion/react");
const api_1 = require("app/api");
const eventsChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/eventsChart"));
const eventsRequest_1 = (0, tslib_1.__importDefault)(require("app/components/charts/eventsRequest"));
const styles_1 = require("app/components/charts/styles");
const utils_1 = require("app/components/charts/utils");
const questionTooltip_1 = (0, tslib_1.__importDefault)(require("app/components/questionTooltip"));
const locale_1 = require("app/locale");
const types_1 = require("app/types");
const charts_1 = require("app/utils/discover/charts");
const tokenizeSearch_1 = require("app/utils/tokenizeSearch");
const useApi_1 = (0, tslib_1.__importDefault)(require("app/utils/useApi"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const data_1 = require("app/views/performance/data");
const utils_2 = require("../../utils");
function ReleaseEventsChart({ release, project, chartType, value, diff, organization, router, period, start, end, utc, location, }) {
    const api = (0, useApi_1.default)();
    const theme = (0, react_2.useTheme)();
    function getColors() {
        const colors = theme.charts.getColorPalette(14);
        switch (chartType) {
            case types_1.ReleaseComparisonChartType.ERROR_COUNT:
                return [colors[12]];
            case types_1.ReleaseComparisonChartType.TRANSACTION_COUNT:
                return [colors[0]];
            case types_1.ReleaseComparisonChartType.FAILURE_RATE:
                return [colors[9]];
            default:
                return undefined;
        }
    }
    function getQuery() {
        const releaseFilter = `release:${release.version}`;
        switch (chartType) {
            case types_1.ReleaseComparisonChartType.ERROR_COUNT:
                return new tokenizeSearch_1.MutableSearch([
                    '!event.type:transaction',
                    releaseFilter,
                ]).formatString();
            case types_1.ReleaseComparisonChartType.TRANSACTION_COUNT:
                return new tokenizeSearch_1.MutableSearch([
                    'event.type:transaction',
                    releaseFilter,
                ]).formatString();
            case types_1.ReleaseComparisonChartType.FAILURE_RATE:
                return new tokenizeSearch_1.MutableSearch([
                    'event.type:transaction',
                    releaseFilter,
                ]).formatString();
            default:
                return '';
        }
    }
    function getField() {
        switch (chartType) {
            case types_1.ReleaseComparisonChartType.ERROR_COUNT:
                return ['count()'];
            case types_1.ReleaseComparisonChartType.TRANSACTION_COUNT:
                return ['count()'];
            case types_1.ReleaseComparisonChartType.FAILURE_RATE:
                return ['failure_rate()'];
            default:
                return undefined;
        }
    }
    function getYAxis() {
        switch (chartType) {
            case types_1.ReleaseComparisonChartType.ERROR_COUNT:
                return 'count()';
            case types_1.ReleaseComparisonChartType.TRANSACTION_COUNT:
                return 'count()';
            case types_1.ReleaseComparisonChartType.FAILURE_RATE:
                return 'failure_rate()';
            default:
                return '';
        }
    }
    function getHelp() {
        switch (chartType) {
            case types_1.ReleaseComparisonChartType.FAILURE_RATE:
                return (0, data_1.getTermHelp)(organization, data_1.PERFORMANCE_TERM.FAILURE_RATE);
            default:
                return null;
        }
    }
    const projects = location.query.project;
    const environments = location.query.environment;
    const markLines = (0, utils_2.generateReleaseMarkLines)(release, project, theme, location);
    return (
    /**
     * EventsRequest is used to fetch the second series of Failure Rate chart.
     * First one is "This Release" - fetched as usual inside EventsChart
     * component and this one is "All Releases" that's shoehorned in place
     * of Previous Period via previousSeriesTransformer
     */
    <eventsRequest_1.default organization={organization} api={new api_1.Client()} period={period} project={projects} environment={environments} start={start} end={end} interval={(0, utils_1.getInterval)({ start, end, period, utc }, 'high')} query="event.type:transaction" includePrevious={false} currentSeriesNames={[(0, locale_1.t)('All Releases')]} yAxis={getYAxis()} field={getField()} confirmedQuery={chartType === types_1.ReleaseComparisonChartType.FAILURE_RATE} partial referrer="api.releases.release-details-chart">
      {({ timeseriesData, loading, reloading }) => (<eventsChart_1.default query={getQuery()} yAxis={getYAxis()} field={getField()} colors={getColors()} api={api} router={router} organization={organization} disableReleases disablePrevious showLegend projects={projects} environments={environments} start={start} end={end} period={period !== null && period !== void 0 ? period : undefined} utc={utc} currentSeriesName={(0, locale_1.t)('This Release') + (loading || reloading ? ' ' : '')} // HACK: trigger echarts rerender without remounting
         previousSeriesName={(0, locale_1.t)('All Releases')} disableableSeries={[(0, locale_1.t)('This Release'), (0, locale_1.t)('All Releases')]} chartHeader={<react_1.Fragment>
              <styles_1.HeaderTitleLegend>
                {utils_2.releaseComparisonChartTitles[chartType]}
                {getHelp() && (<questionTooltip_1.default size="sm" position="top" title={getHelp()}/>)}
              </styles_1.HeaderTitleLegend>

              <styles_1.HeaderValue>
                {value} {diff}
              </styles_1.HeaderValue>
            </react_1.Fragment>} legendOptions={{ right: 10, top: 0 }} chartOptions={{
                grid: { left: '10px', right: '10px', top: '70px', bottom: '0px' },
                tooltip: {
                    trigger: 'axis',
                    truncate: 80,
                    valueFormatter: (val, label) => {
                        if (label && Object.values(utils_2.releaseMarkLinesLabels).includes(label)) {
                            return '';
                        }
                        return (0, charts_1.tooltipFormatter)(val, getYAxis());
                    },
                },
            }} usePageZoom height={240} seriesTransformer={series => [...series, ...markLines]} previousSeriesTransformer={series => {
                if (chartType === types_1.ReleaseComparisonChartType.FAILURE_RATE) {
                    return timeseriesData === null || timeseriesData === void 0 ? void 0 : timeseriesData[0];
                }
                return series;
            }} referrer="api.releases.release-details-chart"/>)}
    </eventsRequest_1.default>);
}
exports.default = (0, withOrganization_1.default)((0, react_router_1.withRouter)(ReleaseEventsChart));
//# sourceMappingURL=releaseEventsChart.jsx.map