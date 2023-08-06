Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const breadcrumbs_1 = (0, tslib_1.__importDefault)(require("app/components/breadcrumbs"));
const dropdownControl_1 = (0, tslib_1.__importStar)(require("app/components/dropdownControl"));
const searchBar_1 = (0, tslib_1.__importDefault)(require("app/components/events/searchBar"));
const Layout = (0, tslib_1.__importStar)(require("app/components/layouts/thirds"));
const globalSelectionHeader_1 = (0, tslib_1.__importDefault)(require("app/components/organizations/globalSelectionHeader"));
const constants_1 = require("app/constants");
const iconFlag_1 = require("app/icons/iconFlag");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const fields_1 = require("app/utils/discover/fields");
const queryString_1 = require("app/utils/queryString");
const tokenizeSearch_1 = require("app/utils/tokenizeSearch");
const withGlobalSelection_1 = (0, tslib_1.__importDefault)(require("app/utils/withGlobalSelection"));
const utils_1 = require("../utils");
const changedTransactions_1 = (0, tslib_1.__importDefault)(require("./changedTransactions"));
const types_1 = require("./types");
const utils_2 = require("./utils");
class TrendsContent extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {};
        this.handleSearch = (searchQuery) => {
            const { location } = this.props;
            const cursors = (0, utils_2.resetCursors)();
            react_router_1.browserHistory.push({
                pathname: location.pathname,
                query: Object.assign(Object.assign(Object.assign({}, location.query), cursors), { query: String(searchQuery).trim() || undefined }),
            });
        };
        this.setError = (error) => {
            this.setState({ error });
        };
        this.handleTrendFunctionChange = (field) => {
            const { organization, location } = this.props;
            const offsets = {};
            Object.values(types_1.TrendChangeType).forEach(trendChangeType => {
                const queryKey = (0, utils_2.getSelectedQueryKey)(trendChangeType);
                offsets[queryKey] = undefined;
            });
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'performance_views.trends.change_function',
                eventName: 'Performance Views: Change Function',
                organization_id: parseInt(organization.id, 10),
                function_name: field,
            });
            this.setState({
                previousTrendFunction: (0, utils_2.getCurrentTrendFunction)(location).field,
            });
            const cursors = (0, utils_2.resetCursors)();
            react_router_1.browserHistory.push({
                pathname: location.pathname,
                query: Object.assign(Object.assign(Object.assign(Object.assign({}, location.query), offsets), cursors), { trendFunction: field }),
            });
        };
        this.handleParameterChange = (label) => {
            const { organization, location } = this.props;
            const cursors = (0, utils_2.resetCursors)();
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'performance_views.trends.change_parameter',
                eventName: 'Performance Views: Change Parameter',
                organization_id: parseInt(organization.id, 10),
                parameter_name: label,
            });
            react_router_1.browserHistory.push({
                pathname: location.pathname,
                query: Object.assign(Object.assign(Object.assign({}, location.query), cursors), { trendParameter: label }),
            });
        };
    }
    renderError() {
        const { error } = this.state;
        if (!error) {
            return null;
        }
        return (<alert_1.default type="error" icon={<iconFlag_1.IconFlag size="md"/>}>
        {error}
      </alert_1.default>);
    }
    getPerformanceLink() {
        const { location } = this.props;
        const newQuery = Object.assign({}, location.query);
        const query = (0, queryString_1.decodeScalar)(location.query.query, '');
        const conditions = new tokenizeSearch_1.MutableSearch(query);
        // This stops errors from occurring when navigating to other views since we are appending aggregates to the trends view
        conditions.removeFilter('tpm()');
        conditions.removeFilter('confidence()');
        conditions.removeFilter('transaction.duration');
        newQuery.query = conditions.formatString();
        return {
            pathname: (0, utils_1.getPerformanceLandingUrl)(this.props.organization),
            query: newQuery,
        };
    }
    render() {
        const { organization, eventView, location } = this.props;
        const { previousTrendFunction } = this.state;
        const trendView = eventView.clone();
        (0, utils_2.modifyTrendsViewDefaultPeriod)(trendView, location);
        const fields = (0, fields_1.generateAggregateFields)(organization, [
            {
                field: 'absolute_correlation()',
            },
            {
                field: 'trend_percentage()',
            },
            {
                field: 'trend_difference()',
            },
            {
                field: 'count_percentage()',
            },
            {
                field: 'tpm()',
            },
            {
                field: 'tps()',
            },
        ], ['epm()', 'eps()']);
        const currentTrendFunction = (0, utils_2.getCurrentTrendFunction)(location);
        const currentTrendParameter = (0, utils_2.getCurrentTrendParameter)(location);
        const query = (0, utils_1.getTransactionSearchQuery)(location);
        return (<globalSelectionHeader_1.default defaultSelection={{
                datetime: {
                    start: null,
                    end: null,
                    utc: false,
                    period: utils_2.DEFAULT_TRENDS_STATS_PERIOD,
                },
            }}>
        <Layout.Header>
          <Layout.HeaderContent>
            <breadcrumbs_1.default crumbs={[
                {
                    label: 'Performance',
                    to: this.getPerformanceLink(),
                },
                {
                    label: 'Trends',
                },
            ]}/>
            <Layout.Title>{(0, locale_1.t)('Trends')}</Layout.Title>
          </Layout.HeaderContent>
        </Layout.Header>
        <Layout.Body>
          <Layout.Main fullWidth>
            <DefaultTrends location={location} eventView={eventView}>
              <StyledSearchContainer>
                <StyledSearchBar searchSource="trends" organization={organization} projectIds={trendView.project} query={query} fields={fields} onSearch={this.handleSearch} maxQueryLength={constants_1.MAX_QUERY_LENGTH}/>
                <TrendsDropdown>
                  <dropdownControl_1.default buttonProps={{ prefix: (0, locale_1.t)('Percentile') }} label={currentTrendFunction.label}>
                    {utils_2.TRENDS_FUNCTIONS.map(({ label, field }) => (<dropdownControl_1.DropdownItem key={field} onSelect={this.handleTrendFunctionChange} eventKey={field} data-test-id={field} isActive={field === currentTrendFunction.field}>
                        {label}
                      </dropdownControl_1.DropdownItem>))}
                  </dropdownControl_1.default>
                </TrendsDropdown>
                <TrendsDropdown>
                  <dropdownControl_1.default buttonProps={{ prefix: (0, locale_1.t)('Parameter') }} label={currentTrendParameter.label}>
                    {utils_2.TRENDS_PARAMETERS.map(({ label }) => (<dropdownControl_1.DropdownItem key={label} onSelect={this.handleParameterChange} eventKey={label} data-test-id={label} isActive={label === currentTrendParameter.label}>
                        {label}
                      </dropdownControl_1.DropdownItem>))}
                  </dropdownControl_1.default>
                </TrendsDropdown>
              </StyledSearchContainer>
              <TrendsLayoutContainer>
                <changedTransactions_1.default trendChangeType={types_1.TrendChangeType.IMPROVED} previousTrendFunction={previousTrendFunction} trendView={trendView} location={location} setError={this.setError}/>
                <changedTransactions_1.default trendChangeType={types_1.TrendChangeType.REGRESSION} previousTrendFunction={previousTrendFunction} trendView={trendView} location={location} setError={this.setError}/>
              </TrendsLayoutContainer>
            </DefaultTrends>
          </Layout.Main>
        </Layout.Body>
      </globalSelectionHeader_1.default>);
    }
}
class DefaultTrends extends React.Component {
    constructor() {
        super(...arguments);
        this.hasPushedDefaults = false;
    }
    render() {
        const { children, location, eventView } = this.props;
        const queryString = (0, queryString_1.decodeScalar)(location.query.query);
        const trendParameter = (0, utils_2.getCurrentTrendParameter)(location);
        const conditions = new tokenizeSearch_1.MutableSearch(queryString || '');
        if (queryString || this.hasPushedDefaults) {
            this.hasPushedDefaults = true;
            return <React.Fragment>{children}</React.Fragment>;
        }
        else {
            this.hasPushedDefaults = true;
            conditions.setFilterValues('tpm()', ['>0.01']);
            conditions.setFilterValues(trendParameter.column, [
                '>0',
                `<${utils_2.DEFAULT_MAX_DURATION}`,
            ]);
        }
        const query = conditions.formatString();
        eventView.query = query;
        react_router_1.browserHistory.push({
            pathname: location.pathname,
            query: Object.assign(Object.assign({}, location.query), { cursor: undefined, query: String(query).trim() || undefined }),
        });
        return null;
    }
}
const StyledSearchBar = (0, styled_1.default)(searchBar_1.default) `
  flex-grow: 1;
  margin-bottom: ${(0, space_1.default)(2)};
`;
const TrendsDropdown = (0, styled_1.default)('div') `
  margin-left: ${(0, space_1.default)(1)};
  flex-grow: 0;
`;
const StyledSearchContainer = (0, styled_1.default)('div') `
  display: flex;
`;
const TrendsLayoutContainer = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(2)};

  @media (min-width: ${p => p.theme.breakpoints[1]}) {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    align-items: stretch;
  }
`;
exports.default = (0, withGlobalSelection_1.default)(TrendsContent);
//# sourceMappingURL=content.jsx.map