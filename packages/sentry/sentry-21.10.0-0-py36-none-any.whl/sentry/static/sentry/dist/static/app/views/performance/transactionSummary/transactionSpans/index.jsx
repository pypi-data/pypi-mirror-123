Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const locale_1 = require("app/locale");
const eventView_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/eventView"));
const queryString_1 = require("app/utils/queryString");
const tokenizeSearch_1 = require("app/utils/tokenizeSearch");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
const pageLayout_1 = (0, tslib_1.__importDefault)(require("../pageLayout"));
const tabs_1 = (0, tslib_1.__importDefault)(require("../tabs"));
const content_1 = (0, tslib_1.__importDefault)(require("./content"));
function TransactionSpans(props) {
    const { location, organization, projects } = props;
    return (<pageLayout_1.default location={location} organization={organization} projects={projects} tab={tabs_1.default.Spans} getDocumentTitle={getDocumentTitle} generateEventView={generateEventView} childComponent={content_1.default}/>);
}
function generateEventView(location, transactionName) {
    const query = (0, queryString_1.decodeScalar)(location.query.query, '');
    const conditions = new tokenizeSearch_1.MutableSearch(query);
    // TODO: what should this event type be?
    conditions
        .setFilterValues('event.type', ['transaction'])
        .setFilterValues('transaction', [transactionName]);
    return eventView_1.default.fromNewQueryWithLocation({
        id: undefined,
        version: 2,
        name: transactionName,
        fields: ['count()'],
        query: conditions.formatString(),
        projects: [],
    }, location);
}
function getDocumentTitle(transactionName) {
    const hasTransactionName = typeof transactionName === 'string' && String(transactionName).trim().length > 0;
    if (hasTransactionName) {
        return [String(transactionName).trim(), (0, locale_1.t)('Performance')].join(' - ');
    }
    return [(0, locale_1.t)('Summary'), (0, locale_1.t)('Performance')].join(' - ');
}
exports.default = (0, withProjects_1.default)((0, withOrganization_1.default)(TransactionSpans));
//# sourceMappingURL=index.jsx.map