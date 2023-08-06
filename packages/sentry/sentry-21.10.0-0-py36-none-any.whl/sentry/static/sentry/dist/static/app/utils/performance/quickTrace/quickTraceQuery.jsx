Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const traceFullQuery_1 = require("app/utils/performance/quickTrace/traceFullQuery");
const traceLiteQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/performance/quickTrace/traceLiteQuery"));
const utils_1 = require("app/utils/performance/quickTrace/utils");
function QuickTraceQuery(_a) {
    var _b, _c;
    var { children, event } = _a, props = (0, tslib_1.__rest)(_a, ["children", "event"]);
    const traceId = (_c = (_b = event.contexts) === null || _b === void 0 ? void 0 : _b.trace) === null || _c === void 0 ? void 0 : _c.trace_id;
    if (!traceId) {
        return (<React.Fragment>
        {children({
                isLoading: false,
                error: null,
                trace: [],
                type: 'empty',
                currentEvent: null,
            })}
      </React.Fragment>);
    }
    const { start, end } = (0, utils_1.getTraceTimeRangeFromEvent)(event);
    return (<traceLiteQuery_1.default eventId={event.id} traceId={traceId} start={start} end={end} {...props}>
      {traceLiteResults => (<traceFullQuery_1.TraceFullQuery eventId={event.id} traceId={traceId} start={start} end={end} {...props}>
          {traceFullResults => {
                var _a, _b, _c;
                if (!traceFullResults.isLoading &&
                    traceFullResults.error === null &&
                    traceFullResults.traces !== null) {
                    for (const subtrace of traceFullResults.traces) {
                        try {
                            const trace = (0, utils_1.flattenRelevantPaths)(event, subtrace);
                            return children(Object.assign(Object.assign({}, traceFullResults), { trace, currentEvent: (_a = trace.find(e => (0, utils_1.isCurrentEvent)(e, event))) !== null && _a !== void 0 ? _a : null }));
                        }
                        catch (_d) {
                            // let this fall through and check the next subtrace
                            // or use the trace lite results
                        }
                    }
                }
                if (!traceLiteResults.isLoading &&
                    traceLiteResults.error === null &&
                    traceLiteResults.trace !== null) {
                    const { trace } = traceLiteResults;
                    return children(Object.assign(Object.assign({}, traceLiteResults), { currentEvent: (_b = trace.find(e => (0, utils_1.isCurrentEvent)(e, event))) !== null && _b !== void 0 ? _b : null }));
                }
                return children({
                    // only use the light results loading state if it didn't error
                    // if it did, we should rely on the full results
                    isLoading: traceLiteResults.error
                        ? traceFullResults.isLoading
                        : traceLiteResults.isLoading || traceFullResults.isLoading,
                    // swallow any errors from the light results because we
                    // should rely on the full results in this situations
                    error: traceFullResults.error,
                    trace: [],
                    // if we reach this point but there were some traces in the full results,
                    // that means there were other transactions in the trace, but the current
                    // event could not be found
                    type: ((_c = traceFullResults.traces) === null || _c === void 0 ? void 0 : _c.length) ? 'missing' : 'empty',
                    currentEvent: null,
                });
            }}
        </traceFullQuery_1.TraceFullQuery>)}
    </traceLiteQuery_1.default>);
}
exports.default = QuickTraceQuery;
//# sourceMappingURL=quickTraceQuery.jsx.map