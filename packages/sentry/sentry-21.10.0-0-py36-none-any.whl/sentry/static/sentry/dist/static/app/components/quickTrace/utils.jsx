Object.defineProperty(exports, "__esModule", { value: true });
exports.generateTraceTarget = exports.generateMultiTransactionsTarget = exports.generateSingleTransactionTarget = exports.generateSingleErrorTarget = exports.generateIssueEventTarget = exports.isQuickTraceEvent = void 0;
const tslib_1 = require("tslib");
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
const utils_1 = require("app/utils");
const eventView_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/eventView"));
const urls_1 = require("app/utils/discover/urls");
const utils_2 = require("app/utils/performance/quickTrace/utils");
const tokenizeSearch_1 = require("app/utils/tokenizeSearch");
const utils_3 = require("app/views/performance/traceDetails/utils");
const utils_4 = require("app/views/performance/utils");
function isQuickTraceEvent(event) {
    return (0, utils_1.defined)(event['transaction.duration']);
}
exports.isQuickTraceEvent = isQuickTraceEvent;
function generateIssueEventTarget(event, organization) {
    return `/organizations/${organization.slug}/issues/${event.issue_id}/events/${event.event_id}`;
}
exports.generateIssueEventTarget = generateIssueEventTarget;
function generatePerformanceEventTarget(event, organization, location) {
    const eventSlug = (0, urls_1.generateEventSlug)({
        id: event.event_id,
        project: event.project_slug,
    });
    const query = Object.assign(Object.assign({}, location.query), { project: String(event.project_id) });
    return (0, utils_4.getTransactionDetailsUrl)(organization, eventSlug, event.transaction, query);
}
function generateDiscoverEventTarget(event, organization, location) {
    const eventSlug = (0, urls_1.generateEventSlug)({
        id: event.event_id,
        project: event.project_slug,
    });
    const newLocation = Object.assign(Object.assign({}, location), { query: Object.assign(Object.assign({}, location.query), { project: String(event.project_id) }) });
    return (0, urls_1.eventDetailsRouteWithEventView)({
        orgSlug: organization.slug,
        eventSlug,
        eventView: eventView_1.default.fromLocation(newLocation),
    });
}
function generateSingleErrorTarget(event, organization, location, destination) {
    switch (destination) {
        case 'issue':
            return generateIssueEventTarget(event, organization);
        case 'discover':
        default:
            return generateDiscoverEventTarget(event, organization, location);
    }
}
exports.generateSingleErrorTarget = generateSingleErrorTarget;
function generateSingleTransactionTarget(event, organization, location, destination) {
    switch (destination) {
        case 'performance':
            return generatePerformanceEventTarget(event, organization, location);
        case 'discover':
        default:
            return generateDiscoverEventTarget(event, organization, location);
    }
}
exports.generateSingleTransactionTarget = generateSingleTransactionTarget;
function generateMultiTransactionsTarget(currentEvent, events, organization, groupType) {
    const queryResults = new tokenizeSearch_1.MutableSearch([]);
    const eventIds = events.map(child => child.event_id);
    for (let i = 0; i < eventIds.length; i++) {
        queryResults.addOp(i === 0 ? '(' : 'OR');
        queryResults.addFreeText(`id:${eventIds[i]}`);
        if (i === eventIds.length - 1) {
            queryResults.addOp(')');
        }
    }
    const { start, end } = (0, utils_2.getTraceTimeRangeFromEvent)(currentEvent);
    const traceEventView = eventView_1.default.fromSavedQuery({
        id: undefined,
        name: `${groupType} Transactions of Event ID ${currentEvent.id}`,
        fields: ['transaction', 'project', 'trace.span', 'transaction.duration', 'timestamp'],
        orderby: '-timestamp',
        query: queryResults.formatString(),
        projects: [...new Set(events.map(child => child.project_id))],
        version: 2,
        start,
        end,
    });
    return traceEventView.getResultsViewUrlTarget(organization.slug);
}
exports.generateMultiTransactionsTarget = generateMultiTransactionsTarget;
function generateTraceTarget(event, organization) {
    var _a, _b, _c;
    const traceId = (_c = (_b = (_a = event.contexts) === null || _a === void 0 ? void 0 : _a.trace) === null || _b === void 0 ? void 0 : _b.trace_id) !== null && _c !== void 0 ? _c : '';
    const dateSelection = (0, getParams_1.getParams)((0, utils_2.getTraceTimeRangeFromEvent)(event));
    if (organization.features.includes('performance-view')) {
        // TODO(txiao): Should this persist the current query when going to trace view?
        return (0, utils_3.getTraceDetailsUrl)(organization, traceId, dateSelection, {});
    }
    const eventView = eventView_1.default.fromSavedQuery(Object.assign({ id: undefined, name: `Events with Trace ID ${traceId}`, fields: ['title', 'event.type', 'project', 'trace.span', 'timestamp'], orderby: '-timestamp', query: `trace:${traceId}`, projects: organization.features.includes('global-views')
            ? [globalSelectionHeader_1.ALL_ACCESS_PROJECTS]
            : [Number(event.projectID)], version: 2 }, dateSelection));
    return eventView.getResultsViewUrlTarget(organization.slug);
}
exports.generateTraceTarget = generateTraceTarget;
//# sourceMappingURL=utils.jsx.map