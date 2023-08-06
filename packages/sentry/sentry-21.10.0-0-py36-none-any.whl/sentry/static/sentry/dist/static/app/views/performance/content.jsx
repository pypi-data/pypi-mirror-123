Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const tags_1 = require("app/actionCreators/tags");
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const globalSdkUpdateAlert_1 = (0, tslib_1.__importDefault)(require("app/components/globalSdkUpdateAlert"));
const noProjectMessage_1 = (0, tslib_1.__importDefault)(require("app/components/noProjectMessage"));
const globalSelectionHeader_1 = (0, tslib_1.__importDefault)(require("app/components/organizations/globalSelectionHeader"));
const pageHeading_1 = (0, tslib_1.__importDefault)(require("app/components/pageHeading"));
const sentryDocumentTitle_1 = (0, tslib_1.__importDefault)(require("app/components/sentryDocumentTitle"));
const globalSelectionHeader_2 = require("app/constants/globalSelectionHeader");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const organization_1 = require("app/styles/organization");
const analytics_1 = require("app/utils/analytics");
const performanceEventViewContext_1 = require("app/utils/performance/contexts/performanceEventViewContext");
const queryString_1 = require("app/utils/queryString");
const tokenizeSearch_1 = require("app/utils/tokenizeSearch");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withGlobalSelection_1 = (0, tslib_1.__importDefault)(require("app/utils/withGlobalSelection"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
const content_1 = (0, tslib_1.__importDefault)(require("./landing/content"));
const utils_1 = require("./trends/utils");
const data_1 = require("./data");
const landing_1 = require("./landing");
const onboarding_1 = (0, tslib_1.__importDefault)(require("./onboarding"));
const utils_2 = require("./utils");
class PerformanceContent extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            eventView: (0, data_1.generatePerformanceEventView)(this.props.organization, this.props.location, this.props.projects),
            error: undefined,
        };
        this.setError = (error) => {
            this.setState({ error });
        };
        this.handleSearch = (searchQuery) => {
            const { location, organization } = this.props;
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'performance_views.overview.search',
                eventName: 'Performance Views: Transaction overview search',
                organization_id: parseInt(organization.id, 10),
            });
            react_router_1.browserHistory.push({
                pathname: location.pathname,
                query: Object.assign(Object.assign({}, location.query), { cursor: undefined, query: String(searchQuery).trim() || undefined }),
            });
        };
        this.handleTrendsClick = () => {
            const { location, organization } = this.props;
            const newQuery = Object.assign({}, location.query);
            const query = (0, queryString_1.decodeScalar)(location.query.query, '');
            const conditions = new tokenizeSearch_1.MutableSearch(query);
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'performance_views.change_view',
                eventName: 'Performance Views: Change View',
                organization_id: parseInt(organization.id, 10),
                view_name: 'TRENDS',
            });
            const modifiedConditions = new tokenizeSearch_1.MutableSearch([]);
            if (conditions.hasFilter('tpm()')) {
                modifiedConditions.setFilterValues('tpm()', conditions.getFilterValues('tpm()'));
            }
            else {
                modifiedConditions.setFilterValues('tpm()', ['>0.01']);
            }
            if (conditions.hasFilter('transaction.duration')) {
                modifiedConditions.setFilterValues('transaction.duration', conditions.getFilterValues('transaction.duration'));
            }
            else {
                modifiedConditions.setFilterValues('transaction.duration', [
                    '>0',
                    `<${utils_1.DEFAULT_MAX_DURATION}`,
                ]);
            }
            newQuery.query = modifiedConditions.formatString();
            react_router_1.browserHistory.push({
                pathname: (0, utils_2.getPerformanceTrendsUrl)(organization),
                query: Object.assign({}, newQuery),
            });
        };
    }
    static getDerivedStateFromProps(nextProps, prevState) {
        return Object.assign(Object.assign({}, prevState), { eventView: (0, data_1.generatePerformanceEventView)(nextProps.organization, nextProps.location, nextProps.projects) });
    }
    componentDidMount() {
        const { api, organization, selection } = this.props;
        (0, tags_1.loadOrganizationTags)(api, organization.slug, selection);
        (0, utils_2.addRoutePerformanceContext)(selection);
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey: 'performance_views.overview.view',
            eventName: 'Performance Views: Transaction overview view',
            organization_id: parseInt(organization.id, 10),
            show_onboarding: this.shouldShowOnboarding(),
        });
    }
    componentDidUpdate(prevProps) {
        const { api, organization, selection } = this.props;
        if (!(0, isEqual_1.default)(prevProps.selection.projects, selection.projects) ||
            !(0, isEqual_1.default)(prevProps.selection.datetime, selection.datetime)) {
            (0, tags_1.loadOrganizationTags)(api, organization.slug, selection);
            (0, utils_2.addRoutePerformanceContext)(selection);
        }
    }
    renderError() {
        const { error } = this.state;
        if (!error) {
            return null;
        }
        return (<alert_1.default type="error" icon={<icons_1.IconFlag size="md"/>}>
        {error}
      </alert_1.default>);
    }
    shouldShowOnboarding() {
        const { projects, demoMode } = this.props;
        const { eventView } = this.state;
        // XXX used by getsentry to bypass onboarding for the upsell demo state.
        if (demoMode) {
            return false;
        }
        if (projects.length === 0) {
            return false;
        }
        // Current selection is 'my projects' or 'all projects'
        if (eventView.project.length === 0 || eventView.project === [globalSelectionHeader_2.ALL_ACCESS_PROJECTS]) {
            return (projects.filter(p => p.firstTransactionEvent === false).length === projects.length);
        }
        // Any other subset of projects.
        return (projects.filter(p => eventView.project.includes(parseInt(p.id, 10)) &&
            p.firstTransactionEvent === false).length === eventView.project.length);
    }
    renderBody() {
        const { organization, projects, selection } = this.props;
        const eventView = this.state.eventView;
        const showOnboarding = this.shouldShowOnboarding();
        return (<organization_1.PageContent>
        <noProjectMessage_1.default organization={organization}>
          <organization_1.PageHeader>
            <pageHeading_1.default>{(0, locale_1.t)('Performance')}</pageHeading_1.default>
            {!showOnboarding && (<button_1.default priority="primary" data-test-id="landing-header-trends" onClick={this.handleTrendsClick}>
                {(0, locale_1.t)('View Trends')}
              </button_1.default>)}
          </organization_1.PageHeader>
          <globalSdkUpdateAlert_1.default />
          {this.renderError()}
          {showOnboarding ? (<onboarding_1.default organization={organization} project={selection.projects.length > 0
                    ? // If some projects selected, use the first selection
                        projects.find(project => selection.projects[0].toString() === project.id) || projects[0]
                    : // Otherwise, use the first project in the org
                        projects[0]}/>) : (<content_1.default eventView={eventView} projects={projects} organization={organization} setError={this.setError} handleSearch={this.handleSearch}/>)}
        </noProjectMessage_1.default>
      </organization_1.PageContent>);
    }
    renderLandingV3() {
        return (<landing_1.PerformanceLanding eventView={this.state.eventView} setError={this.setError} handleSearch={this.handleSearch} handleTrendsClick={this.handleTrendsClick} shouldShowOnboarding={this.shouldShowOnboarding()} {...this.props}/>);
    }
    render() {
        const { organization } = this.props;
        return (<sentryDocumentTitle_1.default title={(0, locale_1.t)('Performance')} orgSlug={organization.slug}>
        <performanceEventViewContext_1.PerformanceEventViewProvider value={{ eventView: this.state.eventView }}>
          <globalSelectionHeader_1.default defaultSelection={{
                datetime: {
                    start: null,
                    end: null,
                    utc: false,
                    period: data_1.DEFAULT_STATS_PERIOD,
                },
            }}>
            <feature_1.default features={['organizations:performance-landing-widgets']}>
              {({ hasFeature }) => hasFeature ? this.renderLandingV3() : this.renderBody()}
            </feature_1.default>
          </globalSelectionHeader_1.default>
        </performanceEventViewContext_1.PerformanceEventViewProvider>
      </sentryDocumentTitle_1.default>);
    }
}
exports.default = (0, withApi_1.default)((0, withOrganization_1.default)((0, withProjects_1.default)((0, withGlobalSelection_1.default)(PerformanceContent))));
//# sourceMappingURL=content.jsx.map