Object.defineProperty(exports, "__esModule", { value: true });
exports.discoverCharts = void 0;
const tslib_1 = require("tslib");
const isArray_1 = (0, tslib_1.__importDefault)(require("lodash/isArray"));
const xAxis_1 = (0, tslib_1.__importDefault)(require("app/components/charts/components/xAxis"));
const areaSeries_1 = (0, tslib_1.__importDefault)(require("app/components/charts/series/areaSeries"));
const barSeries_1 = (0, tslib_1.__importDefault)(require("app/components/charts/series/barSeries"));
const lineSeries_1 = (0, tslib_1.__importDefault)(require("app/components/charts/series/lineSeries"));
const utils_1 = require("app/components/charts/utils");
const locale_1 = require("app/locale");
const theme_1 = require("app/utils/theme");
const slack_1 = require("./slack");
const types_1 = require("./types");
const discoverxAxis = (0, xAxis_1.default)({
    theme: theme_1.lightTheme,
    boundaryGap: true,
    splitNumber: 3,
    isGroupedByDate: true,
    axisLabel: { fontSize: 11 },
});
exports.discoverCharts = [];
exports.discoverCharts.push(Object.assign({ key: types_1.ChartType.SLACK_DISCOVER_TOTAL_PERIOD, getOption: (data) => {
        if ((0, isArray_1.default)(data.stats.data)) {
            const color = theme_1.lightTheme.charts.getColorPalette(data.stats.data.length - 2);
            const areaSeries = (0, areaSeries_1.default)({
                name: data.seriesName,
                data: data.stats.data.map(([timestamp, countsForTimestamp]) => [
                    timestamp * 1000,
                    countsForTimestamp.reduce((acc, { count }) => acc + count, 0),
                ]),
                lineStyle: { color: color === null || color === void 0 ? void 0 : color[0], opacity: 1, width: 0.4 },
                areaStyle: { color: color === null || color === void 0 ? void 0 : color[0], opacity: 1 },
            });
            return Object.assign(Object.assign({}, slack_1.slackChartDefaults), { useUTC: true, color, series: [areaSeries] });
        }
        const stats = Object.keys(data.stats).map(key => Object.assign({}, { key }, data.stats[key]));
        const color = theme_1.lightTheme.charts.getColorPalette(stats.length - 2);
        const series = stats
            .sort((a, b) => { var _a, _b; return ((_a = a.order) !== null && _a !== void 0 ? _a : 0) - ((_b = b.order) !== null && _b !== void 0 ? _b : 0); })
            .map((s, i) => (0, areaSeries_1.default)({
            name: s.key,
            stack: 'area',
            data: s.data.map(([timestamp, countsForTimestamp]) => [
                timestamp * 1000,
                countsForTimestamp.reduce((acc, { count }) => acc + count, 0),
            ]),
            lineStyle: { color: color === null || color === void 0 ? void 0 : color[i], opacity: 1, width: 0.4 },
            areaStyle: { color: color === null || color === void 0 ? void 0 : color[i], opacity: 1 },
        }));
        return Object.assign(Object.assign({}, slack_1.slackChartDefaults), { xAxis: discoverxAxis, useUTC: true, color,
            series });
    } }, slack_1.slackChartSize));
exports.discoverCharts.push(Object.assign({ key: types_1.ChartType.SLACK_DISCOVER_TOTAL_DAILY, getOption: (data) => {
        if ((0, isArray_1.default)(data.stats.data)) {
            const color = theme_1.lightTheme.charts.getColorPalette(data.stats.data.length - 2);
            const barSeries = (0, barSeries_1.default)({
                name: data.seriesName,
                data: data.stats.data.map(([timestamp, countsForTimestamp]) => ({
                    value: [
                        timestamp * 1000,
                        countsForTimestamp.reduce((acc, { count }) => acc + count, 0),
                    ],
                })),
                itemStyle: { color: color === null || color === void 0 ? void 0 : color[0], opacity: 1 },
            });
            return Object.assign(Object.assign({}, slack_1.slackChartDefaults), { xAxis: discoverxAxis, useUTC: true, color, series: [barSeries] });
        }
        const stats = Object.keys(data.stats).map(key => Object.assign({}, { key }, data.stats[key]));
        const color = theme_1.lightTheme.charts.getColorPalette(stats.length - 2);
        const series = stats
            .sort((a, b) => { var _a, _b; return ((_a = a.order) !== null && _a !== void 0 ? _a : 0) - ((_b = b.order) !== null && _b !== void 0 ? _b : 0); })
            .map((s, i) => (0, barSeries_1.default)({
            name: s.key,
            stack: 'area',
            data: s.data.map(([timestamp, countsForTimestamp]) => ({
                value: [
                    timestamp * 1000,
                    countsForTimestamp.reduce((acc, { count }) => acc + count, 0),
                ],
            })),
            itemStyle: { color: color === null || color === void 0 ? void 0 : color[i], opacity: 1 },
        }));
        return Object.assign(Object.assign({}, slack_1.slackChartDefaults), { xAxis: discoverxAxis, useUTC: true, color,
            series });
    } }, slack_1.slackChartSize));
