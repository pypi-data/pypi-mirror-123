Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
require("echarts/lib/chart/heatmap");
require("echarts/lib/component/visualMap");
function HeatMapSeries(props = {}) {
    const { data } = props, rest = (0, tslib_1.__rest)(props, ["data"]);
    return Object.assign(Object.assign({ data: data }, rest), { type: 'heatmap' });
}
exports.default = HeatMapSeries;
//# sourceMappingURL=heatMapSeries.jsx.map