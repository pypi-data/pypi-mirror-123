Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const miniBarChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/miniBarChart"));
const locale_1 = require("app/locale");
const formatters_1 = require("app/utils/formatters");
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const sidebarSection_1 = (0, tslib_1.__importDefault)(require("./sidebarSection"));
function GroupReleaseChart(props) {
    const { className, group, lastSeen, firstSeen, statsPeriod, release, releaseStats, environment, environmentStats, title, } = props;
    const stats = group.stats[statsPeriod];
    if (!stats || !stats.length) {
        return null;
    }
    const series = [];
    // Add all events.
    series.push({
        seriesName: (0, locale_1.t)('Events'),
        data: stats.map(point => ({ name: point[0] * 1000, value: point[1] })),
    });
    // Get the timestamp of the first point.
    const firstTime = series[0].data[0].value;
    if (environment && environmentStats) {
        series.push({
            seriesName: (0, locale_1.t)('Events in %s', environment),
            data: environmentStats[statsPeriod].map(point => ({
                name: point[0] * 1000,
                value: point[1],
            })),
        });
    }
    if (release && releaseStats) {
        series.push({
            seriesName: (0, locale_1.t)('Events in release %s', (0, formatters_1.formatVersion)(release.version)),
            data: releaseStats[statsPeriod].map(point => ({
                name: point[0] * 1000,
                value: point[1],
            })),
        });
    }
    const markers = [];
    if (firstSeen) {
        const firstSeenX = new Date(firstSeen).getTime();
        if (firstSeenX >= firstTime) {
            markers.push({
                name: (0, locale_1.t)('First seen'),
                value: firstSeenX,
                color: theme_1.default.pink300,
            });
        }
    }
    if (lastSeen) {
        const lastSeenX = new Date(lastSeen).getTime();
        if (lastSeenX >= firstTime) {
            markers.push({
                name: (0, locale_1.t)('Last seen'),
                value: lastSeenX,
                color: theme_1.default.green300,
            });
        }
    }
    return (<sidebarSection_1.default secondary title={title} className={className}>
      <miniBarChart_1.default isGroupedByDate showTimeInTooltip height={42} series={series} markers={markers}/>
    </sidebarSection_1.default>);
}
exports.default = GroupReleaseChart;
//# sourceMappingURL=releaseChart.jsx.map