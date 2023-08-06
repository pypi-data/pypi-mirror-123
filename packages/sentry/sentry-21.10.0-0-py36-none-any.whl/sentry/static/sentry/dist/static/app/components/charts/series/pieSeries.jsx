Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
require("echarts/lib/chart/pie");
function PieSeries(props = {}) {
    const { data } = props, rest = (0, tslib_1.__rest)(props, ["data"]);
    return Object.assign(Object.assign({ radius: ['50%', '70%'], data: data }, rest), { type: 'pie' });
}
exports.default = PieSeries;
//# sourceMappingURL=pieSeries.jsx.map