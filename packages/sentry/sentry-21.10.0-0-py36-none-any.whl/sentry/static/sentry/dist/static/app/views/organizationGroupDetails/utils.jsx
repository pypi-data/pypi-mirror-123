Object.defineProperty(exports, "__esModule", { value: true });
exports.getGroupReprocessingStatus = exports.ReprocessingStatus = exports.getGroupMostRecentActivity = exports.getSubscriptionReason = exports.getEventEnvironment = exports.fetchGroupUserReports = exports.markEventSeen = exports.fetchGroupEvent = void 0;
const tslib_1 = require("tslib");
const orderBy_1 = (0, tslib_1.__importDefault)(require("lodash/orderBy"));
const group_1 = require("app/actionCreators/group");
const api_1 = require("app/api");
const locale_1 = require("app/locale");
/**
 * Fetches group data and mark as seen
 *
 * @param orgId organization slug
 * @param groupId groupId
 * @param eventId eventId or "latest" or "oldest"
 * @param envNames
 * @param projectId project slug required for eventId that is not latest or oldest
 */
function fetchGroupEvent(api, orgId, groupId, eventId, envNames, projectId) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const url = eventId === 'latest' || eventId === 'oldest'
            ? `/issues/${groupId}/events/${eventId}/`
            : `/projects/${orgId}/${projectId}/events/${eventId}/`;
        const query = {};
        if (envNames.length !== 0) {
            query.environment = envNames;
        }
        const data = yield api.requestPromise(url, { query });
        return data;
    });
}
exports.fetchGroupEvent = fetchGroupEvent;
function markEventSeen(api, orgId, projectId, groupId) {
    (0, group_1.bulkUpdate)(api, {
        orgId,
        projectId,
        itemIds: [groupId],
        failSilently: true,
        data: { hasSeen: true },
    }, {});
}
exports.markEventSeen = markEventSeen;
function fetchGroupUserReports(groupId, query) {
    const api = new api_1.Client();
    return api.requestPromise(`/issues/${groupId}/user-reports/`, {
        includeAllArgs: true,
        query,
    });
}
exports.fetchGroupUserReports = fetchGroupUserReports;
/**
 * Returns the environment name for an event or null
 *
 * @param event
 */
function getEventEnvironment(event) {
    const tag = event.tags.find(({ key }) => key === 'environment');
    return tag ? tag.value : null;
}
exports.getEventEnvironment = getEventEnvironment;
const SUBSCRIPTION_REASONS = {
    commented: (0, locale_1.t)("You're receiving workflow notifications because you have commented on this issue."),
    assigned: (0, locale_1.t)("You're receiving workflow notifications because you were assigned to this issue."),
    bookmarked: (0, locale_1.t)("You're receiving workflow notifications because you have bookmarked this issue."),
    changed_status: (0, locale_1.t)("You're receiving workflow notifications because you have changed the status of this issue."),
    mentioned: (0, locale_1.t)("You're receiving workflow notifications because you have been mentioned in this issue."),
};
/**
 * @param group
 * @param removeLinks add/remove links to subscription reasons text (default: false)
 * @returns Reason for subscription
 */
function getSubscriptionReason(group, removeLinks = false) {
    if (group.subscriptionDetails && group.subscriptionDetails.disabled) {
        return (0, locale_1.tct)('You have [link:disabled workflow notifications] for this project.', {
            link: removeLinks ? <span /> : <a href="/account/settings/notifications/"/>,
        });
    }
    if (!group.isSubscribed) {
        return (0, locale_1.t)('Subscribe to workflow notifications for this issue');
    }
    if (group.subscriptionDetails) {
        const { reason } = group.subscriptionDetails;
        if (reason === 'unknown') {
            return (0, locale_1.t)("You're receiving workflow notifications because you are subscribed to this issue.");
        }
        if (reason && SUBSCRIPTION_REASONS.hasOwnProperty(reason)) {
            return SUBSCRIPTION_REASONS[reason];
        }
    }
    return (0, locale_1.tct)("You're receiving updates because you are [link:subscribed to workflow notifications] for this project.", {
        link: removeLinks ? <span /> : <a href="/account/settings/notifications/"/>,
    });
}
exports.getSubscriptionReason = getSubscriptionReason;
function getGroupMostRecentActivity(activities) {
    // Most recent activity
    return (0, orderBy_1.default)([...activities], ({ dateCreated }) => new Date(dateCreated), ['desc'])[0];
}
exports.getGroupMostRecentActivity = getGroupMostRecentActivity;
var ReprocessingStatus;
(function (ReprocessingStatus) {
    ReprocessingStatus["REPROCESSED_AND_HASNT_EVENT"] = "reprocessed_and_hasnt_event";
    ReprocessingStatus["REPROCESSED_AND_HAS_EVENT"] = "reprocessed_and_has_event";
    ReprocessingStatus["REPROCESSING"] = "reprocessing";
    ReprocessingStatus["NO_STATUS"] = "no_status";
})(ReprocessingStatus = exports.ReprocessingStatus || (exports.ReprocessingStatus = {}));
// Reprocessing Checks
function getGroupReprocessingStatus(group, mostRecentActivity) {
    const { status, count, activity: activities } = group;
    const groupCount = Number(count);
    switch (status) {
        case 'reprocessing':
            return ReprocessingStatus.REPROCESSING;
        case 'unresolved': {
            const groupMostRecentActivity = mostRecentActivity !== null && mostRecentActivity !== void 0 ? mostRecentActivity : getGroupMostRecentActivity(activities);
            if ((groupMostRecentActivity === null || groupMostRecentActivity === void 0 ? void 0 : groupMostRecentActivity.type) === 'reprocess') {
                if (groupCount === 0) {
                    return ReprocessingStatus.REPROCESSED_AND_HASNT_EVENT;
                }
                return ReprocessingStatus.REPROCESSED_AND_HAS_EVENT;
            }
            return ReprocessingStatus.NO_STATUS;
        }
        default:
            return ReprocessingStatus.NO_STATUS;
    }
}
exports.getGroupReprocessingStatus = getGroupReprocessingStatus;
//# sourceMappingURL=utils.jsx.map