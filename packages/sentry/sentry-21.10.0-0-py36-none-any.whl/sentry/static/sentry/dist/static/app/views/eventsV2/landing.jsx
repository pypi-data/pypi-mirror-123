Object.defineProperty(exports, "__esModule", { value: true });
exports.DiscoverLanding = void 0;
const tslib_1 = require("tslib");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const query_string_1 = require("query-string");
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const guideAnchor_1 = (0, tslib_1.__importDefault)(require("app/components/assistant/guideAnchor"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const dropdownControl_1 = (0, tslib_1.__importStar)(require("app/components/dropdownControl"));
const noProjectMessage_1 = (0, tslib_1.__importDefault)(require("app/components/noProjectMessage"));
const searchBar_1 = (0, tslib_1.__importDefault)(require("app/components/searchBar"));
const sentryDocumentTitle_1 = (0, tslib_1.__importDefault)(require("app/components/sentryDocumentTitle"));
const switchButton_1 = (0, tslib_1.__importDefault)(require("app/components/switchButton"));
const locale_1 = require("app/locale");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const organization_1 = require("app/styles/organization");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const eventView_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/eventView"));
const queryString_1 = require("app/utils/queryString");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const banner_1 = (0, tslib_1.__importDefault)(require("./banner"));
const data_1 = require("./data");
const queryList_1 = (0, tslib_1.__importDefault)(require("./queryList"));
const utils_1 = require("./utils");
const SORT_OPTIONS = [
    { label: (0, locale_1.t)('My Queries'), value: 'myqueries' },
    { label: (0, locale_1.t)('Recently Edited'), value: '-dateUpdated' },
    { label: (0, locale_1.t)('Query Name (A-Z)'), value: 'name' },
    { label: (0, locale_1.t)('Date Created (Newest)'), value: '-dateCreated' },
    { label: (0, locale_1.t)('Date Created (Oldest)'), value: 'dateCreated' },
    { label: (0, locale_1.t)('Most Outdated'), value: 'dateUpdated' },
    { label: (0, locale_1.t)('Most Popular'), value: 'mostPopular' },
    { label: (0, locale_1.t)('Recently Viewed'), value: 'recentlyViewed' },
];
class DiscoverLanding extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.state = {
            // AsyncComponent state
            loading: true,
            reloading: false,
            error: false,
            errors: {},
            // local component state
            renderPrebuilt: (0, utils_1.shouldRenderPrebuilt)(),
            savedQueries: null,
            savedQueriesPageLinks: '',
        };
        this.shouldReload = true;
        this.handleQueryChange = () => {
            this.fetchData({ reloading: true });
        };
        this.handleSearchQuery = (searchQuery) => {
            const { location } = this.props;
            react_router_1.browserHistory.push({
                pathname: location.pathname,
                query: Object.assign(Object.assign({}, location.query), { cursor: undefined, query: String(searchQuery).trim() || undefined }),
            });
        };
        this.handleSortChange = (value) => {
            const { location } = this.props;
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'discover_v2.change_sort',
                eventName: 'Discoverv2: Sort By Changed',
                organization_id: parseInt(this.props.organization.id, 10),
                sort: value,
            });
            react_router_1.browserHistory.push({
                pathname: location.pathname,
                query: Object.assign(Object.assign({}, location.query), { cursor: undefined, sort: value }),
            });
        };
        this.togglePrebuilt = () => {
            const { renderPrebuilt } = this.state;
            this.setState({ renderPrebuilt: !renderPrebuilt }, () => {
                (0, utils_1.setRenderPrebuilt)(!renderPrebuilt);
                this.fetchData({ reloading: true });
            });
        };
        this.onGoLegacyDiscover = () => {
            localStorage.setItem('discover:version', '1');
            const user = configStore_1.default.get('user');
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'discover_v2.opt_out',
                eventName: 'Discoverv2: Go to discover',
                organization_id: parseInt(this.props.organization.id, 10),
                user_id: parseInt(user.id, 10),
            });
        };
    }
    getSavedQuerySearchQuery() {
        const { location } = this.props;
        return (0, queryString_1.decodeScalar)(location.query.query, '').trim();
    }
    getActiveSort() {
        const { location } = this.props;
        const urlSort = (0, queryString_1.decodeScalar)(location.query.sort, 'myqueries');
        return SORT_OPTIONS.find(item => item.value === urlSort) || SORT_OPTIONS[0];
    }
    getEndpoints() {
        const { organization, location } = this.props;
        const views = (0, utils_1.getPrebuiltQueries)(organization);
        const searchQuery = this.getSavedQuerySearchQuery();
        const cursor = (0, queryString_1.decodeScalar)(location.query.cursor);
        let perPage = 9;
        const canRenderPrebuilt = this.state
            ? this.state.renderPrebuilt
            : (0, utils_1.shouldRenderPrebuilt)();
        if (!cursor && canRenderPrebuilt) {
            // invariant: we're on the first page
            if (searchQuery && searchQuery.length > 0) {
                const needleSearch = searchQuery.toLowerCase();
                const numOfPrebuiltQueries = views.reduce((sum, view) => {
                    const eventView = eventView_1.default.fromNewQueryWithLocation(view, location);
                    // if a search is performed on the list of queries, we filter
                    // on the pre-built queries
                    if (eventView.name && eventView.name.toLowerCase().includes(needleSearch)) {
                        return sum + 1;
                    }
                    return sum;
                }, 0);
                perPage = Math.max(1, perPage - numOfPrebuiltQueries);
            }
            else {
                perPage = Math.max(1, perPage - views.length);
            }
        }
        const queryParams = {
            cursor,
            query: `version:2 name:"${searchQuery}"`,
            per_page: perPage.toString(),
            sortBy: this.getActiveSort().value,
        };
        if (!cursor) {
            delete queryParams.cursor;
        }
        return [
            [
                'savedQueries',
                `/organizations/${organization.slug}/discover/saved/`,
                {
                    query: queryParams,
                },
            ],
        ];
    }
    componentDidUpdate(prevProps) {
        const PAYLOAD_KEYS = ['sort', 'cursor', 'query'];
        const payloadKeysChanged = !(0, isEqual_1.default)((0, pick_1.default)(prevProps.location.query, PAYLOAD_KEYS), (0, pick_1.default)(this.props.location.query, PAYLOAD_KEYS));
        // if any of the query strings relevant for the payload has changed,
        // we re-fetch data
        if (payloadKeysChanged) {
            this.fetchData();
        }
    }
    renderBanner() {
        const { location, organization } = this.props;
        const eventView = eventView_1.default.fromNewQueryWithLocation(data_1.DEFAULT_EVENT_VIEW, location);
        const to = eventView.getResultsViewUrlTarget(organization.slug);
        const resultsUrl = `${to.pathname}?${(0, query_string_1.stringify)(to.query)}`;
        return <banner_1.default organization={organization} resultsUrl={resultsUrl}/>;
    }
    renderActions() {
        const activeSort = this.getActiveSort();
        const { renderPrebuilt, savedQueries } = this.state;
        return (<StyledActions>
        <StyledSearchBar defaultQuery="" query={this.getSavedQuerySearchQuery()} placeholder={(0, locale_1.t)('Search saved queries')} onSearch={this.handleSearchQuery}/>
        <PrebuiltSwitch>
          <SwitchLabel>Show Prebuilt</SwitchLabel>
          <switchButton_1.default isActive={renderPrebuilt} isDisabled={renderPrebuilt && (savedQueries !== null && savedQueries !== void 0 ? savedQueries : []).length === 0} size="lg" toggle={this.togglePrebuilt}/>
        </PrebuiltSwitch>
        <dropdownControl_1.default buttonProps={{ prefix: (0, locale_1.t)('Sort By') }} label={activeSort.label}>
          {SORT_OPTIONS.map(({ label, value }) => (<dropdownControl_1.DropdownItem key={value} onSelect={this.handleSortChange} eventKey={value} isActive={value === activeSort.value}>
              {label}
            </dropdownControl_1.DropdownItem>))}
        </dropdownControl_1.default>
      </StyledActions>);
    }
    renderNoAccess() {
        return (<organization_1.PageContent>
        <alert_1.default type="warning">{(0, locale_1.t)("You don't have access to this feature")}</alert_1.default>
      </organization_1.PageContent>);
    }
    renderBody() {
        const { location, organization } = this.props;
        const { savedQueries, savedQueriesPageLinks, renderPrebuilt } = this.state;
        return (<queryList_1.default pageLinks={savedQueriesPageLinks} savedQueries={savedQueries !== null && savedQueries !== void 0 ? savedQueries : []} savedQuerySearchQuery={this.getSavedQuerySearchQuery()} renderPrebuilt={renderPrebuilt} location={location} organization={organization} onQueryChange={this.handleQueryChange}/>);
    }
    render() {
        const { location, organization } = this.props;
        const eventView = eventView_1.default.fromNewQueryWithLocation(data_1.DEFAULT_EVENT_VIEW, location);
        const to = eventView.getResultsViewUrlTarget(organization.slug);
        return (<feature_1.default organization={organization} features={['discover-query']} renderDisabled={this.renderNoAccess}>
        <sentryDocumentTitle_1.default title={(0, locale_1.t)('Discover')} orgSlug={organization.slug}>
          <StyledPageContent>
            <noProjectMessage_1.default organization={organization}>
              <organization_1.PageContent>
                <StyledPageHeader>
                  <guideAnchor_1.default target="discover_landing_header">
                    {(0, locale_1.t)('Discover')}
                  </guideAnchor_1.default>
                  <StyledButton data-test-id="build-new-query" to={to} priority="primary" onClick={() => {
                (0, analytics_1.trackAnalyticsEvent)({
                    eventKey: 'discover_v2.build_new_query',
                    eventName: 'Discoverv2: Build a new Discover Query',
                    organization_id: parseInt(this.props.organization.id, 10),
                });
            }}>
                    {(0, locale_1.t)('Build a new query')}
                  </StyledButton>
                </StyledPageHeader>
                {this.renderBanner()}
                {this.renderActions()}
                {this.renderComponent()}
              </organization_1.PageContent>
            </noProjectMessage_1.default>
          </StyledPageContent>
        </sentryDocumentTitle_1.default>
      </feature_1.default>);
    }
}
exports.DiscoverLanding = DiscoverLanding;
const StyledPageContent = (0, styled_1.default)(organization_1.PageContent) `
  padding: 0;
`;
const PrebuiltSwitch = (0, styled_1.default)('div') `
  display: flex;
`;
const SwitchLabel = (0, styled_1.default)('div') `
  padding-right: 8px;
`;
const StyledPageHeader = (0, styled_1.default)('div') `
  display: flex;
  align-items: flex-end;
  font-size: ${p => p.theme.headerFontSize};
  color: ${p => p.theme.textColor};
  justify-content: space-between;
  margin-bottom: ${(0, space_1.default)(2)};
`;
const StyledSearchBar = (0, styled_1.default)(searchBar_1.default) `
  flex-grow: 1;
`;
const StyledActions = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(2)};
  grid-template-columns: auto max-content min-content;
  align-items: center;
  margin-bottom: ${(0, space_1.default)(2)};

  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    grid-template-columns: auto;
  }
`;
const StyledButton = (0, styled_1.default)(button_1.default) `
  white-space: nowrap;
`;
exports.default = (0, withOrganization_1.default)(DiscoverLanding);
//# sourceMappingURL=landing.jsx.map