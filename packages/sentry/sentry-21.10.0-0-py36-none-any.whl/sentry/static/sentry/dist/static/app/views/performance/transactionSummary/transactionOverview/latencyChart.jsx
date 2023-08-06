Object.defineProperty(exports, "__esModule", { value: true });
exports.decodeHistogramZoom = exports.LatencyChartControls = exports.ZOOM_END = exports.ZOOM_START = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const barChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/barChart"));
const barChartZoom_1 = (0, tslib_1.__importDefault)(require("app/components/charts/barChartZoom"));
const errorPanel_1 = (0, tslib_1.__importDefault)(require("app/components/charts/errorPanel"));
const loadingPanel_1 = (0, tslib_1.__importDefault)(require("app/components/charts/loadingPanel"));
const optionSelector_1 = (0, tslib_1.__importDefault)(require("app/components/charts/optionSelector"));
const styles_1 = require("app/components/charts/styles");
const questionTooltip_1 = (0, tslib_1.__importDefault)(require("app/components/questionTooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const analytics_1 = require("app/utils/analytics");
const eventView_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/eventView"));
const histogram_1 = (0, tslib_1.__importDefault)(require("app/utils/performance/histogram"));
const histogramQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/performance/histogram/histogramQuery"));
const utils_1 = require("app/utils/performance/histogram/utils");
const queryString_1 = require("app/utils/queryString");
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const filter_1 = require("../filter");
exports.ZOOM_START = 'startDuration';
exports.ZOOM_END = 'endDuration';
const NUM_BUCKETS = 50;
const QUERY_KEYS = [
    'environment',
    'project',
    'query',
    'start',
    'end',
    'statsPeriod',
];
/**
 * Fetch and render a bar chart that shows event volume
 * for each duration bucket. We always render 50 buckets of
 * equal widths based on the endpoints min + max durations.
 *
 * This graph visualizes how many transactions were recorded
 * at each duration bucket, showing the modality of the transaction.
 */
class LatencyChart extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            zoomError: false,
        };
        this.handleMouseOver = () => {
            // Hide the zoom error tooltip on the next hover.
            if (this.state.zoomError) {
                this.setState({ zoomError: false });
            }
        };
        this.handleDataZoom = () => {
            const { organization } = this.props;
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'performance_views.latency_chart.zoom',
                eventName: 'Performance Views: Transaction Summary Latency Chart Zoom',
                organization_id: parseInt(organization.id, 10),
            });
        };
        this.handleDataZoomCancelled = () => {
            this.setState({ zoomError: true });
        };
    }
    bucketWidth(data) {
        // We can assume that all buckets are of equal width, use the first two
        // buckets to get the width. The value of each histogram function indicates
        // the beginning of the bucket.
        return data.length > 2 ? data[1].bin - data[0].bin : 0;
    }
    renderLoading() {
        return <loadingPanel_1.default data-test-id="histogram-loading"/>;
    }
    renderError() {
        // Don't call super as we don't really need issues for this.
        return (<errorPanel_1.default>
        <icons_1.IconWarning color="gray300" size="lg"/>
      </errorPanel_1.default>);
    }
    renderChart(data) {
        const { location, currentFilter } = this.props;
        const { zoomError } = this.state;
        const xAxis = {
            type: 'category',
            truncate: true,
            axisTick: {
                interval: 0,
                alignWithLabel: true,
            },
        };
        const colors = currentFilter === filter_1.SpanOperationBreakdownFilter.None
            ? [...theme_1.default.charts.getColorPalette(1)]
            : [(0, filter_1.filterToColor)(currentFilter)];
        // Use a custom tooltip formatter as we need to replace
        // the tooltip content entirely when zooming is no longer available.
        const tooltip = {
            formatter(series) {
                const seriesData = Array.isArray(series) ? series : [series];
                let contents = [];
                if (!zoomError) {
                    // Replicate the necessary logic from app/components/charts/components/tooltip.jsx
                    contents = seriesData.map(item => {
                        const label = item.seriesName;
                        const value = item.value[1].toLocaleString();
                        return [
                            '<div class="tooltip-series">',
                            `<div><span class="tooltip-label">${item.marker} <strong>${label}</strong></span> ${value}</div>`,
                            '</div>',
                        ].join('');
                    });
                    const seriesLabel = seriesData[0].value[0];
                    contents.push(`<div class="tooltip-date">${seriesLabel}</div>`);
                }
                else {
                    contents = [
                        '<div class="tooltip-series tooltip-series-solo">',
                        (0, locale_1.t)('Target zoom region too small'),
                        '</div>',
                    ];
                }
                contents.push('<div class="tooltip-arrow"></div>');
                return contents.join('');
            },
        };
        const series = {
            seriesName: (0, locale_1.t)('Count'),
            data: (0, utils_1.formatHistogramData)(data, { type: 'duration' }),
        };
        return (<barChartZoom_1.default minZoomWidth={NUM_BUCKETS} location={location} paramStart={exports.ZOOM_START} paramEnd={exports.ZOOM_END} xAxisIndex={[0]} buckets={(0, utils_1.computeBuckets)(data)} onDataZoomCancelled={this.handleDataZoomCancelled}>
        {zoomRenderProps => (<barChart_1.default grid={{ left: '10px', right: '10px', top: '40px', bottom: '0px' }} xAxis={xAxis} yAxis={{ type: 'value' }} series={[series]} tooltip={tooltip} colors={colors} onMouseOver={this.handleMouseOver} {...zoomRenderProps}/>)}
      </barChartZoom_1.default>);
    }
    render() {
        var _a;
        const { organization, query, start, end, statsPeriod, environment, project, location, currentFilter, } = this.props;
        const eventView = eventView_1.default.fromNewQueryWithLocation({
            id: undefined,
            version: 2,
            name: '',
            fields: ['transaction.duration'],
            projects: project,
            range: statsPeriod,
            query,
            environment,
            start,
            end,
        }, location);
        const { min, max } = decodeHistogramZoom(location);
        const field = (_a = (0, filter_1.filterToField)(currentFilter)) !== null && _a !== void 0 ? _a : 'transaction.duration';
        const headerTitle = currentFilter === filter_1.SpanOperationBreakdownFilter.None
            ? (0, locale_1.t)('Duration Distribution')
            : (0, locale_1.tct)('Span Operation Distribution - [operationName]', {
                operationName: currentFilter,
            });
        return (<react_1.Fragment>
        <styles_1.HeaderTitleLegend>
          {headerTitle}
          <questionTooltip_1.default position="top" size="sm" title={(0, locale_1.t)(`Duration Distribution reflects the volume of transactions per median duration.`)}/>
        </styles_1.HeaderTitleLegend>
        <histogram_1.default location={location} zoomKeys={[exports.ZOOM_START, exports.ZOOM_END]}>
          {({ activeFilter }) => (<histogramQuery_1.default location={location} orgSlug={organization.slug} eventView={eventView} numBuckets={NUM_BUCKETS} fields={[field]} min={min} max={max} dataFilter={activeFilter.value}>
              {({ histograms, isLoading, error }) => {
                    var _a;
                    if (isLoading) {
                        return this.renderLoading();
                    }
                    else if (error) {
                        return this.renderError();
                    }
                    const data = (_a = histograms === null || histograms === void 0 ? void 0 : histograms[field]) !== null && _a !== void 0 ? _a : [];
                    return this.renderChart(data);
                }}
            </histogramQuery_1.default>)}
        </histogram_1.default>
      </react_1.Fragment>);
    }
}
function LatencyChartControls(props) {
    const { location } = props;
    return (<histogram_1.default location={location} zoomKeys={[exports.ZOOM_START, exports.ZOOM_END]}>
      {({ filterOptions, handleFilterChange, activeFilter }) => {
            return (<react_1.Fragment>
            <optionSelector_1.default title={(0, locale_1.t)('Outliers')} selected={activeFilter.value} options={filterOptions} onChange={handleFilterChange}/>
          </react_1.Fragment>);
        }}
    </histogram_1.default>);
}
exports.LatencyChartControls = LatencyChartControls;
function decodeHistogramZoom(location) {
    let min = undefined;
    let max = undefined;
    if (exports.ZOOM_START in location.query) {
        min = (0, queryString_1.decodeInteger)(location.query[exports.ZOOM_START], 0);
    }
    if (exports.ZOOM_END in location.query) {
        const decodedMax = (0, queryString_1.decodeInteger)(location.query[exports.ZOOM_END]);
        if (typeof decodedMax === 'number') {
            max = decodedMax;
        }
    }
    return { min, max };
}
exports.decodeHistogramZoom = decodeHistogramZoom;
exports.default = LatencyChart;
//# sourceMappingURL=latencyChart.jsx.map