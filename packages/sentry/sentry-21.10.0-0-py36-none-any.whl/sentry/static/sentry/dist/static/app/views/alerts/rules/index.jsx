Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const flatten_1 = (0, tslib_1.__importDefault)(require("lodash/flatten"));
const indicator_1 = require("app/actionCreators/indicator");
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const Layout = (0, tslib_1.__importStar)(require("app/components/layouts/thirds"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const globalSelectionHeader_1 = (0, tslib_1.__importDefault)(require("app/components/organizations/globalSelectionHeader"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const panels_1 = require("app/components/panels");
const searchBar_1 = (0, tslib_1.__importDefault)(require("app/components/searchBar"));
const sentryDocumentTitle_1 = (0, tslib_1.__importDefault)(require("app/components/sentryDocumentTitle"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const projects_1 = (0, tslib_1.__importDefault)(require("app/utils/projects"));
const withGlobalSelection_1 = (0, tslib_1.__importDefault)(require("app/utils/withGlobalSelection"));
const withTeams_1 = (0, tslib_1.__importDefault)(require("app/utils/withTeams"));
const header_1 = (0, tslib_1.__importDefault)(require("../list/header"));
const utils_1 = require("../utils");
const row_1 = (0, tslib_1.__importDefault)(require("./row"));
const teamFilter_1 = (0, tslib_1.__importStar)(require("./teamFilter"));
const DOCS_URL = 'https://docs.sentry.io/product/alerts-notifications/metric-alerts/';
class AlertRulesList extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.handleChangeFilter = (_sectionId, activeFilters) => {
            const { router, location } = this.props;
            const _a = location.query, { cursor: _cursor, page: _page } = _a, currentQuery = (0, tslib_1.__rest)(_a, ["cursor", "page"]);
            const teams = [...activeFilters];
            router.push({
                pathname: location.pathname,
                query: Object.assign(Object.assign({}, currentQuery), { team: teams.length ? teams : '' }),
            });
        };
        this.handleChangeSearch = (name) => {
            const { router, location } = this.props;
            const _a = location.query, { cursor: _cursor, page: _page } = _a, currentQuery = (0, tslib_1.__rest)(_a, ["cursor", "page"]);
            router.push({
                pathname: location.pathname,
                query: Object.assign(Object.assign({}, currentQuery), { name }),
            });
        };
        this.handleDeleteRule = (projectId, rule) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { params } = this.props;
            const { orgId } = params;
            const alertPath = (0, utils_1.isIssueAlert)(rule) ? 'rules' : 'alert-rules';
            try {
                yield this.api.requestPromise(`/projects/${orgId}/${projectId}/${alertPath}/${rule.id}/`, {
                    method: 'DELETE',
                });
                this.reloadData();
            }
            catch (_err) {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Error deleting rule'));
            }
        });
    }
    getEndpoints() {
        const { params, location } = this.props;
        const { query } = location;
        query.expand = ['latestIncident'];
        query.team = (0, teamFilter_1.getTeamParams)(query.team);
        if (!query.sort) {
            query.sort = ['incident_status', 'date_triggered'];
        }
        return [
            [
                'ruleList',
                `/organizations/${params && params.orgId}/combined-rules/`,
                {
                    query,
                },
            ],
        ];
    }
    renderLoading() {
        return this.renderBody();
    }
    renderFilterBar() {
        var _a;
        const { teams, location } = this.props;
        const selectedTeams = new Set((0, teamFilter_1.getTeamParams)(location.query.team));
        return (<FilterWrapper>
        <teamFilter_1.default teams={teams} selectedTeams={selectedTeams} handleChangeFilter={this.handleChangeFilter}/>
        <StyledSearchBar placeholder={(0, locale_1.t)('Search by name')} query={(_a = location.query) === null || _a === void 0 ? void 0 : _a.name} onSearch={this.handleChangeSearch}/>
      </FilterWrapper>);
    }
    renderList() {
        const { params: { orgId }, location: { query }, organization, teams, } = this.props;
        const { loading, ruleList = [], ruleListPageLinks } = this.state;
        const allProjectsFromIncidents = new Set((0, flatten_1.default)(ruleList === null || ruleList === void 0 ? void 0 : ruleList.map(({ projects }) => projects)));
        const sort = {
            asc: query.asc === '1',
            field: query.sort || 'date_added',
        };
        const { cursor: _cursor, page: _page } = query, currentQuery = (0, tslib_1.__rest)(query, ["cursor", "page"]);
        const isAlertRuleSort = sort.field.includes('incident_status') || sort.field.includes('date_triggered');
        const sortArrow = (<icons_1.IconArrow color="gray300" size="xs" direction={sort.asc ? 'up' : 'down'}/>);
        const userTeams = new Set(teams.filter(({ isMember }) => isMember).map(({ id }) => id));
        return (<StyledLayoutBody>
        <Layout.Main fullWidth>
          {this.renderFilterBar()}
          <StyledPanelTable headers={[
                <StyledSortLink key="name" to={{
                        pathname: location.pathname,
                        query: Object.assign(Object.assign({}, currentQuery), { 
                            // sort by name should start by ascending on first click
                            asc: sort.field === 'name' && sort.asc ? undefined : '1', sort: 'name' }),
                    }}>
                {(0, locale_1.t)('Alert Rule')} {sort.field === 'name' && sortArrow}
              </StyledSortLink>,
                <StyledSortLink key="status" to={{
                        pathname: location.pathname,
                        query: Object.assign(Object.assign({}, currentQuery), { asc: isAlertRuleSort && !sort.asc ? '1' : undefined, sort: ['incident_status', 'date_triggered'] }),
                    }}>
                {(0, locale_1.t)('Status')} {isAlertRuleSort && sortArrow}
              </StyledSortLink>,
                (0, locale_1.t)('Project'),
                (0, locale_1.t)('Team'),
                <StyledSortLink key="dateAdded" to={{
                        pathname: location.pathname,
                        query: Object.assign(Object.assign({}, currentQuery), { asc: sort.field === 'date_added' && !sort.asc ? '1' : undefined, sort: 'date_added' }),
                    }}>
                {(0, locale_1.t)('Created')} {sort.field === 'date_added' && sortArrow}
              </StyledSortLink>,
                (0, locale_1.t)('Actions'),
            ]} isLoading={loading} isEmpty={(ruleList === null || ruleList === void 0 ? void 0 : ruleList.length) === 0} emptyMessage={(0, locale_1.t)('No alert rules found for the current query.')} emptyAction={<EmptyStateAction>
                {(0, locale_1.tct)('Learn more about [link:Alerts]', {
                    link: <externalLink_1.default href={DOCS_URL}/>,
                })}
              </EmptyStateAction>}>
            <projects_1.default orgId={orgId} slugs={Array.from(allProjectsFromIncidents)}>
              {({ initiallyLoaded, projects }) => ruleList.map(rule => (<row_1.default 
            // Metric and issue alerts can have the same id
            key={`${(0, utils_1.isIssueAlert)(rule) ? 'metric' : 'issue'}-${rule.id}`} projectsLoaded={initiallyLoaded} projects={projects} rule={rule} orgId={orgId} onDelete={this.handleDeleteRule} organization={organization} userTeams={userTeams}/>))}
            </projects_1.default>
          </StyledPanelTable>
          <pagination_1.default pageLinks={ruleListPageLinks}/>
        </Layout.Main>
      </StyledLayoutBody>);
    }
    renderBody() {
        const { params, organization, router } = this.props;
        const { orgId } = params;
        return (<sentryDocumentTitle_1.default title={(0, locale_1.t)('Alerts')} orgSlug={orgId}>
        <globalSelectionHeader_1.default organization={organization} showDateSelector={false} showEnvironmentSelector={false}>
          <header_1.default organization={organization} router={router} activeTab="rules"/>
          {this.renderList()}
        </globalSelectionHeader_1.default>
      </sentryDocumentTitle_1.default>);
    }
}
class AlertRulesListContainer extends react_1.Component {
    componentDidMount() {
        this.trackView();
    }
    componentDidUpdate(prevProps) {
        var _a, _b;
        const { location } = this.props;
        if (((_a = prevProps.location.query) === null || _a === void 0 ? void 0 : _a.sort) !== ((_b = location.query) === null || _b === void 0 ? void 0 : _b.sort)) {
            this.trackView();
        }
    }
    trackView() {
        const { organization, location } = this.props;
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey: 'alert_rules.viewed',
            eventName: 'Alert Rules: Viewed',
            organization_id: organization.id,
            sort: Array.isArray(location.query.sort)
                ? location.query.sort.join(',')
                : location.query.sort,
        });
    }
    render() {
        return <AlertRulesList {...this.props}/>;
    }
}
exports.default = (0, withGlobalSelection_1.default)((0, withTeams_1.default)(AlertRulesListContainer));
const StyledLayoutBody = (0, styled_1.default)(Layout.Body) `
  margin-bottom: -20px;
`;
const StyledSortLink = (0, styled_1.default)(link_1.default) `
  color: inherit;

  :hover {
    color: inherit;
  }
`;
const FilterWrapper = (0, styled_1.default)('div') `
  display: flex;
  margin-bottom: ${(0, space_1.default)(1.5)};
`;
const StyledSearchBar = (0, styled_1.default)(searchBar_1.default) `
  flex-grow: 1;
  margin-left: ${(0, space_1.default)(1.5)};
`;
const StyledPanelTable = (0, styled_1.default)(panels_1.PanelTable) `
  overflow: auto;
  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    overflow: initial;
  }

  grid-template-columns: auto 1.5fr 1fr 1fr 1fr auto;
  white-space: nowrap;
  font-size: ${p => p.theme.fontSizeMedium};
`;
const EmptyStateAction = (0, styled_1.default)('p') `
  font-size: ${p => p.theme.fontSizeLarge};
`;
//# sourceMappingURL=index.jsx.map