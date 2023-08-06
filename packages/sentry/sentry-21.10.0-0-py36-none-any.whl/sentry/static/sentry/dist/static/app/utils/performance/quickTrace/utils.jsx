Object.defineProperty(exports, "__esModule", { value: true });
exports.isTraceFullDetailed = exports.isTraceFull = exports.filterTrace = exports.reduceTrace = exports.getTraceTimeRangeFromEvent = exports.makeEventView = exports.getTraceRequestPayload = exports.parseQuickTrace = exports.flattenRelevantPaths = exports.isCurrentEvent = exports.isTransaction = void 0;
const tslib_1 = require("tslib");
const omit_1 = (0, tslib_1.__importDefault)(require("lodash/omit"));
const moment_timezone_1 = (0, tslib_1.__importDefault)(require("moment-timezone"));
const utils_1 = require("app/components/events/interfaces/spans/utils");
const globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
const analytics_1 = require("app/utils/analytics");
const eventView_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/eventView"));
function isTransaction(event) {
    return event.type === 'transaction';
}
exports.isTransaction = isTransaction;
/**
 * An event can be an error or a transaction. We need to check whether the current
 * event id is in the list of errors as well
 */
function isCurrentEvent(event, currentEvent) {
    if (isTransaction(currentEvent)) {
        return event.event_id === currentEvent.id;
    }
    else {
        return (event.errors !== undefined && event.errors.some(e => e.event_id === currentEvent.id));
    }
}
exports.isCurrentEvent = isCurrentEvent;
/**
 * The `events-full` endpoint returns the full trace containing the specified event.
 * This means any sibling paths in the trace will also be returned.
 *
 * This method strips away these sibling paths leaving only the path from the root to
 * the specified event and all of its children/descendants.
 *
 * This method additionally flattens the trace into an array of the transactions in
 * the trace.
 */
