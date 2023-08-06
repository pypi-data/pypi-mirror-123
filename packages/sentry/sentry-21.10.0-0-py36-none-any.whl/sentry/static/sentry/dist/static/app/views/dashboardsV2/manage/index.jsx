Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const dropdownControl_1 = (0, tslib_1.__importStar)(require("app/components/dropdownControl"));
const noProjectMessage_1 = (0, tslib_1.__importDefault)(require("app/components/noProjectMessage"));
const searchBar_1 = (0, tslib_1.__importDefault)(require("app/components/searchBar"));
const sentryDocumentTitle_1 = (0, tslib_1.__importDefault)(require("app/components/sentryDocumentTitle"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const organization_1 = require("app/styles/organization");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const queryString_1 = require("app/utils/queryString");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const dashboardList_1 = (0, tslib_1.__importDefault)(require("./dashboardList"));
const SORT_OPTIONS = [
    { label: (0, locale_1.t)('My Dashboards'), value: 'mydashboards' },
    { label: (0, locale_1.t)('Dashboard Name (A-Z)'), value: 'title' },
    { label: (0, locale_1.t)('Date Created (Newest)'), value: '-dateCreated' },
    { label: (0, locale_1.t)('Date Created (Oldest)'), value: 'dateCreated' },
    { label: (0, locale_1.t)('Most Popular'), value: 'mostPopular' },
    { label: (0, locale_1.t)('Recently Viewed'), value: 'recentlyViewed' },
];
class ManageDashboards extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.handleSortChange = (value) => {
            const { location } = this.props;
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'dashboards_manage.change_sort',
                eventName: 'Dashboards Manager: Sort By Changed',
                organization_id: parseInt(this.props.organization.id, 10),
                sort: value,
            });
            react_router_1.browserHistory.push({
                pathname: location.pathname,
                query: Object.assign(Object.assign({}, location.query), { cursor: undefined, sort: value }),
            });
        };
    }
    getEndpoints() {
        const { organization, location } = this.props;
        return [
            [
                'dashboards',
                `/organizations/${organization.slug}/dashboards/`,
                {
                    query: Object.assign(Object.assign({}, (0, pick_1.default)(location.query, ['cursor', 'query'])), { sort: this.getActiveSort().value, per_page: '9' }),
                },
            ],
        ];
    }
    getActiveSort() {
        const { location } = this.props;
        const urlSort = (0, queryString_1.decodeScalar)(location.query.sort, 'mydashboards');
        return SORT_OPTIONS.find(item => item.value === urlSort) || SORT_OPTIONS[0];
    }
    onDashboardsChange() {
        this.reloadData();
    }
    handleSearch(query) {
        const { location, router } = this.props;
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey: 'dashboards_manage.search',
            eventName: 'Dashboards Manager: Search',
            organization_id: parseInt(this.props.organization.id, 10),
        });
        router.push({
            pathname: location.pathname,
            query: Object.assign(Object.assign({}, location.query), { cursor: undefined, query }),
        });
    }
    getQuery() {
        const { query } = this.props.location.query;
        return typeof query === 'string' ? query : undefined;
    }
    renderActions() {
        const activeSort = this.getActiveSort();
        return (<StyledActions>
        <searchBar_1.default defaultQuery="" query={this.getQuery()} placeholder={(0, locale_1.t)('Search Dashboards')} onSearch={query => this.handleSearch(query)}/>
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
    renderDashboards() {
        const { dashboards, dashboardsPageLinks } = this.state;
        const { organization, location, api } = this.props;
        return (<dashboardList_1.default api={api} dashboards={dashboards} organization={organization} pageLinks={dashboardsPageLinks} location={location} onDashboardsChange={() => this.onDashboardsChange()}/>);
    }
    getTitle() {
        return (0, locale_1.t)('Dashboards');
    }
    onCreate() {
        const { organization, location } = this.props;
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey: 'dashboards_manage.create.start',
            eventName: 'Dashboards Manager: Dashboard Create Started',
            organization_id: parseInt(organization.id, 10),
        });
        react_router_1.browserHistory.push({
            pathname: `/organizations/${organization.slug}/dashboards/new/`,
            query: location.query,
        });
    }
    renderBody() {
        const { organization } = this.props;
        return (<feature_1.default organization={organization} features={['dashboards-edit']} renderDisabled={this.renderNoAccess}>
        <sentryDocumentTitle_1.default title={(0, locale_1.t)('Dashboards')} orgSlug={organization.slug}>
          <StyledPageContent>
            <noProjectMessage_1.default organization={organization}>
              <organization_1.PageContent>
                <StyledPageHeader>
                  {(0, locale_1.t)('Dashboards')}
                  <button_1.default data-test-id="dashboard-create" onClick={event => {
                event.preventDefault();
                this.onCreate();
            }} priority="primary" icon={<icons_1.IconAdd size="xs" isCircled/>}>
                    {(0, locale_1.t)('Create Dashboard')}
                  </button_1.default>
                </StyledPageHeader>
                {this.renderActions()}
                {this.renderDashboards()}
              </organization_1.PageContent>
            </noProjectMessage_1.default>
          </StyledPageContent>
        </sentryDocumentTitle_1.default>
      </feature_1.default>);
    }
}
const StyledPageContent = (0, styled_1.default)(organization_1.PageContent) `
  padding: 0;
`;
const StyledPageHeader = (0, styled_1.default)('div') `
  display: flex;
  align-items: flex-end;
  font-size: ${p => p.theme.headerFontSize};
  color: ${p => p.theme.textColor};
  justify-content: space-between;
  margin-bottom: ${(0, space_1.default)(2)};
`;
const StyledActions = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: auto max-content;
  grid-gap: ${(0, space_1.default)(2)};
  margin-bottom: ${(0, space_1.default)(2)};

  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    grid-template-columns: auto;
  }
`;
exports.default = (0, withApi_1.default)((0, withOrganization_1.default)(ManageDashboards));
//# sourceMappingURL=index.jsx.map