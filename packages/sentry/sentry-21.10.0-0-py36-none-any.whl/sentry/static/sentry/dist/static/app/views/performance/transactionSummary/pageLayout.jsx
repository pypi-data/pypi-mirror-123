Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const globalSdkUpdateAlert_1 = (0, tslib_1.__importDefault)(require("app/components/globalSdkUpdateAlert"));
const Layout = (0, tslib_1.__importStar)(require("app/components/layouts/thirds"));
const noProjectMessage_1 = (0, tslib_1.__importDefault)(require("app/components/noProjectMessage"));
const globalSelectionHeader_1 = (0, tslib_1.__importDefault)(require("app/components/organizations/globalSelectionHeader"));
const sentryDocumentTitle_1 = (0, tslib_1.__importDefault)(require("app/components/sentryDocumentTitle"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const organization_1 = require("app/styles/organization");
const utils_1 = require("app/utils");
const performanceEventViewContext_1 = require("app/utils/performance/contexts/performanceEventViewContext");
const queryString_1 = require("app/utils/queryString");
const utils_2 = require("../utils");
const header_1 = (0, tslib_1.__importDefault)(require("./header"));
const tabs_1 = (0, tslib_1.__importDefault)(require("./tabs"));
function PageLayout(props) {
    const { location, organization, projects, tab, getDocumentTitle, generateEventView, childComponent: ChildComponent, features = [], } = props;
    const projectId = (0, queryString_1.decodeScalar)(location.query.project);
    const transactionName = (0, utils_2.getTransactionName)(location);
    if (!(0, utils_1.defined)(projectId) || !(0, utils_1.defined)(transactionName)) {
        // If there is no transaction name, redirect to the Performance landing page
        react_router_1.browserHistory.replace({
            pathname: `/organizations/${organization.slug}/performance/`,
            query: Object.assign({}, location.query),
        });
        return null;
    }
    const project = projects.find(p => p.id === projectId);
    const [error, setError] = (0, react_1.useState)();
    const [incompatibleAlertNotice, setIncompatibleAlertNotice] = (0, react_1.useState)(null);
    const handleIncompatibleQuery = (incompatibleAlertNoticeFn, _errors) => {
        const notice = incompatibleAlertNoticeFn(() => setIncompatibleAlertNotice(null));
        setIncompatibleAlertNotice(notice);
    };
    const [transactionThreshold, setTransactionThreshold] = (0, react_1.useState)();
    const [transactionThresholdMetric, setTransactionThresholdMetric] = (0, react_1.useState)();
    const eventView = generateEventView(location, transactionName);
    return (<sentryDocumentTitle_1.default title={getDocumentTitle(transactionName)} orgSlug={organization.slug} projectSlug={project === null || project === void 0 ? void 0 : project.slug}>
      <feature_1.default features={['performance-view', ...features]} organization={organization} renderDisabled={NoAccess}>
        <performanceEventViewContext_1.PerformanceEventViewProvider value={{ eventView }}>
          <globalSelectionHeader_1.default lockedMessageSubject={(0, locale_1.t)('transaction')} shouldForceProject={(0, utils_1.defined)(project)} forceProject={project} specificProjectSlugs={(0, utils_1.defined)(project) ? [project.slug] : []} disableMultipleProjectSelection showProjectSettingsLink>
            <StyledPageContent>
              <noProjectMessage_1.default organization={organization}>
                <header_1.default eventView={eventView} location={location} organization={organization} projects={projects} projectId={projectId} transactionName={transactionName} currentTab={tab} hasWebVitals={tab === tabs_1.default.WebVitals ? 'yes' : 'maybe'} handleIncompatibleQuery={handleIncompatibleQuery} onChangeThreshold={(threshold, metric) => {
            setTransactionThreshold(threshold);
            setTransactionThresholdMetric(metric);
        }}/>
                <Layout.Body>
                  <StyledSdkUpdatesAlert />
                  {(0, utils_1.defined)(error) && (<StyledAlert type="error" icon={<icons_1.IconFlag size="md"/>}>
                      {error}
                    </StyledAlert>)}
                  {incompatibleAlertNotice && (<Layout.Main fullWidth>{incompatibleAlertNotice}</Layout.Main>)}
                  <ChildComponent location={location} organization={organization} projects={projects} eventView={eventView} transactionName={transactionName} setError={setError} transactionThreshold={transactionThreshold} transactionThresholdMetric={transactionThresholdMetric}/>
                </Layout.Body>
              </noProjectMessage_1.default>
            </StyledPageContent>
          </globalSelectionHeader_1.default>
        </performanceEventViewContext_1.PerformanceEventViewProvider>
      </feature_1.default>
    </sentryDocumentTitle_1.default>);
}
function NoAccess() {
    return <alert_1.default type="warning">{(0, locale_1.t)("You don't have access to this feature")}</alert_1.default>;
}
const StyledPageContent = (0, styled_1.default)(organization_1.PageContent) `
  padding: 0;
`;
const StyledSdkUpdatesAlert = (0, styled_1.default)(globalSdkUpdateAlert_1.default) `
  @media (min-width: ${p => p.theme.breakpoints[1]}) {
    margin-bottom: 0;
  }
`;
StyledSdkUpdatesAlert.defaultProps = {
    Wrapper: p => <Layout.Main fullWidth {...p}/>,
};
const StyledAlert = (0, styled_1.default)(alert_1.default) `
  grid-column: 1/3;
  margin: 0;
`;
exports.default = PageLayout;
//# sourceMappingURL=pageLayout.jsx.map