Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const memoize_1 = (0, tslib_1.__importDefault)(require("lodash/memoize"));
const lazyLoad_1 = (0, tslib_1.__importDefault)(require("app/components/lazyLoad"));
const constants_1 = require("app/constants");
const locale_1 = require("app/locale");
const hookStore_1 = (0, tslib_1.__importDefault)(require("app/stores/hookStore"));
const errorHandler_1 = (0, tslib_1.__importDefault)(require("app/utils/errorHandler"));
const app_1 = (0, tslib_1.__importDefault)(require("app/views/app"));
const layout_1 = (0, tslib_1.__importDefault)(require("app/views/auth/layout"));
const container_1 = (0, tslib_1.__importDefault)(require("app/views/issueList/container"));
const overview_1 = (0, tslib_1.__importDefault)(require("app/views/issueList/overview"));
const organizationContext_1 = (0, tslib_1.__importDefault)(require("app/views/organizationContext"));
const organizationDetails_1 = (0, tslib_1.__importDefault)(require("app/views/organizationDetails"));
const types_1 = require("app/views/organizationGroupDetails/types");
const organizationRoot_1 = (0, tslib_1.__importDefault)(require("app/views/organizationRoot"));
const projectEventRedirect_1 = (0, tslib_1.__importDefault)(require("app/views/projectEventRedirect"));
const redirectDeprecatedProjectRoute_1 = (0, tslib_1.__importDefault)(require("app/views/projects/redirectDeprecatedProjectRoute"));
const routeNotFound_1 = (0, tslib_1.__importDefault)(require("app/views/routeNotFound"));
const settingsWrapper_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsWrapper"));
/**
 * We add some additional props to our routes
 */
const Route = react_router_1.Route;
const IndexRoute = react_router_1.IndexRoute;
/**
 * Use react-router to lazy load a route. Use this for codesplitting containers
 * (e.g. SettingsLayout)
 *
 * The typical method for lazy loading a route leaf node is using the
 * <LazyLoad> component + `componentPromise`
 *
 * For wrapper / layout views react-router handles the route tree better by
 * using getComponent with this lazyLoad helper. If we just use <LazyLoad> it
 * will end up having to re-render more components than necessary.
 */
