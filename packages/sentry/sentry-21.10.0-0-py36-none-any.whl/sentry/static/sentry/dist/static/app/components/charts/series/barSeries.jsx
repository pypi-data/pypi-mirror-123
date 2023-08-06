Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
require("echarts/lib/chart/bar");
function barSeries(_a) {
    var { data } = _a, rest = (0, tslib_1.__rest)(_a, ["data"]);
    return Object.assign(Object.assign({}, rest), { data: data, type: 'bar' });
}
exports.default = barSeries;
//# sourceMappingURL=barSeries.jsx.map