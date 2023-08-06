Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const areaSeries_1 = (0, tslib_1.__importDefault)(require("./series/areaSeries"));
const baseChart_1 = (0, tslib_1.__importDefault)(require("./baseChart"));
const FILLER_NAME = '__filler';
/**
 * A stacked 100% column chart over time
 *
 * See https://exceljet.net/chart-type/100-stacked-bar-chart
 */
class PercentageAreaChart extends React.Component {
    getSeries() {
        const { series, getDataItemName, getValue } = this.props;
        const totalsArray = series.length
            ? series[0].data.map(({ name }, i) => [
                name,
                series.reduce((sum, { data }) => sum + data[i].value, 0),
            ])
            : [];
        const totals = new Map(totalsArray);
        return [
            ...series.map(({ seriesName, data }) => (0, areaSeries_1.default)({
                name: seriesName,
                lineStyle: { width: 1 },
                areaStyle: { opacity: 1 },
                smooth: true,
                stack: 'percentageAreaChartStack',
                data: data.map((dataObj) => [
                    getDataItemName(dataObj),
                    getValue(dataObj, totals.get(dataObj.name)),
                ]),
            })),
        ];
    }
    render() {
        return (<baseChart_1.default {...this.props} tooltip={{
                formatter: seriesParams => {
                    // `seriesParams` can be an array or an object :/
                    const series = Array.isArray(seriesParams) ? seriesParams : [seriesParams];
                    // Filter series that have 0 counts
                    const date = `${series.length && (0, moment_1.default)(series[0].axisValue).format('MMM D, YYYY')}<br />` || '';
                    return [
                        '<div class="tooltip-series">',
                        series
                            .filter(({ seriesName, data }) => data[1] > 0.001 && seriesName !== FILLER_NAME)
                            .map(({ marker, seriesName, data }) => `<div><span class="tooltip-label">${marker} <strong>${seriesName}</strong></span> ${data[1]}%</div>`)
                            .join(''),
                        '</div>',
                        `<div class="tooltip-date">${date}</div>`,
                        '<div class="tooltip-arrow"></div>',
                    ].join('');
                },
            }} xAxis={{ boundaryGap: true }} yAxis={{
                min: 0,
                max: 100,
                type: 'value',
                interval: 25,
                splitNumber: 4,
                data: [0, 25, 50, 100],
                axisLabel: {
                    formatter: '{value}%',
                },
            }} series={this.getSeries()}/>);
    }
}
exports.default = PercentageAreaChart;
PercentageAreaChart.defaultProps = {
    // TODO(billyvg): Move these into BaseChart? or get rid completely
    getDataItemName: ({ name }) => name,
    getValue: ({ value }, total) => (!total ? 0 : Math.round((value / total) * 1000) / 10),
};
//# sourceMappingURL=percentageAreaChart.jsx.map