exports.discoverCharts.push(Object.assign({ key: types_1.ChartType.SLACK_DISCOVER_TOP5_PERIOD, getOption: (data) => {
        if ((0, isArray_1.default)(data.stats.data)) {
            const color = theme_1.lightTheme.charts.getColorPalette(data.stats.data.length - 2);
            const areaSeries = (0, areaSeries_1.default)({
                data: data.stats.data.map(([timestamp, countsForTimestamp]) => [
                    timestamp * 1000,
                    countsForTimestamp.reduce((acc, { count }) => acc + count, 0),
                ]),
                lineStyle: { color: color === null || color === void 0 ? void 0 : color[0], opacity: 1, width: 0.4 },
                areaStyle: { color: color === null || color === void 0 ? void 0 : color[0], opacity: 1 },
            });
            return Object.assign(Object.assign({}, slack_1.slackChartDefaults), { useUTC: true, color, series: [areaSeries] });
        }
        const stats = Object.values(data.stats);
        const color = theme_1.lightTheme.charts.getColorPalette(stats.length - 2);
        const series = stats
            .sort((a, b) => { var _a, _b; return ((_a = a.order) !== null && _a !== void 0 ? _a : 0) - ((_b = b.order) !== null && _b !== void 0 ? _b : 0); })
            .map((topSeries, i) => (0, areaSeries_1.default)({
            stack: 'area',
            data: topSeries.data.map(([timestamp, countsForTimestamp]) => [
                timestamp * 1000,
                countsForTimestamp.reduce((acc, { count }) => acc + count, 0),
            ]),
            lineStyle: { color: color === null || color === void 0 ? void 0 : color[i], opacity: 1, width: 0.4 },
            areaStyle: { color: color === null || color === void 0 ? void 0 : color[i], opacity: 1 },
        }));
        return Object.assign(Object.assign({}, slack_1.slackChartDefaults), { xAxis: discoverxAxis, useUTC: true, color,
            series });
    } }, slack_1.slackChartSize));
exports.discoverCharts.push(Object.assign({ key: types_1.ChartType.SLACK_DISCOVER_TOP5_DAILY, getOption: (data) => {
        if ((0, isArray_1.default)(data.stats.data)) {
            const color = theme_1.lightTheme.charts.getColorPalette(data.stats.data.length - 2);
            const areaSeries = (0, areaSeries_1.default)({
                data: data.stats.data.map(([timestamp, countsForTimestamp]) => [
                    timestamp * 1000,
                    countsForTimestamp.reduce((acc, { count }) => acc + count, 0),
                ]),
                lineStyle: { color: color === null || color === void 0 ? void 0 : color[0], opacity: 1, width: 0.4 },
                areaStyle: { color: color === null || color === void 0 ? void 0 : color[0], opacity: 1 },
            });
            return Object.assign(Object.assign({}, slack_1.slackChartDefaults), { useUTC: true, color, series: [areaSeries] });
        }
        const stats = Object.values(data.stats);
        const color = theme_1.lightTheme.charts.getColorPalette(stats.length - 2);
        const series = stats
            .sort((a, b) => { var _a, _b; return ((_a = a.order) !== null && _a !== void 0 ? _a : 0) - ((_b = b.order) !== null && _b !== void 0 ? _b : 0); })
            .map((topSeries, i) => (0, barSeries_1.default)({
            stack: 'area',
            data: topSeries.data.map(([timestamp, countsForTimestamp]) => [
                timestamp * 1000,
                countsForTimestamp.reduce((acc, { count }) => acc + count, 0),
            ]),
            itemStyle: { color: color === null || color === void 0 ? void 0 : color[i], opacity: 1 },
        }));
        return Object.assign(Object.assign({}, slack_1.slackChartDefaults), { xAxis: discoverxAxis, useUTC: true, color,
            series });
    } }, slack_1.slackChartSize));
