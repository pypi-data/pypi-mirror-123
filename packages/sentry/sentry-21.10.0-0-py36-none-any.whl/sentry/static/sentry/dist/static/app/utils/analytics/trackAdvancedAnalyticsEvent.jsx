Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const dashboardsAnalyticsEvents_1 = require("./dashboardsAnalyticsEvents");
const discoverAnalyticsEvents_1 = require("./discoverAnalyticsEvents");
const growthAnalyticsEvents_1 = require("./growthAnalyticsEvents");
const issueAnalyticsEvents_1 = require("./issueAnalyticsEvents");
const makeAnalyticsFunction_1 = (0, tslib_1.__importDefault)(require("./makeAnalyticsFunction"));
const performanceAnalyticsEvents_1 = require("./performanceAnalyticsEvents");
const allEventMap = Object.assign(Object.assign(Object.assign(Object.assign(Object.assign({}, growthAnalyticsEvents_1.growthEventMap), issueAnalyticsEvents_1.issueEventMap), performanceAnalyticsEvents_1.performanceEventMap), dashboardsAnalyticsEvents_1.dashboardsEventMap), discoverAnalyticsEvents_1.discoverEventMap);
/**
 * Generic typed analytics function for growth, issue, and performance events.
 * Can split up analytics functions to a smaller set of events like we do for trackIntegrationAnalytics
 */
const trackAdvancedAnalyticsEvent = (0, makeAnalyticsFunction_1.default)(allEventMap);
exports.default = trackAdvancedAnalyticsEvent;
//# sourceMappingURL=trackAdvancedAnalyticsEvent.jsx.map