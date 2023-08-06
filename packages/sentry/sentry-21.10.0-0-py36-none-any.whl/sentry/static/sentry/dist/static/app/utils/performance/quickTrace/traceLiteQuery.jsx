Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const genericDiscoverQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/genericDiscoverQuery"));
const utils_1 = require("app/utils/performance/quickTrace/utils");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
function getTraceLiteRequestPayload(_a) {
    var { eventId } = _a, props = (0, tslib_1.__rest)(_a, ["eventId"]);
    const additionalApiPayload = (0, utils_1.getTraceRequestPayload)(props);
    return Object.assign({ event_id: eventId }, additionalApiPayload);
}
function EmptyTrace({ children }) {
    return (<React.Fragment>
      {children({
            isLoading: false,
            error: null,
            trace: null,
            type: 'partial',
        })}
    </React.Fragment>);
}
function TraceLiteQuery(_a) {
    var { traceId, start, end, statsPeriod, children } = _a, props = (0, tslib_1.__rest)(_a, ["traceId", "start", "end", "statsPeriod", "children"]);
    if (!traceId) {
        return <EmptyTrace>{children}</EmptyTrace>;
    }
    const eventView = (0, utils_1.makeEventView)({ start, end, statsPeriod });
    return (<genericDiscoverQuery_1.default route={`events-trace-light/${traceId}`} getRequestPayload={getTraceLiteRequestPayload} eventView={eventView} {...props}>
      {(_a) => {
            var { tableData } = _a, rest = (0, tslib_1.__rest)(_a, ["tableData"]);
            return children(Object.assign({ 
                // This is using '||` instead of '??` here because
                // the client returns a empty string when the response
                // is 204. And we want the empty string, undefined and
                // null to be converted to null.
                trace: tableData || null, type: 'partial' }, rest));
        }}
    </genericDiscoverQuery_1.default>);
}
exports.default = (0, withApi_1.default)(TraceLiteQuery);
//# sourceMappingURL=traceLiteQuery.jsx.map