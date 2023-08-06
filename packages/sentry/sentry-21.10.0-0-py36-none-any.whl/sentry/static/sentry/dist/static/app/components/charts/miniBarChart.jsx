Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
// Import to ensure echarts components are loaded.
require("./components/markPoint");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const set_1 = (0, tslib_1.__importDefault)(require("lodash/set"));
const dates_1 = require("app/utils/dates");
const barChart_1 = (0, tslib_1.__importDefault)(require("./barChart"));
const utils_1 = require("./utils");
function MiniBarChart(_a) {
    var { markers, emphasisColors, series: _series, series, hideDelay, tooltipFormatter, colors, stacked = false, labelYAxisExtents = false, height } = _a, props = (0, tslib_1.__rest)(_a, ["markers", "emphasisColors", "series", "series", "hideDelay", "tooltipFormatter", "colors", "stacked", "labelYAxisExtents", "height"]);
    const { ref: _ref } = props, barChartProps = (0, tslib_1.__rest)(props, ["ref"]);
    const theme = (0, react_1.useTheme)();
    const colorList = Array.isArray(colors)
        ? colors
        : [theme.gray200, theme.purple300, theme.purple300];
    let chartSeries = [];
    // Ensure bars overlap and that empty values display as we're disabling the axis lines.
    if (!!(series === null || series === void 0 ? void 0 : series.length)) {
        chartSeries = series.map((original, i) => {
            var _a;
            const updated = Object.assign(Object.assign({}, original), { cursor: 'normal', type: 'bar' });
            if (i === 0) {
                updated.barMinHeight = 1;
                if (stacked === false) {
                    updated.barGap = '-100%';
                }
            }
            if (stacked) {
                updated.stack = 'stack1';
            }
            (0, set_1.default)(updated, 'itemStyle.color', colorList[i]);
            (0, set_1.default)(updated, 'itemStyle.opacity', 0.6);
            (0, set_1.default)(updated, 'itemStyle.emphasis.opacity', 1.0);
            (0, set_1.default)(updated, 'itemStyle.emphasis.color', (_a = emphasisColors === null || emphasisColors === void 0 ? void 0 : emphasisColors[i]) !== null && _a !== void 0 ? _a : colorList[i]);
            return updated;
        });
    }
    if (markers) {
        const markerTooltip = {
            show: true,
            trigger: 'item',
            formatter: ({ data }) => {
                var _a;
                const time = (0, dates_1.getFormattedDate)(data.coord[0], 'MMM D, YYYY LT', {
                    local: !props.utc,
                });
                const name = (0, utils_1.truncationFormatter)(data.name, (_a = props === null || props === void 0 ? void 0 : props.xAxis) === null || _a === void 0 ? void 0 : _a.truncate);
                return [
                    '<div class="tooltip-series">',
                    `<div><span class="tooltip-label"><strong>${name}</strong></span></div>`,
                    '</div>',
                    '<div class="tooltip-date">',
                    time,
                    '</div>',
                    '</div>',
                    '<div class="tooltip-arrow"></div>',
                ].join('');
            },
        };
        const markPoint = {
            data: markers.map((marker) => {
                var _a;
                return ({
                    name: marker.name,
                    coord: [marker.value, 0],
                    tooltip: markerTooltip,
                    symbol: 'circle',
                    symbolSize: (_a = marker.symbolSize) !== null && _a !== void 0 ? _a : 8,
                    itemStyle: {
                        color: marker.color,
                        borderColor: theme.background,
                    },
                });
            }),
        };
        chartSeries[0].markPoint = markPoint;
    }
    const yAxisOptions = labelYAxisExtents
        ? {
            showMinLabel: true,
            showMaxLabel: true,
            interval: Infinity,
        }
        : {
            axisLabel: {
                show: false,
            },
        };
    const chartOptions = {
        tooltip: {
            trigger: 'axis',
            hideDelay,
            valueFormatter: tooltipFormatter
                ? (value) => tooltipFormatter(value)
                : undefined,
        },
        yAxis: Object.assign({ max(value) {
                // This keeps small datasets from looking 'scary'
                // by having full bars for < 10 values.
                if (value.max < 10) {
                    return 10;
                }
                // Adds extra spacing at the top of the chart canvas, ensuring the series doesn't hit the ceiling, leaving more empty space.
                // When the user hovers over an empty space, a tooltip with all series information is displayed.
                return (value.max * (height + 10)) / height;
            }, splitLine: {
                show: false,
            } }, yAxisOptions),
        grid: {
            // Offset to ensure there is room for the marker symbols at the
            // default size.
            top: labelYAxisExtents ? 6 : 0,
            bottom: markers || labelYAxisExtents ? 4 : 0,
            left: markers ? 8 : 4,
            right: markers ? 4 : 0,
        },
        xAxis: {
            axisLine: {
                show: false,
            },
            axisTick: {
                show: false,
                alignWithLabel: true,
            },
            axisLabel: {
                show: false,
            },
            axisPointer: {
                type: 'line',
                label: {
                    show: false,
                },
                lineStyle: {
                    width: 0,
                },
            },
        },
        options: {
            animation: false,
        },
    };
    return (<barChart_1.default series={chartSeries} height={height} {...chartOptions} {...barChartProps}/>);
}
exports.default = MiniBarChart;
//# sourceMappingURL=miniBarChart.jsx.map