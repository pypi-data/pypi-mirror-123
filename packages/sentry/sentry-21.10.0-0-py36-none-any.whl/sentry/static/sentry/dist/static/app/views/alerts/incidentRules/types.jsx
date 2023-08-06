Object.defineProperty(exports, "__esModule", { value: true });
exports.TargetLabel = exports.TargetType = exports.ActionLabel = exports.ActionType = exports.TimeWindow = exports.TimePeriod = exports.SessionsAggregate = exports.Datasource = exports.EventTypes = exports.Dataset = exports.AlertRuleComparisonType = exports.AlertRuleThresholdType = void 0;
const locale_1 = require("app/locale");
var AlertRuleThresholdType;
(function (AlertRuleThresholdType) {
    AlertRuleThresholdType[AlertRuleThresholdType["ABOVE"] = 0] = "ABOVE";
    AlertRuleThresholdType[AlertRuleThresholdType["BELOW"] = 1] = "BELOW";
})(AlertRuleThresholdType = exports.AlertRuleThresholdType || (exports.AlertRuleThresholdType = {}));
var AlertRuleComparisonType;
(function (AlertRuleComparisonType) {
    AlertRuleComparisonType["COUNT"] = "count";
    AlertRuleComparisonType["CHANGE"] = "change";
})(AlertRuleComparisonType = exports.AlertRuleComparisonType || (exports.AlertRuleComparisonType = {}));
var Dataset;
(function (Dataset) {
    Dataset["ERRORS"] = "events";
    Dataset["TRANSACTIONS"] = "transactions";
    Dataset["SESSIONS"] = "sessions";
})(Dataset = exports.Dataset || (exports.Dataset = {}));
var EventTypes;
(function (EventTypes) {
    EventTypes["DEFAULT"] = "default";
    EventTypes["ERROR"] = "error";
    EventTypes["TRANSACTION"] = "transaction";
    EventTypes["USER"] = "user";
    EventTypes["SESSION"] = "session";
})(EventTypes = exports.EventTypes || (exports.EventTypes = {}));
var Datasource;
(function (Datasource) {
    Datasource["ERROR_DEFAULT"] = "error_default";
    Datasource["DEFAULT"] = "default";
    Datasource["ERROR"] = "error";
    Datasource["TRANSACTION"] = "transaction";
})(Datasource = exports.Datasource || (exports.Datasource = {}));
/**
 * This is not a real aggregate as crash-free sessions/users can be only calculated on frontend by comparing the count of sessions broken down by status
 * It is here nevertheless to shoehorn sessions dataset into existing alerts codebase
 * This will most likely be revised as we introduce the metrics dataset
 */
var SessionsAggregate;
(function (SessionsAggregate) {
    SessionsAggregate["CRASH_FREE_SESSIONS"] = "percentage(sessions_crashed, sessions) AS _crash_rate_alert_aggregate";
    SessionsAggregate["CRASH_FREE_USERS"] = "percentage(users_crashed, users) AS _crash_rate_alert_aggregate";
})(SessionsAggregate = exports.SessionsAggregate || (exports.SessionsAggregate = {}));
var TimePeriod;
(function (TimePeriod) {
    TimePeriod["SIX_HOURS"] = "6h";
    TimePeriod["ONE_DAY"] = "1d";
    TimePeriod["THREE_DAYS"] = "3d";
    // Seven days is actually 10080m but we have a max of 10000 events
    TimePeriod["SEVEN_DAYS"] = "10000m";
    TimePeriod["FOURTEEN_DAYS"] = "14d";
    TimePeriod["THIRTY_DAYS"] = "30d";
})(TimePeriod = exports.TimePeriod || (exports.TimePeriod = {}));
var TimeWindow;
(function (TimeWindow) {
    TimeWindow[TimeWindow["ONE_MINUTE"] = 1] = "ONE_MINUTE";
    TimeWindow[TimeWindow["FIVE_MINUTES"] = 5] = "FIVE_MINUTES";
    TimeWindow[TimeWindow["TEN_MINUTES"] = 10] = "TEN_MINUTES";
    TimeWindow[TimeWindow["FIFTEEN_MINUTES"] = 15] = "FIFTEEN_MINUTES";
    TimeWindow[TimeWindow["THIRTY_MINUTES"] = 30] = "THIRTY_MINUTES";
    TimeWindow[TimeWindow["ONE_HOUR"] = 60] = "ONE_HOUR";
    TimeWindow[TimeWindow["TWO_HOURS"] = 120] = "TWO_HOURS";
    TimeWindow[TimeWindow["FOUR_HOURS"] = 240] = "FOUR_HOURS";
    TimeWindow[TimeWindow["ONE_DAY"] = 1440] = "ONE_DAY";
})(TimeWindow = exports.TimeWindow || (exports.TimeWindow = {}));
var ActionType;
(function (ActionType) {
    ActionType["EMAIL"] = "email";
    ActionType["SLACK"] = "slack";
    ActionType["PAGERDUTY"] = "pagerduty";
    ActionType["MSTEAMS"] = "msteams";
    ActionType["SENTRY_APP"] = "sentry_app";
})(ActionType = exports.ActionType || (exports.ActionType = {}));
exports.ActionLabel = {
    [ActionType.EMAIL]: (0, locale_1.t)('Email'),
    [ActionType.SLACK]: (0, locale_1.t)('Slack'),
    [ActionType.PAGERDUTY]: (0, locale_1.t)('Pagerduty'),
    [ActionType.MSTEAMS]: (0, locale_1.t)('MS Teams'),
    [ActionType.SENTRY_APP]: (0, locale_1.t)('Notification'),
};
var TargetType;
(function (TargetType) {
    // A direct reference, like an email address, Slack channel, or PagerDuty service
    TargetType["SPECIFIC"] = "specific";
    // A specific user. This could be used to grab the user's email address.
    TargetType["USER"] = "user";
    // A specific team. This could be used to send an email to everyone associated with a team.
    TargetType["TEAM"] = "team";
    // A Sentry App instead of any of the above.
    TargetType["SENTRY_APP"] = "sentry_app";
})(TargetType = exports.TargetType || (exports.TargetType = {}));
exports.TargetLabel = {
    [TargetType.USER]: (0, locale_1.t)('Member'),
    [TargetType.TEAM]: (0, locale_1.t)('Team'),
};
//# sourceMappingURL=types.jsx.map