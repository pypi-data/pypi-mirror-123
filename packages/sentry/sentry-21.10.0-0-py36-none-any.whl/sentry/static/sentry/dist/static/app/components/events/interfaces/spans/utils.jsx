Object.defineProperty(exports, "__esModule", { value: true });
exports.scrollToSpan = exports.getMeasurementBounds = exports.getMeasurements = exports.durationlessBrowserOps = exports.isEventFromBrowserJavaScriptSDK = exports.unwrapTreeDepth = exports.isOrphanTreeDepth = exports.parseTrace = exports.getTraceContext = exports.getSpanParentSpanID = exports.getSpanTraceID = exports.getSpanOperation = exports.getSpanID = exports.isOrphanSpan = exports.isGapSpan = exports.getTraceDateTimeRange = exports.generateRootSpan = exports.boundsGenerator = exports.parseSpanTimestamps = exports.TimestampStatus = exports.isValidSpanID = void 0;
const tslib_1 = require("tslib");
const react_router_1 = require("react-router");
const isNumber_1 = (0, tslib_1.__importDefault)(require("lodash/isNumber"));
const isString_1 = (0, tslib_1.__importDefault)(require("lodash/isString"));
const set_1 = (0, tslib_1.__importDefault)(require("lodash/set"));
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const event_1 = require("app/types/event");
const utils_1 = require("app/types/utils");
const constants_1 = require("app/utils/performance/vitals/constants");
const isValidSpanID = (maybeSpanID) => (0, isString_1.default)(maybeSpanID) && maybeSpanID.length > 0;
exports.isValidSpanID = isValidSpanID;
const normalizeTimestamps = (spanBounds) => {
    const { startTimestamp, endTimestamp } = spanBounds;
    if (startTimestamp > endTimestamp) {
        return { startTimestamp: endTimestamp, endTimestamp: startTimestamp };
    }
    return spanBounds;
};
var TimestampStatus;
(function (TimestampStatus) {
    TimestampStatus[TimestampStatus["Stable"] = 0] = "Stable";
    TimestampStatus[TimestampStatus["Reversed"] = 1] = "Reversed";
    TimestampStatus[TimestampStatus["Equal"] = 2] = "Equal";
})(TimestampStatus = exports.TimestampStatus || (exports.TimestampStatus = {}));
const parseSpanTimestamps = (spanBounds) => {
    const startTimestamp = spanBounds.startTimestamp;
    const endTimestamp = spanBounds.endTimestamp;
    if (startTimestamp < endTimestamp) {
        return TimestampStatus.Stable;
    }
    if (startTimestamp === endTimestamp) {
        return TimestampStatus.Equal;
    }
    return TimestampStatus.Reversed;
};
exports.parseSpanTimestamps = parseSpanTimestamps;
// given the start and end trace timestamps, and the view window, we want to generate a function
// that'll output the relative %'s for the width and placements relative to the left-hand side.
//
// The view window (viewStart and viewEnd) are percentage values (between 0% and 100%), they correspond to the window placement
// between the start and end trace timestamps.
const boundsGenerator = (bounds) => {
    const { viewStart, viewEnd } = bounds;
    const { startTimestamp: traceStartTimestamp, endTimestamp: traceEndTimestamp } = normalizeTimestamps({
        startTimestamp: bounds.traceStartTimestamp,
        endTimestamp: bounds.traceEndTimestamp,
    });
    // viewStart and viewEnd are percentage values (%) of the view window relative to the left
    // side of the trace view minimap
    // invariant: viewStart <= viewEnd
    // duration of the entire trace in seconds
    const traceDuration = traceEndTimestamp - traceStartTimestamp;
    const viewStartTimestamp = traceStartTimestamp + viewStart * traceDuration;
    const viewEndTimestamp = traceEndTimestamp - (1 - viewEnd) * traceDuration;
    const viewDuration = viewEndTimestamp - viewStartTimestamp;
    return (spanBounds) => {
        // TODO: alberto.... refactor so this is impossible 😠
        if (traceDuration <= 0) {
            return {
                type: 'TRACE_TIMESTAMPS_EQUAL',
                isSpanVisibleInView: true,
            };
        }
        if (viewDuration <= 0) {
            return {
                type: 'INVALID_VIEW_WINDOW',
                isSpanVisibleInView: true,
            };
        }
        const { startTimestamp, endTimestamp } = normalizeTimestamps(spanBounds);
        const timestampStatus = (0, exports.parseSpanTimestamps)(spanBounds);
        const start = (startTimestamp - viewStartTimestamp) / viewDuration;
        const end = (endTimestamp - viewStartTimestamp) / viewDuration;
        const isSpanVisibleInView = end > 0 && start < 1;
        switch (timestampStatus) {
            case TimestampStatus.Equal: {
                return {
                    type: 'TIMESTAMPS_EQUAL',
                    start,
                    width: 1,
                    // a span bar is visible even if they're at the extreme ends of the view selection.
                    // these edge cases are:
                    // start == end == 0, and
                    // start == end == 1
                    isSpanVisibleInView: end >= 0 && start <= 1,
                };
            }
            case TimestampStatus.Reversed: {
                return {
                    type: 'TIMESTAMPS_REVERSED',
                    start,
                    end,
                    isSpanVisibleInView,
                };
            }
            case TimestampStatus.Stable: {
                return {
                    type: 'TIMESTAMPS_STABLE',
                    start,
                    end,
                    isSpanVisibleInView,
                };
            }
            default: {
                const _exhaustiveCheck = timestampStatus;
                return _exhaustiveCheck;
            }
        }
    };
};
exports.boundsGenerator = boundsGenerator;
function generateRootSpan(trace) {
    const rootSpan = {
        trace_id: trace.traceID,
        span_id: trace.rootSpanID,
        parent_span_id: trace.parentSpanID,
        start_timestamp: trace.traceStartTimestamp,
        timestamp: trace.traceEndTimestamp,
        op: trace.op,
        description: trace.description,
        data: {},
        status: trace.rootSpanStatus,
    };
    return rootSpan;
}
exports.generateRootSpan = generateRootSpan;
// start and end are assumed to be unix timestamps with fractional seconds
function getTraceDateTimeRange(input) {
    const start = moment_1.default
        .unix(input.start)
        .subtract(12, 'hours')
        .utc()
        .format('YYYY-MM-DDTHH:mm:ss.SSS');
    const end = moment_1.default
        .unix(input.end)
        .add(12, 'hours')
        .utc()
        .format('YYYY-MM-DDTHH:mm:ss.SSS');
    return {
        start,
        end,
    };
}
exports.getTraceDateTimeRange = getTraceDateTimeRange;
function isGapSpan(span) {
    if ('type' in span) {
        return span.type === 'gap';
    }
    return false;
}
exports.isGapSpan = isGapSpan;
function isOrphanSpan(span) {
    if ('type' in span) {
        if (span.type === 'orphan') {
            return true;
        }
        if (span.type === 'gap') {
            return span.isOrphan;
        }
    }
    return false;
}
exports.isOrphanSpan = isOrphanSpan;
function getSpanID(span, defaultSpanID = '') {
    if (isGapSpan(span)) {
        return defaultSpanID;
    }
    return span.span_id;
}
exports.getSpanID = getSpanID;
function getSpanOperation(span) {
    if (isGapSpan(span)) {
        return undefined;
    }
    return span.op;
}
exports.getSpanOperation = getSpanOperation;
function getSpanTraceID(span) {
    if (isGapSpan(span)) {
        return 'gap-span';
    }
    return span.trace_id;
}
exports.getSpanTraceID = getSpanTraceID;
function getSpanParentSpanID(span) {
    if (isGapSpan(span)) {
        return 'gap-span';
    }
    return span.parent_span_id;
}
exports.getSpanParentSpanID = getSpanParentSpanID;
function getTraceContext(event) {
    var _a;
    return (_a = event === null || event === void 0 ? void 0 : event.contexts) === null || _a === void 0 ? void 0 : _a.trace;
}
exports.getTraceContext = getTraceContext;
function parseTrace(event) {
    var _a;
    const spanEntry = event.entries.find((entry) => {
        return entry.type === event_1.EntryType.SPANS;
    });
    const spans = (_a = spanEntry === null || spanEntry === void 0 ? void 0 : spanEntry.data) !== null && _a !== void 0 ? _a : [];
    const traceContext = getTraceContext(event);
    const traceID = (traceContext && traceContext.trace_id) || '';
    const rootSpanID = (traceContext && traceContext.span_id) || '';
    const rootSpanOpName = (traceContext && traceContext.op) || 'transaction';
    const description = traceContext && traceContext.description;
    const parentSpanID = traceContext && traceContext.parent_span_id;
    const rootSpanStatus = traceContext && traceContext.status;
    if (!spanEntry || spans.length <= 0) {
        return {
            op: rootSpanOpName,
            childSpans: {},
            traceStartTimestamp: event.startTimestamp,
            traceEndTimestamp: event.endTimestamp,
            traceID,
            rootSpanID,
            rootSpanStatus,
            parentSpanID,
            spans: [],
            description,
        };
    }
    // any span may be a parent of another span
    const potentialParents = new Set(spans.map(span => {
        return span.span_id;
    }));
    // the root transaction span is a parent of all other spans
    potentialParents.add(rootSpanID);
    // we reduce spans to become an object mapping span ids to their children
    const init = {
        op: rootSpanOpName,
        childSpans: {},
        traceStartTimestamp: event.startTimestamp,
        traceEndTimestamp: event.endTimestamp,
        traceID,
        rootSpanID,
        rootSpanStatus,
        parentSpanID,
        spans,
        description,
    };
    const reduced = spans.reduce((acc, inputSpan) => {
        var _a;
        let span = inputSpan;
        const parentSpanId = getSpanParentSpanID(span);
        const hasParent = parentSpanId && potentialParents.has(parentSpanId);
        if (!(0, exports.isValidSpanID)(parentSpanId) || !hasParent) {
            // this span is considered an orphan with respect to the spans within this transaction.
            // although the span is an orphan, it's still a descendant of this transaction,
            // so we set its parent span id to be the root transaction span's id
            span.parent_span_id = rootSpanID;
            span = Object.assign({ type: 'orphan' }, span);
        }
        (0, utils_1.assert)(span.parent_span_id);
        // get any span children whose parent_span_id is equal to span.parent_span_id,
        // otherwise start with an empty array
        const spanChildren = (_a = acc.childSpans[span.parent_span_id]) !== null && _a !== void 0 ? _a : [];
        spanChildren.push(span);
        (0, set_1.default)(acc.childSpans, span.parent_span_id, spanChildren);
        // set trace start & end timestamps based on given span's start and end timestamps
        if (!acc.traceStartTimestamp || span.start_timestamp < acc.traceStartTimestamp) {
            acc.traceStartTimestamp = span.start_timestamp;
        }
        // establish trace end timestamp
        const hasEndTimestamp = (0, isNumber_1.default)(span.timestamp);
        if (!acc.traceEndTimestamp) {
            if (hasEndTimestamp) {
                acc.traceEndTimestamp = span.timestamp;
                return acc;
            }
            acc.traceEndTimestamp = span.start_timestamp;
            return acc;
        }
        if (hasEndTimestamp && span.timestamp > acc.traceEndTimestamp) {
            acc.traceEndTimestamp = span.timestamp;
            return acc;
        }
        if (span.start_timestamp > acc.traceEndTimestamp) {
            acc.traceEndTimestamp = span.start_timestamp;
        }
        return acc;
    }, init);
    // sort span children
    Object.values(reduced.childSpans).forEach(spanChildren => {
        spanChildren.sort(sortSpans);
    });
    return reduced;
}
exports.parseTrace = parseTrace;
function sortSpans(firstSpan, secondSpan) {
    // orphan spans come after non-orphan spans.
    if (isOrphanSpan(firstSpan) && !isOrphanSpan(secondSpan)) {
        // sort secondSpan before firstSpan
        return 1;
    }
    if (!isOrphanSpan(firstSpan) && isOrphanSpan(secondSpan)) {
        // sort firstSpan before secondSpan
        return -1;
    }
    // sort spans by their start timestamp in ascending order
    if (firstSpan.start_timestamp < secondSpan.start_timestamp) {
        // sort firstSpan before secondSpan
        return -1;
    }
    if (firstSpan.start_timestamp === secondSpan.start_timestamp) {
        return 0;
    }
    // sort secondSpan before firstSpan
    return 1;
}
function isOrphanTreeDepth(treeDepth) {
    if (typeof treeDepth === 'number') {
        return false;
    }
    return (treeDepth === null || treeDepth === void 0 ? void 0 : treeDepth.type) === 'orphan';
}
exports.isOrphanTreeDepth = isOrphanTreeDepth;
function unwrapTreeDepth(treeDepth) {
    if (isOrphanTreeDepth(treeDepth)) {
        return treeDepth.depth;
    }
    return treeDepth;
}
exports.unwrapTreeDepth = unwrapTreeDepth;
function isEventFromBrowserJavaScriptSDK(event) {
    var _a;
    const sdkName = (_a = event.sdk) === null || _a === void 0 ? void 0 : _a.name;
    if (!sdkName) {
        return false;
    }
    // based on https://github.com/getsentry/sentry-javascript/blob/master/packages/browser/src/version.ts
    return [
        'sentry.javascript.browser',
        'sentry.javascript.react',
        'sentry.javascript.gatsby',
        'sentry.javascript.ember',
        'sentry.javascript.vue',
        'sentry.javascript.angular',
        'sentry.javascript.nextjs',
    ].includes(sdkName.toLowerCase());
}
exports.isEventFromBrowserJavaScriptSDK = isEventFromBrowserJavaScriptSDK;
// Durationless ops from: https://github.com/getsentry/sentry-javascript/blob/0defcdcc2dfe719343efc359d58c3f90743da2cd/packages/apm/src/integrations/tracing.ts#L629-L688
// PerformanceMark: Duration is 0 as per https://developer.mozilla.org/en-US/docs/Web/API/PerformanceMark
// PerformancePaintTiming: Duration is 0 as per https://developer.mozilla.org/en-US/docs/Web/API/PerformancePaintTiming
exports.durationlessBrowserOps = ['mark', 'paint'];
function hasFailedThreshold(marks) {
    const names = Object.keys(marks);
    const records = Object.values(constants_1.WEB_VITAL_DETAILS).filter(vital => names.includes(vital.slug));
    return records.some(record => {
        const value = marks[record.slug];
        if (typeof value === 'number' && typeof record.poorThreshold === 'number') {
            return value >= record.poorThreshold;
        }
        return false;
    });
}
function getMeasurements(event) {
    if (!event.measurements) {
        return new Map();
    }
    const measurements = Object.keys(event.measurements)
        .filter(name => name.startsWith('mark.'))
        .map(name => {
        const slug = name.slice('mark.'.length);
        const associatedMeasurement = event.measurements[slug];
        return {
            name,
            timestamp: event.measurements[name].value,
            value: associatedMeasurement ? associatedMeasurement.value : undefined,
        };
    });
    const mergedMeasurements = new Map();
    measurements.forEach(measurement => {
        const name = measurement.name.slice('mark.'.length);
        const value = measurement.value;
        if (mergedMeasurements.has(measurement.timestamp)) {
            const verticalMark = mergedMeasurements.get(measurement.timestamp);
            verticalMark.marks = Object.assign(Object.assign({}, verticalMark.marks), { [name]: value });
            if (!verticalMark.failedThreshold) {
                verticalMark.failedThreshold = hasFailedThreshold(verticalMark.marks);
            }
            mergedMeasurements.set(measurement.timestamp, verticalMark);
            return;
        }
        const marks = {
            [name]: value,
        };
        mergedMeasurements.set(measurement.timestamp, {
            marks,
            failedThreshold: hasFailedThreshold(marks),
        });
    });
    return mergedMeasurements;
}
exports.getMeasurements = getMeasurements;
function getMeasurementBounds(timestamp, generateBounds) {
    const bounds = generateBounds({
        startTimestamp: timestamp,
        endTimestamp: timestamp,
    });
    switch (bounds.type) {
        case 'TRACE_TIMESTAMPS_EQUAL':
        case 'INVALID_VIEW_WINDOW': {
            return {
                warning: undefined,
                left: undefined,
                width: undefined,
                isSpanVisibleInView: bounds.isSpanVisibleInView,
            };
        }
        case 'TIMESTAMPS_EQUAL': {
            return {
                warning: undefined,
                left: bounds.start,
                width: 0.00001,
                isSpanVisibleInView: bounds.isSpanVisibleInView,
            };
        }
        case 'TIMESTAMPS_REVERSED': {
            return {
                warning: undefined,
                left: bounds.start,
                width: bounds.end - bounds.start,
                isSpanVisibleInView: bounds.isSpanVisibleInView,
            };
        }
        case 'TIMESTAMPS_STABLE': {
            return {
                warning: void 0,
                left: bounds.start,
                width: bounds.end - bounds.start,
                isSpanVisibleInView: bounds.isSpanVisibleInView,
            };
        }
        default: {
            const _exhaustiveCheck = bounds;
            return _exhaustiveCheck;
        }
    }
}
exports.getMeasurementBounds = getMeasurementBounds;
function scrollToSpan(spanId, scrollToHash, location) {
    return (e) => {
        // do not use the default anchor behaviour
        // because it will be hidden behind the minimap
        e.preventDefault();
        const hash = `#span-${spanId}`;
        scrollToHash(hash);
        // TODO(txiao): This is causing a rerender of the whole page,
        // which can be slow.
        //
        // make sure to update the location
        react_router_1.browserHistory.push(Object.assign(Object.assign({}, location), { hash }));
    };
}
exports.scrollToSpan = scrollToSpan;
//# sourceMappingURL=utils.jsx.map