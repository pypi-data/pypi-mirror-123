Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const tags_1 = require("app/actionCreators/tags");
const locale_1 = require("app/locale");
const analytics_1 = require("app/utils/analytics");
const discoverQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/discoverQuery"));
const eventView_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/eventView"));
const fields_1 = require("app/utils/discover/fields");
const histogram_1 = require("app/utils/performance/histogram");
const queryString_1 = require("app/utils/queryString");
const tokenizeSearch_1 = require("app/utils/tokenizeSearch");
const useApi_1 = (0, tslib_1.__importDefault)(require("app/utils/useApi"));
const withGlobalSelection_1 = (0, tslib_1.__importDefault)(require("app/utils/withGlobalSelection"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
const utils_1 = require("../../utils");
const filter_1 = require("../filter");
const pageLayout_1 = (0, tslib_1.__importDefault)(require("../pageLayout"));
const tabs_1 = (0, tslib_1.__importDefault)(require("../tabs"));
const constants_1 = require("../transactionVitals/constants");
const content_1 = (0, tslib_1.__importDefault)(require("./content"));
const latencyChart_1 = require("./latencyChart");
function TransactionOverview(props) {
    const api = (0, useApi_1.default)();
    const { location, selection, organization, projects } = props;
    (0, react_1.useEffect)(() => {
        (0, tags_1.loadOrganizationTags)(api, organization.slug, selection);
        (0, utils_1.addRoutePerformanceContext)(selection);
    }, [selection]);
    return (<pageLayout_1.default location={location} organization={organization} projects={projects} tab={tabs_1.default.TransactionSummary} getDocumentTitle={getDocumentTitle} generateEventView={generateEventView} childComponent={OverviewContentWrapper}/>);
}
function OverviewContentWrapper(props) {
    const { location, organization, eventView, transactionName, transactionThreshold, transactionThresholdMetric, } = props;
    const spanOperationBreakdownFilter = (0, filter_1.decodeFilterFromLocation)(location);
    const totalsView = getTotalsEventView(organization, eventView);
    const onChangeFilter = (newFilter) => {
        (0, analytics_1.trackAnalyticsEvent)({
            eventName: 'Performance Views: Filter Dropdown',
            eventKey: 'performance_views.filter_dropdown.selection',
            organization_id: parseInt(organization.id, 10),
            action: newFilter,
        });
        const nextQuery = Object.assign(Object.assign({}, (0, histogram_1.removeHistogramQueryStrings)(location, [latencyChart_1.ZOOM_START, latencyChart_1.ZOOM_END])), (0, filter_1.filterToLocationQuery)(newFilter));
        if (newFilter === filter_1.SpanOperationBreakdownFilter.None) {
            delete nextQuery.breakdown;
        }
        react_router_1.browserHistory.push({
            pathname: location.pathname,
            query: nextQuery,
        });
    };
    return (<discoverQuery_1.default eventView={totalsView} orgSlug={organization.slug} location={location} transactionThreshold={transactionThreshold} transactionThresholdMetric={transactionThresholdMetric} referrer="api.performance.transaction-summary">
      {({ isLoading, error, tableData }) => {
            var _a, _b;
            const totals = (_b = (_a = tableData === null || tableData === void 0 ? void 0 : tableData.data) === null || _a === void 0 ? void 0 : _a[0]) !== null && _b !== void 0 ? _b : null;
            return (<content_1.default location={location} organization={organization} eventView={eventView} transactionName={transactionName} isLoading={isLoading} error={error} totalValues={totals} onChangeFilter={onChangeFilter} spanOperationBreakdownFilter={spanOperationBreakdownFilter}/>);
        }}
    </discoverQuery_1.default>);
}
function getDocumentTitle(transactionName) {
    const hasTransactionName = typeof transactionName === 'string' && String(transactionName).trim().length > 0;
    if (hasTransactionName) {
        return [String(transactionName).trim(), (0, locale_1.t)('Performance')].join(' - ');
    }
    return [(0, locale_1.t)('Summary'), (0, locale_1.t)('Performance')].join(' - ');
}
function generateEventView(location, transactionName) {
    // Use the user supplied query but overwrite any transaction or event type
    // conditions they applied.
    const query = (0, queryString_1.decodeScalar)(location.query.query, '');
    const conditions = new tokenizeSearch_1.MutableSearch(query);
    conditions
        .setFilterValues('event.type', ['transaction'])
        .setFilterValues('transaction', [transactionName]);
    Object.keys(conditions.filters).forEach(field => {
        if ((0, fields_1.isAggregateField)(field))
            conditions.removeFilter(field);
    });
    const fields = ['id', 'user.display', 'transaction.duration', 'trace', 'timestamp'];
    return eventView_1.default.fromNewQueryWithLocation({
        id: undefined,
        version: 2,
        name: transactionName,
        fields,
        query: conditions.formatString(),
        projects: [],
    }, location);
}
function getTotalsEventView(_organization, eventView) {
    const vitals = constants_1.VITAL_GROUPS.map(({ vitals: vs }) => vs).reduce((keys, vs) => {
        vs.forEach(vital => keys.push(vital));
        return keys;
    }, []);
    const totalsColumns = [
        {
            kind: 'function',
            function: ['p95', '', undefined, undefined],
        },
        {
            kind: 'function',
            function: ['count', '', undefined, undefined],
        },
        {
            kind: 'function',
            function: ['count_unique', 'user', undefined, undefined],
        },
        {
            kind: 'function',
            function: ['failure_rate', '', undefined, undefined],
        },
        {
            kind: 'function',
            function: ['tpm', '', undefined, undefined],
        },
        {
            kind: 'function',
            function: ['count_miserable', 'user', undefined, undefined],
        },
        {
            kind: 'function',
            function: ['user_misery', '', undefined, undefined],
        },
        {
            kind: 'function',
            function: ['apdex', '', undefined, undefined],
        },
    ];
    return eventView.withColumns([
        ...totalsColumns,
        ...vitals.map(vital => ({
            kind: 'function',
            function: ['percentile', vital, constants_1.PERCENTILE.toString(), undefined],
        })),
    ]);
}
exports.default = (0, withGlobalSelection_1.default)((0, withProjects_1.default)((0, withOrganization_1.default)(TransactionOverview)));
//# sourceMappingURL=index.jsx.map