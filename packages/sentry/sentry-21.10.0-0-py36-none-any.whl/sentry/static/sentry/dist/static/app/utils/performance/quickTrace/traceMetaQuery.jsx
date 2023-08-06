Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const genericDiscoverQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/genericDiscoverQuery"));
const utils_1 = require("app/utils/performance/quickTrace/utils");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
function TraceMetaQuery(_a) {
    var { traceId, start, end, statsPeriod, children } = _a, props = (0, tslib_1.__rest)(_a, ["traceId", "start", "end", "statsPeriod", "children"]);
    if (!traceId) {
        return (<React.Fragment>
        {children({
                isLoading: false,
                error: null,
                meta: null,
            })}
      </React.Fragment>);
    }
    const eventView = (0, utils_1.makeEventView)({ start, end, statsPeriod });
    return (<genericDiscoverQuery_1.default route={`events-trace-meta/${traceId}`} getRequestPayload={utils_1.getTraceRequestPayload} eventView={eventView} {...props}>
      {(_a) => {
            var { tableData } = _a, rest = (0, tslib_1.__rest)(_a, ["tableData"]);
            return children(Object.assign({ meta: tableData }, rest));
        }}
    </genericDiscoverQuery_1.default>);
}
exports.default = (0, withApi_1.default)(TraceMetaQuery);
//# sourceMappingURL=traceMetaQuery.jsx.map