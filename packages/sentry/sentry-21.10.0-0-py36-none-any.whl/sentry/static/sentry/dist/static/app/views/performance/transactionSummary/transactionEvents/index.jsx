Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_router_1 = require("react-router");
const Layout = (0, tslib_1.__importStar)(require("app/components/layouts/thirds"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const locale_1 = require("app/locale");
const analytics_1 = require("app/utils/analytics");
const discoverQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/discoverQuery"));
const eventView_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/eventView"));
const fields_1 = require("app/utils/discover/fields");
const histogram_1 = require("app/utils/performance/histogram");
const queryString_1 = require("app/utils/queryString");
const tokenizeSearch_1 = require("app/utils/tokenizeSearch");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
const filter_1 = require("../filter");
const pageLayout_1 = (0, tslib_1.__importDefault)(require("../pageLayout"));
const tabs_1 = (0, tslib_1.__importDefault)(require("../tabs"));
const latencyChart_1 = require("../transactionOverview/latencyChart");
const content_1 = (0, tslib_1.__importDefault)(require("./content"));
const utils_1 = require("./utils");
function TransactionEvents(props) {
    const { location, organization, projects } = props;
    return (<pageLayout_1.default location={location} organization={organization} projects={projects} tab={tabs_1.default.Events} getDocumentTitle={getDocumentTitle} generateEventView={generateEventView} childComponent={EventsContentWrapper} features={['performance-events-page']}/>);
}
function EventsContentWrapper(props) {
    const { location, organization, eventView, transactionName, setError } = props;
    const eventsDisplayFilterName = (0, utils_1.decodeEventsDisplayFilterFromLocation)(location);
    const spanOperationBreakdownFilter = (0, filter_1.decodeFilterFromLocation)(location);
    const webVital = getWebVital(location);
    const percentilesView = getPercentilesEventView(eventView);
    const getFilteredEventView = (percentiles) => {
        const filter = (0, utils_1.getEventsFilterOptions)(spanOperationBreakdownFilter, percentiles)[eventsDisplayFilterName];
        const filteredEventView = eventView === null || eventView === void 0 ? void 0 : eventView.clone();
        if (filteredEventView && (filter === null || filter === void 0 ? void 0 : filter.query)) {
            const query = new tokenizeSearch_1.MutableSearch(filteredEventView.query);
            filter.query.forEach(item => query.setFilterValues(item[0], [item[1]]));
            filteredEventView.query = query.formatString();
        }
        return filteredEventView;
    };
    const onChangeSpanOperationBreakdownFilter = (newFilter) => {
        var _a;
        (0, analytics_1.trackAnalyticsEvent)({
            eventName: 'Performance Views: Transaction Events Ops Breakdown Filter Dropdown',
            eventKey: 'performance_views.transactionEvents.ops_filter_dropdown.selection',
            organization_id: parseInt(organization.id, 10),
            action: newFilter,
        });
        // Check to see if the current table sort matches the EventsDisplayFilter.
        // If it does, we can re-sort using the new SpanOperationBreakdownFilter
        const eventsFilterOptionSort = (0, utils_1.getEventsFilterOptions)(spanOperationBreakdownFilter)[eventsDisplayFilterName].sort;
        const currentSort = (_a = eventView === null || eventView === void 0 ? void 0 : eventView.sorts) === null || _a === void 0 ? void 0 : _a[0];
        let sortQuery = {};
        if ((eventsFilterOptionSort === null || eventsFilterOptionSort === void 0 ? void 0 : eventsFilterOptionSort.kind) === (currentSort === null || currentSort === void 0 ? void 0 : currentSort.kind) &&
            (eventsFilterOptionSort === null || eventsFilterOptionSort === void 0 ? void 0 : eventsFilterOptionSort.field) === (currentSort === null || currentSort === void 0 ? void 0 : currentSort.field)) {
            sortQuery = (0, utils_1.filterEventsDisplayToLocationQuery)(eventsDisplayFilterName, newFilter);
        }
        const nextQuery = Object.assign(Object.assign(Object.assign({}, (0, histogram_1.removeHistogramQueryStrings)(location, [latencyChart_1.ZOOM_START, latencyChart_1.ZOOM_END])), (0, filter_1.filterToLocationQuery)(newFilter)), sortQuery);
        if (newFilter === filter_1.SpanOperationBreakdownFilter.None) {
            delete nextQuery.breakdown;
        }
        react_router_1.browserHistory.push({
            pathname: location.pathname,
            query: nextQuery,
        });
    };
    const onChangeEventsDisplayFilter = (newFilterName) => {
        (0, analytics_1.trackAnalyticsEvent)({
            eventName: 'Performance Views: Transaction Events Display Filter Dropdown',
            eventKey: 'performance_views.transactionEvents.display_filter_dropdown.selection',
            organization_id: parseInt(organization.id, 10),
            action: newFilterName,
        });
        const nextQuery = Object.assign(Object.assign({}, (0, histogram_1.removeHistogramQueryStrings)(location, [latencyChart_1.ZOOM_START, latencyChart_1.ZOOM_END])), (0, utils_1.filterEventsDisplayToLocationQuery)(newFilterName, spanOperationBreakdownFilter));
        if (newFilterName === utils_1.EventsDisplayFilterName.p100) {
            delete nextQuery.showTransaction;
        }
        react_router_1.browserHistory.push({
            pathname: location.pathname,
            query: nextQuery,
        });
    };
    return (<discoverQuery_1.default eventView={percentilesView} orgSlug={organization.slug} location={location} referrer="api.performance.transaction-events">
      {({ isLoading, tableData }) => {
            var _a;
            if (isLoading) {
                return (<Layout.Main fullWidth>
              <loadingIndicator_1.default />
            </Layout.Main>);
            }
            const percentiles = (_a = tableData === null || tableData === void 0 ? void 0 : tableData.data) === null || _a === void 0 ? void 0 : _a[0];
            const filteredEventView = getFilteredEventView(percentiles);
            return (<content_1.default location={location} organization={organization} eventView={filteredEventView} transactionName={transactionName} spanOperationBreakdownFilter={spanOperationBreakdownFilter} onChangeSpanOperationBreakdownFilter={onChangeSpanOperationBreakdownFilter} eventsDisplayFilterName={eventsDisplayFilterName} onChangeEventsDisplayFilter={onChangeEventsDisplayFilter} percentileValues={percentiles} webVital={webVital} setError={setError}/>);
        }}
    </discoverQuery_1.default>);
}
function getDocumentTitle(transactionName) {
    const hasTransactionName = typeof transactionName === 'string' && String(transactionName).trim().length > 0;
    if (hasTransactionName) {
        return [String(transactionName).trim(), (0, locale_1.t)('Events')].join(' \u2014 ');
    }
    return [(0, locale_1.t)('Summary'), (0, locale_1.t)('Events')].join(' \u2014 ');
}
function getWebVital(location) {
    const webVital = (0, queryString_1.decodeScalar)(location.query.webVital, '');
    if (Object.values(fields_1.WebVital).includes(webVital)) {
        return webVital;
    }
    return undefined;
}
function generateEventView(location, transactionName) {
    const query = (0, queryString_1.decodeScalar)(location.query.query, '');
    const conditions = new tokenizeSearch_1.MutableSearch(query);
    conditions
        .setFilterValues('event.type', ['transaction'])
        .setFilterValues('transaction', [transactionName]);
    Object.keys(conditions.filters).forEach(field => {
        if ((0, fields_1.isAggregateField)(field))
            conditions.removeFilter(field);
    });
    // Default fields for relative span view
    const fields = [
        'id',
        'user.display',
        fields_1.SPAN_OP_RELATIVE_BREAKDOWN_FIELD,
        'transaction.duration',
        'trace',
        'timestamp',
    ];
    const breakdown = (0, filter_1.decodeFilterFromLocation)(location);
    if (breakdown !== filter_1.SpanOperationBreakdownFilter.None) {
        fields.splice(2, 1, `spans.${breakdown}`);
    }
    else {
        fields.push(...fields_1.SPAN_OP_BREAKDOWN_FIELDS);
    }
    const webVital = getWebVital(location);
    if (webVital) {
        fields.splice(3, 0, webVital);
    }
    return eventView_1.default.fromNewQueryWithLocation({
        id: undefined,
        version: 2,
        name: transactionName,
        fields,
        query: conditions.formatString(),
        projects: [],
        orderby: (0, queryString_1.decodeScalar)(location.query.sort, '-timestamp'),
    }, location);
}
function getPercentilesEventView(eventView) {
    const percentileColumns = [
        {
            kind: 'function',
            function: ['p100', '', undefined, undefined],
        },
        {
            kind: 'function',
            function: ['p99', '', undefined, undefined],
        },
        {
            kind: 'function',
            function: ['p95', '', undefined, undefined],
        },
        {
            kind: 'function',
            function: ['p75', '', undefined, undefined],
        },
        {
            kind: 'function',
            function: ['p50', '', undefined, undefined],
        },
    ];
    return eventView.withColumns(percentileColumns);
}
exports.default = (0, withProjects_1.default)((0, withOrganization_1.default)(TransactionEvents));
//# sourceMappingURL=index.jsx.map