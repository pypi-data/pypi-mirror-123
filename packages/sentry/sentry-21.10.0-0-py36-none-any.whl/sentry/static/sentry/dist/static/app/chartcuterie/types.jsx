Object.defineProperty(exports, "__esModule", { value: true });
exports.ChartType = void 0;
/**
 * Defines the keys which may be passed into the chartcuterie chart rendering
 * service.
 *
 * When adding or removing from this list, please also update the
 * sentry/charts/types.py file
 */
var ChartType;
(function (ChartType) {
    ChartType["SLACK_DISCOVER_TOTAL_PERIOD"] = "slack:discover.totalPeriod";
    ChartType["SLACK_DISCOVER_TOTAL_DAILY"] = "slack:discover.totalDaily";
    ChartType["SLACK_DISCOVER_TOP5_PERIOD"] = "slack:discover.top5Period";
    ChartType["SLACK_DISCOVER_TOP5_DAILY"] = "slack:discover.top5Daily";
    ChartType["SLACK_DISCOVER_PREVIOUS_PERIOD"] = "slack:discover.previousPeriod";
})(ChartType = exports.ChartType || (exports.ChartType = {}));
//# sourceMappingURL=types.jsx.map