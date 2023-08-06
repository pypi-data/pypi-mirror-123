Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const omit_1 = (0, tslib_1.__importDefault)(require("lodash/omit"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const dropdownControl_1 = (0, tslib_1.__importStar)(require("app/components/dropdownControl"));
const searchBar_1 = (0, tslib_1.__importDefault)(require("app/components/events/searchBar"));
const globalSdkUpdateAlert_1 = (0, tslib_1.__importDefault)(require("app/components/globalSdkUpdateAlert"));
const Layout = (0, tslib_1.__importStar)(require("app/components/layouts/thirds"));
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const queryString_1 = require("app/utils/queryString");
const filter_1 = (0, tslib_1.__importStar)(require("../filter"));
const eventsTable_1 = (0, tslib_1.__importDefault)(require("./eventsTable"));
const utils_1 = require("./utils");
function EventsContent(props) {
    const { location, organization, eventView: originalEventView, transactionName, spanOperationBreakdownFilter, webVital, setError, } = props;
    const eventView = originalEventView.clone();
    const transactionsListTitles = [
        (0, locale_1.t)('event id'),
        (0, locale_1.t)('user'),
        (0, locale_1.t)('operation duration'),
        (0, locale_1.t)('total duration'),
        (0, locale_1.t)('trace id'),
        (0, locale_1.t)('timestamp'),
    ];
    if (webVital) {
        transactionsListTitles.splice(3, 0, (0, locale_1.t)(webVital));
    }
    const spanOperationBreakdownConditions = (0, filter_1.filterToSearchConditions)(spanOperationBreakdownFilter, location);
    if (spanOperationBreakdownConditions) {
        eventView.query = `${eventView.query} ${spanOperationBreakdownConditions}`.trim();
        transactionsListTitles.splice(2, 1, (0, locale_1.t)(`${spanOperationBreakdownFilter} duration`));
    }
    return (<Layout.Main fullWidth>
      <Search {...props}/>
      <StyledTable>
        <eventsTable_1.default eventView={eventView} organization={organization} location={location} setError={setError} columnTitles={transactionsListTitles} transactionName={transactionName}/>
      </StyledTable>
    </Layout.Main>);
}
function Search(props) {
    const { eventView, location, organization, spanOperationBreakdownFilter, onChangeSpanOperationBreakdownFilter, eventsDisplayFilterName, onChangeEventsDisplayFilter, percentileValues, } = props;
    const handleSearch = (query) => {
        const queryParams = (0, getParams_1.getParams)(Object.assign(Object.assign({}, (location.query || {})), { query }));
        // do not propagate pagination when making a new search
        const searchQueryParams = (0, omit_1.default)(queryParams, 'cursor');
        react_router_1.browserHistory.push({
            pathname: location.pathname,
            query: searchQueryParams,
        });
    };
    const query = (0, queryString_1.decodeScalar)(location.query.query, '');
    const eventsFilterOptions = (0, utils_1.getEventsFilterOptions)(spanOperationBreakdownFilter, percentileValues);
    return (<SearchWrapper>
      <filter_1.default organization={organization} currentFilter={spanOperationBreakdownFilter} onChangeFilter={onChangeSpanOperationBreakdownFilter}/>
      <StyledSearchBar organization={organization} projectIds={eventView.project} query={query} fields={eventView.fields} onSearch={handleSearch}/>
      <SearchRowMenuItem>
        <dropdownControl_1.default buttonProps={{ prefix: (0, locale_1.t)('Percentile') }} label={eventsFilterOptions[eventsDisplayFilterName].label}>
          {Object.entries(eventsFilterOptions).map(([name, filter]) => {
            return (<dropdownControl_1.DropdownItem key={name} onSelect={onChangeEventsDisplayFilter} eventKey={name} data-test-id={name} isActive={eventsDisplayFilterName === name}>
                {filter.label}
              </dropdownControl_1.DropdownItem>);
        })}
        </dropdownControl_1.default>
      </SearchRowMenuItem>
      <SearchRowMenuItem>
        <button_1.default to={eventView.getResultsViewUrlTarget(organization.slug)}>
          {(0, locale_1.t)('Open in Discover')}
        </button_1.default>
      </SearchRowMenuItem>
    </SearchWrapper>);
}
const SearchWrapper = (0, styled_1.default)('div') `
  display: flex;
  width: 100%;
  margin-bottom: ${(0, space_1.default)(3)};
`;
const StyledSearchBar = (0, styled_1.default)(searchBar_1.default) `
  flex-grow: 1;
`;
const StyledTable = (0, styled_1.default)('div') `
  flex-grow: 1;
`;
const StyledSdkUpdatesAlert = (0, styled_1.default)(globalSdkUpdateAlert_1.default) `
  @media (min-width: ${p => p.theme.breakpoints[1]}) {
    margin-bottom: 0;
  }
`;
const SearchRowMenuItem = (0, styled_1.default)('div') `
  margin-left: ${(0, space_1.default)(1)};
  flex-grow: 0;
`;
StyledSdkUpdatesAlert.defaultProps = {
    Wrapper: p => <Layout.Main fullWidth {...p}/>,
};
exports.default = EventsContent;
//# sourceMappingURL=content.jsx.map