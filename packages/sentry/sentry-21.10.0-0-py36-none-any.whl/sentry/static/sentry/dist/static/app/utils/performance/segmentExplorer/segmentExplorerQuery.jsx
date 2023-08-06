Object.defineProperty(exports, "__esModule", { value: true });
exports.getRequestFunction = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const genericDiscoverQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/genericDiscoverQuery"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
function getRequestFunction(_props) {
    const { aggregateColumn } = _props;
    function getTagExplorerRequestPayload(props) {
        const { eventView } = props;
        const apiPayload = eventView.getEventsAPIPayload(props.location);
        apiPayload.aggregateColumn = aggregateColumn;
        apiPayload.sort = _props.sort ? _props.sort : apiPayload.sort;
        if (_props.allTagKeys) {
            apiPayload.allTagKeys = _props.allTagKeys;
        }
        if (_props.tagKey) {
            apiPayload.tagKey = _props.tagKey;
        }
        return apiPayload;
    }
    return getTagExplorerRequestPayload;
}
exports.getRequestFunction = getRequestFunction;
function shouldRefetchData(prevProps, nextProps) {
    return (prevProps.aggregateColumn !== nextProps.aggregateColumn ||
        prevProps.sort !== nextProps.sort ||
        prevProps.allTagKeys !== nextProps.allTagKeys ||
        prevProps.tagKey !== nextProps.tagKey);
}
function SegmentExplorerQuery(props) {
    return (<genericDiscoverQuery_1.default route="events-facets-performance" getRequestPayload={getRequestFunction(props)} shouldRefetchData={shouldRefetchData} {...props}/>);
}
exports.default = (0, withApi_1.default)(SegmentExplorerQuery);
//# sourceMappingURL=segmentExplorerQuery.jsx.map