Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const areaChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/areaChart"));
class StackedAreaChart extends React.Component {
    render() {
        return <areaChart_1.default tooltip={{ filter: val => val > 0 }} {...this.props} stacked/>;
    }
}
exports.default = StackedAreaChart;
//# sourceMappingURL=stackedAreaChart.jsx.map