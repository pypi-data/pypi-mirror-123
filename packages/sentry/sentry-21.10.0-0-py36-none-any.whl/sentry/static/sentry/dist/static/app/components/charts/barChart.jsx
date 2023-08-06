Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const barSeries_1 = (0, tslib_1.__importDefault)(require("./series/barSeries"));
const baseChart_1 = (0, tslib_1.__importDefault)(require("./baseChart"));
class BarChart extends React.Component {
    render() {
        const _a = this.props, { series, stacked, xAxis } = _a, props = (0, tslib_1.__rest)(_a, ["series", "stacked", "xAxis"]);
        return (<baseChart_1.default {...props} xAxis={xAxis !== null ? Object.assign(Object.assign({}, (xAxis || {})), { boundaryGap: true }) : null} series={series.map((_a) => {
                var { seriesName, data } = _a, options = (0, tslib_1.__rest)(_a, ["seriesName", "data"]);
                return (0, barSeries_1.default)(Object.assign({ name: seriesName, stack: stacked ? 'stack1' : undefined, data: data.map(({ value, name, itemStyle }) => {
                        if (itemStyle === undefined) {
                            return [name, value];
                        }
                        return { value: [name, value], itemStyle };
                    }) }, options));
            })}/>);
    }
}
exports.default = BarChart;
//# sourceMappingURL=barChart.jsx.map