Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const genericDiscoverQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/genericDiscoverQuery"));
const constants_1 = require("app/utils/performance/constants");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
function getRequestPayload(props) {
    const { eventView, vitals } = props;
    const apiPayload = eventView === null || eventView === void 0 ? void 0 : eventView.getEventsAPIPayload(props.location);
    return Object.assign({ vital: vitals }, (0, pick_1.default)(apiPayload, ['query', ...Object.values(constants_1.PERFORMANCE_URL_PARAM)]));
}
function VitalsCardsDiscoverQuery(props) {
    return (<genericDiscoverQuery_1.default getRequestPayload={getRequestPayload} route="events-vitals" {...props}>
      {(_a) => {
            var { tableData } = _a, rest = (0, tslib_1.__rest)(_a, ["tableData"]);
            return props.children(Object.assign({ vitalsData: tableData }, rest));
        }}
    </genericDiscoverQuery_1.default>);
}
exports.default = (0, withApi_1.default)(VitalsCardsDiscoverQuery);
//# sourceMappingURL=vitalsCardsDiscoverQuery.jsx.map