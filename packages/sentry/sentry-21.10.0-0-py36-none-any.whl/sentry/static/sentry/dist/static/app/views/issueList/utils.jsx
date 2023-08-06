Object.defineProperty(exports, "__esModule", { value: true });
exports.getDisplayLabel = exports.IssueDisplayOptions = exports.getSortLabel = exports.IssueSortOptions = exports.TAB_MAX_COUNT = exports.isForReviewQuery = exports.getTabsWithCounts = exports.getTabs = exports.Query = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const locale_1 = require("app/locale");
var Query;
(function (Query) {
    Query["FOR_REVIEW"] = "is:unresolved is:for_review assigned_or_suggested:[me, none]";
    Query["UNRESOLVED"] = "is:unresolved";
    Query["IGNORED"] = "is:ignored";
    Query["REPROCESSING"] = "is:reprocessing";
})(Query = exports.Query || (exports.Query = {}));
/**
 * Get a list of currently active tabs
 */
function getTabs(organization) {
    const tabs = [
        [
            Query.UNRESOLVED,
            {
                name: (0, locale_1.t)('All Unresolved'),
                analyticsName: 'unresolved',
                count: true,
                enabled: true,
                tooltipTitle: (0, locale_1.t)(`All unresolved issues.`),
            },
        ],
        [
            Query.FOR_REVIEW,
            {
                name: (0, locale_1.t)('For Review'),
                analyticsName: 'needs_review',
                count: true,
                enabled: true,
                tooltipTitle: (0, locale_1.t)(`Issues are marked for review when they are created, unresolved, or unignored.
          Mark an issue reviewed to move it out of this list.
          Issues are automatically marked reviewed in 7 days.`),
            },
        ],
        [
            Query.IGNORED,
            {
                name: (0, locale_1.t)('Ignored'),
                analyticsName: 'ignored',
                count: true,
                enabled: true,
                tooltipTitle: (0, locale_1.t)(`Ignored issues don’t trigger alerts. When their ignore
        conditions are met they become Unresolved and are flagged for review.`),
            },
        ],
        [
            Query.REPROCESSING,
            {
                name: (0, locale_1.t)('Reprocessing'),
                analyticsName: 'reprocessing',
                count: true,
                enabled: organization.features.includes('reprocessing-v2'),
                tooltipTitle: (0, locale_1.tct)(`These [link:reprocessing issues] will take some time to complete.
        Any new issues that are created during reprocessing will be flagged for review.`, {
                    link: (<externalLink_1.default href="https://docs.sentry.io/product/error-monitoring/reprocessing/"/>),
                }),
                tooltipHoverable: true,
            },
        ],
    ];
    return tabs.filter(([_query, tab]) => tab.enabled);
}
exports.getTabs = getTabs;
/**
 * @returns queries that should have counts fetched
 */
function getTabsWithCounts(organization) {
    const tabs = getTabs(organization);
    return tabs.filter(([_query, tab]) => tab.count).map(([query]) => query);
}
exports.getTabsWithCounts = getTabsWithCounts;
function isForReviewQuery(query) {
    return !!query && /\bis:for_review\b/.test(query);
}
exports.isForReviewQuery = isForReviewQuery;
// the tab counts will look like 99+
exports.TAB_MAX_COUNT = 99;
var IssueSortOptions;
(function (IssueSortOptions) {
    IssueSortOptions["DATE"] = "date";
    IssueSortOptions["NEW"] = "new";
    IssueSortOptions["PRIORITY"] = "priority";
    IssueSortOptions["FREQ"] = "freq";
    IssueSortOptions["USER"] = "user";
    IssueSortOptions["TREND"] = "trend";
    IssueSortOptions["INBOX"] = "inbox";
})(IssueSortOptions = exports.IssueSortOptions || (exports.IssueSortOptions = {}));
function getSortLabel(key) {
    switch (key) {
        case IssueSortOptions.NEW:
            return (0, locale_1.t)('First Seen');
        case IssueSortOptions.PRIORITY:
            return (0, locale_1.t)('Priority');
        case IssueSortOptions.FREQ:
            return (0, locale_1.t)('Events');
        case IssueSortOptions.USER:
            return (0, locale_1.t)('Users');
        case IssueSortOptions.TREND:
            return (0, locale_1.t)('Relative Change');
        case IssueSortOptions.INBOX:
            return (0, locale_1.t)('Date Added');
        case IssueSortOptions.DATE:
        default:
            return (0, locale_1.t)('Last Seen');
    }
}
exports.getSortLabel = getSortLabel;
var IssueDisplayOptions;
(function (IssueDisplayOptions) {
    IssueDisplayOptions["EVENTS"] = "events";
    IssueDisplayOptions["SESSIONS"] = "sessions";
})(IssueDisplayOptions = exports.IssueDisplayOptions || (exports.IssueDisplayOptions = {}));
function getDisplayLabel(key) {
    switch (key) {
        case IssueDisplayOptions.SESSIONS:
            return (0, locale_1.t)('Events as %');
        case IssueDisplayOptions.EVENTS:
        default:
            return (0, locale_1.t)('Event Count');
    }
}
exports.getDisplayLabel = getDisplayLabel;
//# sourceMappingURL=utils.jsx.map