const lazyLoad = (load) => (_loc, cb) => load().then(module => cb(null, module.default));
const hook = (name) => hookStore_1.default.get(name).map(cb => cb());
const SafeLazyLoad = (0, errorHandler_1.default)(lazyLoad_1.default);
function buildRoutes() {
    // Read this to understand where to add new routes, how / why the routing
    // tree is structured the way it is, and how the lazy-loading /
    // code-splitting works for pages.
    //
    // ## Formatting
    //
    // NOTE that there are intentionally NO blank lines within route tree blocks.
    // This helps make it easier to navigate within the file by using your
    // editors shortcuts to jump between 'paragraphs' of code.
    //
    // [!!] Do NOT add blank lines within route blocks to preserve this behavior!
    //
    //
    // ## Lazy loading
    //
    // * The `SafeLazyLoad` component
    //
    //   Most routes are rendered as LazyLoad components (SafeLazyLoad is the
    //   errorHandler wrapped version). This means the rendered component for the
    //   route will only be loaded when the route is loaded. This helps us
    //   "code-split" the app.
    //
    // * The `lazyLoad` function
    //
    //   This function is to be used with `getComponent`. It is used for
    //   container component routes for performances reasons. See the
    //   documentation on the function for more details.
    //
    //
    // ## Hooks
    //
    // There are a number of `hook()` routes placed within the routing tree to
    // allow for additional routes to be augmented into the application via the
    // hookStore mechanism.
    //
    //
    // ## The structure
    //
    // * `experimentalSpaRoutes`
    //
    //   These routes are specifically for the experimental single-page-app mode,
    //   where Sentry is run separate from Django. These are NOT part of the root
    //   <App /> component.
    //
    //   Right now these are mainly used for authentication pages. In the future
    //   they would be used for other pages like registration.
    //
    // * `rootRoutes`
    //
    //   These routes live directly under the <App /> container, and generally
    //   are not specific to an organization.
    //
    // * `settingsRoutes`
    //
    //   This is the route tree for all of `/settings/`. This route tree is
    //   composed of a few different sub-trees.
    //
    //   - `accountSettingsRoutes`    User specific settings
    //   - `orgSettingsRoutes`        Specific to a organization
    //   - `projectSettingsRoutes`    Specific to a project
    //   - `legacySettingsRedirects`  Routes that used to exist in settings
    //
    // * `organizationRoutes`
    //
    //   This is where a majority of the app routes live. This is wrapped with
    //   the <OrganizationDetails /> component, which provides the sidebar and
    //   organization context.
    //
    //   Within these routes are a variety of subroutes. They are not all
    //   listed here as the subroutes will be added and removed, and most are
    //   self explanatory.
    //
    // * `legacyRedirectRoutes`
    //
    //   This route tree contains <Redirect /> routes for many old legacy paths.
    //
    //   You may also find <Redirect />'s collocated next to the feature routes
    //   they have redirects for. A good rule here is to place 'helper' redirects
    //   next to the routes they redirect to, and place 'legacy route' redirects
    //   for routes that have completely changed in this tree.
    const experimentalSpaRoutes = constants_1.EXPERIMENTAL_SPA ? (<Route path="/auth/login/" component={(0, errorHandler_1.default)(layout_1.default)}>
      <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/auth/login')))} component={SafeLazyLoad}/>
    </Route>) : null;
    const rootRoutes = (<react_1.Fragment>
      <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/app/root')))} component={SafeLazyLoad}/>
      <Route path="/accept/:memberId/:token/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/acceptOrganizationInvite')))} component={SafeLazyLoad}/>
      <Route path="/accept-transfer/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/acceptProjectTransfer')))} component={SafeLazyLoad}/>
      <Route path="/extensions/external-install/:integrationSlug/:installationId" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/integrationOrganizationLink')))} component={SafeLazyLoad}/>
      <Route path="/extensions/:integrationSlug/link/" getComponent={lazyLoad(() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/integrationOrganizationLink'))))}/>
      <Route path="/sentry-apps/:sentryAppSlug/external-install/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/sentryAppExternalInstallation')))} component={SafeLazyLoad}/>
      <react_router_1.Redirect from="/account/" to="/settings/account/details/"/>
      <react_router_1.Redirect from="/share/group/:shareId/" to="/share/issue/:shareId/"/>
      <Route path="/share/issue/:shareId/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/sharedGroupDetails')))} component={SafeLazyLoad}/>
      <Route path="/organizations/new/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationCreate')))} component={SafeLazyLoad}/>
      <Route path="/organizations/:orgId/data-export/:dataExportId" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/dataExport/dataDownload')))} component={SafeLazyLoad}/>
      <Route path="/organizations/:orgId/disabled-member/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/disabledMember')))} component={SafeLazyLoad}/>
      <Route path="/join-request/:orgId/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationJoinRequest')))} component={SafeLazyLoad}/>
      <Route path="/onboarding/:orgId/" component={(0, errorHandler_1.default)(organizationContext_1.default)}>
        <react_router_1.IndexRedirect to="welcome/"/>
        <Route path=":step/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/onboarding/onboarding')))} component={SafeLazyLoad}/>
      </Route>
    </react_1.Fragment>);
    const accountSettingsRoutes = (<Route path="account/" name={(0, locale_1.t)('Account')} getComponent={lazyLoad(() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/account/accountSettingsLayout'))))}>
      <react_router_1.IndexRedirect to="details/"/>
      <Route path="details/" name={(0, locale_1.t)('Details')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/account/accountDetails')))} component={SafeLazyLoad}/>
      <Route path="notifications/" name={(0, locale_1.t)('Notifications')}>
        <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/account/notifications/notificationSettings')))} component={SafeLazyLoad}/>
        <Route path=":fineTuneType/" name={(0, locale_1.t)('Fine Tune Alerts')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/account/accountNotificationFineTuning')))} component={SafeLazyLoad}/>
      </Route>
      <Route path="emails/" name={(0, locale_1.t)('Emails')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/account/accountEmails')))} component={SafeLazyLoad}/>
      <Route path="authorizations/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/account/accountAuthorizations')))} component={SafeLazyLoad}/>
      <Route name={(0, locale_1.t)('Security')} path="security/">
        <Route componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/account/accountSecurity/accountSecurityWrapper')))} component={SafeLazyLoad}>
          <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/account/accountSecurity')))} component={SafeLazyLoad}/>
          <Route path="session-history/" name={(0, locale_1.t)('Session History')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/account/accountSecurity/sessionHistory')))} component={SafeLazyLoad}/>
          <Route path="mfa/:authId/" name={(0, locale_1.t)('Details')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/account/accountSecurity/accountSecurityDetails')))} component={SafeLazyLoad}/>
        </Route>
        <Route path="mfa/:authId/enroll/" name={(0, locale_1.t)('Enroll')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/account/accountSecurity/accountSecurityEnroll')))} component={SafeLazyLoad}/>
      </Route>
      <Route path="subscriptions/" name={(0, locale_1.t)('Subscriptions')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/account/accountSubscriptions')))} component={SafeLazyLoad}/>
      <Route path="identities/" name={(0, locale_1.t)('Identities')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/account/accountIdentities')))} component={SafeLazyLoad}/>
      <Route path="api/" name={(0, locale_1.t)('API')}>
        <react_router_1.IndexRedirect to="auth-tokens/"/>
        <Route path="auth-tokens/" name={(0, locale_1.t)('Auth Tokens')}>
          <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/account/apiTokens')))} component={SafeLazyLoad}/>
          <Route path="new-token/" name={(0, locale_1.t)('Create New Token')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/account/apiNewToken')))} component={SafeLazyLoad}/>
        </Route>
        <Route path="applications/" name={(0, locale_1.t)('Applications')}>
          <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/account/apiApplications')))} component={SafeLazyLoad}/>
          <Route path=":appId/" name={(0, locale_1.t)('Details')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/account/apiApplications/details')))} component={SafeLazyLoad}/>
        </Route>
        {hook('routes:api')}
      </Route>
      <Route path="close-account/" name={(0, locale_1.t)('Close Account')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/account/accountClose')))} component={SafeLazyLoad}/>
    </Route>);
    const projectSettingsRoutes = (<Route name={(0, locale_1.t)('Project')} path="projects/:projectId/" getComponent={lazyLoad(() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/project/projectSettingsLayout'))))}>
      <IndexRoute name={(0, locale_1.t)('General')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/projectGeneralSettings')))} component={SafeLazyLoad}/>
      <Route path="teams/" name={(0, locale_1.t)('Teams')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/project/projectTeams')))} component={SafeLazyLoad}/>
      <Route name={(0, locale_1.t)('Alerts')} path="alerts/" component={SafeLazyLoad} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/projectAlerts')))}>
        <IndexRoute component={SafeLazyLoad} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/projectAlerts/settings')))}/>
        <react_router_1.Redirect from="new/" to="/organizations/:orgId/alerts/:projectId/new/"/>
        <react_router_1.Redirect from="rules/" to="/organizations/:orgId/alerts/rules/"/>
        <react_router_1.Redirect from="rules/new/" to="/organizations/:orgId/alerts/:projectId/new/"/>
        <react_router_1.Redirect from="metric-rules/new/" to="/organizations/:orgId/alerts/:projectId/new/"/>
        <react_router_1.Redirect from="rules/:ruleId/" to="/organizations/:orgId/alerts/rules/:projectId/:ruleId/"/>
        <react_router_1.Redirect from="metric-rules/:ruleId/" to="/organizations/:orgId/alerts/metric-rules/:projectId/:ruleId/"/>
      </Route>
      <Route name={(0, locale_1.t)('Environments')} path="environments/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/project/projectEnvironments')))} component={SafeLazyLoad}>
        <IndexRoute />
        <Route path="hidden/"/>
      </Route>
      <Route name={(0, locale_1.t)('Tags')} path="tags/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/projectTags')))} component={SafeLazyLoad}/>
      <react_router_1.Redirect from="issue-tracking/" to="/settings/:orgId/:projectId/plugins/"/>
      <Route path="release-tracking/" name={(0, locale_1.t)('Release Tracking')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/project/projectReleaseTracking')))} component={SafeLazyLoad}/>
      <Route path="ownership/" name={(0, locale_1.t)('Issue Owners')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/project/projectOwnership')))} component={SafeLazyLoad}/>
      <Route path="data-forwarding/" name={(0, locale_1.t)('Data Forwarding')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/projectDataForwarding')))} component={SafeLazyLoad}/>
      <Route name={(0, locale_1.t)('Security & Privacy')} path="security-and-privacy/" component={SafeLazyLoad} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/projectSecurityAndPrivacy')))}/>
      <Route path="debug-symbols/" name={(0, locale_1.t)('Debug Information Files')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/projectDebugFiles')))} component={SafeLazyLoad}/>
      <Route path="proguard/" name={(0, locale_1.t)('ProGuard Mappings')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/projectProguard')))} component={SafeLazyLoad}/>
      <Route path="performance/" name={(0, locale_1.t)('Performance')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/projectPerformance')))} component={SafeLazyLoad}/>
      <Route path="source-maps/" name={(0, locale_1.t)('Source Maps')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/projectSourceMaps')))} component={SafeLazyLoad}>
        <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/projectSourceMaps/list')))} component={SafeLazyLoad}/>
        <Route path=":name/" name={(0, locale_1.t)('Archive')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/projectSourceMaps/detail')))} component={SafeLazyLoad}/>
      </Route>
      <Route path="processing-issues/" name={(0, locale_1.t)('Processing Issues')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/project/projectProcessingIssues')))} component={SafeLazyLoad}/>
      <Route path="filters/" name={(0, locale_1.t)('Inbound Filters')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/project/projectFilters')))} component={SafeLazyLoad}>
        <react_router_1.IndexRedirect to="data-filters/"/>
        <Route path=":filterType/"/>
      </Route>
      <Route name={(0, locale_1.t)('Filters & Sampling')} path="filters-and-sampling/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/project/filtersAndSampling')))} component={SafeLazyLoad}/>
      <Route path="issue-grouping/" name={(0, locale_1.t)('Issue Grouping')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/projectIssueGrouping')))} component={SafeLazyLoad}/>
      <Route path="hooks/" name={(0, locale_1.t)('Service Hooks')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/project/projectServiceHooks')))} component={SafeLazyLoad}/>
      <Route path="hooks/new/" name={(0, locale_1.t)('Create Service Hook')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/project/projectCreateServiceHook')))} component={SafeLazyLoad}/>
      <Route path="hooks/:hookId/" name={(0, locale_1.t)('Service Hook Details')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/project/projectServiceHookDetails')))} component={SafeLazyLoad}/>
      <Route path="keys/" name={(0, locale_1.t)('Client Keys')}>
        <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/project/projectKeys/list')))} component={SafeLazyLoad}/>
        <Route path=":keyId/" name={(0, locale_1.t)('Details')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/project/projectKeys/details')))} component={SafeLazyLoad}/>
      </Route>
      <Route path="user-feedback/" name={(0, locale_1.t)('User Feedback')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/project/projectUserFeedback')))} component={SafeLazyLoad}/>
      <react_router_1.Redirect from="csp/" to="security-headers/"/>
      <Route path="security-headers/" name={(0, locale_1.t)('Security Headers')}>
        <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/projectSecurityHeaders')))} component={SafeLazyLoad}/>
        <Route path="csp/" name={(0, locale_1.t)('Content Security Policy')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/projectSecurityHeaders/csp')))} component={SafeLazyLoad}/>
        <Route path="expect-ct/" name={(0, locale_1.t)('Certificate Transparency')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/projectSecurityHeaders/expectCt')))} component={SafeLazyLoad}/>
        <Route path="hpkp/" name={(0, locale_1.t)('HPKP')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/projectSecurityHeaders/hpkp')))} component={SafeLazyLoad}/>
      </Route>
      <Route path="plugins/" name={(0, locale_1.t)('Legacy Integrations')}>
        <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/projectPlugins')))} component={SafeLazyLoad}/>
        <Route path=":pluginId/" name={(0, locale_1.t)('Integration Details')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/projectPlugins/details')))} component={SafeLazyLoad}/>
      </Route>
      <Route path="install/" name={(0, locale_1.t)('Configuration')}>
        <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/projectInstall/overview')))} component={SafeLazyLoad}/>
        <Route path=":platform/" name={(0, locale_1.t)('Docs')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/projectInstall/platformOrIntegration')))} component={SafeLazyLoad}/>
      </Route>
    </Route>);
    const orgSettingsRoutes = (<Route getComponent={lazyLoad(() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organization/organizationSettingsLayout'))))}>
      {hook('routes:organization')}
      <IndexRoute name={(0, locale_1.t)('General')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationGeneralSettings')))} component={SafeLazyLoad}/>
      <Route path="projects/" name={(0, locale_1.t)('Projects')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationProjects')))} component={SafeLazyLoad}/>
      <Route path="api-keys/" name={(0, locale_1.t)('API Key')}>
        <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationApiKeys')))} component={SafeLazyLoad}/>
        <Route path=":apiKey/" name={(0, locale_1.t)('Details')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationApiKeys/organizationApiKeyDetails')))} component={SafeLazyLoad}/>
      </Route>
      <Route path="audit-log/" name={(0, locale_1.t)('Audit Log')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationAuditLog')))} component={SafeLazyLoad}/>
      <Route path="auth/" name={(0, locale_1.t)('Auth Providers')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationAuth')))} component={SafeLazyLoad}/>
      <react_router_1.Redirect from="members/requests" to="members/"/>
      <Route path="members/" name={(0, locale_1.t)('Members')}>
        <Route componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationMembers/organizationMembersWrapper')))} component={SafeLazyLoad}>
          <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationMembers/organizationMembersList')))} component={SafeLazyLoad}/>
        </Route>
        <Route path=":memberId/" name={(0, locale_1.t)('Details')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationMembers/organizationMemberDetail')))} component={SafeLazyLoad}/>
      </Route>
      <Route path="rate-limits/" name={(0, locale_1.t)('Rate Limits')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationRateLimits')))} component={SafeLazyLoad}/>
      <Route name={(0, locale_1.t)('Relay')} path="relay/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationRelay')))} component={SafeLazyLoad}/>
      <Route path="repos/" name={(0, locale_1.t)('Repositories')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationRepositories')))} component={SafeLazyLoad}/>
      <Route path="performance/" name={(0, locale_1.t)('Performance')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationPerformance')))} component={SafeLazyLoad}/>
      <Route path="settings/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationGeneralSettings')))} component={SafeLazyLoad}/>
      <Route name={(0, locale_1.t)('Security & Privacy')} path="security-and-privacy/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationSecurityAndPrivacy')))} component={SafeLazyLoad}/>
      <Route name={(0, locale_1.t)('Teams')} path="teams/">
        <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationTeams')))} component={SafeLazyLoad}/>
        <Route name={(0, locale_1.t)('Team')} path=":teamId/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationTeams/teamDetails')))} component={SafeLazyLoad}>
          <react_router_1.IndexRedirect to="members/"/>
          <Route path="members/" name={(0, locale_1.t)('Members')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationTeams/teamMembers')))} component={SafeLazyLoad}/>
          <Route path="notifications/" name={(0, locale_1.t)('Notifications')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationTeams/teamNotifications')))} component={SafeLazyLoad}/>
          <Route path="projects/" name={(0, locale_1.t)('Projects')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationTeams/teamProjects')))} component={SafeLazyLoad}/>
          <Route path="settings/" name={(0, locale_1.t)('Settings')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationTeams/teamSettings')))} component={SafeLazyLoad}/>
        </Route>
      </Route>
      <react_router_1.Redirect from="plugins/" to="integrations/"/>
      <Route name={(0, locale_1.t)('Integrations')} path="plugins/">
        <Route name={(0, locale_1.t)('Integration Details')} path=":integrationSlug/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationIntegrations/pluginDetailedView')))} component={SafeLazyLoad}/>
      </Route>
      <react_router_1.Redirect from="sentry-apps/" to="integrations/"/>
      <Route name={(0, locale_1.t)('Integrations')} path="sentry-apps/">
        <Route name={(0, locale_1.t)('Details')} path=":integrationSlug" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationIntegrations/sentryAppDetailedView')))} component={SafeLazyLoad}/>
      </Route>
      <react_router_1.Redirect from="document-integrations/" to="integrations/"/>
      <Route name={(0, locale_1.t)('Integrations')} path="document-integrations/">
        <Route name={(0, locale_1.t)('Details')} path=":integrationSlug" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationIntegrations/docIntegrationDetailedView')))} component={SafeLazyLoad}/>
      </Route>
      <Route name={(0, locale_1.t)('Integrations')} path="integrations/">
        <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationIntegrations/integrationListDirectory')))} component={SafeLazyLoad}/>
        <Route name={(0, locale_1.t)('Integration Details')} path=":integrationSlug" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationIntegrations/integrationDetailedView')))} component={SafeLazyLoad}/>
        <Route name={(0, locale_1.t)('Configure Integration')} path=":providerKey/:integrationId/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationIntegrations/configureIntegration')))} component={SafeLazyLoad}/>
      </Route>
      <Route name={(0, locale_1.t)('Developer Settings')} path="developer-settings/">
        <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationDeveloperSettings')))} component={SafeLazyLoad}/>
        <Route name={(0, locale_1.t)('New Public Integration')} path="new-public/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationDeveloperSettings/sentryApplicationDetails')))} component={SafeLazyLoad}/>
        <Route name={(0, locale_1.t)('New Internal Integration')} path="new-internal/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationDeveloperSettings/sentryApplicationDetails')))} component={SafeLazyLoad}/>
        <Route name={(0, locale_1.t)('Edit Integration')} path=":appSlug/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationDeveloperSettings/sentryApplicationDetails')))} component={SafeLazyLoad}/>
        <Route name={(0, locale_1.t)('Integration Dashboard')} path=":appSlug/dashboard/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationDeveloperSettings/sentryApplicationDashboard')))} component={SafeLazyLoad}/>
      </Route>
    </Route>);
    const legacySettingsRedirects = (<react_1.Fragment>
      <react_router_1.Redirect from=":projectId/" to="projects/:projectId/"/>
      <react_router_1.Redirect from=":projectId/alerts/" to="projects/:projectId/alerts/"/>
      <react_router_1.Redirect from=":projectId/alerts/rules/" to="projects/:projectId/alerts/rules/"/>
      <react_router_1.Redirect from=":projectId/alerts/rules/:ruleId/" to="projects/:projectId/alerts/rules/:ruleId/"/>
    </react_1.Fragment>);
    const settingsRoutes = (<Route path="/settings/" name={(0, locale_1.t)('Settings')} component={settingsWrapper_1.default}>
      <IndexRoute getComponent={lazyLoad(() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/settingsIndex'))))}/>
      {accountSettingsRoutes}
      <Route name={(0, locale_1.t)('Organization')} path=":orgId/">
        {orgSettingsRoutes}
        {projectSettingsRoutes}
        {legacySettingsRedirects}
      </Route>
    </Route>);
    const projectsRoutes = (<Route path="/organizations/:orgId/projects/">
      <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/projectsDashboard')))} component={SafeLazyLoad}/>
      <Route path="new/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/projectInstall/newProject')))} component={SafeLazyLoad}/>
      <Route path=":projectId/getting-started/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/projectInstall/gettingStarted')))} component={SafeLazyLoad}>
        <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/projectInstall/overview')))} component={SafeLazyLoad}/>
        <Route path=":platform/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/projectInstall/platformOrIntegration')))} component={SafeLazyLoad}/>
      </Route>
      <Route path=":projectId/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/projectDetail')))} component={SafeLazyLoad}/>
      <Route path=":projectId/events/:eventId/" component={(0, errorHandler_1.default)(projectEventRedirect_1.default)}/>
    </Route>);
    const teamInsightsRoutes = (<Route path="/organizations/:orgId/teamInsights/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/teamInsights')))} component={SafeLazyLoad}>
      <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/teamInsights/overview')))} component={SafeLazyLoad}/>
    </Route>);
    const dashboardRoutes = (<react_1.Fragment>
      <Route path="/organizations/:orgId/dashboards/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/dashboardsV2')))} component={SafeLazyLoad}>
        <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/dashboardsV2/manage')))} component={SafeLazyLoad}/>
      </Route>
      <Route path="/organizations/:orgId/dashboards/new/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/dashboardsV2/create')))} component={SafeLazyLoad}>
        <Route path="widget/:widgetId/edit/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/dashboardsV2/widget')))} component={SafeLazyLoad}/>
        <Route path="widget/new/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/dashboardsV2/widget')))} component={SafeLazyLoad}/>
      </Route>
      <react_router_1.Redirect from="/organizations/:orgId/dashboards/:dashboardId/" to="/organizations/:orgId/dashboard/:dashboardId/"/>
      <Route path="/organizations/:orgId/dashboard/:dashboardId/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/dashboardsV2/view')))} component={SafeLazyLoad}>
        <Route path="widget/:widgetId/edit/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/dashboardsV2/widget')))} component={SafeLazyLoad}/>
        <Route path="widget/new/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/dashboardsV2/widget')))} component={SafeLazyLoad}/>
      </Route>
    </react_1.Fragment>);
    const alertRoutes = (<Route path="/organizations/:orgId/alerts/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/alerts')))} component={SafeLazyLoad}>
      <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/alerts/list')))} component={SafeLazyLoad}/>
      <Route path="rules/details/:ruleId/" name={(0, locale_1.t)('Alert Rule Details')} component={SafeLazyLoad} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/alerts/rules/details')))}/>
      <Route path="rules/">
        <IndexRoute component={SafeLazyLoad} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/alerts/rules')))}/>
        <Route path=":projectId/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/alerts/builder/projectProvider')))} component={SafeLazyLoad}>
          <react_router_1.IndexRedirect to="/organizations/:orgId/alerts/rules/"/>
          <Route path=":ruleId/" name={(0, locale_1.t)('Edit Alert Rule')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/alerts/edit')))} component={SafeLazyLoad}/>
        </Route>
      </Route>
      <Route path="metric-rules/">
        <react_router_1.IndexRedirect to="/organizations/:orgId/alerts/rules/"/>
        <Route path=":projectId/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/alerts/builder/projectProvider')))} component={SafeLazyLoad}>
          <react_router_1.IndexRedirect to="/organizations/:orgId/alerts/rules/"/>
          <Route path=":ruleId/" name={(0, locale_1.t)('Edit Alert Rule')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/alerts/edit')))} component={SafeLazyLoad}/>
        </Route>
      </Route>
      <Route path="rules/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/alerts/rules')))} component={SafeLazyLoad}/>
      <Route path=":alertId/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/alerts/details')))} component={SafeLazyLoad}/>
      <Route path=":projectId/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/alerts/builder/projectProvider')))} component={SafeLazyLoad}>
        <Route path="new/" name={(0, locale_1.t)('New Alert Rule')} component={SafeLazyLoad} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/alerts/create')))}/>
        <Route path="wizard/" name={(0, locale_1.t)('Alert Creation Wizard')} component={SafeLazyLoad} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/alerts/wizard')))}/>
      </Route>
    </Route>);
    const monitorsRoutes = (<Route path="/organizations/:orgId/monitors/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/monitors')))} component={SafeLazyLoad}>
      <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/monitors/monitors')))} component={SafeLazyLoad}/>
      <Route path="/organizations/:orgId/monitors/create/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/monitors/create')))} component={SafeLazyLoad}/>
      <Route path="/organizations/:orgId/monitors/:monitorId/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/monitors/details')))} component={SafeLazyLoad}/>
      <Route path="/organizations/:orgId/monitors/:monitorId/edit/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/monitors/edit')))} component={SafeLazyLoad}/>
    </Route>);
    const releasesRoutes = (<Route path="/organizations/:orgId/releases/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/releases')))} component={SafeLazyLoad}>
      <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/releases/list')))} component={SafeLazyLoad}/>
      <Route path=":release/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/releases/detail')))} component={SafeLazyLoad}>
        <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/releases/detail/overview')))} component={SafeLazyLoad}/>
        <Route path="commits/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/releases/detail/commits')))} component={SafeLazyLoad}/>
        <Route path="files-changed/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/releases/detail/filesChanged')))} component={SafeLazyLoad}/>
        <react_router_1.Redirect from="new-events/" to="/organizations/:orgId/releases/:release/"/>
        <react_router_1.Redirect from="all-events/" to="/organizations/:orgId/releases/:release/"/>
      </Route>
    </Route>);
    const activityRoutes = (<Route path="/organizations/:orgId/activity/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationActivity')))} component={SafeLazyLoad}/>);
    const statsRoutes = (<Route path="/organizations/:orgId/stats/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationStats')))} component={SafeLazyLoad}/>);
    // TODO(mark) Long term this /queries route should go away and /discover
    // should be the canonical route for discover2. We have a redirect right now
    // as /discover was for discover 1 and most of the application is linking to
    // /discover/queries and not /discover
    const discoverRoutes = (<Route path="/organizations/:orgId/discover/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/eventsV2')))} component={SafeLazyLoad}>
      <react_router_1.IndexRedirect to="queries/"/>
      <Route path="queries/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/eventsV2/landing')))} component={SafeLazyLoad}/>
      <Route path="results/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/eventsV2/results')))} component={SafeLazyLoad}/>
      <Route path=":eventSlug/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/eventsV2/eventDetails')))} component={SafeLazyLoad}/>
    </Route>);
    const performanceRoutes = (<Route path="/organizations/:orgId/performance/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/performance')))} component={SafeLazyLoad}>
      <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/performance/content')))} component={SafeLazyLoad}/>
      <Route path="trends/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/performance/trends')))} component={SafeLazyLoad}/>
      <Route path="/organizations/:orgId/performance/summary/">
        <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/performance/transactionSummary/transactionOverview')))} component={SafeLazyLoad}/>
        <Route path="vitals/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/performance/transactionSummary/transactionVitals')))} component={SafeLazyLoad}/>
        <Route path="tags/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/performance/transactionSummary/transactionTags')))} component={SafeLazyLoad}/>
        <Route path="events/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/performance/transactionSummary/transactionEvents')))} component={SafeLazyLoad}/>
        <Route path="spans/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/performance/transactionSummary/transactionSpans')))} component={SafeLazyLoad}/>
      </Route>
      <Route path="vitaldetail/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/performance/vitalDetail')))} component={SafeLazyLoad}/>
      <Route path="trace/:traceSlug/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/performance/traceDetails')))} component={SafeLazyLoad}/>
      <Route path=":eventSlug/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/performance/transactionDetails')))} component={SafeLazyLoad}/>
      <Route path="compare/:baselineEventSlug/:regressionEventSlug/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/performance/compare')))} component={SafeLazyLoad}/>
    </Route>);
    const userFeedbackRoutes = (<Route path="/organizations/:orgId/user-feedback/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/userFeedback')))} component={SafeLazyLoad}/>);
    const issueListRoutes = (<Route path="/organizations/:orgId/issues/" component={(0, errorHandler_1.default)(container_1.default)}>
      <react_router_1.Redirect from="/organizations/:orgId/" to="/organizations/:orgId/issues/"/>
      <IndexRoute component={(0, errorHandler_1.default)(overview_1.default)}/>
      <Route path="searches/:searchId/" component={(0, errorHandler_1.default)(overview_1.default)}/>
      <Route path="sessionPercent" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/issueList/testSessionPercent')))} component={SafeLazyLoad}/>
    </Route>);
    // Once org issues is complete, these routes can be nested under
    // /organizations/:orgId/issues
    const groupDetailsRoutes = (<Route path="/organizations/:orgId/issues/:groupId/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails')))} component={SafeLazyLoad}>
      <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails/groupEventDetails')))} component={SafeLazyLoad} props={{
            currentTab: types_1.Tab.DETAILS,
            isEventRoute: false,
        }}/>
      <Route path="activity/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails/groupActivity')))} component={SafeLazyLoad} props={{
            currentTab: types_1.Tab.ACTIVITY,
            isEventRoute: false,
        }}/>
      <Route path="events/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails/groupEvents')))} component={SafeLazyLoad} props={{
            currentTab: types_1.Tab.EVENTS,
            isEventRoute: false,
        }}/>
      <Route path="tags/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails/groupTags')))} component={SafeLazyLoad} props={{
            currentTab: types_1.Tab.TAGS,
            isEventRoute: false,
        }}/>
      <Route path="tags/:tagKey/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails/groupTagValues')))} component={SafeLazyLoad} props={{
            currentTab: types_1.Tab.TAGS,
            isEventRoute: false,
        }}/>
      <Route path="feedback/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails/groupUserFeedback')))} component={SafeLazyLoad} props={{
            currentTab: types_1.Tab.USER_FEEDBACK,
            isEventRoute: false,
        }}/>
      <Route path="attachments/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails/groupEventAttachments')))} component={SafeLazyLoad} props={{
            currentTab: types_1.Tab.ATTACHMENTS,
            isEventRoute: false,
        }}/>
      <Route path="similar/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails/groupSimilarIssues')))} component={SafeLazyLoad} props={{
            currentTab: types_1.Tab.SIMILAR_ISSUES,
            isEventRoute: false,
        }}/>
      <Route path="merged/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails/groupMerged')))} component={SafeLazyLoad} props={{
            currentTab: types_1.Tab.MERGED,
            isEventRoute: false,
        }}/>
      <Route path="grouping/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails/grouping')))} component={SafeLazyLoad} props={{
            currentTab: types_1.Tab.GROUPING,
            isEventRoute: false,
        }}/>
      <Route path="events/:eventId/">
        <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails/groupEventDetails')))} component={SafeLazyLoad} props={{
            currentTab: types_1.Tab.DETAILS,
            isEventRoute: true,
        }}/>
        <Route path="activity/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails/groupActivity')))} component={SafeLazyLoad} props={{
            currentTab: types_1.Tab.ACTIVITY,
            isEventRoute: true,
        }}/>
        <Route path="events/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails/groupEvents')))} component={SafeLazyLoad} props={{
            currentTab: types_1.Tab.EVENTS,
            isEventRoute: true,
        }}/>
        <Route path="similar/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails/groupSimilarIssues')))} component={SafeLazyLoad} props={{
            currentTab: types_1.Tab.SIMILAR_ISSUES,
            isEventRoute: true,
        }}/>
        <Route path="tags/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails/groupTags')))} component={SafeLazyLoad} props={{
            currentTab: types_1.Tab.TAGS,
            isEventRoute: true,
        }}/>
        <Route path="tags/:tagKey/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails/groupTagValues')))} component={SafeLazyLoad} props={{
            currentTab: types_1.Tab.TAGS,
            isEventRoute: true,
        }}/>
        <Route path="feedback/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails/groupUserFeedback')))} component={SafeLazyLoad} props={{
            currentTab: types_1.Tab.USER_FEEDBACK,
            isEventRoute: true,
        }}/>
        <Route path="attachments/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails/groupEventAttachments')))} component={SafeLazyLoad} props={{
            currentTab: types_1.Tab.ATTACHMENTS,
            isEventRoute: true,
        }}/>
        <Route path="merged/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails/groupMerged')))} component={SafeLazyLoad} props={{
            currentTab: types_1.Tab.MERGED,
            isEventRoute: true,
        }}/>
        <Route path="grouping/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails/grouping')))} component={SafeLazyLoad} props={{
            currentTab: types_1.Tab.GROUPING,
            isEventRoute: true,
        }}/>
      </Route>
    </Route>);
    // These are the "manage" pages. For sentry.io, these are _different_ from
    // the SaaS admin routes in getsentry.
    const adminManageRoutes = (<Route name={(0, locale_1.t)('Admin')} path="/manage/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/admin/adminLayout')))} component={SafeLazyLoad}>
      <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/admin/adminOverview')))} component={SafeLazyLoad}/>
      <Route name={(0, locale_1.t)('Buffer')} path="buffer/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/admin/adminBuffer')))} component={SafeLazyLoad}/>
      <Route name={(0, locale_1.t)('Relays')} path="relays/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/admin/adminRelays')))} component={SafeLazyLoad}/>
      <Route name={(0, locale_1.t)('Organizations')} path="organizations/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/admin/adminOrganizations')))} component={SafeLazyLoad}/>
      <Route name={(0, locale_1.t)('Projects')} path="projects/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/admin/adminProjects')))} component={SafeLazyLoad}/>
      <Route name={(0, locale_1.t)('Queue')} path="queue/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/admin/adminQueue')))} component={SafeLazyLoad}/>
      <Route name={(0, locale_1.t)('Quotas')} path="quotas/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/admin/adminQuotas')))} component={SafeLazyLoad}/>
      <Route name={(0, locale_1.t)('Settings')} path="settings/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/admin/adminSettings')))} component={SafeLazyLoad}/>
      <Route name={(0, locale_1.t)('Users')} path="users/">
        <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/admin/adminUsers')))} component={SafeLazyLoad}/>
        <Route path=":id" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/admin/adminUserEdit')))} component={SafeLazyLoad}/>
      </Route>
      <Route name={(0, locale_1.t)('Mail')} path="status/mail/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/admin/adminMail')))} component={SafeLazyLoad}/>
      <Route name={(0, locale_1.t)('Environment')} path="status/environment/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/admin/adminEnvironment')))} component={SafeLazyLoad}/>
      <Route name={(0, locale_1.t)('Packages')} path="status/packages/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/admin/adminPackages')))} component={SafeLazyLoad}/>
      <Route name={(0, locale_1.t)('Warnings')} path="status/warnings/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/admin/adminWarnings')))} component={SafeLazyLoad}/>
      {hook('routes:admin')}
    </Route>);
    // XXX(epurkhiser): This should probably go away. It's not totally clear to
    // me why we need the OrganizationRoot root container.
    const legacyOrganizationRootRoutes = (<Route component={(0, errorHandler_1.default)(organizationRoot_1.default)}>
      <Route path="/organizations/:orgId/teams/new/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/teamCreate')))} component={SafeLazyLoad}/>
      <Route path="/organizations/:orgId/">
        {hook('routes:organization')}
        <react_router_1.Redirect from="/organizations/:orgId/teams/" to="/settings/:orgId/teams/"/>
        <react_router_1.Redirect from="/organizations/:orgId/teams/your-teams/" to="/settings/:orgId/teams/"/>
        <react_router_1.Redirect from="/organizations/:orgId/teams/all-teams/" to="/settings/:orgId/teams/"/>
        <react_router_1.Redirect from="/organizations/:orgId/teams/:teamId/" to="/settings/:orgId/teams/:teamId/"/>
        <react_router_1.Redirect from="/organizations/:orgId/teams/:teamId/members/" to="/settings/:orgId/teams/:teamId/members/"/>
        <react_router_1.Redirect from="/organizations/:orgId/teams/:teamId/projects/" to="/settings/:orgId/teams/:teamId/projects/"/>
        <react_router_1.Redirect from="/organizations/:orgId/teams/:teamId/settings/" to="/settings/:orgId/teams/:teamId/settings/"/>
        <react_router_1.Redirect from="/organizations/:orgId/settings/" to="/settings/:orgId/"/>
        <react_router_1.Redirect from="/organizations/:orgId/api-keys/" to="/settings/:orgId/api-keys/"/>
        <react_router_1.Redirect from="/organizations/:orgId/api-keys/:apiKey/" to="/settings/:orgId/api-keys/:apiKey/"/>
        <react_router_1.Redirect from="/organizations/:orgId/members/" to="/settings/:orgId/members/"/>
        <react_router_1.Redirect from="/organizations/:orgId/members/:memberId/" to="/settings/:orgId/members/:memberId/"/>
        <react_router_1.Redirect from="/organizations/:orgId/rate-limits/" to="/settings/:orgId/rate-limits/"/>
        <react_router_1.Redirect from="/organizations/:orgId/repos/" to="/settings/:orgId/repos/"/>
      </Route>
    </Route>);
    // XXX(epurkhiser): These also exist in the legacyOrganizationRootRoutes. Not
    // sure which one here is more correct.
    const legacyGettingStartedRoutes = (<Route path="/:orgId/:projectId/getting-started/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/projectInstall/gettingStarted')))} component={SafeLazyLoad}>
      <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/projectInstall/overview')))} component={SafeLazyLoad}/>
      <Route path=":platform/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/projectInstall/platformOrIntegration')))} component={SafeLazyLoad}/>
    </Route>);
    // Support for deprecated URLs (pre-Sentry 10). We just redirect users to new
    // canonical URLs.
    //
    // XXX(epurkhiser): Can these be moved over to the legacyOrgRedirects routes,
    // or do these need to be nested into the OrganizationDetails tree?
    const legacyOrgRedirects = (<Route name={(0, locale_1.t)('Organization')} path="/:orgId/:projectId/">
      <IndexRoute component={(0, errorHandler_1.default)((0, redirectDeprecatedProjectRoute_1.default)(({ orgId, projectId }) => `/organizations/${orgId}/issues/?project=${projectId}`))}/>
      <Route path="issues/" component={(0, errorHandler_1.default)((0, redirectDeprecatedProjectRoute_1.default)(({ orgId, projectId }) => `/organizations/${orgId}/issues/?project=${projectId}`))}/>
      <Route path="dashboard/" component={(0, errorHandler_1.default)((0, redirectDeprecatedProjectRoute_1.default)(({ orgId, projectId }) => `/organizations/${orgId}/dashboards/?project=${projectId}`))}/>
      <Route path="user-feedback/" component={(0, errorHandler_1.default)((0, redirectDeprecatedProjectRoute_1.default)(({ orgId, projectId }) => `/organizations/${orgId}/user-feedback/?project=${projectId}`))}/>
      <Route path="releases/" component={(0, errorHandler_1.default)((0, redirectDeprecatedProjectRoute_1.default)(({ orgId, projectId }) => `/organizations/${orgId}/releases/?project=${projectId}`))}/>
      <Route path="releases/:version/" component={(0, errorHandler_1.default)((0, redirectDeprecatedProjectRoute_1.default)(({ orgId, projectId, router }) => `/organizations/${orgId}/releases/${router.params.version}/?project=${projectId}`))}/>
      <Route path="releases/:version/new-events/" component={(0, errorHandler_1.default)((0, redirectDeprecatedProjectRoute_1.default)(({ orgId, projectId, router }) => `/organizations/${orgId}/releases/${router.params.version}/new-events/?project=${projectId}`))}/>
      <Route path="releases/:version/all-events/" component={(0, errorHandler_1.default)((0, redirectDeprecatedProjectRoute_1.default)(({ orgId, projectId, router }) => `/organizations/${orgId}/releases/${router.params.version}/all-events/?project=${projectId}`))}/>
      <Route path="releases/:version/commits/" component={(0, errorHandler_1.default)((0, redirectDeprecatedProjectRoute_1.default)(({ orgId, projectId, router }) => `/organizations/${orgId}/releases/${router.params.version}/commits/?project=${projectId}`))}/>
    </Route>);
    const organizationRoutes = (<Route component={(0, errorHandler_1.default)(organizationDetails_1.default)}>
      {settingsRoutes}
      {projectsRoutes}
      {teamInsightsRoutes}
      {dashboardRoutes}
      {userFeedbackRoutes}
      {issueListRoutes}
      {groupDetailsRoutes}
      {alertRoutes}
      {monitorsRoutes}
      {releasesRoutes}
      {activityRoutes}
      {statsRoutes}
      {discoverRoutes}
      {performanceRoutes}
      {adminManageRoutes}
      {legacyOrganizationRootRoutes}
      {legacyGettingStartedRoutes}
      {legacyOrgRedirects}
    </Route>);
    const legacyRedirectRoutes = (<Route path="/:orgId/">
      <react_router_1.IndexRedirect to="/organizations/:orgId/"/>
      <Route path=":projectId/settings/">
        <react_router_1.Redirect from="teams/" to="/settings/:orgId/projects/:projectId/teams/"/>
        <react_router_1.Redirect from="alerts/" to="/settings/:orgId/projects/:projectId/alerts/"/>
        <react_router_1.Redirect from="alerts/rules/" to="/settings/:orgId/projects/:projectId/alerts/rules/"/>
        <react_router_1.Redirect from="alerts/rules/new/" to="/settings/:orgId/projects/:projectId/alerts/rules/new/"/>
        <react_router_1.Redirect from="alerts/rules/:ruleId/" to="/settings/:orgId/projects/:projectId/alerts/rules/:ruleId/"/>
        <react_router_1.Redirect from="environments/" to="/settings/:orgId/projects/:projectId/environments/"/>
        <react_router_1.Redirect from="environments/hidden/" to="/settings/:orgId/projects/:projectId/environments/hidden/"/>
        <react_router_1.Redirect from="tags/" to="/settings/projects/:orgId/projects/:projectId/tags/"/>
        <react_router_1.Redirect from="issue-tracking/" to="/settings/:orgId/projects/:projectId/issue-tracking/"/>
        <react_router_1.Redirect from="release-tracking/" to="/settings/:orgId/projects/:projectId/release-tracking/"/>
        <react_router_1.Redirect from="ownership/" to="/settings/:orgId/projects/:projectId/ownership/"/>
        <react_router_1.Redirect from="data-forwarding/" to="/settings/:orgId/projects/:projectId/data-forwarding/"/>
        <react_router_1.Redirect from="debug-symbols/" to="/settings/:orgId/projects/:projectId/debug-symbols/"/>
        <react_router_1.Redirect from="processing-issues/" to="/settings/:orgId/projects/:projectId/processing-issues/"/>
        <react_router_1.Redirect from="filters/" to="/settings/:orgId/projects/:projectId/filters/"/>
        <react_router_1.Redirect from="hooks/" to="/settings/:orgId/projects/:projectId/hooks/"/>
        <react_router_1.Redirect from="keys/" to="/settings/:orgId/projects/:projectId/keys/"/>
        <react_router_1.Redirect from="keys/:keyId/" to="/settings/:orgId/projects/:projectId/keys/:keyId/"/>
        <react_router_1.Redirect from="user-feedback/" to="/settings/:orgId/projects/:projectId/user-feedback/"/>
        <react_router_1.Redirect from="security-headers/" to="/settings/:orgId/projects/:projectId/security-headers/"/>
        <react_router_1.Redirect from="security-headers/csp/" to="/settings/:orgId/projects/:projectId/security-headers/csp/"/>
        <react_router_1.Redirect from="security-headers/expect-ct/" to="/settings/:orgId/projects/:projectId/security-headers/expect-ct/"/>
        <react_router_1.Redirect from="security-headers/hpkp/" to="/settings/:orgId/projects/:projectId/security-headers/hpkp/"/>
        <react_router_1.Redirect from="plugins/" to="/settings/:orgId/projects/:projectId/plugins/"/>
        <react_router_1.Redirect from="plugins/:pluginId/" to="/settings/:orgId/projects/:projectId/plugins/:pluginId/"/>
        <react_router_1.Redirect from="integrations/:providerKey/" to="/settings/:orgId/projects/:projectId/integrations/:providerKey/"/>
        <react_router_1.Redirect from="install/" to="/settings/:orgId/projects/:projectId/install/"/>
        <react_router_1.Redirect from="install/:platform'" to="/settings/:orgId/projects/:projectId/install/:platform/"/>
      </Route>
      <react_router_1.Redirect from=":projectId/group/:groupId/" to="issues/:groupId/"/>
      <react_router_1.Redirect from=":projectId/issues/:groupId/" to="/organizations/:orgId/issues/:groupId/"/>
      <react_router_1.Redirect from=":projectId/issues/:groupId/events/" to="/organizations/:orgId/issues/:groupId/events/"/>
      <react_router_1.Redirect from=":projectId/issues/:groupId/events/:eventId/" to="/organizations/:orgId/issues/:groupId/events/:eventId/"/>
      <react_router_1.Redirect from=":projectId/issues/:groupId/tags/" to="/organizations/:orgId/issues/:groupId/tags/"/>
      <react_router_1.Redirect from=":projectId/issues/:groupId/tags/:tagKey/" to="/organizations/:orgId/issues/:groupId/tags/:tagKey/"/>
      <react_router_1.Redirect from=":projectId/issues/:groupId/feedback/" to="/organizations/:orgId/issues/:groupId/feedback/"/>
      <react_router_1.Redirect from=":projectId/issues/:groupId/similar/" to="/organizations/:orgId/issues/:groupId/similar/"/>
      <react_router_1.Redirect from=":projectId/issues/:groupId/merged/" to="/organizations/:orgId/issues/:groupId/merged/"/>
      <Route path=":projectId/events/:eventId/" component={(0, errorHandler_1.default)(projectEventRedirect_1.default)}/>
    </Route>);
    const appRoutes = (<Route>
      {experimentalSpaRoutes}
      <Route path="/" component={(0, errorHandler_1.default)(app_1.default)}>
        {rootRoutes}
        {organizationRoutes}
        {legacyRedirectRoutes}
        {hook('routes')}
        <Route path="*" component={(0, errorHandler_1.default)(routeNotFound_1.default)}/>
      </Route>
    </Route>);
    return appRoutes;
}
// We load routes both when initlaizing the SDK (for routing integrations) and
// when the app renders Main. Memoize to avoid rebuilding the route tree.
const routes = (0, memoize_1.default)(buildRoutes);
exports.default = routes;
//# sourceMappingURL=routes.jsx.map