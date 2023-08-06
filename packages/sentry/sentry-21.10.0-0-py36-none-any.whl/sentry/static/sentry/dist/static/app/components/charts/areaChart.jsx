Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const areaSeries_1 = (0, tslib_1.__importDefault)(require("./series/areaSeries"));
const baseChart_1 = (0, tslib_1.__importDefault)(require("./baseChart"));
class AreaChart extends React.Component {
    render() {
        const _a = this.props, { series, stacked, colors } = _a, props = (0, tslib_1.__rest)(_a, ["series", "stacked", "colors"]);
        return (<baseChart_1.default {...props} colors={colors} series={series.map((_a, i) => {
                var { seriesName, data } = _a, otherSeriesProps = (0, tslib_1.__rest)(_a, ["seriesName", "data"]);
                return (0, areaSeries_1.default)(Object.assign({ stack: stacked ? 'area' : undefined, name: seriesName, data: data.map(({ name, value }) => [name, value]), lineStyle: {
                        color: colors === null || colors === void 0 ? void 0 : colors[i],
                        opacity: 1,
                        width: 0.4,
                    }, areaStyle: {
                        color: colors === null || colors === void 0 ? void 0 : colors[i],
                        opacity: 1.0,
                    }, animation: false, animationThreshold: 1, animationDuration: 0 }, otherSeriesProps));
            })}/>);
    }
}
exports.default = AreaChart;
//# sourceMappingURL=areaChart.jsx.map