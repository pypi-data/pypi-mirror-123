Object.defineProperty(exports, "__esModule", { value: true });
exports.PerformanceLanding = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const searchBar_1 = (0, tslib_1.__importDefault)(require("app/components/events/searchBar"));
const featureBadge_1 = (0, tslib_1.__importDefault)(require("app/components/featureBadge"));
const globalSdkUpdateAlert_1 = (0, tslib_1.__importDefault)(require("app/components/globalSdkUpdateAlert"));
const Layout = (0, tslib_1.__importStar)(require("app/components/layouts/thirds"));
const navTabs_1 = (0, tslib_1.__importDefault)(require("app/components/navTabs"));
const pageHeading_1 = (0, tslib_1.__importDefault)(require("app/components/pageHeading"));
const TeamKeyTransactionManager = (0, tslib_1.__importStar)(require("app/components/performance/teamKeyTransactionsManager"));
const constants_1 = require("app/constants");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const fields_1 = require("app/utils/discover/fields");
const isActiveSuperuser_1 = require("app/utils/isActiveSuperuser");
const operationBreakdownFilter_1 = require("app/utils/performance/contexts/operationBreakdownFilter");
const withTeams_1 = (0, tslib_1.__importDefault)(require("app/utils/withTeams"));
const filter_1 = (0, tslib_1.__importStar)(require("../transactionSummary/filter"));
const utils_1 = require("../utils");
const allTransactionsView_1 = require("./views/allTransactionsView");
const backendView_1 = require("./views/backendView");
const frontendOtherView_1 = require("./views/frontendOtherView");
const frontendPageloadView_1 = require("./views/frontendPageloadView");
const mobileView_1 = require("./views/mobileView");
const utils_2 = require("./utils");
const fieldToViewMap = {
    [utils_2.LandingDisplayField.ALL]: allTransactionsView_1.AllTransactionsView,
    [utils_2.LandingDisplayField.BACKEND]: backendView_1.BackendView,
    [utils_2.LandingDisplayField.FRONTEND_OTHER]: frontendOtherView_1.FrontendOtherView,
    [utils_2.LandingDisplayField.FRONTEND_PAGELOAD]: frontendPageloadView_1.FrontendPageloadView,
    [utils_2.LandingDisplayField.MOBILE]: mobileView_1.MobileView,
};
function _PerformanceLanding(props) {
    const { organization, location, eventView, projects, teams, handleSearch, handleTrendsClick, shouldShowOnboarding, } = props;
    const currentLandingDisplay = (0, utils_2.getCurrentLandingDisplay)(location, projects, eventView);
    const filterString = (0, utils_1.getTransactionSearchQuery)(location, eventView.query);
    const isSuperuser = (0, isActiveSuperuser_1.isActiveSuperuser)();
    const userTeams = teams.filter(({ isMember }) => isMember || isSuperuser);
    const [spanFilter, setSpanFilter] = (0, react_1.useState)(filter_1.SpanOperationBreakdownFilter.None);
    const showOnboarding = shouldShowOnboarding;
    const shownLandingDisplays = utils_2.LANDING_DISPLAYS.filter(({ isShown }) => !isShown || isShown(organization));
    const ViewComponent = fieldToViewMap[currentLandingDisplay.field];
    return (<div data-test-id="performance-landing-v3">
      <Layout.Header>
        <Layout.HeaderContent>
          <StyledHeading>{(0, locale_1.t)('Performance')}</StyledHeading>
        </Layout.HeaderContent>
        <Layout.HeaderActions>
          {!showOnboarding && (<button_1.default priority="primary" data-test-id="landing-header-trends" onClick={() => handleTrendsClick()}>
              {(0, locale_1.t)('View Trends')}
            </button_1.default>)}
        </Layout.HeaderActions>

        <StyledNavTabs>
          {shownLandingDisplays.map(({ badge, label, field }) => (<li key={label} className={currentLandingDisplay.field === field ? 'active' : ''}>
              <a href="#" onClick={() => (0, utils_2.handleLandingDisplayChange)(field, location)}>
                {(0, locale_1.t)(label)}
                {badge && <featureBadge_1.default type={badge}/>}
              </a>
            </li>))}
        </StyledNavTabs>
      </Layout.Header>
      <Layout.Body>
        <Layout.Main fullWidth>
          <globalSdkUpdateAlert_1.default />
          <operationBreakdownFilter_1.OpBreakdownFilterProvider>
            <SearchContainerWithFilter>
              <filter_1.default organization={organization} currentFilter={spanFilter} onChangeFilter={setSpanFilter}/>
              <searchBar_1.default searchSource="performance_landing" organization={organization} projectIds={eventView.project} query={filterString} fields={(0, fields_1.generateAggregateFields)(organization, [...eventView.fields, { field: 'tps()' }], ['epm()', 'eps()'])} onSearch={handleSearch} maxQueryLength={constants_1.MAX_QUERY_LENGTH}/>
            </SearchContainerWithFilter>
            <TeamKeyTransactionManager.Provider organization={organization} teams={userTeams} selectedTeams={['myteams']} selectedProjects={eventView.project.map(String)}>
              <ViewComponent {...props}/>
            </TeamKeyTransactionManager.Provider>
          </operationBreakdownFilter_1.OpBreakdownFilterProvider>
        </Layout.Main>
      </Layout.Body>
    </div>);
}
exports.PerformanceLanding = (0, withTeams_1.default)(_PerformanceLanding);
const StyledHeading = (0, styled_1.default)(pageHeading_1.default) `
  line-height: 40px;
`;
const StyledNavTabs = (0, styled_1.default)(navTabs_1.default) `
  margin-bottom: 0;
  /* Makes sure the tabs are pushed into another row */
  width: 100%;
`;
const SearchContainerWithFilter = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(0)};
  margin-bottom: ${(0, space_1.default)(2)};

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    grid-template-columns: min-content 1fr;
  }
`;
//# sourceMappingURL=index.jsx.map