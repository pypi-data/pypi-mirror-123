Object.defineProperty(exports, "__esModule", { value: true });
exports.TrendsEventsDiscoverQuery = exports.getTrendsRequestPayload = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const genericDiscoverQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/genericDiscoverQuery"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const utils_1 = require("app/views/performance/trends/utils");
function getTrendsRequestPayload(props) {
    const { eventView } = props;
    const apiPayload = eventView === null || eventView === void 0 ? void 0 : eventView.getEventsAPIPayload(props.location);
    const trendFunction = (0, utils_1.getCurrentTrendFunction)(props.location);
    const trendParameter = (0, utils_1.getCurrentTrendParameter)(props.location);
    apiPayload.trendFunction = (0, utils_1.generateTrendFunctionAsString)(trendFunction.field, trendParameter.column);
    apiPayload.trendType = eventView === null || eventView === void 0 ? void 0 : eventView.trendType;
    apiPayload.interval = eventView === null || eventView === void 0 ? void 0 : eventView.interval;
    apiPayload.middle = eventView === null || eventView === void 0 ? void 0 : eventView.middle;
    return apiPayload;
}
exports.getTrendsRequestPayload = getTrendsRequestPayload;
function TrendsDiscoverQuery(props) {
    return (<genericDiscoverQuery_1.default route="events-trends-stats" getRequestPayload={getTrendsRequestPayload} {...props}>
      {(_a) => {
            var { tableData } = _a, rest = (0, tslib_1.__rest)(_a, ["tableData"]);
            return props.children(Object.assign({ trendsData: tableData }, rest));
        }}
    </genericDiscoverQuery_1.default>);
}
function EventsDiscoverQuery(props) {
    return (<genericDiscoverQuery_1.default route="events-trends" getRequestPayload={getTrendsRequestPayload} {...props}>
      {(_a) => {
            var { tableData } = _a, rest = (0, tslib_1.__rest)(_a, ["tableData"]);
            return props.children(Object.assign({ trendsData: tableData }, rest));
        }}
    </genericDiscoverQuery_1.default>);
}
exports.TrendsEventsDiscoverQuery = (0, withApi_1.default)(EventsDiscoverQuery);
exports.default = (0, withApi_1.default)(TrendsDiscoverQuery);
//# sourceMappingURL=trendsDiscoverQuery.jsx.map