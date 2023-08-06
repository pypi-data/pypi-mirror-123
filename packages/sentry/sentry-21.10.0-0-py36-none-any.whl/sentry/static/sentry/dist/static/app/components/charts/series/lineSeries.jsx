Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
require("echarts/lib/chart/line");
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
function LineSeries(props) {
    return Object.assign(Object.assign({ showSymbol: false, symbolSize: theme_1.default.charts.symbolSize }, props), { type: 'line' });
}
exports.default = LineSeries;
//# sourceMappingURL=lineSeries.jsx.map