exports.discoverCharts.push(Object.assign({ key: types_1.ChartType.SLACK_DISCOVER_PREVIOUS_PERIOD, getOption: (data) => {
        if ((0, isArray_1.default)(data.stats.data)) {
            const dataMiddleIndex = Math.floor(data.stats.data.length / 2);
            const current = data.stats.data.slice(dataMiddleIndex);
            const previous = data.stats.data.slice(0, dataMiddleIndex);
            const color = theme_1.lightTheme.charts.getColorPalette(data.stats.data.length - 2);
            const areaSeries = (0, areaSeries_1.default)({
                name: data.seriesName,
                data: current.map(([timestamp, countsForTimestamp]) => [
                    timestamp * 1000,
                    countsForTimestamp.reduce((acc, { count }) => acc + count, 0),
                ]),
                lineStyle: { color: color === null || color === void 0 ? void 0 : color[0], opacity: 1, width: 0.4 },
                areaStyle: { color: color === null || color === void 0 ? void 0 : color[0], opacity: 1 },
            });
            const previousPeriod = (0, lineSeries_1.default)({
                name: (0, locale_1.t)('previous %s', data.seriesName),
                data: previous.map(([_, countsForTimestamp], i) => [
                    current[i][0] * 1000,
                    countsForTimestamp.reduce((acc, { count }) => acc + count, 0),
                ]),
                lineStyle: { color: theme_1.lightTheme.gray200, type: 'dotted' },
                itemStyle: { color: theme_1.lightTheme.gray200 },
            });
            return Object.assign(Object.assign({}, slack_1.slackChartDefaults), { useUTC: true, color, series: [areaSeries, previousPeriod] });
        }
        const stats = Object.keys(data.stats).map(key => Object.assign({}, { key }, data.stats[key]));
        const color = theme_1.lightTheme.charts.getColorPalette(stats.length - 2);
        const previousPeriodColor = (0, utils_1.lightenHexToRgb)(color);
        const areaSeries = [];
        const lineSeries = [];
        stats
            .sort((a, b) => { var _a, _b; return ((_a = a.order) !== null && _a !== void 0 ? _a : 0) - ((_b = b.order) !== null && _b !== void 0 ? _b : 0); })
            .map((s, i) => {
            const dataMiddleIndex = Math.floor(s.data.length / 2);
            const current = s.data.slice(dataMiddleIndex);
            const previous = s.data.slice(0, dataMiddleIndex);
            areaSeries.push((0, areaSeries_1.default)({
                name: s.key,
                stack: 'area',
                data: s.data
                    .slice(dataMiddleIndex)
                    .map(([timestamp, countsForTimestamp]) => [
                    timestamp * 1000,
                    countsForTimestamp.reduce((acc, { count }) => acc + count, 0),
                ]),
                lineStyle: { color: color === null || color === void 0 ? void 0 : color[i], opacity: 1, width: 0.4 },
                areaStyle: { color: color === null || color === void 0 ? void 0 : color[i], opacity: 1 },
            }));
            lineSeries.push((0, lineSeries_1.default)({
                name: (0, locale_1.t)('previous %s', s.key),
                stack: 'previous',
                data: previous.map(([_, countsForTimestamp], index) => [
                    current[index][0] * 1000,
                    countsForTimestamp.reduce((acc, { count }) => acc + count, 0),
                ]),
                lineStyle: { color: previousPeriodColor === null || previousPeriodColor === void 0 ? void 0 : previousPeriodColor[i], type: 'dotted' },
                itemStyle: { color: previousPeriodColor === null || previousPeriodColor === void 0 ? void 0 : previousPeriodColor[i] },
            }));
        });
        return Object.assign(Object.assign({}, slack_1.slackChartDefaults), { xAxis: discoverxAxis, useUTC: true, color, series: [...areaSeries, ...lineSeries] });
    } }, slack_1.slackChartSize));
//# sourceMappingURL=discover.jsx.map