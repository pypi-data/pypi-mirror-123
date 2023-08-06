Object.defineProperty(exports, "__esModule", { value: true });
exports.isRootTransaction = exports.getTraceInfo = exports.getTraceDetailsUrl = void 0;
const globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
const utils_1 = require("app/utils/performance/quickTrace/utils");
function getTraceDetailsUrl(organization, traceSlug, dateSelection, query) {
    const { start, end, statsPeriod } = dateSelection;
    return {
        pathname: `/organizations/${organization.slug}/performance/trace/${traceSlug}/`,
        query: Object.assign(Object.assign({}, query), { statsPeriod, [globalSelectionHeader_1.PAGE_URL_PARAM.PAGE_START]: start, [globalSelectionHeader_1.PAGE_URL_PARAM.PAGE_END]: end }),
    };
}
exports.getTraceDetailsUrl = getTraceDetailsUrl;
function traceVisitor() {
    return (accumulator, event) => {
        var _a;
        for (const error of (_a = event.errors) !== null && _a !== void 0 ? _a : []) {
            accumulator.errors.add(error.event_id);
        }
        accumulator.transactions.add(event.event_id);
        accumulator.projects.add(event.project_slug);
        accumulator.startTimestamp = Math.min(accumulator.startTimestamp, event.start_timestamp);
        accumulator.endTimestamp = Math.max(accumulator.endTimestamp, event.timestamp);
        accumulator.maxGeneration = Math.max(accumulator.maxGeneration, event.generation);
        return accumulator;
    };
}
function getTraceInfo(traces) {
    const initial = {
        projects: new Set(),
        errors: new Set(),
        transactions: new Set(),
        startTimestamp: Number.MAX_SAFE_INTEGER,
        endTimestamp: 0,
        maxGeneration: 0,
    };
    return traces.reduce((info, trace) => (0, utils_1.reduceTrace)(trace, traceVisitor(), info), initial);
}
exports.getTraceInfo = getTraceInfo;
function isRootTransaction(trace) {
    // Root transactions has no parent_span_id
    return trace.parent_span_id === null;
}
exports.isRootTransaction = isRootTransaction;
//# sourceMappingURL=utils.jsx.map