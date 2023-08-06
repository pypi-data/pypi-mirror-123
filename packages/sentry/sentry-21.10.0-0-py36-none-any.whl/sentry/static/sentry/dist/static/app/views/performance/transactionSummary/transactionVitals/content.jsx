Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const dropdownControl_1 = (0, tslib_1.__importStar)(require("app/components/dropdownControl"));
const searchBar_1 = (0, tslib_1.__importDefault)(require("app/components/events/searchBar"));
const Layout = (0, tslib_1.__importStar)(require("app/components/layouts/thirds"));
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const histogram_1 = (0, tslib_1.__importDefault)(require("app/utils/performance/histogram"));
const constants_1 = require("app/utils/performance/histogram/constants");
const queryString_1 = require("app/utils/queryString");
const constants_2 = require("./constants");
const vitalsPanel_1 = (0, tslib_1.__importDefault)(require("./vitalsPanel"));
function VitalsContent(props) {
    const { location, organization, eventView } = props;
    const query = (0, queryString_1.decodeScalar)(location.query.query, '');
    const handleSearch = (newQuery) => {
        const queryParams = (0, getParams_1.getParams)(Object.assign(Object.assign({}, (location.query || {})), { query: newQuery }));
        // do not propagate pagination when making a new search
        delete queryParams.cursor;
        react_router_1.browserHistory.push({
            pathname: location.pathname,
            query: queryParams,
        });
    };
    return (<histogram_1.default location={location} zoomKeys={constants_2.ZOOM_KEYS}>
      {({ activeFilter, handleFilterChange, handleResetView, isZoomed }) => (<Layout.Main fullWidth>
          <StyledActions>
            <StyledSearchBar organization={organization} projectIds={eventView.project} query={query} fields={eventView.fields} onSearch={handleSearch}/>
            <dropdownControl_1.default buttonProps={{ prefix: (0, locale_1.t)('Outliers') }} label={activeFilter.label}>
              {constants_1.FILTER_OPTIONS.map(({ label, value }) => (<dropdownControl_1.DropdownItem key={value} onSelect={(filterOption) => {
                    (0, analytics_1.trackAnalyticsEvent)({
                        eventKey: 'performance_views.vitals.filter_changed',
                        eventName: 'Performance Views: Change vitals filter',
                        organization_id: organization.id,
                        value: filterOption,
                    });
                    handleFilterChange(filterOption);
                }} eventKey={value} isActive={value === activeFilter.value}>
                  {label}
                </dropdownControl_1.DropdownItem>))}
            </dropdownControl_1.default>
            <button_1.default onClick={() => {
                (0, analytics_1.trackAnalyticsEvent)({
                    eventKey: 'performance_views.vitals.reset_view',
                    eventName: 'Performance Views: Reset vitals view',
                    organization_id: organization.id,
                });
                handleResetView();
            }} disabled={!isZoomed} data-test-id="reset-view">
              {(0, locale_1.t)('Reset View')}
            </button_1.default>
          </StyledActions>
          <vitalsPanel_1.default organization={organization} location={location} eventView={eventView} dataFilter={activeFilter.value}/>
        </Layout.Main>)}
    </histogram_1.default>);
}
const StyledSearchBar = (0, styled_1.default)(searchBar_1.default) `
  flex-grow: 1;
`;
const StyledActions = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(2)};
  grid-template-columns: auto max-content max-content;
  align-items: center;
  margin-bottom: ${(0, space_1.default)(3)};
`;
exports.default = VitalsContent;
//# sourceMappingURL=content.jsx.map