Object.defineProperty(exports, "__esModule", { value: true });
exports.fillChartDataFromMetricsResponse = exports.getBreakdownChartData = void 0;
function getSerieNameByGroups(groupByKeys, groupBy) {
    return groupByKeys.map(groupByKey => groupBy[groupByKey]).join('_');
}
function getBreakdownChartData({ response, sessionResponseIndex, legend, }) {
    return response.groups.reduce((groups, group, index) => {
        const groupByKeys = Object.keys(group.by);
        if (!groupByKeys.length) {
            groups[index] = {
                seriesName: legend !== null && legend !== void 0 ? legend : `Query ${sessionResponseIndex}`,
                data: [],
            };
            return groups;
        }
        const serieNameByGroups = getSerieNameByGroups(groupByKeys, group.by);
        groups[serieNameByGroups] = {
            seriesName: legend ? `${legend}_${serieNameByGroups}` : serieNameByGroups,
            data: [],
        };
        return groups;
    }, {});
}
exports.getBreakdownChartData = getBreakdownChartData;
function fillChartDataFromMetricsResponse({ response, field, chartData, valueFormatter, }) {
    response.intervals.forEach((interval, index) => {
        for (const groupsIndex in response.groups) {
            const group = response.groups[groupsIndex];
            const groupByKeys = Object.keys(group.by);
            const value = group.series[field][index];
            if (!groupByKeys.length) {
                chartData[0].data.push({
                    name: interval,
                    value: typeof valueFormatter === 'function' ? valueFormatter(value) : value,
                });
                return;
            }
            const serieNameByGroups = getSerieNameByGroups(groupByKeys, group.by);
            chartData[serieNameByGroups].data.push({
                name: interval,
                value: typeof valueFormatter === 'function' ? valueFormatter(value) : value,
            });
        }
    });
    return chartData;
}
exports.fillChartDataFromMetricsResponse = fillChartDataFromMetricsResponse;
//# sourceMappingURL=utils.jsx.map