function flattenRelevantPaths(currentEvent, traceFull) {
    const relevantPath = [];
    const events = [];
    /**
     * First find a path from the root transaction to the current transaction via
     * a breadth first search. This adds all transactions from the root to the
     * current transaction (excluding the current transaction itself), to the
     * relevant path.
     */
    const paths = [{ event: traceFull, path: [] }];
    while (paths.length) {
        const current = paths.shift();
        if (isCurrentEvent(current.event, currentEvent)) {
            for (const node of current.path) {
                relevantPath.push(node);
            }
            events.push(current.event);
        }
        else {
            const path = [...current.path, simplifyEvent(current.event)];
            for (const child of current.event.children) {
                paths.push({ event: child, path });
            }
        }
    }
    if (!events.length) {
        throw new Error('No relevant path exists!');
    }
    /**
     * Traverse all transactions from current transaction onwards and add
     * them all to the relevant path.
     */
    while (events.length) {
        const current = events.shift();
        for (const child of current.children) {
            events.push(child);
        }
        relevantPath.push(simplifyEvent(current));
    }
    return relevantPath;
}
exports.flattenRelevantPaths = flattenRelevantPaths;
function simplifyEvent(event) {
    return (0, omit_1.default)(event, ['children']);
}
function parseQuickTrace(quickTrace, event, organization) {
    var _a, _b, _c;
    const { type, trace } = quickTrace;
    if (type === 'empty' || trace === null) {
        throw new Error('Current event not in trace navigator!');
    }
    const isFullTrace = type === 'full';
    const current = (_a = trace.find(e => isCurrentEvent(e, event))) !== null && _a !== void 0 ? _a : null;
    if (current === null) {
        throw new Error('Current event not in trace navigator!');
    }
    /**
     * The parent event is the direct ancestor of the current event.
     * This takes priority over the root, meaning if the parent is
     * the root of the trace, this favours showing it as the parent.
     */
    const parent = current.parent_event_id
        ? (_b = trace.find(e => e.event_id === current.parent_event_id)) !== null && _b !== void 0 ? _b : null
        : null;
    /**
     * The root event is the first event in the trace. This has lower priority
     * than the parent event, meaning if the root event is the parent event of
     * the current event, this favours showing it as the parent event.
     */
    const root = (_c = trace.find(e => 
    // a root can't be the current event
    e.event_id !== current.event_id &&
        // a root can't be the direct parent
        e.event_id !== (parent === null || parent === void 0 ? void 0 : parent.event_id) &&
        // a root has to to be the first generation
        e.generation === 0)) !== null && _c !== void 0 ? _c : null;
    const isChildren = e => e.parent_event_id === current.event_id;
    const isDescendant = e => 
    // the current generation needs to be known to determine a descendant
    current.generation !== null &&
        // the event's generation needs to be known to determine a descendant
        e.generation !== null &&
        // a descendant is the generation after the direct children
        current.generation + 1 < e.generation;
    const isAncestor = e => 
    // the current generation needs to be known to determine an ancestor
    current.generation !== null &&
        // the event's generation needs to be known to determine an ancestor
        e.generation !== null &&
        // an ancestor can't be the root
        e.generation > 0 &&
        // an ancestor is the generation before the direct parent
        current.generation - 1 > e.generation;
    const ancestors = isFullTrace ? [] : null;
    const children = [];
    const descendants = isFullTrace ? [] : null;
    const projects = new Set();
    trace.forEach(e => {
        projects.add(e.project_id);
        if (isChildren(e)) {
            children.push(e);
        }
        else if (isFullTrace) {
            if (isAncestor(e)) {
                ancestors === null || ancestors === void 0 ? void 0 : ancestors.push(e);
            }
            else if (isDescendant(e)) {
                descendants === null || descendants === void 0 ? void 0 : descendants.push(e);
            }
        }
    });
    if (isFullTrace && projects.size > 1) {
        handleProjectMeta(organization, projects.size);
    }
    return {
        root,
        ancestors: ancestors === null ? null : sortTraceLite(ancestors),
        parent,
        current,
        children: sortTraceLite(children),
        descendants: descendants === null ? null : sortTraceLite(descendants),
    };
}
exports.parseQuickTrace = parseQuickTrace;
function sortTraceLite(trace) {
    return trace.sort((a, b) => b['transaction.duration'] - a['transaction.duration']);
}
function getTraceRequestPayload({ eventView, location }) {
    return (0, omit_1.default)(eventView.getEventsAPIPayload(location), ['field', 'sort', 'per_page']);
}
exports.getTraceRequestPayload = getTraceRequestPayload;
function makeEventView({ start, end, statsPeriod, }) {
    return eventView_1.default.fromSavedQuery({
        id: undefined,
        version: 2,
        name: '',
        // This field doesn't actually do anything,
        // just here to satisfy a constraint in EventView.
        fields: ['transaction.duration'],
        projects: [globalSelectionHeader_1.ALL_ACCESS_PROJECTS],
        query: '',
        environment: [],
        start,
        end,
        range: statsPeriod,
    });
}
exports.makeEventView = makeEventView;
function getTraceTimeRangeFromEvent(event) {
    const start = isTransaction(event)
        ? event.startTimestamp
        : (0, moment_timezone_1.default)(event.dateReceived ? event.dateReceived : event.dateCreated).valueOf() /
            1000;
    const end = isTransaction(event) ? event.endTimestamp : start;
    return (0, utils_1.getTraceDateTimeRange)({ start, end });
}
exports.getTraceTimeRangeFromEvent = getTraceTimeRangeFromEvent;
function reduceTrace(trace, visitor, initialValue) {
    let result = initialValue;
    const events = [trace];
    while (events.length) {
        const current = events.pop();
        for (const child of current.children) {
            events.push(child);
        }
        result = visitor(result, current);
    }
    return result;
}
exports.reduceTrace = reduceTrace;
function filterTrace(trace, predicate) {
    return reduceTrace(trace, (transactions, transaction) => {
        if (predicate(transaction)) {
            transactions.push(transaction);
        }
        return transactions;
    }, []);
}
exports.filterTrace = filterTrace;
function isTraceFull(transaction) {
    return Boolean(transaction.event_id);
}
exports.isTraceFull = isTraceFull;
function isTraceFullDetailed(transaction) {
    return Boolean(transaction.event_id);
}
exports.isTraceFullDetailed = isTraceFullDetailed;
function handleProjectMeta(organization, projects) {
    (0, analytics_1.trackAnalyticsEvent)({
        eventKey: 'quick_trace.connected_services',
        eventName: 'Quick Trace: Connected Services',
        organization_id: parseInt(organization.id, 10),
        projects,
    });
}
//# sourceMappingURL=utils.jsx.map