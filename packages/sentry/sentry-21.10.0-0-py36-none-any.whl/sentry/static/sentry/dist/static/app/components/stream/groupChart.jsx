Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_lazyload_1 = (0, tslib_1.__importDefault)(require("react-lazyload"));
const miniBarChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/miniBarChart"));
const locale_1 = require("app/locale");
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
function GroupChart({ data, statsPeriod, showSecondaryPoints = false, height = 24, }) {
    const stats = statsPeriod
        ? data.filtered
            ? data.filtered.stats[statsPeriod]
            : data.stats[statsPeriod]
        : [];
    const secondaryStats = statsPeriod && data.filtered ? data.stats[statsPeriod] : null;
    if (!stats || !stats.length) {
        return null;
    }
    let colors = undefined;
    let emphasisColors = undefined;
    const series = [];
    if (showSecondaryPoints && secondaryStats && secondaryStats.length) {
        series.push({
            seriesName: (0, locale_1.t)('Total Events'),
            data: secondaryStats.map(point => ({ name: point[0] * 1000, value: point[1] })),
        });
        series.push({
            seriesName: (0, locale_1.t)('Matching Events'),
            data: stats.map(point => ({ name: point[0] * 1000, value: point[1] })),
        });
    }
    else {
        // Colors are custom to preserve historical appearance where the single series is
        // considerably darker than the two series results.
        colors = [theme_1.default.gray300];
        emphasisColors = [theme_1.default.purple300];
        series.push({
            seriesName: (0, locale_1.t)('Events'),
            data: stats.map(point => ({ name: point[0] * 1000, value: point[1] })),
        });
    }
    return (<react_lazyload_1.default debounce={50} height={height}>
      <miniBarChart_1.default height={height} isGroupedByDate showTimeInTooltip series={series} colors={colors} emphasisColors={emphasisColors} hideDelay={50}/>
    </react_lazyload_1.default>);
}
exports.default = GroupChart;
//# sourceMappingURL=groupChart.jsx.map