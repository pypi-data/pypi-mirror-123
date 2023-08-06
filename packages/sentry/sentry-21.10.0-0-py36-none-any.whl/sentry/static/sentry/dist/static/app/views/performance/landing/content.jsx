Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const dropdownControl_1 = (0, tslib_1.__importStar)(require("app/components/dropdownControl"));
const searchBar_1 = (0, tslib_1.__importDefault)(require("app/components/events/searchBar"));
const featureBadge_1 = (0, tslib_1.__importDefault)(require("app/components/featureBadge"));
const TeamKeyTransactionManager = (0, tslib_1.__importStar)(require("app/components/performance/teamKeyTransactionsManager"));
const constants_1 = require("app/constants");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const fields_1 = require("app/utils/discover/fields");
const isActiveSuperuser_1 = require("app/utils/isActiveSuperuser");
const queryString_1 = require("app/utils/queryString");
const tokenizeSearch_1 = require("app/utils/tokenizeSearch");
const withTeams_1 = (0, tslib_1.__importDefault)(require("app/utils/withTeams"));
const index_1 = (0, tslib_1.__importDefault)(require("../charts/index"));
const data_1 = require("../data");
const table_1 = (0, tslib_1.__importDefault)(require("../table"));
const utils_1 = require("../utils");
const doubleAxisDisplay_1 = (0, tslib_1.__importDefault)(require("./display/doubleAxisDisplay"));
const data_2 = require("./data");
const utils_2 = require("./utils");
const vitalsCards_1 = require("./vitalsCards");
class LandingContent extends react_1.Component {
    constructor() {
        super(...arguments);
        this.handleLandingDisplayChange = (field) => {
            const { location, organization, eventView, projects } = this.props;
            const newQuery = Object.assign({}, location.query);
            delete newQuery[utils_2.LEFT_AXIS_QUERY_KEY];
            delete newQuery[utils_2.RIGHT_AXIS_QUERY_KEY];
            const defaultDisplay = (0, utils_2.getDefaultDisplayFieldForPlatform)(projects, eventView);
            const currentDisplay = (0, queryString_1.decodeScalar)(location.query.landingDisplay);
            // Transaction op can affect the display and show no results if it is explicitly set.
            const query = (0, queryString_1.decodeScalar)(location.query.query, '');
            const searchConditions = new tokenizeSearch_1.MutableSearch(query);
            searchConditions.removeFilter('transaction.op');
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'performance_views.landingv2.display_change',
                eventName: 'Performance Views: Landing v2 Display Change',
                organization_id: parseInt(organization.id, 10),
                change_to_display: field,
                default_display: defaultDisplay,
                current_display: currentDisplay,
                is_default: defaultDisplay === currentDisplay,
            });
            react_router_1.browserHistory.push({
                pathname: location.pathname,
                query: Object.assign(Object.assign({}, newQuery), { query: searchConditions.formatString(), landingDisplay: field }),
            });
        };
        this.renderLandingFrontend = isPageload => {
            const { organization, location, projects, eventView, setError } = this.props;
            const columnTitles = isPageload
                ? data_2.FRONTEND_PAGELOAD_COLUMN_TITLES
                : data_2.FRONTEND_OTHER_COLUMN_TITLES;
            const axisOptions = isPageload
                ? (0, data_1.getFrontendAxisOptions)(organization)
                : (0, data_1.getFrontendOtherAxisOptions)(organization);
            const { leftAxis, rightAxis } = (0, utils_2.getDisplayAxes)(axisOptions, location);
            return (<react_1.Fragment>
        {isPageload && (<vitalsCards_1.FrontendCards eventView={eventView} organization={organization} location={location} projects={projects}/>)}
        <doubleAxisDisplay_1.default eventView={eventView} organization={organization} location={location} axisOptions={axisOptions} leftAxis={leftAxis} rightAxis={rightAxis}/>
        <table_1.default eventView={eventView} projects={projects} organization={organization} location={location} setError={setError} summaryConditions={eventView.getQueryWithAdditionalConditions()} columnTitles={columnTitles}/>
      </react_1.Fragment>);
        };
        this.renderLandingBackend = () => {
            const { organization, location, projects, eventView, setError } = this.props;
            const axisOptions = (0, data_1.getBackendAxisOptions)(organization);
            const { leftAxis, rightAxis } = (0, utils_2.getDisplayAxes)(axisOptions, location);
            const columnTitles = data_2.BACKEND_COLUMN_TITLES;
            return (<react_1.Fragment>
        <vitalsCards_1.BackendCards eventView={eventView} organization={organization} location={location}/>
        <doubleAxisDisplay_1.default eventView={eventView} organization={organization} location={location} axisOptions={axisOptions} leftAxis={leftAxis} rightAxis={rightAxis}/>
        <table_1.default eventView={eventView} projects={projects} organization={organization} location={location} setError={setError} summaryConditions={eventView.getQueryWithAdditionalConditions()} columnTitles={columnTitles}/>
      </react_1.Fragment>);
        };
        this.renderLandingMobile = () => {
            const { organization, location, projects, eventView, setError } = this.props;
            const axisOptions = (0, data_1.getMobileAxisOptions)(organization);
            const { leftAxis, rightAxis } = (0, utils_2.getDisplayAxes)(axisOptions, location);
            // only react native should contain the stall percentage column
            const isReactNative = Boolean(eventView.getFields().find(field => field.includes('measurements.stall_percentage')));
            const columnTitles = isReactNative
                ? data_2.REACT_NATIVE_COLUMN_TITLES
                : data_2.MOBILE_COLUMN_TITLES;
            return (<react_1.Fragment>
        <vitalsCards_1.MobileCards eventView={eventView} organization={organization} location={location} showStallPercentage={isReactNative}/>
        <doubleAxisDisplay_1.default eventView={eventView} organization={organization} location={location} axisOptions={axisOptions} leftAxis={leftAxis} rightAxis={rightAxis}/>
        <table_1.default eventView={eventView} projects={projects} organization={organization} location={location} setError={setError} summaryConditions={eventView.getQueryWithAdditionalConditions()} columnTitles={columnTitles}/>
      </react_1.Fragment>);
        };
        this.renderLandingAll = () => {
            const { organization, location, router, projects, eventView, setError } = this.props;
            return (<react_1.Fragment>
        <index_1.default eventView={eventView} organization={organization} location={location} router={router}/>
        <table_1.default eventView={eventView} projects={projects} organization={organization} location={location} setError={setError} summaryConditions={eventView.getQueryWithAdditionalConditions()}/>
      </react_1.Fragment>);
        };
    }
    getSummaryConditions(query) {
        const parsed = new tokenizeSearch_1.MutableSearch(query);
        parsed.freeText = [];
        return parsed.formatString();
    }
    renderSelectedDisplay(display) {
        switch (display) {
            case utils_2.LandingDisplayField.ALL:
                return this.renderLandingAll();
            case utils_2.LandingDisplayField.FRONTEND_PAGELOAD:
                return this.renderLandingFrontend(true);
            case utils_2.LandingDisplayField.FRONTEND_OTHER:
                return this.renderLandingFrontend(false);
            case utils_2.LandingDisplayField.BACKEND:
                return this.renderLandingBackend();
            case utils_2.LandingDisplayField.MOBILE:
                return this.renderLandingMobile();
            default:
                throw new Error(`Unknown display: ${display}`);
        }
    }
    render() {
        const { organization, location, eventView, projects, teams, handleSearch } = this.props;
        const currentLandingDisplay = (0, utils_2.getCurrentLandingDisplay)(location, projects, eventView);
        const filterString = (0, utils_1.getTransactionSearchQuery)(location, eventView.query);
        const isSuperuser = (0, isActiveSuperuser_1.isActiveSuperuser)();
        const userTeams = teams.filter(({ isMember }) => isMember || isSuperuser);
        return (<react_1.Fragment>
        <SearchContainer>
          <searchBar_1.default searchSource="performance_landing" organization={organization} projectIds={eventView.project} query={filterString} fields={(0, fields_1.generateAggregateFields)(organization, [...eventView.fields, { field: 'tps()' }], ['epm()', 'eps()'])} onSearch={handleSearch} maxQueryLength={constants_1.MAX_QUERY_LENGTH}/>
          <dropdownControl_1.default buttonProps={{ prefix: (0, locale_1.t)('Display') }} label={currentLandingDisplay.label}>
            {utils_2.LANDING_DISPLAYS.filter(({ isShown }) => !isShown || isShown(organization)).map(({ badge, label, field }) => (<dropdownControl_1.DropdownItem key={field} onSelect={this.handleLandingDisplayChange} eventKey={field} data-test-id={field} isActive={field === currentLandingDisplay.field}>
                {label}
                {badge && <featureBadge_1.default type={badge} noTooltip/>}
              </dropdownControl_1.DropdownItem>))}
          </dropdownControl_1.default>
        </SearchContainer>
        <TeamKeyTransactionManager.Provider organization={organization} teams={userTeams} selectedTeams={['myteams']} selectedProjects={eventView.project.map(String)}>
          {this.renderSelectedDisplay(currentLandingDisplay.field)}
        </TeamKeyTransactionManager.Provider>
      </react_1.Fragment>);
    }
}
const SearchContainer = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(2)};
  margin-bottom: ${(0, space_1.default)(2)};

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    grid-template-columns: 1fr min-content;
  }
`;
exports.default = (0, react_router_1.withRouter)((0, withTeams_1.default)(LandingContent));
//# sourceMappingURL=content.jsx.map