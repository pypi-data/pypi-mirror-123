Object.defineProperty(exports, "__esModule", { value: true });
exports.TraceFullDetailedQuery = exports.TraceFullQuery = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const genericDiscoverQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/genericDiscoverQuery"));
const utils_1 = require("app/utils/performance/quickTrace/utils");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
function getTraceFullRequestPayload(_a) {
    var { detailed, eventId } = _a, props = (0, tslib_1.__rest)(_a, ["detailed", "eventId"]);
    const additionalApiPayload = (0, utils_1.getTraceRequestPayload)(props);
    additionalApiPayload.detailed = detailed ? '1' : '0';
    if (eventId) {
        additionalApiPayload.event_id = eventId;
    }
    return additionalApiPayload;
}
function EmptyTrace({ children }) {
    return (<React.Fragment>
      {children({
            isLoading: false,
            error: null,
            traces: null,
            type: 'full',
        })}
    </React.Fragment>);
}
function GenericTraceFullQuery(_a) {
    var { traceId, start, end, statsPeriod, children } = _a, props = (0, tslib_1.__rest)(_a, ["traceId", "start", "end", "statsPeriod", "children"]);
    if (!traceId) {
        return <EmptyTrace>{children}</EmptyTrace>;
    }
    const eventView = (0, utils_1.makeEventView)({ start, end, statsPeriod });
    return (<genericDiscoverQuery_1.default route={`events-trace/${traceId}`} getRequestPayload={getTraceFullRequestPayload} eventView={eventView} {...props}>
      {(_a) => {
            var { tableData } = _a, rest = (0, tslib_1.__rest)(_a, ["tableData"]);
            return children(Object.assign({ 
                // This is using '||` instead of '??` here because
                // the client returns a empty string when the response
                // is 204. And we want the empty string, undefined and
                // null to be converted to null.
                traces: tableData || null, type: 'full' }, rest));
        }}
    </genericDiscoverQuery_1.default>);
}
exports.TraceFullQuery = (0, withApi_1.default)((props) => (<GenericTraceFullQuery {...props} detailed={false}/>));
exports.TraceFullDetailedQuery = (0, withApi_1.default)((props) => (<GenericTraceFullQuery {...props} detailed/>));
//# sourceMappingURL=traceFullQuery.jsx.map