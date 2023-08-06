Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const lineSeries_1 = (0, tslib_1.__importDefault)(require("./series/lineSeries"));
const baseChart_1 = (0, tslib_1.__importDefault)(require("./baseChart"));
class LineChart extends React.Component {
    render() {
        const _a = this.props, { series, seriesOptions } = _a, props = (0, tslib_1.__rest)(_a, ["series", "seriesOptions"]);
        return (<baseChart_1.default {...props} series={series.map((_a) => {
                var { seriesName, data, dataArray } = _a, options = (0, tslib_1.__rest)(_a, ["seriesName", "data", "dataArray"]);
                return (0, lineSeries_1.default)(Object.assign(Object.assign(Object.assign({}, seriesOptions), options), { name: seriesName, data: dataArray || data.map(({ value, name }) => [name, value]), animation: false, animationThreshold: 1, animationDuration: 0 }));
            })}/>);
    }
}
exports.default = LineChart;
//# sourceMappingURL=lineChart.jsx.map