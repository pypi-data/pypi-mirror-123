Object.defineProperty(exports, "__esModule", { value: true });
exports.slackChartDefaults = exports.slackChartSize = void 0;
const tslib_1 = require("tslib");
const grid_1 = (0, tslib_1.__importDefault)(require("app/components/charts/components/grid"));
const legend_1 = (0, tslib_1.__importDefault)(require("app/components/charts/components/legend"));
const xAxis_1 = (0, tslib_1.__importDefault)(require("app/components/charts/components/xAxis"));
const yAxis_1 = (0, tslib_1.__importDefault)(require("app/components/charts/components/yAxis"));
const theme_1 = require("app/utils/theme");
/**
 * Size configuration for SLACK_* type charts
 */
exports.slackChartSize = {
    height: 150,
    width: 450,
};
/**
 * Default echarts option config for slack charts
 */
exports.slackChartDefaults = {
    grid: (0, grid_1.default)({ left: 5, right: 5, bottom: 5 }),
    backgroundColor: theme_1.lightTheme.background,
    legend: (0, legend_1.default)({ theme: theme_1.lightTheme, itemHeight: 6, top: 2, right: 10 }),
    yAxis: (0, yAxis_1.default)({ theme: theme_1.lightTheme, splitNumber: 3, axisLabel: { fontSize: 11 } }),
    xAxis: (0, xAxis_1.default)({ theme: theme_1.lightTheme, nameGap: 5, isGroupedByDate: true, axisLabel: { fontSize: 11 } }),
};
//# sourceMappingURL=slack.jsx.map