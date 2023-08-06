Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const merge_1 = (0, tslib_1.__importDefault)(require("lodash/merge"));
function YAxis(_a) {
    var { theme } = _a, props = (0, tslib_1.__rest)(_a, ["theme"]);
    return (0, merge_1.default)({
        axisLine: {
            show: false,
        },
        axisTick: {
            show: false,
        },
        axisLabel: {
            color: theme.chartLabel,
            fontFamily: theme.text.family,
        },
        splitLine: {
            lineStyle: {
                color: theme.chartLineColor,
                opacity: 0.3,
            },
        },
    }, props);
}
exports.default = YAxis;
//# sourceMappingURL=yAxis.jsx.map