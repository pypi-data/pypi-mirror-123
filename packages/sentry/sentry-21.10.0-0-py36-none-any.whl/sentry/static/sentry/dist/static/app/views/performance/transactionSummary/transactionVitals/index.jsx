Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const locale_1 = require("app/locale");
const eventView_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/eventView"));
const fields_1 = require("app/utils/discover/fields");
const constants_1 = require("app/utils/performance/vitals/constants");
const queryString_1 = require("app/utils/queryString");
const tokenizeSearch_1 = require("app/utils/tokenizeSearch");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
const pageLayout_1 = (0, tslib_1.__importDefault)(require("../pageLayout"));
const tabs_1 = (0, tslib_1.__importDefault)(require("../tabs"));
const constants_2 = require("./constants");
const content_1 = (0, tslib_1.__importDefault)(require("./content"));
function TransactionVitals(props) {
    const { location, organization, projects } = props;
    return (<pageLayout_1.default location={location} organization={organization} projects={projects} tab={tabs_1.default.WebVitals} getDocumentTitle={getDocumentTitle} generateEventView={generateEventView} childComponent={content_1.default}/>);
}
function getDocumentTitle(transactionName) {
    const hasTransactionName = typeof transactionName === 'string' && String(transactionName).trim().length > 0;
    if (hasTransactionName) {
        return [String(transactionName).trim(), (0, locale_1.t)('Vitals')].join(' \u2014 ');
    }
    return [(0, locale_1.t)('Summary'), (0, locale_1.t)('Vitals')].join(' \u2014 ');
}
function generateEventView(location, transactionName) {
    const query = (0, queryString_1.decodeScalar)(location.query.query, '');
    const conditions = new tokenizeSearch_1.MutableSearch(query);
    conditions
        .setFilterValues('event.type', ['transaction'])
        .setFilterValues('transaction.op', ['pageload'])
        .setFilterValues('transaction', [transactionName]);
    Object.keys(conditions.filters).forEach(field => {
        if ((0, fields_1.isAggregateField)(field))
            conditions.removeFilter(field);
    });
    const vitals = constants_2.VITAL_GROUPS.reduce((allVitals, group) => {
        return allVitals.concat(group.vitals);
    }, []);
    return eventView_1.default.fromNewQueryWithLocation({
        id: undefined,
        version: 2,
        name: transactionName,
        fields: [
            ...vitals.map(vital => `percentile(${vital}, ${constants_2.PERCENTILE})`),
            ...vitals.map(vital => `count_at_least(${vital}, 0)`),
            ...vitals.map(vital => `count_at_least(${vital}, ${constants_1.WEB_VITAL_DETAILS[vital].poorThreshold})`),
        ],
        query: conditions.formatString(),
        projects: [],
    }, location);
}
exports.default = (0, withProjects_1.default)((0, withOrganization_1.default)(TransactionVitals));
//# sourceMappingURL=index.jsx.map