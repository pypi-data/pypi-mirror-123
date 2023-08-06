Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const omit_1 = (0, tslib_1.__importDefault)(require("lodash/omit"));
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const transactionsList_1 = (0, tslib_1.__importDefault)(require("app/components/discover/transactionsList"));
const searchBar_1 = (0, tslib_1.__importDefault)(require("app/components/events/searchBar"));
const globalSdkUpdateAlert_1 = (0, tslib_1.__importDefault)(require("app/components/globalSdkUpdateAlert"));
const Layout = (0, tslib_1.__importStar)(require("app/components/layouts/thirds"));
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const constants_1 = require("app/constants");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const analytics_1 = require("app/utils/analytics");
const fields_1 = require("app/utils/discover/fields");
const queryString_1 = require("app/utils/queryString");
const tokenizeSearch_1 = require("app/utils/tokenizeSearch");
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
const cellAction_1 = require("app/views/eventsV2/table/cellAction");
const tags_1 = (0, tslib_1.__importDefault)(require("app/views/eventsV2/tags"));
const constants_2 = require("app/views/performance/transactionSummary/transactionVitals/constants");
const utils_2 = require("../../utils");
const filter_1 = (0, tslib_1.__importStar)(require("../filter"));
const utils_3 = require("../utils");
const charts_1 = (0, tslib_1.__importDefault)(require("./charts"));
const relatedIssues_1 = (0, tslib_1.__importDefault)(require("./relatedIssues"));
const sidebarCharts_1 = (0, tslib_1.__importDefault)(require("./sidebarCharts"));
const statusBreakdown_1 = (0, tslib_1.__importDefault)(require("./statusBreakdown"));
const tagExplorer_1 = require("./tagExplorer");
const userStats_1 = (0, tslib_1.__importDefault)(require("./userStats"));
class SummaryContent extends React.Component {
    constructor() {
        super(...arguments);
        this.handleSearch = (query) => {
            const { location } = this.props;
            const queryParams = (0, getParams_1.getParams)(Object.assign(Object.assign({}, (location.query || {})), { query }));
            // do not propagate pagination when making a new search
            const searchQueryParams = (0, omit_1.default)(queryParams, 'cursor');
            react_router_1.browserHistory.push({
                pathname: location.pathname,
                query: searchQueryParams,
            });
        };
        this.generateTagUrl = (key, value) => {
            const { location } = this.props;
            const query = (0, utils_1.generateQueryWithTag)(location.query, { key, value });
            return Object.assign(Object.assign({}, location), { query });
        };
        this.handleCellAction = (column) => {
            return (action, value) => {
                const { eventView, location } = this.props;
                const searchConditions = new tokenizeSearch_1.MutableSearch(eventView.query);
                // remove any event.type queries since it is implied to apply to only transactions
                searchConditions.removeFilter('event.type');
                // no need to include transaction as its already in the query params
                searchConditions.removeFilter('transaction');
                (0, cellAction_1.updateQuery)(searchConditions, action, column, value);
                react_router_1.browserHistory.push({
                    pathname: location.pathname,
                    query: Object.assign(Object.assign({}, location.query), { cursor: undefined, query: searchConditions.formatString() }),
                });
            };
        };
        this.handleTransactionsListSortChange = (value) => {
            const { location } = this.props;
            const target = {
                pathname: location.pathname,
                query: Object.assign(Object.assign({}, location.query), { showTransactions: value, transactionCursor: undefined }),
            };
            react_router_1.browserHistory.push(target);
        };
        this.handleAllEventsViewClick = () => {
            const { organization } = this.props;
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'performance_views.summary.view_in_transaction_events',
                eventName: 'Performance Views: View in All Events from Transaction Summary',
                organization_id: parseInt(organization.id, 10),
            });
        };
        this.handleDiscoverViewClick = () => {
            const { organization } = this.props;
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'performance_views.summary.view_in_discover',
                eventName: 'Performance Views: View in Discover from Transaction Summary',
                organization_id: parseInt(organization.id, 10),
            });
        };
        this.handleViewDetailsClick = (_e) => {
            const { organization } = this.props;
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'performance_views.summary.view_details',
                eventName: 'Performance Views: View Details from Transaction Summary',
                organization_id: parseInt(organization.id, 10),
            });
        };
    }
    generateEventView(transactionsListEventView, transactionsListTitles) {
        var _a;
        const { location, totalValues, spanOperationBreakdownFilter } = this.props;
        const { selected } = getTransactionsListSort(location, {
            p95: (_a = totalValues === null || totalValues === void 0 ? void 0 : totalValues.p95) !== null && _a !== void 0 ? _a : 0,
            spanOperationBreakdownFilter,
        });
        const sortedEventView = transactionsListEventView.withSorts([selected.sort]);
        if (spanOperationBreakdownFilter === filter_1.SpanOperationBreakdownFilter.None) {
            const fields = [
                // Remove the extra field columns
                ...sortedEventView.fields.slice(0, transactionsListTitles.length),
            ];
            // omit "Operation Duration" column
            sortedEventView.fields = fields.filter(({ field }) => {
                return !(0, fields_1.isRelativeSpanOperationBreakdownField)(field);
            });
        }
        return sortedEventView;
    }
    render() {
        var _a;
        let { eventView } = this.props;
        const { transactionName, location, organization, projects, isLoading, error, totalValues, onChangeFilter, spanOperationBreakdownFilter, } = this.props;
        const hasPerformanceEventsPage = organization.features.includes('performance-events-page');
        const hasPerformanceChartInterpolation = organization.features.includes('performance-chart-interpolation');
        const query = (0, queryString_1.decodeScalar)(location.query.query, '');
        const totalCount = totalValues === null ? null : totalValues.count;
        // NOTE: This is not a robust check for whether or not a transaction is a front end
        // transaction, however it will suffice for now.
        const hasWebVitals = (0, utils_2.isSummaryViewFrontendPageLoad)(eventView, projects) ||
            (totalValues !== null &&
                constants_2.VITAL_GROUPS.some(group => group.vitals.some(vital => {
                    const alias = (0, fields_1.getAggregateAlias)(`percentile(${vital}, ${constants_2.PERCENTILE})`);
                    return Number.isFinite(totalValues[alias]);
                })));
        const isFrontendView = (0, utils_2.isSummaryViewFrontend)(eventView, projects);
        const transactionsListTitles = [
            (0, locale_1.t)('event id'),
            (0, locale_1.t)('user'),
            (0, locale_1.t)('total duration'),
            (0, locale_1.t)('trace id'),
            (0, locale_1.t)('timestamp'),
        ];
        let transactionsListEventView = eventView.clone();
        if (organization.features.includes('performance-ops-breakdown')) {
            // update search conditions
            const spanOperationBreakdownConditions = (0, filter_1.filterToSearchConditions)(spanOperationBreakdownFilter, location);
            if (spanOperationBreakdownConditions) {
                eventView = eventView.clone();
                eventView.query = `${eventView.query} ${spanOperationBreakdownConditions}`.trim();
                transactionsListEventView = eventView.clone();
            }
            // update header titles of transactions list
            const operationDurationTableTitle = spanOperationBreakdownFilter === filter_1.SpanOperationBreakdownFilter.None
                ? (0, locale_1.t)('operation duration')
                : `${spanOperationBreakdownFilter} duration`;
            // add ops breakdown duration column as the 3rd column
            transactionsListTitles.splice(2, 0, operationDurationTableTitle);
            // span_ops_breakdown.relative is a preserved name and a marker for the associated
            // field renderer to be used to generate the relative ops breakdown
            let durationField = fields_1.SPAN_OP_RELATIVE_BREAKDOWN_FIELD;
            if (spanOperationBreakdownFilter !== filter_1.SpanOperationBreakdownFilter.None) {
                durationField = (0, filter_1.filterToField)(spanOperationBreakdownFilter);
            }
            const fields = [...transactionsListEventView.fields];
            // add ops breakdown duration column as the 3rd column
            fields.splice(2, 0, { field: durationField });
            if (spanOperationBreakdownFilter === filter_1.SpanOperationBreakdownFilter.None) {
                fields.push(...fields_1.SPAN_OP_BREAKDOWN_FIELDS.map(field => {
                    return { field };
                }));
            }
            transactionsListEventView.fields = fields;
        }
        const openAllEventsProps = {
            generatePerformanceTransactionEventsView: () => {
                const performanceTransactionEventsView = this.generateEventView(transactionsListEventView, transactionsListTitles);
                performanceTransactionEventsView.query = query;
                return performanceTransactionEventsView;
            },
            handleOpenAllEventsClick: this.handleAllEventsViewClick,
        };
        const openInDiscoverProps = {
            generateDiscoverEventView: () => this.generateEventView(transactionsListEventView, transactionsListTitles),
            handleOpenInDiscoverClick: this.handleDiscoverViewClick,
        };
        return (<React.Fragment>
        <Layout.Main>
          <Search>
            <filter_1.default organization={organization} currentFilter={spanOperationBreakdownFilter} onChangeFilter={onChangeFilter}/>
            <StyledSearchBar searchSource="transaction_summary" organization={organization} projectIds={eventView.project} query={query} fields={eventView.fields} onSearch={this.handleSearch} maxQueryLength={constants_1.MAX_QUERY_LENGTH}/>
          </Search>
          <charts_1.default organization={organization} location={location} eventView={eventView} totalValues={totalCount} currentFilter={spanOperationBreakdownFilter} withoutZerofill={hasPerformanceChartInterpolation}/>
          <transactionsList_1.default location={location} organization={organization} eventView={transactionsListEventView} {...(hasPerformanceEventsPage ? openAllEventsProps : openInDiscoverProps)} showTransactions={(0, queryString_1.decodeScalar)(location.query.showTransactions, utils_3.TransactionFilterOptions.SLOW)} breakdown={(0, filter_1.decodeFilterFromLocation)(location)} titles={transactionsListTitles} handleDropdownChange={this.handleTransactionsListSortChange} generateLink={{
                id: (0, utils_3.generateTransactionLink)(transactionName),
                trace: (0, utils_3.generateTraceLink)(eventView.normalizeDateSelection(location)),
            }} baseline={transactionName} handleBaselineClick={this.handleViewDetailsClick} handleCellAction={this.handleCellAction} {...getTransactionsListSort(location, {
            p95: (_a = totalValues === null || totalValues === void 0 ? void 0 : totalValues.p95) !== null && _a !== void 0 ? _a : 0,
            spanOperationBreakdownFilter,
        })} forceLoading={isLoading}/>
          <feature_1.default requireAll={false} features={['performance-tag-explorer', 'performance-tag-page']}>
            <tagExplorer_1.TagExplorer eventView={eventView} organization={organization} location={location} projects={projects} transactionName={transactionName} currentFilter={spanOperationBreakdownFilter}/>
          </feature_1.default>
          <relatedIssues_1.default organization={organization} location={location} transaction={transactionName} start={eventView.start} end={eventView.end} statsPeriod={eventView.statsPeriod}/>
        </Layout.Main>
        <Layout.Side>
          <userStats_1.default organization={organization} location={location} isLoading={isLoading} hasWebVitals={hasWebVitals} error={error} totals={totalValues} transactionName={transactionName}/>
          {!isFrontendView && (<statusBreakdown_1.default eventView={eventView} organization={organization} location={location}/>)}
          <utils_3.SidebarSpacer />
          <sidebarCharts_1.default organization={organization} isLoading={isLoading} error={error} totals={totalValues} eventView={eventView}/>
          <utils_3.SidebarSpacer />
          <tags_1.default generateUrl={this.generateTagUrl} totalValues={totalCount} eventView={eventView} organization={organization} location={location}/>
        </Layout.Side>
      </React.Fragment>);
    }
}
function getFilterOptions({ p95, spanOperationBreakdownFilter, }) {
    if (spanOperationBreakdownFilter === filter_1.SpanOperationBreakdownFilter.None) {
        return [
            {
                sort: { kind: 'asc', field: 'transaction.duration' },
                value: utils_3.TransactionFilterOptions.FASTEST,
                label: (0, locale_1.t)('Fastest Transactions'),
            },
            {
                query: [['transaction.duration', `<=${p95.toFixed(0)}`]],
                sort: { kind: 'desc', field: 'transaction.duration' },
                value: utils_3.TransactionFilterOptions.SLOW,
                label: (0, locale_1.t)('Slow Transactions (p95)'),
            },
            {
                sort: { kind: 'desc', field: 'transaction.duration' },
                value: utils_3.TransactionFilterOptions.OUTLIER,
                label: (0, locale_1.t)('Outlier Transactions (p100)'),
            },
            {
                sort: { kind: 'desc', field: 'timestamp' },
                value: utils_3.TransactionFilterOptions.RECENT,
                label: (0, locale_1.t)('Recent Transactions'),
            },
        ];
    }
    const field = (0, filter_1.filterToField)(spanOperationBreakdownFilter);
    const operationName = spanOperationBreakdownFilter;
    return [
        {
            sort: { kind: 'asc', field },
            value: utils_3.TransactionFilterOptions.FASTEST,
            label: (0, locale_1.t)('Fastest %s Operations', operationName),
        },
        {
            query: [['transaction.duration', `<=${p95.toFixed(0)}`]],
            sort: { kind: 'desc', field },
            value: utils_3.TransactionFilterOptions.SLOW,
            label: (0, locale_1.t)('Slow %s Operations (p95)', operationName),
        },
        {
            sort: { kind: 'desc', field },
            value: utils_3.TransactionFilterOptions.OUTLIER,
            label: (0, locale_1.t)('Outlier %s Operations (p100)', operationName),
        },
        {
            sort: { kind: 'desc', field: 'timestamp' },
            value: utils_3.TransactionFilterOptions.RECENT,
            label: (0, locale_1.t)('Recent Transactions'),
        },
    ];
}
function getTransactionsListSort(location, options) {
    const sortOptions = getFilterOptions(options);
    const urlParam = (0, queryString_1.decodeScalar)(location.query.showTransactions, utils_3.TransactionFilterOptions.SLOW);
    const selectedSort = sortOptions.find(opt => opt.value === urlParam) || sortOptions[0];
    return { selected: selectedSort, options: sortOptions };
}
const Search = (0, styled_1.default)('div') `
  display: flex;
  width: 100%;
  margin-bottom: ${(0, space_1.default)(3)};
`;
const StyledSearchBar = (0, styled_1.default)(searchBar_1.default) `
  flex-grow: 1;
`;
const StyledSdkUpdatesAlert = (0, styled_1.default)(globalSdkUpdateAlert_1.default) `
  @media (min-width: ${p => p.theme.breakpoints[1]}) {
    margin-bottom: 0;
  }
`;
StyledSdkUpdatesAlert.defaultProps = {
    Wrapper: p => <Layout.Main fullWidth {...p}/>,
};
exports.default = (0, withProjects_1.default)(SummaryContent);
//# sourceMappingURL=content.jsx.map