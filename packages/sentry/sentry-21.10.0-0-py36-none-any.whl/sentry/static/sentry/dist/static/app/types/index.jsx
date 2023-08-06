// XXX(epurkhiser): When we switch to the new React JSX runtime we will no
// longer need this import and can drop babel-preset-css-prop for babel-preset.
/// <reference types="@emotion/react/types/css-prop" />
Object.defineProperty(exports, "__esModule", { value: true });
exports.HealthStatsPeriodOption = exports.ReleaseComparisonChartType = exports.SessionStatus = exports.SessionField = exports.FrameBadge = exports.EventGroupVariantType = exports.ResolutionStatus = exports.OnboardingTaskKey = exports.ReleaseStatus = exports.RepositoryStatus = exports.GroupActivityType = exports.EventOrGroupType = exports.DataCategoryName = exports.DataCategory = exports.SavedSearchType = exports.SentryInitRenderReactComponent = void 0;
var SentryInitRenderReactComponent;
(function (SentryInitRenderReactComponent) {
    SentryInitRenderReactComponent["INDICATORS"] = "Indicators";
    SentryInitRenderReactComponent["SETUP_WIZARD"] = "SetupWizard";
    SentryInitRenderReactComponent["SYSTEM_ALERTS"] = "SystemAlerts";
    SentryInitRenderReactComponent["U2F_SIGN"] = "U2fSign";
})(SentryInitRenderReactComponent = exports.SentryInitRenderReactComponent || (exports.SentryInitRenderReactComponent = {}));
var SavedSearchType;
(function (SavedSearchType) {
    SavedSearchType[SavedSearchType["ISSUE"] = 0] = "ISSUE";
    SavedSearchType[SavedSearchType["EVENT"] = 1] = "EVENT";
})(SavedSearchType = exports.SavedSearchType || (exports.SavedSearchType = {}));
// https://github.com/getsentry/relay/blob/master/relay-common/src/constants.rs
// Note: the value of the enum on the frontend is plural,
// but the value of the enum on the backend is singular
var DataCategory;
(function (DataCategory) {
    DataCategory["DEFAULT"] = "default";
    DataCategory["ERRORS"] = "errors";
    DataCategory["TRANSACTIONS"] = "transactions";
    DataCategory["ATTACHMENTS"] = "attachments";
})(DataCategory = exports.DataCategory || (exports.DataCategory = {}));
exports.DataCategoryName = {
    [DataCategory.ERRORS]: 'Errors',
    [DataCategory.TRANSACTIONS]: 'Transactions',
    [DataCategory.ATTACHMENTS]: 'Attachments',
};
var EventOrGroupType;
(function (EventOrGroupType) {
    EventOrGroupType["ERROR"] = "error";
    EventOrGroupType["CSP"] = "csp";
    EventOrGroupType["HPKP"] = "hpkp";
    EventOrGroupType["EXPECTCT"] = "expectct";
    EventOrGroupType["EXPECTSTAPLE"] = "expectstaple";
    EventOrGroupType["DEFAULT"] = "default";
    EventOrGroupType["TRANSACTION"] = "transaction";
})(EventOrGroupType = exports.EventOrGroupType || (exports.EventOrGroupType = {}));
var GroupActivityType;
(function (GroupActivityType) {
    GroupActivityType["NOTE"] = "note";
    GroupActivityType["SET_RESOLVED"] = "set_resolved";
    GroupActivityType["SET_RESOLVED_BY_AGE"] = "set_resolved_by_age";
    GroupActivityType["SET_RESOLVED_IN_RELEASE"] = "set_resolved_in_release";
    GroupActivityType["SET_RESOLVED_IN_COMMIT"] = "set_resolved_in_commit";
    GroupActivityType["SET_RESOLVED_IN_PULL_REQUEST"] = "set_resolved_in_pull_request";
    GroupActivityType["SET_UNRESOLVED"] = "set_unresolved";
    GroupActivityType["SET_IGNORED"] = "set_ignored";
    GroupActivityType["SET_PUBLIC"] = "set_public";
    GroupActivityType["SET_PRIVATE"] = "set_private";
    GroupActivityType["SET_REGRESSION"] = "set_regression";
    GroupActivityType["CREATE_ISSUE"] = "create_issue";
    GroupActivityType["UNMERGE_SOURCE"] = "unmerge_source";
    GroupActivityType["UNMERGE_DESTINATION"] = "unmerge_destination";
    GroupActivityType["FIRST_SEEN"] = "first_seen";
    GroupActivityType["ASSIGNED"] = "assigned";
    GroupActivityType["UNASSIGNED"] = "unassigned";
    GroupActivityType["MERGE"] = "merge";
    GroupActivityType["REPROCESS"] = "reprocess";
    GroupActivityType["MARK_REVIEWED"] = "mark_reviewed";
})(GroupActivityType = exports.GroupActivityType || (exports.GroupActivityType = {}));
var RepositoryStatus;
(function (RepositoryStatus) {
    RepositoryStatus["ACTIVE"] = "active";
    RepositoryStatus["DISABLED"] = "disabled";
    RepositoryStatus["HIDDEN"] = "hidden";
    RepositoryStatus["PENDING_DELETION"] = "pending_deletion";
    RepositoryStatus["DELETION_IN_PROGRESS"] = "deletion_in_progress";
})(RepositoryStatus = exports.RepositoryStatus || (exports.RepositoryStatus = {}));
var ReleaseStatus;
(function (ReleaseStatus) {
    ReleaseStatus["Active"] = "open";
    ReleaseStatus["Archived"] = "archived";
})(ReleaseStatus = exports.ReleaseStatus || (exports.ReleaseStatus = {}));
var OnboardingTaskKey;
(function (OnboardingTaskKey) {
    OnboardingTaskKey["FIRST_PROJECT"] = "create_project";
    OnboardingTaskKey["FIRST_EVENT"] = "send_first_event";
    OnboardingTaskKey["INVITE_MEMBER"] = "invite_member";
    OnboardingTaskKey["SECOND_PLATFORM"] = "setup_second_platform";
    OnboardingTaskKey["USER_CONTEXT"] = "setup_user_context";
    OnboardingTaskKey["RELEASE_TRACKING"] = "setup_release_tracking";
    OnboardingTaskKey["SOURCEMAPS"] = "setup_sourcemaps";
    OnboardingTaskKey["USER_REPORTS"] = "setup_user_reports";
    OnboardingTaskKey["ISSUE_TRACKER"] = "setup_issue_tracker";
    OnboardingTaskKey["ALERT_RULE"] = "setup_alert_rules";
    OnboardingTaskKey["FIRST_TRANSACTION"] = "setup_transactions";
})(OnboardingTaskKey = exports.OnboardingTaskKey || (exports.OnboardingTaskKey = {}));
var ResolutionStatus;
(function (ResolutionStatus) {
    ResolutionStatus["RESOLVED"] = "resolved";
    ResolutionStatus["UNRESOLVED"] = "unresolved";
    ResolutionStatus["IGNORED"] = "ignored";
})(ResolutionStatus = exports.ResolutionStatus || (exports.ResolutionStatus = {}));
var EventGroupVariantType;
(function (EventGroupVariantType) {
    EventGroupVariantType["CUSTOM_FINGERPRINT"] = "custom-fingerprint";
    EventGroupVariantType["COMPONENT"] = "component";
    EventGroupVariantType["SALTED_COMPONENT"] = "salted-component";
})(EventGroupVariantType = exports.EventGroupVariantType || (exports.EventGroupVariantType = {}));
var FrameBadge;
(function (FrameBadge) {
    FrameBadge["SENTINEL"] = "sentinel";
    FrameBadge["PREFIX"] = "prefix";
    FrameBadge["GROUPING"] = "grouping";
})(FrameBadge = exports.FrameBadge || (exports.FrameBadge = {}));
var SessionField;
(function (SessionField) {
    SessionField["SESSIONS"] = "sum(session)";
    SessionField["USERS"] = "count_unique(user)";
    SessionField["DURATION"] = "p50(session.duration)";
})(SessionField = exports.SessionField || (exports.SessionField = {}));
var SessionStatus;
(function (SessionStatus) {
    SessionStatus["HEALTHY"] = "healthy";
    SessionStatus["ABNORMAL"] = "abnormal";
    SessionStatus["ERRORED"] = "errored";
    SessionStatus["CRASHED"] = "crashed";
})(SessionStatus = exports.SessionStatus || (exports.SessionStatus = {}));
var ReleaseComparisonChartType;
(function (ReleaseComparisonChartType) {
    ReleaseComparisonChartType["CRASH_FREE_USERS"] = "crashFreeUsers";
    ReleaseComparisonChartType["HEALTHY_USERS"] = "healthyUsers";
    ReleaseComparisonChartType["ABNORMAL_USERS"] = "abnormalUsers";
    ReleaseComparisonChartType["ERRORED_USERS"] = "erroredUsers";
    ReleaseComparisonChartType["CRASHED_USERS"] = "crashedUsers";
    ReleaseComparisonChartType["CRASH_FREE_SESSIONS"] = "crashFreeSessions";
    ReleaseComparisonChartType["HEALTHY_SESSIONS"] = "healthySessions";
    ReleaseComparisonChartType["ABNORMAL_SESSIONS"] = "abnormalSessions";
    ReleaseComparisonChartType["ERRORED_SESSIONS"] = "erroredSessions";
    ReleaseComparisonChartType["CRASHED_SESSIONS"] = "crashedSessions";
    ReleaseComparisonChartType["SESSION_COUNT"] = "sessionCount";
    ReleaseComparisonChartType["USER_COUNT"] = "userCount";
    ReleaseComparisonChartType["ERROR_COUNT"] = "errorCount";
    ReleaseComparisonChartType["TRANSACTION_COUNT"] = "transactionCount";
    ReleaseComparisonChartType["FAILURE_RATE"] = "failureRate";
    ReleaseComparisonChartType["SESSION_DURATION"] = "sessionDuration";
})(ReleaseComparisonChartType = exports.ReleaseComparisonChartType || (exports.ReleaseComparisonChartType = {}));
var HealthStatsPeriodOption;
(function (HealthStatsPeriodOption) {
    HealthStatsPeriodOption["AUTO"] = "auto";
    HealthStatsPeriodOption["TWENTY_FOUR_HOURS"] = "24h";
})(HealthStatsPeriodOption = exports.HealthStatsPeriodOption || (exports.HealthStatsPeriodOption = {}));
//# sourceMappingURL=index.jsx.map