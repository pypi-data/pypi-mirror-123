Object.defineProperty(exports, "__esModule", { value: true });
exports.UsageChart = exports.SeriesTypes = exports.CHART_OPTIONS_DATA_TRANSFORM = exports.ChartDataTransform = exports.CHART_OPTIONS_DATACATEGORY = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const color_1 = (0, tslib_1.__importDefault)(require("color"));
const baseChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/baseChart"));
const legend_1 = (0, tslib_1.__importDefault)(require("app/components/charts/components/legend"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/charts/components/tooltip"));
const xAxis_1 = (0, tslib_1.__importDefault)(require("app/components/charts/components/xAxis"));
const barSeries_1 = (0, tslib_1.__importDefault)(require("app/components/charts/series/barSeries"));
const styles_1 = require("app/components/charts/styles");
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const panel_1 = (0, tslib_1.__importDefault)(require("app/components/panels/panel"));
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const types_1 = require("app/types");
const dates_1 = require("app/utils/dates");
const formatters_1 = require("app/utils/formatters");
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const utils_1 = require("../utils");
const utils_2 = require("./utils");
const COLOR_ERRORS = (0, color_1.default)(theme_1.default.dataCategory.errors).lighten(0.25).string();
const COLOR_TRANSACTIONS = (0, color_1.default)(theme_1.default.dataCategory.transactions)
    .lighten(0.35)
    .string();
const COLOR_ATTACHMENTS = (0, color_1.default)(theme_1.default.dataCategory.attachments)
    .lighten(0.65)
    .string();
const COLOR_DROPPED = theme_1.default.red300;
const COLOR_PROJECTED = theme_1.default.gray100;
const COLOR_FILTERED = theme_1.default.pink100;
exports.CHART_OPTIONS_DATACATEGORY = [
    {
        label: types_1.DataCategoryName[types_1.DataCategory.ERRORS],
        value: types_1.DataCategory.ERRORS,
        disabled: false,
    },
    {
        label: types_1.DataCategoryName[types_1.DataCategory.TRANSACTIONS],
        value: types_1.DataCategory.TRANSACTIONS,
        disabled: false,
    },
    {
        label: types_1.DataCategoryName[types_1.DataCategory.ATTACHMENTS],
        value: types_1.DataCategory.ATTACHMENTS,
        disabled: false,
    },
];
var ChartDataTransform;
(function (ChartDataTransform) {
    ChartDataTransform["CUMULATIVE"] = "cumulative";
    ChartDataTransform["PERIODIC"] = "periodic";
})(ChartDataTransform = exports.ChartDataTransform || (exports.ChartDataTransform = {}));
exports.CHART_OPTIONS_DATA_TRANSFORM = [
    {
        label: (0, locale_1.t)('Cumulative'),
        value: ChartDataTransform.CUMULATIVE,
        disabled: false,
    },
    {
        label: (0, locale_1.t)('Periodic'),
        value: ChartDataTransform.PERIODIC,
        disabled: false,
    },
];
var SeriesTypes;
(function (SeriesTypes) {
    SeriesTypes["ACCEPTED"] = "Accepted";
    SeriesTypes["DROPPED"] = "Dropped";
    SeriesTypes["PROJECTED"] = "Projected";
    SeriesTypes["FILTERED"] = "Filtered";
})(SeriesTypes = exports.SeriesTypes || (exports.SeriesTypes = {}));
class UsageChart extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            xAxisDates: [],
        };
    }
    /**
     * UsageChart needs to generate the X-Axis dates as props.usageStats may
     * not pass the complete range of X-Axis data points
     *
     * E.g. usageStats.accepted covers day 1-15 of a month, usageStats.projected
     * either covers day 16-30 or may not be available at all.
     */
    static getDerivedStateFromProps(nextProps, prevState) {
        const { usageDateStart, usageDateEnd, usageDateShowUtc, usageDateInterval } = nextProps;
        return Object.assign(Object.assign({}, prevState), { xAxisDates: (0, utils_2.getXAxisDates)(usageDateStart, usageDateEnd, usageDateShowUtc, usageDateInterval) });
    }
    get chartColors() {
        const { dataCategory } = this.props;
        if (dataCategory === types_1.DataCategory.ERRORS) {
            return [COLOR_ERRORS, COLOR_FILTERED, COLOR_DROPPED, COLOR_PROJECTED];
        }
        if (dataCategory === types_1.DataCategory.ATTACHMENTS) {
            return [COLOR_ATTACHMENTS, COLOR_FILTERED, COLOR_DROPPED, COLOR_PROJECTED];
        }
        return [COLOR_TRANSACTIONS, COLOR_FILTERED, COLOR_DROPPED, COLOR_PROJECTED];
    }
    get chartMetadata() {
        const { usageDateStart, usageDateEnd } = this.props;
        const { usageDateInterval, usageStats, dataCategory, dataTransform, handleDataTransformation, } = this.props;
        const { xAxisDates } = this.state;
        const selectDataCategory = exports.CHART_OPTIONS_DATACATEGORY.find(o => o.value === dataCategory);
        if (!selectDataCategory) {
            throw new Error('Selected item is not supported');
        }
        // Do not assume that handleDataTransformation is a pure function
        const chartData = Object.assign({}, handleDataTransformation(usageStats, dataTransform));
        Object.keys(chartData).forEach(k => {
            const isProjected = k === SeriesTypes.PROJECTED;
            // Map the array and destructure elements to avoid side-effects
            chartData[k] = chartData[k].map(stat => {
                return Object.assign(Object.assign({}, stat), { tooltip: { show: false }, itemStyle: { opacity: isProjected ? 0.6 : 1 } });
            });
        });
        // Use hours as common units
        const dataPeriod = (0, dates_1.statsPeriodToDays)(undefined, usageDateStart, usageDateEnd) * 24;
        const barPeriod = (0, dates_1.parsePeriodToHours)(usageDateInterval);
        if (dataPeriod < 0 || barPeriod < 0) {
            throw new Error('UsageChart: Unable to parse data time period');
        }
        const { xAxisTickInterval, xAxisLabelInterval } = (0, utils_2.getXAxisLabelInterval)(dataPeriod, dataPeriod / barPeriod);
        const { label, value } = selectDataCategory;
        if (value === types_1.DataCategory.ERRORS || value === types_1.DataCategory.TRANSACTIONS) {
            return {
                chartLabel: label,
                chartData,
                xAxisData: xAxisDates,
                xAxisTickInterval,
                xAxisLabelInterval,
                yAxisMinInterval: 100,
                yAxisFormatter: formatters_1.formatAbbreviatedNumber,
                tooltipValueFormatter: (0, utils_2.getTooltipFormatter)(dataCategory),
            };
        }
        return {
            chartLabel: label,
            chartData,
            xAxisData: xAxisDates,
            xAxisTickInterval,
            xAxisLabelInterval,
            yAxisMinInterval: 0.5 * utils_1.GIGABYTE,
            yAxisFormatter: (val) => (0, utils_1.formatUsageWithUnits)(val, types_1.DataCategory.ATTACHMENTS, {
                isAbbreviated: true,
                useUnitScaling: true,
            }),
            tooltipValueFormatter: (0, utils_2.getTooltipFormatter)(dataCategory),
        };
    }
    get chartSeries() {
        const { chartSeries } = this.props;
        const { chartData } = this.chartMetadata;
        let series = [
            (0, barSeries_1.default)({
                name: SeriesTypes.ACCEPTED,
                data: chartData.accepted,
                barMinHeight: 1,
                stack: 'usage',
                legendHoverLink: false,
            }),
            (0, barSeries_1.default)({
                name: SeriesTypes.FILTERED,
                data: chartData.filtered,
                barMinHeight: 1,
                stack: 'usage',
                legendHoverLink: false,
            }),
            (0, barSeries_1.default)({
                name: SeriesTypes.DROPPED,
                data: chartData.dropped,
                stack: 'usage',
                legendHoverLink: false,
            }),
            (0, barSeries_1.default)({
                name: SeriesTypes.PROJECTED,
                data: chartData.projected,
                barMinHeight: 1,
                stack: 'usage',
                legendHoverLink: false,
            }),
        ];
        // Additional series passed by parent component
        if (chartSeries) {
            series = series.concat(chartSeries);
        }
        return series;
    }
    get chartLegend() {
        const { chartData } = this.chartMetadata;
        const legend = [
            {
                name: SeriesTypes.ACCEPTED,
            },
        ];
        if (chartData.filtered && chartData.filtered.length > 0) {
            legend.push({
                name: SeriesTypes.FILTERED,
            });
        }
        if (chartData.dropped.length > 0) {
            legend.push({
                name: SeriesTypes.DROPPED,
            });
        }
        if (chartData.projected.length > 0) {
            legend.push({
                name: SeriesTypes.PROJECTED,
            });
        }
        return legend;
    }
    get chartTooltip() {
        const { chartTooltip } = this.props;
        if (chartTooltip) {
            return chartTooltip;
        }
        const { tooltipValueFormatter } = this.chartMetadata;
        return (0, tooltip_1.default)({
            // Trigger to axis prevents tooltip from redrawing when hovering
            // over individual bars
            trigger: 'axis',
            valueFormatter: tooltipValueFormatter,
        });
    }
    renderChart() {
        const { theme, title, isLoading, isError, errors } = this.props;
        if (isLoading) {
            return (<placeholder_1.default height="200px">
          <loadingIndicator_1.default mini/>
        </placeholder_1.default>);
        }
        if (isError) {
            return (<placeholder_1.default height="200px">
          <icons_1.IconWarning size={theme.fontSizeExtraLarge}/>
          <ErrorMessages>
            {errors &&
                    Object.keys(errors).map(k => { var _a; return <span key={k}>{(_a = errors[k]) === null || _a === void 0 ? void 0 : _a.message}</span>; })}
          </ErrorMessages>
        </placeholder_1.default>);
        }
        const { xAxisData, xAxisTickInterval, xAxisLabelInterval, yAxisMinInterval, yAxisFormatter, } = this.chartMetadata;
        return (<React.Fragment>
        <styles_1.HeaderTitleLegend>{title || (0, locale_1.t)('Current Usage Period')}</styles_1.HeaderTitleLegend>
        <baseChart_1.default colors={this.chartColors} grid={{ bottom: '3px', left: '0px', right: '10px', top: '40px' }} xAxis={(0, xAxis_1.default)({
                show: true,
                type: 'category',
                name: 'Date',
                boundaryGap: true,
                data: xAxisData,
                axisTick: {
                    interval: xAxisTickInterval,
                    alignWithLabel: true,
                },
                axisLabel: {
                    interval: xAxisLabelInterval,
                    formatter: (label) => label.slice(0, 6), // Limit label to 6 chars
                },
                theme,
            })} yAxis={{
                min: 0,
                minInterval: yAxisMinInterval,
                axisLabel: {
                    formatter: yAxisFormatter,
                    color: theme.chartLabel,
                },
            }} series={this.chartSeries} tooltip={this.chartTooltip} onLegendSelectChanged={() => { }} legend={(0, legend_1.default)({
                right: 10,
                top: 5,
                data: this.chartLegend,
                theme,
            })}/>
      </React.Fragment>);
    }
    render() {
        const { footer } = this.props;
        return (<panel_1.default id="usage-chart">
        <styles_1.ChartContainer>{this.renderChart()}</styles_1.ChartContainer>
        {footer}
      </panel_1.default>);
    }
}
exports.UsageChart = UsageChart;
UsageChart.defaultProps = {
    usageDateShowUtc: true,
    usageDateInterval: '1d',
    handleDataTransformation: (stats, transform) => {
        const chartData = {
            accepted: [],
            dropped: [],
            projected: [],
            filtered: [],
        };
        const isCumulative = transform === ChartDataTransform.CUMULATIVE;
        Object.keys(stats).forEach(k => {
            let count = 0;
            chartData[k] = stats[k].map(stat => {
                const [x, y] = stat.value;
                count = isCumulative ? count + y : y;
                return Object.assign(Object.assign({}, stat), { value: [x, count] });
            });
        });
        return chartData;
    },
};
exports.default = (0, react_1.withTheme)(UsageChart);
const ErrorMessages = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: column;

  margin-top: ${(0, space_1.default)(1)};
  font-size: ${p => p.theme.fontSizeSmall};
`;
//# sourceMappingURL=index.jsx.map