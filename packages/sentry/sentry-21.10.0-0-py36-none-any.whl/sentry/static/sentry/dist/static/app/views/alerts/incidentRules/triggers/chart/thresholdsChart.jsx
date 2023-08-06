Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const color_1 = (0, tslib_1.__importDefault)(require("color"));
const debounce_1 = (0, tslib_1.__importDefault)(require("lodash/debounce"));
const flatten_1 = (0, tslib_1.__importDefault)(require("lodash/flatten"));
const graphic_1 = (0, tslib_1.__importDefault)(require("app/components/charts/components/graphic"));
const lineChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/lineChart"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const utils_1 = require("app/views/alerts/utils");
const types_1 = require("../../types");
const CHART_GRID = {
    left: (0, space_1.default)(2),
    right: (0, space_1.default)(2),
    top: (0, space_1.default)(4),
    bottom: (0, space_1.default)(2),
};
// Colors to use for trigger thresholds
const COLOR = {
    RESOLUTION_FILL: (0, color_1.default)(theme_1.default.green200).alpha(0.1).rgb().string(),
    CRITICAL_FILL: (0, color_1.default)(theme_1.default.red300).alpha(0.25).rgb().string(),
    WARNING_FILL: (0, color_1.default)(theme_1.default.yellow200).alpha(0.1).rgb().string(),
};
/**
 * This chart displays shaded regions that represent different Trigger thresholds in a
 * Metric Alert rule.
 */
