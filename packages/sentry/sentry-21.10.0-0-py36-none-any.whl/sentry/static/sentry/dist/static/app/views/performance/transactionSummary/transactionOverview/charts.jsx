Object.defineProperty(exports, "__esModule", { value: true });
exports.DisplayModes = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const optionSelector_1 = (0, tslib_1.__importDefault)(require("app/components/charts/optionSelector"));
const styles_1 = require("app/components/charts/styles");
const panels_1 = require("app/components/panels");
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const locale_1 = require("app/locale");
const histogram_1 = require("app/utils/performance/histogram");
const queryString_1 = require("app/utils/queryString");
const overview_1 = require("app/views/releases/detail/overview");
const types_1 = require("../../trends/types");
const utils_1 = require("../../trends/utils");
const filter_1 = require("../filter");
const durationChart_1 = (0, tslib_1.__importDefault)(require("./durationChart"));
const durationPercentileChart_1 = (0, tslib_1.__importDefault)(require("./durationPercentileChart"));
const latencyChart_1 = (0, tslib_1.__importStar)(require("./latencyChart"));
const trendChart_1 = (0, tslib_1.__importDefault)(require("./trendChart"));
const vitalsChart_1 = (0, tslib_1.__importDefault)(require("./vitalsChart"));
var DisplayModes;
(function (DisplayModes) {
    DisplayModes["DURATION_PERCENTILE"] = "durationpercentile";
    DisplayModes["DURATION"] = "duration";
    DisplayModes["LATENCY"] = "latency";
    DisplayModes["TREND"] = "trend";
    DisplayModes["VITALS"] = "vitals";
})(DisplayModes = exports.DisplayModes || (exports.DisplayModes = {}));
function generateDisplayOptions(currentFilter) {
    if (currentFilter === filter_1.SpanOperationBreakdownFilter.None) {
        return [
            { value: DisplayModes.DURATION, label: (0, locale_1.t)('Duration Breakdown') },
            { value: DisplayModes.DURATION_PERCENTILE, label: (0, locale_1.t)('Duration Percentiles') },
            { value: DisplayModes.LATENCY, label: (0, locale_1.t)('Duration Distribution') },
            { value: DisplayModes.TREND, label: (0, locale_1.t)('Trends') },
            { value: DisplayModes.VITALS, label: (0, locale_1.t)('Web Vitals') },
        ];
    }
    // A span operation name breakdown has been chosen.
    return [
        { value: DisplayModes.DURATION, label: (0, locale_1.t)('Span Operation Breakdown') },
        { value: DisplayModes.DURATION_PERCENTILE, label: (0, locale_1.t)('Span Operation Percentiles') },
        { value: DisplayModes.LATENCY, label: (0, locale_1.t)('Span Operation Distribution') },
        { value: DisplayModes.TREND, label: (0, locale_1.t)('Trends') },
        { value: DisplayModes.VITALS, label: (0, locale_1.t)('Web Vitals') },
    ];
}
const TREND_FUNCTIONS_OPTIONS = utils_1.TRENDS_FUNCTIONS.map(({ field, label }) => ({
    value: field,
    label,
}));
class TransactionSummaryCharts extends react_1.Component {
    constructor() {
        super(...arguments);
        this.handleDisplayChange = (value) => {
            const { location } = this.props;
            react_router_1.browserHistory.push({
                pathname: location.pathname,
                query: Object.assign(Object.assign({}, (0, histogram_1.removeHistogramQueryStrings)(location, [latencyChart_1.ZOOM_START, latencyChart_1.ZOOM_END])), { display: value }),
            });
        };
        this.handleTrendDisplayChange = (value) => {
            const { location } = this.props;
            react_router_1.browserHistory.push({
                pathname: location.pathname,
                query: Object.assign(Object.assign({}, location.query), { trendFunction: value }),
            });
        };
        this.handleTrendColumnChange = (value) => {
            const { location } = this.props;
            react_router_1.browserHistory.push({
                pathname: location.pathname,
                query: Object.assign(Object.assign({}, location.query), { trendColumn: value }),
            });
        };
    }
    render() {
        const { totalValues, eventView, organization, location, currentFilter, withoutZerofill, } = this.props;
        const TREND_PARAMETERS_OPTIONS = utils_1.TRENDS_PARAMETERS.map(({ column, label }) => ({
            value: column,
            label,
        }));
        let display = (0, queryString_1.decodeScalar)(location.query.display, DisplayModes.DURATION);
        let trendFunction = (0, queryString_1.decodeScalar)(location.query.trendFunction, TREND_FUNCTIONS_OPTIONS[0].value);
        let trendColumn = (0, queryString_1.decodeScalar)(location.query.trendColumn, TREND_PARAMETERS_OPTIONS[0].value);
        if (!Object.values(DisplayModes).includes(display)) {
            display = DisplayModes.DURATION;
        }
        if (!Object.values(types_1.TrendFunctionField).includes(trendFunction)) {
            trendFunction = types_1.TrendFunctionField.P50;
        }
        if (!Object.values(types_1.TrendColumnField).includes(trendColumn)) {
            trendColumn = types_1.TrendColumnField.DURATION;
        }
        const releaseQueryExtra = {
            yAxis: display === DisplayModes.VITALS ? 'countVital' : 'countDuration',
            showTransactions: display === DisplayModes.VITALS
                ? overview_1.TransactionsListOption.SLOW_LCP
                : display === DisplayModes.DURATION
                    ? overview_1.TransactionsListOption.SLOW
                    : undefined,
        };
        return (<panels_1.Panel>
        <styles_1.ChartContainer>
          {display === DisplayModes.LATENCY && (<latencyChart_1.default organization={organization} location={location} query={eventView.query} project={eventView.project} environment={eventView.environment} start={eventView.start} end={eventView.end} statsPeriod={eventView.statsPeriod} currentFilter={currentFilter}/>)}
          {display === DisplayModes.DURATION && (<durationChart_1.default organization={organization} query={eventView.query} queryExtra={releaseQueryExtra} project={eventView.project} environment={eventView.environment} start={eventView.start} end={eventView.end} statsPeriod={eventView.statsPeriod} currentFilter={currentFilter} withoutZerofill={withoutZerofill}/>)}
          {display === DisplayModes.DURATION_PERCENTILE && (<durationPercentileChart_1.default organization={organization} location={location} query={eventView.query} project={eventView.project} environment={eventView.environment} start={eventView.start} end={eventView.end} statsPeriod={eventView.statsPeriod} currentFilter={currentFilter}/>)}
          {display === DisplayModes.TREND && (<trendChart_1.default trendDisplay={(0, utils_1.generateTrendFunctionAsString)(trendFunction, trendColumn)} organization={organization} query={eventView.query} queryExtra={releaseQueryExtra} project={eventView.project} environment={eventView.environment} start={eventView.start} end={eventView.end} statsPeriod={eventView.statsPeriod} withoutZerofill={withoutZerofill}/>)}
          {display === DisplayModes.VITALS && (<vitalsChart_1.default organization={organization} query={eventView.query} queryExtra={releaseQueryExtra} project={eventView.project} environment={eventView.environment} start={eventView.start} end={eventView.end} statsPeriod={eventView.statsPeriod} withoutZerofill={withoutZerofill}/>)}
        </styles_1.ChartContainer>

        <styles_1.ChartControls>
          <styles_1.InlineContainer>
            <styles_1.SectionHeading key="total-heading">{(0, locale_1.t)('Total Transactions')}</styles_1.SectionHeading>
            <styles_1.SectionValue key="total-value">
              {totalValues === null ? (<placeholder_1.default height="24px"/>) : (totalValues.toLocaleString())}
            </styles_1.SectionValue>
          </styles_1.InlineContainer>
          <styles_1.InlineContainer>
            {display === DisplayModes.TREND && (<optionSelector_1.default title={(0, locale_1.t)('Percentile')} selected={trendFunction} options={TREND_FUNCTIONS_OPTIONS} onChange={this.handleTrendDisplayChange}/>)}
            {display === DisplayModes.TREND && (<optionSelector_1.default title={(0, locale_1.t)('Parameter')} selected={trendColumn} options={TREND_PARAMETERS_OPTIONS} onChange={this.handleTrendColumnChange}/>)}
            {display === DisplayModes.LATENCY && (<latencyChart_1.LatencyChartControls location={location}/>)}
            <optionSelector_1.default title={(0, locale_1.t)('Display')} selected={display} options={generateDisplayOptions(currentFilter)} onChange={this.handleDisplayChange}/>
          </styles_1.InlineContainer>
        </styles_1.ChartControls>
      </panels_1.Panel>);
    }
}
exports.default = TransactionSummaryCharts;
//# sourceMappingURL=charts.jsx.map