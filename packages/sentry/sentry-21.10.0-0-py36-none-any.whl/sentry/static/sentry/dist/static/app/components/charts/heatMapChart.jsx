Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
require("./components/visualMap");
const React = (0, tslib_1.__importStar)(require("react"));
const heatMapSeries_1 = (0, tslib_1.__importDefault)(require("./series/heatMapSeries"));
const baseChart_1 = (0, tslib_1.__importDefault)(require("./baseChart"));
exports.default = React.forwardRef((props, ref) => {
    const { series, seriesOptions, visualMaps } = props, otherProps = (0, tslib_1.__rest)(props, ["series", "seriesOptions", "visualMaps"]);
    return (<baseChart_1.default ref={ref} options={{
            visualMap: visualMaps,
        }} {...otherProps} series={series.map((_a) => {
            var { seriesName, data, dataArray } = _a, options = (0, tslib_1.__rest)(_a, ["seriesName", "data", "dataArray"]);
            return (0, heatMapSeries_1.default)(Object.assign(Object.assign(Object.assign({}, seriesOptions), options), { name: seriesName, data: dataArray || data.map(({ value, name }) => [name, value]) }));
        })}/>);
});
//# sourceMappingURL=heatMapChart.jsx.map