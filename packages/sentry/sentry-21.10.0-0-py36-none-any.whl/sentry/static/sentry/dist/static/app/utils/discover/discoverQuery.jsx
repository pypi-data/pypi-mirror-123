Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const genericDiscoverQuery_1 = (0, tslib_1.__importDefault)(require("./genericDiscoverQuery"));
function shouldRefetchData(prevProps, nextProps) {
    return (prevProps.transactionName !== nextProps.transactionName ||
        prevProps.transactionThreshold !== nextProps.transactionThreshold ||
        prevProps.transactionThresholdMetric !== nextProps.transactionThresholdMetric);
}
function DiscoverQuery(props) {
    return (<genericDiscoverQuery_1.default route="eventsv2" shouldRefetchData={shouldRefetchData} {...props}/>);
}
exports.default = (0, withApi_1.default)(DiscoverQuery);
//# sourceMappingURL=discoverQuery.jsx.map