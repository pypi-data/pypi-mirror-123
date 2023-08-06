Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const flatten_1 = (0, tslib_1.__importDefault)(require("lodash/flatten"));
const prompts_1 = require("app/actionCreators/prompts");
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const createAlertButton_1 = (0, tslib_1.__importDefault)(require("app/components/createAlertButton"));
const Layout = (0, tslib_1.__importStar)(require("app/components/layouts/thirds"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
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
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const withTeams_1 = (0, tslib_1.__importDefault)(require("app/utils/withTeams"));
const teamFilter_1 = (0, tslib_1.__importStar)(require("../rules/teamFilter"));
const header_1 = (0, tslib_1.__importDefault)(require("./header"));
const onboarding_1 = (0, tslib_1.__importDefault)(require("./onboarding"));
const row_1 = (0, tslib_1.__importDefault)(require("./row"));
const DOCS_URL = 'https://docs.sentry.io/workflow/alerts-notifications/alerts/?_ga=2.21848383.580096147.1592364314-1444595810.1582160976';
class IncidentsList extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.handleChangeSearch = (title) => {
            const { router, location } = this.props;
            const _a = location.query, { cursor: _cursor, page: _page } = _a, currentQuery = (0, tslib_1.__rest)(_a, ["cursor", "page"]);
            router.push({
                pathname: location.pathname,
                query: Object.assign(Object.assign({}, currentQuery), { title }),
            });
        };
        this.handleChangeFilter = (sectionId, activeFilters) => {
            const { router, location } = this.props;
            const _a = location.query, { cursor: _cursor, page: _page } = _a, currentQuery = (0, tslib_1.__rest)(_a, ["cursor", "page"]);
            let team = currentQuery.team;
            if (sectionId === 'teams') {
                team = activeFilters.size ? [...activeFilters] : '';
            }
            let status = currentQuery.status;
            if (sectionId === 'status') {
                status = activeFilters.size ? [...activeFilters] : '';
            }
            router.push({
                pathname: location.pathname,
                query: Object.assign(Object.assign({}, currentQuery), { status, 
                    // Preserve empty team query parameter
                    team: team.length === 0 ? '' : team }),
            });
        };
    }
    getEndpoints() {
        const { params, location } = this.props;
        const { query } = location;
        const status = this.getQueryStatus(query.status);
        // Filtering by one status, both does nothing
        if (status.length === 1) {
            query.status = status;
        }
        query.team = (0, teamFilter_1.getTeamParams)(query.team);
        query.expand = ['original_alert_rule'];
        return [['incidentList', `/organizations/${params === null || params === void 0 ? void 0 : params.orgId}/incidents/`, { query }]];
    }
    getQueryStatus(status) {
        if (Array.isArray(status)) {
            return status;
        }
        if (status === '') {
            return [];
        }
        return ['open', 'closed'].includes(status) ? [status] : [];
    }
    /**
     * If our incidentList is empty, determine if we've configured alert rules or
     * if the user has seen the welcome prompt.
     */
    onLoadAllEndpointsSuccess() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { incidentList } = this.state;
            if (!incidentList || incidentList.length !== 0) {
                this.setState({ hasAlertRule: true, firstVisitShown: false });
                return;
            }
            this.setState({ loading: true });
            // Check if they have rules or not, to know which empty state message to
            // display
            const { params, location, organization } = this.props;
            const alertRules = yield this.api.requestPromise(`/organizations/${params === null || params === void 0 ? void 0 : params.orgId}/alert-rules/`, {
                method: 'GET',
                query: location.query,
            });
            const hasAlertRule = alertRules.length > 0;
            // We've already configured alert rules, no need to check if we should show
            // the "first time welcome" prompt
            if (hasAlertRule) {
                this.setState({ hasAlertRule, firstVisitShown: false, loading: false });
                return;
            }
            // Check if they have already seen the prompt for the alert stream
            const prompt = yield (0, prompts_1.promptsCheck)(this.api, {
                organizationId: organization.id,
                feature: 'alert_stream',
            });
            const firstVisitShown = !(prompt === null || prompt === void 0 ? void 0 : prompt.dismissedTime);
            if (firstVisitShown) {
                // Prompt has not been seen, mark the prompt as seen immediately so they
                // don't see it again
                (0, prompts_1.promptsUpdate)(this.api, {
                    feature: 'alert_stream',
                    organizationId: organization.id,
                    status: 'dismissed',
                });
            }
            this.setState({ hasAlertRule, firstVisitShown, loading: false });
        });
    }
    renderFilterBar() {
        var _a;
        const { teams, location } = this.props;
        const selectedTeams = new Set((0, teamFilter_1.getTeamParams)(location.query.team));
        const selectedStatus = new Set(this.getQueryStatus(location.query.status));
        return (<FilterWrapper>
        <teamFilter_1.default showStatus teams={teams} selectedStatus={selectedStatus} selectedTeams={selectedTeams} handleChangeFilter={this.handleChangeFilter}/>
        <StyledSearchBar placeholder={(0, locale_1.t)('Search by name')} query={(_a = location.query) === null || _a === void 0 ? void 0 : _a.name} onSearch={this.handleChangeSearch}/>
      </FilterWrapper>);
    }
    tryRenderOnboarding() {
        const { firstVisitShown } = this.state;
        const { organization } = this.props;
        if (!firstVisitShown) {
            return null;
        }
        const actions = (<react_1.Fragment>
        <button_1.default size="small" external href={DOCS_URL}>
          {(0, locale_1.t)('View Features')}
        </button_1.default>
        <createAlertButton_1.default organization={organization} iconProps={{ size: 'xs' }} size="small" priority="primary" referrer="alert_stream">
          {(0, locale_1.t)('Create Alert Rule')}
        </createAlertButton_1.default>
      </react_1.Fragment>);
        return <onboarding_1.default actions={actions}/>;
    }
    renderLoading() {
        return this.renderBody();
    }
    renderList() {
        var _a;
        const { loading, incidentList, incidentListPageLinks, hasAlertRule } = this.state;
        const { params: { orgId }, organization, } = this.props;
        const allProjectsFromIncidents = new Set((0, flatten_1.default)(incidentList === null || incidentList === void 0 ? void 0 : incidentList.map(({ projects }) => projects)));
        const checkingForAlertRules = incidentList && incidentList.length === 0 && hasAlertRule === undefined
            ? true
            : false;
        const showLoadingIndicator = loading || checkingForAlertRules;
        return (<react_1.Fragment>
        {(_a = this.tryRenderOnboarding()) !== null && _a !== void 0 ? _a : (<panels_1.PanelTable isLoading={showLoadingIndicator} isEmpty={(incidentList === null || incidentList === void 0 ? void 0 : incidentList.length) === 0} emptyMessage={(0, locale_1.t)('No incidents exist for the current query.')} emptyAction={<EmptyStateAction>
                {(0, locale_1.tct)('Learn more about [link:Metric Alerts]', {
                        link: <externalLink_1.default href={DOCS_URL}/>,
                    })}
              </EmptyStateAction>} headers={[
                    (0, locale_1.t)('Alert Rule'),
                    (0, locale_1.t)('Triggered'),
                    (0, locale_1.t)('Duration'),
                    (0, locale_1.t)('Project'),
                    (0, locale_1.t)('Alert ID'),
                    (0, locale_1.t)('Team'),
                ]}>
            <projects_1.default orgId={orgId} slugs={Array.from(allProjectsFromIncidents)}>
              {({ initiallyLoaded, projects }) => incidentList.map(incident => (<row_1.default key={incident.id} projectsLoaded={initiallyLoaded} projects={projects} incident={incident} orgId={orgId} organization={organization}/>))}
            </projects_1.default>
          </panels_1.PanelTable>)}
        <pagination_1.default pageLinks={incidentListPageLinks}/>
      </react_1.Fragment>);
    }
    renderBody() {
        const { params, organization, router } = this.props;
        const { orgId } = params;
        return (<sentryDocumentTitle_1.default title={(0, locale_1.t)('Alerts')} orgSlug={orgId}>
        <globalSelectionHeader_1.default organization={organization} showDateSelector={false}>
          <header_1.default organization={organization} router={router} activeTab="stream"/>
          <StyledLayoutBody>
            <Layout.Main fullWidth>
              {!this.tryRenderOnboarding() && (<react_1.Fragment>
                  <StyledAlert icon={<icons_1.IconInfo />}>
                    {(0, locale_1.t)('This page only shows metric alerts.')}
                  </StyledAlert>
                  {this.renderFilterBar()}
                </react_1.Fragment>)}
              {this.renderList()}
            </Layout.Main>
          </StyledLayoutBody>
        </globalSelectionHeader_1.default>
      </sentryDocumentTitle_1.default>);
    }
}
class IncidentsListContainer extends react_1.Component {
    componentDidMount() {
        this.trackView();
    }
    componentDidUpdate(nextProps) {
        var _a, _b;
        if (((_a = nextProps.location.query) === null || _a === void 0 ? void 0 : _a.status) !== ((_b = this.props.location.query) === null || _b === void 0 ? void 0 : _b.status)) {
            this.trackView();
        }
    }
    trackView() {
        const { organization } = this.props;
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey: 'alert_stream.viewed',
            eventName: 'Alert Stream: Viewed',
            organization_id: organization.id,
        });
    }
    renderNoAccess() {
        return (<Layout.Body>
        <Layout.Main fullWidth>
          <alert_1.default type="warning">{(0, locale_1.t)("You don't have access to this feature")}</alert_1.default>
        </Layout.Main>
      </Layout.Body>);
    }
    render() {
        const { organization } = this.props;
        return (<feature_1.default features={['organizations:incidents']} organization={organization} hookName="feature-disabled:alerts-page" renderDisabled={this.renderNoAccess}>
        <IncidentsList {...this.props}/>
      </feature_1.default>);
    }
}
const StyledAlert = (0, styled_1.default)(alert_1.default) `
  margin-bottom: ${(0, space_1.default)(1.5)};
`;
const FilterWrapper = (0, styled_1.default)('div') `
  display: flex;
  margin-bottom: ${(0, space_1.default)(1.5)};
`;
const StyledSearchBar = (0, styled_1.default)(searchBar_1.default) `
  flex-grow: 1;
  margin-left: ${(0, space_1.default)(1.5)};
`;
const StyledLayoutBody = (0, styled_1.default)(Layout.Body) `
  margin-bottom: -20px;
`;
const EmptyStateAction = (0, styled_1.default)('p') `
  font-size: ${p => p.theme.fontSizeLarge};
`;
exports.default = (0, withOrganization_1.default)((0, withTeams_1.default)(IncidentsListContainer));
//# sourceMappingURL=index.jsx.map