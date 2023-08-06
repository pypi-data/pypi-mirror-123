Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const baseChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/baseChart"));
const locale_1 = require("app/locale");
const charts_1 = require("app/utils/discover/charts");
const noEvents_1 = (0, tslib_1.__importDefault)(require("./noEvents"));
const Chart = ({ firstEvent, stats, transactionStats }) => {
    const series = [];
    const hasTransactions = transactionStats !== undefined;
    const theme = (0, react_1.useTheme)();
    if (transactionStats) {
        const transactionSeries = transactionStats.map(([timestamp, value]) => [
            timestamp * 1000,
            value,
        ]);
        series.push({
            cursor: 'normal',
            name: (0, locale_1.t)('Transactions'),
            type: 'bar',
            data: transactionSeries,
            barMinHeight: 1,
            xAxisIndex: 1,
            yAxisIndex: 1,
            itemStyle: {
                color: theme.gray200,
                opacity: 0.8,
                emphasis: {
                    color: theme.gray200,
                    opacity: 1.0,
                },
            },
        });
    }
    if (stats) {
        series.push({
            cursor: 'normal',
            name: (0, locale_1.t)('Errors'),
            type: 'bar',
            data: stats.map(([timestamp, value]) => [timestamp * 1000, value]),
            barMinHeight: 1,
            xAxisIndex: 0,
            yAxisIndex: 0,
            itemStyle: {
                color: theme.purple300,
                opacity: 0.6,
                emphasis: {
                    color: theme.purple300,
                    opacity: 0.8,
                },
            },
        });
    }
    const grid = hasTransactions
        ? [
            {
                top: 10,
                bottom: 60,
                left: 2,
                right: 2,
            },
            {
                top: 105,
                bottom: 0,
                left: 2,
                right: 2,
            },
        ]
        : [
            {
                top: 10,
                bottom: 0,
                left: 2,
                right: 2,
            },
        ];
    const chartOptions = {
        series,
        colors: [],
        height: 150,
        isGroupedByDate: true,
        showTimeInTooltip: true,
        grid,
        tooltip: {
            trigger: 'axis',
        },
        xAxes: Array.from(new Array(series.length)).map((_i, index) => ({
            gridIndex: index,
            boundaryGap: true,
            axisLine: {
                show: false,
            },
            axisTick: {
                show: false,
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
        })),
        yAxes: Array.from(new Array(series.length)).map((_i, index) => ({
            gridIndex: index,
            interval: Infinity,
            max(value) {
                // This keeps small datasets from looking 'scary'
                // by having full bars for < 10 values.
                return Math.max(10, value.max);
            },
            axisLabel: {
                margin: 2,
                showMaxLabel: true,
                showMinLabel: false,
                color: theme.chartLabel,
                fontFamily: theme.text.family,
                inside: true,
                lineHeight: 12,
                formatter: (value) => (0, charts_1.axisLabelFormatter)(value, 'count()', true),
                textBorderColor: theme.backgroundSecondary,
                textBorderWidth: 1,
            },
            splitLine: {
                show: false,
            },
            zlevel: theme.zIndex.header,
        })),
        axisPointer: {
            // Link each x-axis together.
            link: [{ xAxisIndex: [0, 1] }],
        },
        options: {
            animation: false,
        },
    };
    return (<React.Fragment>
      <baseChart_1.default {...chartOptions}/>
      {!firstEvent && <noEvents_1.default seriesCount={series.length}/>}
    </React.Fragment>);
};
exports.default = Chart;
//# sourceMappingURL=chart.jsx.map