Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const areaChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/areaChart"));
const errorPanel_1 = (0, tslib_1.__importDefault)(require("app/components/charts/errorPanel"));
const loadingPanel_1 = (0, tslib_1.__importDefault)(require("app/components/charts/loadingPanel"));
const styles_1 = require("app/components/charts/styles");
const questionTooltip_1 = (0, tslib_1.__importDefault)(require("app/components/questionTooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const utils_1 = require("app/utils");
const charts_1 = require("app/utils/discover/charts");
const eventView_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/eventView"));
const formatters_1 = require("app/utils/formatters");
const filter_1 = require("../filter");
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
 * for each duration bucket. We always render 15 buckets of
 * equal widths based on the endpoints min + max durations.
 *
 * This graph visualizes how many transactions were recorded
 * at each duration bucket, showing the modality of the transaction.
 */
class DurationPercentileChart extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.generateFields = () => {
            const { currentFilter } = this.props;
            if (currentFilter === filter_1.SpanOperationBreakdownFilter.None) {
                return [
                    'percentile(transaction.duration, 0.10)',
                    'percentile(transaction.duration, 0.25)',
                    'percentile(transaction.duration, 0.50)',
                    'percentile(transaction.duration, 0.75)',
                    'percentile(transaction.duration, 0.90)',
                    'percentile(transaction.duration, 0.95)',
                    'percentile(transaction.duration, 0.99)',
                    'percentile(transaction.duration, 0.995)',
                    'percentile(transaction.duration, 0.999)',
                    'p100()',
                ];
            }
            const field = (0, filter_1.filterToField)(currentFilter);
            return [
                `percentile(${field}, 0.10)`,
                `percentile(${field}, 0.25)`,
                `percentile(${field}, 0.50)`,
                `percentile(${field}, 0.75)`,
                `percentile(${field}, 0.90)`,
                `percentile(${field}, 0.95)`,
                `percentile(${field}, 0.99)`,
                `percentile(${field}, 0.995)`,
                `percentile(${field}, 0.999)`,
                `p100(${field})`,
            ];
        };
        this.getEndpoints = () => {
            const { organization, query, start, end, statsPeriod, environment, project, location } = this.props;
            const eventView = eventView_1.default.fromSavedQuery({
                id: '',
                name: '',
                version: 2,
                fields: this.generateFields(),
                orderby: '',
                projects: project,
                range: statsPeriod,
                query,
                environment,
                start,
                end,
            });
            const apiPayload = eventView.getEventsAPIPayload(location);
            apiPayload.referrer = 'api.performance.durationpercentilechart';
            return [
                ['chartData', `/organizations/${organization.slug}/eventsv2/`, { query: apiPayload }],
            ];
        };
    }
    componentDidUpdate(prevProps) {
        if (this.shouldRefetchData(prevProps)) {
            this.fetchData();
        }
    }
    shouldRefetchData(prevProps) {
        if (this.state.loading) {
            return false;
        }
        return !(0, isEqual_1.default)((0, pick_1.default)(prevProps, QUERY_KEYS), (0, pick_1.default)(this.props, QUERY_KEYS));
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
    renderBody() {
        const { currentFilter } = this.props;
        const { chartData } = this.state;
        if (!(0, utils_1.defined)(chartData)) {
            return null;
        }
        const colors = (theme) => currentFilter === filter_1.SpanOperationBreakdownFilter.None
            ? theme.charts.getColorPalette(1)
            : [(0, filter_1.filterToColor)(currentFilter)];
        return <StyledAreaChart series={transformData(chartData.data)} colors={colors}/>;
    }
    render() {
        const { currentFilter } = this.props;
        const headerTitle = currentFilter === filter_1.SpanOperationBreakdownFilter.None
            ? (0, locale_1.t)('Duration Percentiles')
            : (0, locale_1.tct)('Span Operation Percentiles - [operationName]', {
                operationName: currentFilter,
            });
        return (<React.Fragment>
        <styles_1.HeaderTitleLegend>
          {headerTitle}
          <questionTooltip_1.default position="top" size="sm" title={(0, locale_1.t)(`Compare the duration at each percentile. Compare with Latency Histogram to see transaction volume at duration intervals.`)}/>
        </styles_1.HeaderTitleLegend>
        {this.renderComponent()}
      </React.Fragment>);
    }
}
function StyledAreaChart(props) {
    const theme = (0, react_1.useTheme)();
    return (<areaChart_1.default grid={{ left: '10px', right: '10px', top: '40px', bottom: '0px' }} xAxis={{
            type: 'category',
            truncate: true,
            axisLabel: {
                showMinLabel: true,
                showMaxLabel: true,
            },
            axisTick: {
                interval: 0,
                alignWithLabel: true,
            },
        }} yAxis={{
            type: 'value',
            axisLabel: {
                color: theme.chartLabel,
                // Use p50() to force time formatting.
                formatter: (value) => (0, charts_1.axisLabelFormatter)(value, 'p50()'),
            },
        }} tooltip={{ valueFormatter: value => (0, formatters_1.getDuration)(value / 1000, 2) }} {...props}/>);
}
const VALUE_EXTRACT_PATTERN = /(\d+)$/;
/**
 * Convert a discover response into a barchart compatible series
 */
function transformData(data) {
    const extractedData = Object.keys(data[0])
        .map((key) => {
        const nameMatch = VALUE_EXTRACT_PATTERN.exec(key);
        if (!nameMatch) {
            return [-1, -1];
        }
        let nameValue = Number(nameMatch[1]);
        if (nameValue > 100) {
            nameValue /= 10;
        }
        return [nameValue, data[0][key]];
    })
        .filter(i => i[0] > 0);
    extractedData.sort((a, b) => {
        if (a[0] > b[0]) {
            return 1;
        }
        if (a[0] < b[0]) {
            return -1;
        }
        return 0;
    });
    return [
        {
            seriesName: (0, locale_1.t)('Duration'),
            data: extractedData.map(i => ({ value: i[1], name: `${i[0].toLocaleString()}%` })),
        },
    ];
}
exports.default = DurationPercentileChart;
//# sourceMappingURL=durationPercentileChart.jsx.map