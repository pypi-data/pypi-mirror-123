Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const genericDiscoverQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/genericDiscoverQuery"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
function shouldRefetchData(prevProps, nextProps) {
    return prevProps.query !== nextProps.query;
}
function TagTransactionsQuery(props) {
    return (<genericDiscoverQuery_1.default route="eventsv2" shouldRefetchData={shouldRefetchData} {...props}/>);
}
exports.default = (0, withApi_1.default)(TagTransactionsQuery);
//# sourceMappingURL=tagTransactionsQuery.jsx.map