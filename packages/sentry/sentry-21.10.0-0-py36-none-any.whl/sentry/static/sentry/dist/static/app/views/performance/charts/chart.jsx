Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("@emotion/react");
const max_1 = (0, tslib_1.__importDefault)(require("lodash/max"));
const min_1 = (0, tslib_1.__importDefault)(require("lodash/min"));
const areaChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/areaChart"));
const chartZoom_1 = (0, tslib_1.__importDefault)(require("app/components/charts/chartZoom"));
const charts_1 = require("app/utils/discover/charts");
const fields_1 = require("app/utils/discover/fields");
// adapted from https://stackoverflow.com/questions/11397239/rounding-up-for-a-graph-maximum
function computeAxisMax(data) {
    // assumes min is 0
    const valuesDict = data.map(value => value.data.map(point => point.value));
    const maxValue = (0, max_1.default)(valuesDict.map(max_1.default));
    if (maxValue <= 1) {
        return 1;
    }
    const power = Math.log10(maxValue);
    const magnitude = (0, min_1.default)([(0, max_1.default)([Math.pow(10, (power - Math.floor(power))), 0]), 10]);
    let scale;
    if (magnitude <= 2.5) {
        scale = 0.2;
    }
    else if (magnitude <= 5) {
        scale = 0.5;
    }
    else if (magnitude <= 7.5) {
        scale = 1.0;
    }
    else {
        scale = 2.0;
    }
    const step = Math.pow(10, Math.floor(power)) * scale;
    return Math.round(Math.ceil(maxValue / step) * step);
}
function Chart({ data, previousData, router, statsPeriod, start, end, utc, loading, height, grid, disableMultiAxis, disableXAxis, chartColors, }) {
    const theme = (0, react_1.useTheme)();
    if (!data || data.length <= 0) {
        return null;
    }
    const colors = chartColors !== null && chartColors !== void 0 ? chartColors : theme.charts.getColorPalette(4);
    const durationOnly = data.every(value => (0, fields_1.aggregateOutputType)(value.seriesName) === 'duration');
    const dataMax = durationOnly ? computeAxisMax(data) : undefined;
    const xAxes = disableMultiAxis
        ? undefined
        : [
            {
                gridIndex: 0,
                type: 'time',
            },
            {
                gridIndex: 1,
                type: 'time',
            },
        ];
    const yAxes = disableMultiAxis
        ? [
            {
                axisLabel: {
                    color: theme.chartLabel,
                    formatter(value) {
                        return (0, charts_1.axisLabelFormatter)(value, data[0].seriesName);
                    },
                },
            },
        ]
        : [
            {
                gridIndex: 0,
                scale: true,
                max: dataMax,
                axisLabel: {
                    color: theme.chartLabel,
                    formatter(value) {
                        return (0, charts_1.axisLabelFormatter)(value, data[0].seriesName);
                    },
                },
            },
            {
                gridIndex: 1,
                scale: true,
                max: dataMax,
                axisLabel: {
                    color: theme.chartLabel,
                    formatter(value) {
                        return (0, charts_1.axisLabelFormatter)(value, data[1].seriesName);
                    },
                },
            },
        ];
    const axisPointer = disableMultiAxis
        ? undefined
        : {
            // Link the two series x-axis together.
            link: [{ xAxisIndex: [0, 1] }],
        };
    const areaChartProps = {
        seriesOptions: {
            showSymbol: false,
        },
        grid: disableMultiAxis
            ? grid
            : [
                {
                    top: '8px',
                    left: '24px',
                    right: '52%',
                    bottom: '16px',
                },
                {
                    top: '8px',
                    left: '52%',
                    right: '24px',
                    bottom: '16px',
                },
            ],
        axisPointer,
        xAxes,
        yAxes,
        utc,
        isGroupedByDate: true,
        showTimeInTooltip: true,
        colors: [colors[0], colors[1]],
        tooltip: {
            valueFormatter: (value, seriesName) => {
                return (0, charts_1.tooltipFormatter)(value, seriesName);
            },
            nameFormatter(value) {
                return value === 'epm()' ? 'tpm()' : value;
            },
        },
    };
    if (loading) {
        return <areaChart_1.default height={height} series={[]} {...areaChartProps}/>;
    }
    const series = data.map((values, i) => (Object.assign(Object.assign({}, values), { yAxisIndex: i, xAxisIndex: i })));
    return (<chartZoom_1.default router={router} period={statsPeriod} start={start} end={end} utc={utc} xAxisIndex={disableMultiAxis ? undefined : [0, 1]}>
      {zoomRenderProps => (<areaChart_1.default height={height} {...zoomRenderProps} series={series} previousPeriod={previousData} xAxis={disableXAxis ? { show: false } : undefined} {...areaChartProps}/>)}
    </chartZoom_1.default>);
}
exports.default = Chart;
//# sourceMappingURL=chart.jsx.map