Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
require("zrender/lib/svg/svg");
const react_1 = require("react");
const react_2 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const echarts_1 = (0, tslib_1.__importDefault)(require("echarts/lib/echarts"));
const core_1 = (0, tslib_1.__importDefault)(require("echarts-for-react/lib/core"));
const constants_1 = require("app/constants");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const grid_1 = (0, tslib_1.__importDefault)(require("./components/grid"));
const legend_1 = (0, tslib_1.__importDefault)(require("./components/legend"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("./components/tooltip"));
const xAxis_1 = (0, tslib_1.__importDefault)(require("./components/xAxis"));
const yAxis_1 = (0, tslib_1.__importDefault)(require("./components/yAxis"));
const lineSeries_1 = (0, tslib_1.__importDefault)(require("./series/lineSeries"));
const utils_1 = require("./utils");
// TODO(ts): What is the series type? EChartOption.Series's data cannot have
// `onClick` since it's typically an array.
//
// Handle series item clicks (e.g. Releases mark line or a single series
// item) This is different than when you hover over an "axis" line on a chart
// (e.g.  if there are 2 series for an axis and you're not directly hovered
// over an item)
//
// Calls "onClick" inside of series data
const handleClick = (clickSeries, instance) => {
    var _a, _b;
    if (clickSeries.data) {
        (_b = (_a = clickSeries.data).onClick) === null || _b === void 0 ? void 0 : _b.call(_a, clickSeries, instance);
    }
};
function BaseChartUnwrapped({ colors, grid, tooltip, legend, dataZoom, toolBox, graphic, axisPointer, previousPeriod, echartsTheme, devicePixelRatio, showTimeInTooltip, useShortDate, start, end, period, utc, yAxes, xAxes, style, forwardedRef, onClick, onLegendSelectChanged, onHighlight, onMouseOver, onDataZoom, onRestore, onFinished, onRendered, options = {}, series = [], yAxis = {}, xAxis = {}, height = 200, width = 'auto', renderer = 'svg', notMerge = true, lazyUpdate = false, isGroupedByDate = false, transformSinglePointToBar = false, onChartReady = () => { }, }) {
    var _a, _b, _c, _d, _e, _f;
    const theme = (0, react_2.useTheme)();
    const hasSinglePoints = (_a = series) === null || _a === void 0 ? void 0 : _a.every(s => Array.isArray(s.data) && s.data.length <= 1);
    const resolveColors = colors !== undefined ? (Array.isArray(colors) ? colors : colors(theme)) : null;
    const color = resolveColors ||
        (series.length ? theme.charts.getColorPalette(series.length) : theme.charts.colors);
    const previousPeriodColors = previousPeriod && previousPeriod.length > 1 ? (0, utils_1.lightenHexToRgb)(color) : undefined;
    const transformedSeries = (_c = (hasSinglePoints && transformSinglePointToBar
        ? (_b = series) === null || _b === void 0 ? void 0 : _b.map(s => {
            var _a;
            return (Object.assign(Object.assign({}, s), { type: 'bar', barWidth: 40, barGap: 0, itemStyle: Object.assign({}, ((_a = s.areaStyle) !== null && _a !== void 0 ? _a : {})) }));
        })
        : series)) !== null && _c !== void 0 ? _c : [];
    const transformedPreviousPeriod = (_d = previousPeriod === null || previousPeriod === void 0 ? void 0 : previousPeriod.map((previous, seriesIndex) => (0, lineSeries_1.default)({
        name: previous.seriesName,
        data: previous.data.map(({ name, value }) => [name, value]),
        lineStyle: {
            color: previousPeriodColors ? previousPeriodColors[seriesIndex] : theme.gray200,
            type: 'dotted',
        },
        itemStyle: {
            color: previousPeriodColors ? previousPeriodColors[seriesIndex] : theme.gray200,
        },
        stack: 'previous',
    }))) !== null && _d !== void 0 ? _d : [];
    const resolvedSeries = !previousPeriod
        ? transformedSeries
        : [...transformedSeries, ...transformedPreviousPeriod];
    const defaultAxesProps = { theme };
    const yAxisOrCustom = !yAxes
        ? yAxis !== null
            ? (0, yAxis_1.default)(Object.assign({ theme }, yAxis))
            : undefined
        : Array.isArray(yAxes)
            ? yAxes.map(axis => (0, yAxis_1.default)(Object.assign(Object.assign({}, axis), { theme })))
            : [(0, yAxis_1.default)(defaultAxesProps), (0, yAxis_1.default)(defaultAxesProps)];
    const xAxisOrCustom = !xAxes
        ? xAxis !== null
            ? (0, xAxis_1.default)(Object.assign(Object.assign({}, xAxis), { theme,
                useShortDate,
                start,
                end,
                period,
                isGroupedByDate,
                utc }))
            : undefined
        : Array.isArray(xAxes)
            ? xAxes.map(axis => (0, xAxis_1.default)(Object.assign(Object.assign({}, axis), { theme, useShortDate, start, end, period, isGroupedByDate, utc })))
            : [(0, xAxis_1.default)(defaultAxesProps), (0, xAxis_1.default)(defaultAxesProps)];
    // Maybe changing the series type to types/echarts Series[] would be a better
    // solution and can't use ignore for multiline blocks
    const seriesValid = series && ((_e = series[0]) === null || _e === void 0 ? void 0 : _e.data) && series[0].data.length > 1;
    const seriesData = seriesValid ? series[0].data : undefined;
    const bucketSize = seriesData ? seriesData[1][0] - seriesData[0][0] : undefined;
    const tooltipOrNone = tooltip !== null
        ? (0, tooltip_1.default)(Object.assign({ showTimeInTooltip,
            isGroupedByDate,
            utc,
            bucketSize }, tooltip))
        : undefined;
    const chartOption = Object.assign(Object.assign({}, options), { animation: constants_1.IS_ACCEPTANCE_TEST ? false : (_f = options.animation) !== null && _f !== void 0 ? _f : true, useUTC: utc, color, grid: Array.isArray(grid) ? grid.map(grid_1.default) : (0, grid_1.default)(grid), tooltip: tooltipOrNone, legend: legend ? (0, legend_1.default)(Object.assign({ theme }, legend)) : undefined, yAxis: yAxisOrCustom, xAxis: xAxisOrCustom, series: resolvedSeries, toolbox: toolBox, axisPointer,
        dataZoom,
        graphic });
    const chartStyles = Object.assign({ height: (0, utils_1.getDimensionValue)(height), width: (0, utils_1.getDimensionValue)(width) }, style);
    // XXX(epurkhiser): Echarts can become unhappy if one of these event handlers
    // causes the chart to re-render and be passed a whole different instance of
    // event handlers.
    //
    // We use React.useMemo to keep the value across renders
    //
    const eventsMap = (0, react_1.useMemo)(() => ({
        click: (props, instance) => {
            handleClick(props, instance);
            onClick === null || onClick === void 0 ? void 0 : onClick(props, instance);
        },
        highlight: (props, instance) => onHighlight === null || onHighlight === void 0 ? void 0 : onHighlight(props, instance),
        mouseover: (props, instance) => onMouseOver === null || onMouseOver === void 0 ? void 0 : onMouseOver(props, instance),
        datazoom: (props, instance) => onDataZoom === null || onDataZoom === void 0 ? void 0 : onDataZoom(props, instance),
        restore: (props, instance) => onRestore === null || onRestore === void 0 ? void 0 : onRestore(props, instance),
        finished: (props, instance) => onFinished === null || onFinished === void 0 ? void 0 : onFinished(props, instance),
        rendered: (props, instance) => onRendered === null || onRendered === void 0 ? void 0 : onRendered(props, instance),
        legendselectchanged: (props, instance) => onLegendSelectChanged === null || onLegendSelectChanged === void 0 ? void 0 : onLegendSelectChanged(props, instance),
    }), [onclick, onHighlight, onMouseOver, onDataZoom, onRestore, onFinished, onRendered]);
    return (<ChartContainer>
      <core_1.default ref={forwardedRef} echarts={echarts_1.default} notMerge={notMerge} lazyUpdate={lazyUpdate} theme={echartsTheme} onChartReady={onChartReady} onEvents={eventsMap} style={chartStyles} opts={{ height, width, renderer, devicePixelRatio }} option={chartOption}/>
    </ChartContainer>);
}
// Contains styling for chart elements as we can't easily style those
// elements directly
const ChartContainer = (0, styled_1.default)('div') `
  /* Tooltip styling */
  .tooltip-series,
  .tooltip-date {
    color: ${p => p.theme.gray300};
    font-family: ${p => p.theme.text.family};
    font-variant-numeric: tabular-nums;
    background: ${p => p.theme.gray500};
    padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};
    border-radius: ${p => p.theme.borderRadius} ${p => p.theme.borderRadius} 0 0;
  }
  .tooltip-series-solo {
    border-radius: ${p => p.theme.borderRadius};
  }
  .tooltip-label {
    margin-right: ${(0, space_1.default)(1)};
  }
  .tooltip-label strong {
    font-weight: normal;
    color: ${p => p.theme.white};
  }
  .tooltip-label-indent {
    margin-left: ${(0, space_1.default)(3)};
  }
  .tooltip-series > div {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
  }
  .tooltip-date {
    border-top: 1px solid ${p => p.theme.gray400};
    text-align: center;
    position: relative;
    width: auto;
    border-radius: ${p => p.theme.borderRadiusBottom};
  }
  .tooltip-arrow {
    top: 100%;
    left: 50%;
    border: 0px solid transparent;
    content: ' ';
    height: 0;
    width: 0;
    position: absolute;
    pointer-events: none;
    border-top-color: ${p => p.theme.gray500};
    border-width: 8px;
    margin-left: -8px;
  }

  .echarts-for-react div:first-of-type {
    width: 100% !important;
  }

  .echarts-for-react tspan {
    font-variant-numeric: tabular-nums;
  }

  /* Tooltip description styling */
  .tooltip-description {
    color: ${p => p.theme.white};
    border-radius: ${p => p.theme.borderRadius};
    background: #000;
    opacity: 0.9;
    padding: 5px 10px;
    position: relative;
    font-weight: bold;
    font-size: ${p => p.theme.fontSizeSmall};
    line-height: 1.4;
    font-family: ${p => p.theme.text.family};
    max-width: 230px;
    min-width: 230px;
    white-space: normal;
    text-align: center;
    :after {
      content: '';
      position: absolute;
      top: 100%;
      left: 50%;
      width: 0;
      height: 0;
      border-left: 5px solid transparent;
      border-right: 5px solid transparent;
      border-top: 5px solid #000;
      transform: translateX(-50%);
    }
  }
`;
const BaseChart = (0, react_1.forwardRef)((props, ref) => (<BaseChartUnwrapped forwardedRef={ref} {...props}/>));
BaseChart.displayName = 'forwardRef(BaseChart)';
exports.default = BaseChart;
//# sourceMappingURL=baseChart.jsx.map