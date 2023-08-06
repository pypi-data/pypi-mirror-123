Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const guideAnchor_1 = (0, tslib_1.__importDefault)(require("app/components/assistant/guideAnchor"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const discoverButton_1 = (0, tslib_1.__importDefault)(require("app/components/discoverButton"));
const dropdownButton_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownButton"));
const dropdownControl_1 = (0, tslib_1.__importStar)(require("app/components/dropdownControl"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const discoverQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/discoverQuery"));
const baselineQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/performance/baseline/baselineQuery"));
const trendsDiscoverQuery_1 = require("app/utils/performance/trends/trendsDiscoverQuery");
const queryString_1 = require("app/utils/queryString");
const tokenizeSearch_1 = require("app/utils/tokenizeSearch");
const utils_1 = require("app/views/eventsV2/utils");
const utils_2 = require("app/views/performance/transactionSummary/transactionEvents/utils");
const transactionsTable_1 = (0, tslib_1.__importDefault)(require("./transactionsTable"));
const DEFAULT_TRANSACTION_LIMIT = 5;
class TransactionsList extends React.Component {
    constructor() {
        super(...arguments);
        this.handleCursor = (cursor, pathname, query) => {
            const { cursorName } = this.props;
            react_router_1.browserHistory.push({
                pathname,
                query: Object.assign(Object.assign({}, query), { [cursorName]: cursor }),
            });
        };
    }
    getEventView() {
        const { eventView, selected } = this.props;
        const sortedEventView = eventView.withSorts([selected.sort]);
        if (selected.query) {
            const query = new tokenizeSearch_1.MutableSearch(sortedEventView.query);
            selected.query.forEach(item => query.setFilterValues(item[0], [item[1]]));
            sortedEventView.query = query.formatString();
        }
        return sortedEventView;
    }
    generateDiscoverEventView() {
        const { generateDiscoverEventView } = this.props;
        if (typeof generateDiscoverEventView === 'function') {
            return generateDiscoverEventView();
        }
        return this.getEventView();
    }
    generatePerformanceTransactionEventsView() {
        var _a;
        const { generatePerformanceTransactionEventsView } = this.props;
        return (_a = generatePerformanceTransactionEventsView === null || generatePerformanceTransactionEventsView === void 0 ? void 0 : generatePerformanceTransactionEventsView()) !== null && _a !== void 0 ? _a : this.getEventView();
    }
    renderHeader() {
        const { organization, selected, options, handleDropdownChange, handleOpenAllEventsClick, handleOpenInDiscoverClick, showTransactions, breakdown, } = this.props;
        return (<React.Fragment>
        <div>
          <dropdownControl_1.default data-test-id="filter-transactions" button={({ isOpen, getActorProps }) => (<StyledDropdownButton {...getActorProps()} isOpen={isOpen} prefix={(0, locale_1.t)('Filter')} size="small">
                {selected.label}
              </StyledDropdownButton>)}>
            {options.map(({ value, label }) => (<dropdownControl_1.DropdownItem data-test-id={`option-${value}`} key={value} onSelect={handleDropdownChange} eventKey={value} isActive={value === selected.value}>
                {label}
              </dropdownControl_1.DropdownItem>))}
          </dropdownControl_1.default>
        </div>
        {!this.isTrend() &&
                (handleOpenAllEventsClick ? (<guideAnchor_1.default target="release_transactions_open_in_transaction_events">
              <button_1.default onClick={handleOpenAllEventsClick} to={this.generatePerformanceTransactionEventsView().getPerformanceTransactionEventsViewUrlTarget(organization.slug, {
                        showTransactions: (0, utils_2.mapShowTransactionToPercentile)(showTransactions),
                        breakdown,
                    })} size="small" data-test-id="transaction-events-open">
                {(0, locale_1.t)('View All Events')}
              </button_1.default>
            </guideAnchor_1.default>) : (<guideAnchor_1.default target="release_transactions_open_in_discover">
              <discoverButton_1.default onClick={handleOpenInDiscoverClick} to={this.generateDiscoverEventView().getResultsViewUrlTarget(organization.slug)} size="small" data-test-id="discover-open">
                {(0, locale_1.t)('Open in Discover')}
              </discoverButton_1.default>
            </guideAnchor_1.default>))}
      </React.Fragment>);
    }
    renderTransactionTable() {
        var _a;
        const { location, organization, handleCellAction, cursorName, limit, titles, generateLink, baseline, forceLoading, } = this.props;
        const eventView = this.getEventView();
        const columnOrder = eventView.getColumns();
        const cursor = (0, queryString_1.decodeScalar)((_a = location.query) === null || _a === void 0 ? void 0 : _a[cursorName]);
        const baselineTransactionName = organization.features.includes('transaction-comparison')
            ? baseline !== null && baseline !== void 0 ? baseline : null
            : null;
        let tableRenderer = ({ isLoading, pageLinks, tableData, baselineData }) => (<React.Fragment>
        <Header>
          {this.renderHeader()}
          <StyledPagination pageLinks={pageLinks} onCursor={this.handleCursor} size="small"/>
        </Header>
        <transactionsTable_1.default eventView={eventView} organization={organization} location={location} isLoading={isLoading} tableData={tableData} baselineData={baselineData !== null && baselineData !== void 0 ? baselineData : null} columnOrder={columnOrder} titles={titles} generateLink={generateLink} baselineTransactionName={baselineTransactionName} handleCellAction={handleCellAction}/>
      </React.Fragment>);
        if (forceLoading) {
            return tableRenderer({
                isLoading: true,
                pageLinks: null,
                tableData: null,
                baselineData: null,
            });
        }
        if (baselineTransactionName) {
            const orgTableRenderer = tableRenderer;
            tableRenderer = ({ isLoading, pageLinks, tableData }) => (<baselineQuery_1.default eventView={eventView} orgSlug={organization.slug}>
          {baselineQueryProps => {
                    return orgTableRenderer({
                        isLoading: isLoading || baselineQueryProps.isLoading,
                        pageLinks,
                        tableData,
                        baselineData: baselineQueryProps.results,
                    });
                }}
        </baselineQuery_1.default>);
        }
        return (<discoverQuery_1.default location={location} eventView={eventView} orgSlug={organization.slug} limit={limit} cursor={cursor} referrer="api.discover.transactions-list">
        {tableRenderer}
      </discoverQuery_1.default>);
    }
    renderTrendsTable() {
        var _a;
        const { trendView, location, selected, organization, cursorName, generateLink } = this.props;
        const sortedEventView = trendView.clone();
        sortedEventView.sorts = [selected.sort];
        sortedEventView.trendType = selected.trendType;
        if (selected.query) {
            const query = new tokenizeSearch_1.MutableSearch(sortedEventView.query);
            selected.query.forEach(item => query.setFilterValues(item[0], [item[1]]));
            sortedEventView.query = query.formatString();
        }
        const cursor = (0, queryString_1.decodeScalar)((_a = location.query) === null || _a === void 0 ? void 0 : _a[cursorName]);
        return (<trendsDiscoverQuery_1.TrendsEventsDiscoverQuery eventView={sortedEventView} orgSlug={organization.slug} location={location} cursor={cursor} limit={5}>
        {({ isLoading, trendsData, pageLinks }) => (<React.Fragment>
            <Header>
              {this.renderHeader()}
              <StyledPagination pageLinks={pageLinks} onCursor={this.handleCursor} size="small"/>
            </Header>
            <transactionsTable_1.default eventView={sortedEventView} organization={organization} location={location} isLoading={isLoading} tableData={trendsData} baselineData={null} titles={['transaction', 'percentage', 'difference']} columnOrder={(0, utils_1.decodeColumnOrder)([
                    { field: 'transaction' },
                    { field: 'trend_percentage()' },
                    { field: 'trend_difference()' },
                ])} generateLink={generateLink} baselineTransactionName={null}/>
          </React.Fragment>)}
      </trendsDiscoverQuery_1.TrendsEventsDiscoverQuery>);
    }
    isTrend() {
        const { selected } = this.props;
        return selected.trendType !== undefined;
    }
    render() {
        return (<React.Fragment>
        {this.isTrend() ? this.renderTrendsTable() : this.renderTransactionTable()}
      </React.Fragment>);
    }
}
TransactionsList.defaultProps = {
    cursorName: 'transactionCursor',
    limit: DEFAULT_TRANSACTION_LIMIT,
};
const Header = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: 1fr auto auto;
  margin-bottom: ${(0, space_1.default)(1)};
`;
const StyledDropdownButton = (0, styled_1.default)(dropdownButton_1.default) `
  min-width: 145px;
`;
const StyledPagination = (0, styled_1.default)(pagination_1.default) `
  margin: 0 0 0 ${(0, space_1.default)(1)};
`;
exports.default = TransactionsList;
//# sourceMappingURL=transactionsList.jsx.map