class ThresholdsChart extends react_1.PureComponent {
    constructor() {
        super(...arguments);
        this.state = {
            width: -1,
            height: -1,
            yAxisMax: null,
            yAxisMin: null,
        };
        this.ref = null;
        // If we have ref to chart and data, try to update chart axis so that
        // alertThreshold or resolveThreshold is visible in chart
        this.handleUpdateChartAxis = () => {
            var _a, _b;
            const { triggers, resolveThreshold, hideThresholdLines } = this.props;
            const chartRef = (_b = (_a = this.ref) === null || _a === void 0 ? void 0 : _a.getEchartsInstance) === null || _b === void 0 ? void 0 : _b.call(_a);
            if (hideThresholdLines) {
                return;
            }
            if (chartRef) {
                const thresholds = [
                    resolveThreshold || null,
                    ...triggers.map(t => t.alertThreshold || null),
                ].filter(threshold => threshold !== null);
                this.updateChartAxis(Math.min(...thresholds), Math.max(...thresholds));
            }
        };
        /**
         * Updates the chart so that yAxis is within bounds of our max value
         */
        this.updateChartAxis = (0, debounce_1.default)((minThreshold, maxThreshold) => {
            const { minValue, maxValue, aggregate } = this.props;
            const shouldScale = (0, utils_1.shouldScaleAlertChart)(aggregate);
            let yAxisMax = shouldScale && maxValue
                ? this.clampMaxValue(Math.ceil(maxValue * utils_1.ALERT_CHART_MIN_MAX_BUFFER))
                : null;
            let yAxisMin = shouldScale && minValue ? Math.floor(minValue / utils_1.ALERT_CHART_MIN_MAX_BUFFER) : 0;
            if (typeof maxValue === 'number' && maxThreshold > maxValue) {
                yAxisMax = maxThreshold;
            }
            if (typeof minValue === 'number' && minThreshold < minValue) {
                yAxisMin = Math.floor(minThreshold / utils_1.ALERT_CHART_MIN_MAX_BUFFER);
            }
            // We need to force update after we set a new yAxis min/max because `convertToPixel`
            // can return a negative position (probably because yAxisMin/yAxisMax is not synced with chart yet)
            this.setState({ yAxisMax, yAxisMin }, this.forceUpdate);
        }, 150);
        /**
         * Syncs component state with the chart's width/heights
         */
        this.updateDimensions = () => {
            var _a, _b;
            const chartRef = (_b = (_a = this.ref) === null || _a === void 0 ? void 0 : _a.getEchartsInstance) === null || _b === void 0 ? void 0 : _b.call(_a);
            if (!chartRef) {
                return;
            }
            const width = chartRef.getWidth();
            const height = chartRef.getHeight();
            if (width !== this.state.width || height !== this.state.height) {
                this.setState({
                    width,
                    height,
                });
            }
        };
        this.handleRef = (ref) => {
            // When chart initially renders, we want to update state with its width, as well as initialize starting
            // locations (on y axis) for the draggable lines
            if (ref && !this.ref) {
                this.ref = ref;
                this.updateDimensions();
                this.handleUpdateChartAxis();
            }
            if (!ref) {
                this.ref = null;
            }
        };
        /**
         * Draws the boundary lines and shaded areas for the chart.
         *
         * May need to refactor so that they are aware of other trigger thresholds.
         *
         * e.g. draw warning from threshold -> critical threshold instead of the entire height of chart
         */
        this.getThresholdLine = (trigger, type, isResolution) => {
            var _a, _b, _c;
            const { thresholdType, resolveThreshold, maxValue, hideThresholdLines } = this.props;
            const position = type === 'alertThreshold'
                ? this.getChartPixelForThreshold(trigger[type])
                : this.getChartPixelForThreshold(resolveThreshold);
            const isInverted = thresholdType === types_1.AlertRuleThresholdType.BELOW;
            const chartRef = (_b = (_a = this.ref) === null || _a === void 0 ? void 0 : _a.getEchartsInstance) === null || _b === void 0 ? void 0 : _b.call(_a);
            if (typeof position !== 'number' ||
                isNaN(position) ||
                !this.state.height ||
                !chartRef ||
                hideThresholdLines) {
                return [];
            }
            const yAxisPixelPosition = chartRef.convertToPixel({ yAxisIndex: 0 }, `${this.state.yAxisMin}`);
            const yAxisPosition = typeof yAxisPixelPosition === 'number' ? yAxisPixelPosition : 0;
            // As the yAxis gets larger we want to start our line/area further to the right
            // Handle case where the graph max is 1 and includes decimals
            const yAxisMax = (Math.round(Math.max(maxValue !== null && maxValue !== void 0 ? maxValue : 1, (_c = this.state.yAxisMax) !== null && _c !== void 0 ? _c : 1)) * 100) / 100;
            const yAxisSize = 15 + (yAxisMax <= 1 ? 15 : `${yAxisMax !== null && yAxisMax !== void 0 ? yAxisMax : ''}`.length * 8);
            // Shave off the right margin and yAxisSize from the width to get the actual area we want to render content in
            const graphAreaWidth = this.state.width - parseInt(CHART_GRID.right.slice(0, -2), 10) - yAxisSize;
            // Distance from the top of the chart to save for the legend
            const legendPadding = 20;
            // Shave off the left margin
            const graphAreaMargin = 7;
            const isCritical = trigger.label === 'critical';
            const LINE_STYLE = {
                stroke: isResolution ? theme_1.default.green300 : isCritical ? theme_1.default.red300 : theme_1.default.yellow300,
                lineDash: [2],
            };
            return [
                // This line is used as a "border" for the shaded region
                // and represents the threshold value.
                {
                    type: 'line',
                    // Resolution is considered "off" if it is -1
                    invisible: position === null,
                    draggable: false,
                    position: [yAxisSize, position],
                    shape: { y1: 1, y2: 1, x1: graphAreaMargin, x2: graphAreaWidth },
                    style: LINE_STYLE,
                },
                // Shaded area for incident/resolutions to show user when they can expect to be alerted
                // (or when they will be considered as resolved)
                //
                // Resolution is considered "off" if it is -1
                ...(position !== null
                    ? [
                        {
                            type: 'rect',
                            draggable: false,
                            position: isResolution !== isInverted
                                ? [yAxisSize + graphAreaMargin, position + 1]
                                : [yAxisSize + graphAreaMargin, legendPadding],
                            shape: {
                                width: graphAreaWidth - graphAreaMargin,
                                height: isResolution !== isInverted
                                    ? yAxisPosition - position
                                    : position - legendPadding,
                            },
                            style: {
                                fill: isResolution
                                    ? COLOR.RESOLUTION_FILL
                                    : isCritical
                                        ? COLOR.CRITICAL_FILL
                                        : COLOR.WARNING_FILL,
                            },
                            // This needs to be below the draggable line
                            z: 100,
                        },
                    ]
                    : []),
            ];
        };
        this.getChartPixelForThreshold = (threshold) => {
            var _a, _b;
            const chartRef = (_b = (_a = this.ref) === null || _a === void 0 ? void 0 : _a.getEchartsInstance) === null || _b === void 0 ? void 0 : _b.call(_a);
            return (threshold !== '' &&
                chartRef &&
                chartRef.convertToPixel({ yAxisIndex: 0 }, `${threshold}`));
        };
    }
    componentDidMount() {
        this.handleUpdateChartAxis();
    }
    componentDidUpdate(prevProps) {
        if (this.props.triggers !== prevProps.triggers ||
            this.props.data !== prevProps.data ||
            this.props.comparisonMarkLines !== prevProps.comparisonMarkLines) {
            this.handleUpdateChartAxis();
        }
    }
    clampMaxValue(value) {
        // When we apply top buffer to the crash free percentage (99.7% * 1.03), it
        // can cross 100%, so we clamp it
        if ((0, utils_1.isSessionAggregate)(this.props.aggregate) && value > 100) {
            return 100;
        }
        return value;
    }
    render() {
        var _a, _b;
        const { data, triggers, period, aggregate, comparisonMarkLines } = this.props;
        const dataWithoutRecentBucket = data === null || data === void 0 ? void 0 : data.map((_a) => {
            var { data: eventData } = _a, restOfData = (0, tslib_1.__rest)(_a, ["data"]);
            return (Object.assign(Object.assign({}, restOfData), { data: eventData.slice(0, -1) }));
        });
        // Disable all lines by default but the 1st one
        const selected = dataWithoutRecentBucket.reduce((acc, { seriesName }, index) => {
            acc[seriesName] = index === 0;
            return acc;
        }, {});
        const legend = {
            right: 10,
            top: 0,
            selected,
            data: data.map(d => ({ name: d.seriesName })),
        };
        const chartOptions = {
            tooltip: {
                valueFormatter: (value, seriesName) => (0, utils_1.alertTooltipValueFormatter)(value, seriesName !== null && seriesName !== void 0 ? seriesName : '', aggregate),
            },
            yAxis: {
                min: (_a = this.state.yAxisMin) !== null && _a !== void 0 ? _a : undefined,
                max: (_b = this.state.yAxisMax) !== null && _b !== void 0 ? _b : undefined,
                axisLabel: {
                    formatter: (value) => (0, utils_1.alertAxisFormatter)(value, data[0].seriesName, aggregate),
                },
            },
        };
        return (<lineChart_1.default isGroupedByDate showTimeInTooltip period={period} forwardedRef={this.handleRef} grid={CHART_GRID} {...chartOptions} legend={legend} graphic={(0, graphic_1.default)({
                elements: (0, flatten_1.default)(triggers.map((trigger) => [
                    ...this.getThresholdLine(trigger, 'alertThreshold', false),
                    ...this.getThresholdLine(trigger, 'resolveThreshold', true),
                ])),
            })} series={[...dataWithoutRecentBucket, ...comparisonMarkLines]} onFinished={() => {
                // We want to do this whenever the chart finishes re-rendering so that we can update the dimensions of
                // any graphics related to the triggers (e.g. the threshold areas + boundaries)
                this.updateDimensions();
            }}/>);
    }
}
exports.default = ThresholdsChart;
ThresholdsChart.defaultProps = {
    data: [],
    comparisonMarkLines: [],
};
//# sourceMappingURL=thresholdsChart.jsx.map