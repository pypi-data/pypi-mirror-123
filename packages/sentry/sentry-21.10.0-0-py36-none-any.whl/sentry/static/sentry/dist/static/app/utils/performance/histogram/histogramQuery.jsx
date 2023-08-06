Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const omit_1 = (0, tslib_1.__importDefault)(require("lodash/omit"));
const genericDiscoverQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/genericDiscoverQuery"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
function getHistogramRequestPayload(props) {
    const { fields, numBuckets, min, max, precision, dataFilter, eventView, location } = props;
    const baseApiPayload = {
        field: fields,
        numBuckets,
        min,
        max,
        precision,
        dataFilter,
    };
    const additionalApiPayload = (0, omit_1.default)(eventView.getEventsAPIPayload(location), [
        'field',
        'sort',
        'per_page',
    ]);
    const apiPayload = Object.assign(baseApiPayload, additionalApiPayload);
    return apiPayload;
}
function HistogramQuery(props) {
    const { children, fields, didReceiveMultiAxis } = props;
    function didFetch(data) {
        if (didReceiveMultiAxis) {
            const counts = {};
            Object.entries(data).forEach(([key, values]) => (counts[key] = values.length
                ? values.reduce((prev, curr) => prev + curr.count, 0)
                : 0));
            didReceiveMultiAxis(counts);
        }
    }
    if (fields.length === 0) {
        return (<React.Fragment>
        {children({
                isLoading: false,
                error: null,
                pageLinks: null,
                histograms: {},
            })}
      </React.Fragment>);
    }
    return (<genericDiscoverQuery_1.default route="events-histogram" getRequestPayload={getHistogramRequestPayload} didFetch={didFetch} {...(0, omit_1.default)(props, 'children')}>
      {(_a) => {
            var { tableData } = _a, rest = (0, tslib_1.__rest)(_a, ["tableData"]);
            return props.children(Object.assign({ histograms: tableData }, rest));
        }}
    </genericDiscoverQuery_1.default>);
}
exports.default = (0, withApi_1.default)(HistogramQuery);
//# sourceMappingURL=histogramQuery.jsx.map