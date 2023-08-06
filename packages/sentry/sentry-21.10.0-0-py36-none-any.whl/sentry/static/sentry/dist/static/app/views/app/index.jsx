Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_hotkeys_hook_1 = require("react-hotkeys-hook");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const deployPreview_1 = require("app/actionCreators/deployPreview");
const guides_1 = require("app/actionCreators/guides");
const modal_1 = require("app/actionCreators/modal");
const alertActions_1 = (0, tslib_1.__importDefault)(require("app/actions/alertActions"));
const api_1 = require("app/api");
const errorBoundary_1 = (0, tslib_1.__importDefault)(require("app/components/errorBoundary"));
const globalModal_1 = (0, tslib_1.__importDefault)(require("app/components/globalModal"));
const hookOrDefault_1 = (0, tslib_1.__importDefault)(require("app/components/hookOrDefault"));
const indicators_1 = (0, tslib_1.__importDefault)(require("app/components/indicators"));
const constants_1 = require("app/constants");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const hookStore_1 = (0, tslib_1.__importDefault)(require("app/stores/hookStore"));
const organizationsStore_1 = (0, tslib_1.__importDefault)(require("app/stores/organizationsStore"));
const organizationStore_1 = (0, tslib_1.__importDefault)(require("app/stores/organizationStore"));
const useLegacyStore_1 = require("app/stores/useLegacyStore");
const useApi_1 = (0, tslib_1.__importDefault)(require("app/utils/useApi"));
const systemAlerts_1 = (0, tslib_1.__importDefault)(require("./systemAlerts"));
const GlobalNotifications = (0, hookOrDefault_1.default)({
    hookName: 'component:global-notifications',
    defaultComponent: () => null,
});
const InstallWizard = (0, react_1.lazy)(() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/admin/installWizard'))));
const NewsletterConsent = (0, react_1.lazy)(() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/newsletterConsent'))));
/**
 * App is the root level container for all uathenticated routes.
 */
function App({ children }) {
    var _a, _b, _c;
    const api = (0, useApi_1.default)();
    const config = (0, useLegacyStore_1.useLegacyStore)(configStore_1.default);
    const { organization } = (0, useLegacyStore_1.useLegacyStore)(organizationStore_1.default);
    // Command palette global-shortcut
    (0, react_hotkeys_hook_1.useHotkeys)('command+shift+p, command+k, ctrl+shift+p, ctrl+k', e => {
        (0, modal_1.openCommandPalette)();
        e.preventDefault();
    });
    // Theme toggle global shortcut
    (0, react_hotkeys_hook_1.useHotkeys)('command+shift+l, ctrl+shift+l', e => {
        configStore_1.default.set('theme', config.theme === 'light' ? 'dark' : 'light');
        e.preventDefault();
    }, [config.theme]);
    /**
     * Loads the users organization list into the OrganizationsStore
     */
    function loadOrganizations() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            try {
                const data = yield api.requestPromise('/organizations/', { query: { member: '1' } });
                organizationsStore_1.default.load(data);
            }
            catch (_a) {
                // TODO: do something?
            }
        });
    }
    /**
     * Creates Alerts for any internal health problems
     */
    function checkInternalHealth() {
        var _a, _b;
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            let data = null;
            try {
                data = yield api.requestPromise('/internal/health/');
            }
            catch (_c) {
                // TODO: do something?
            }
            (_b = (_a = data === null || data === void 0 ? void 0 : data.problems) === null || _a === void 0 ? void 0 : _a.forEach) === null || _b === void 0 ? void 0 : _b.call(_a, problem => {
                const { id, message, url } = problem;
                const type = problem.severity === 'critical' ? 'error' : 'warning';
                alertActions_1.default.addAlert({ id, message, type, url });
            });
        });
    }
    (0, react_1.useEffect)(() => {
        loadOrganizations();
        checkInternalHealth();
        // Show system-level alerts
        config.messages.forEach(msg => alertActions_1.default.addAlert({ message: msg.message, type: msg.level, neverExpire: true }));
        // The app is running in deploy preview mode
        if (constants_1.DEPLOY_PREVIEW_CONFIG) {
            (0, deployPreview_1.displayDeployPreviewAlert)();
        }
        // The app is running in local SPA mode
        if (!constants_1.DEPLOY_PREVIEW_CONFIG && constants_1.EXPERIMENTAL_SPA) {
            (0, deployPreview_1.displayExperimentalSpaAlert)();
        }
        // Set the user for analytics
        if (config.user) {
            hookStore_1.default.get('analytics:init-user').map(cb => cb(config.user));
        }
        (0, api_1.initApiClientErrorHandling)();
        (0, guides_1.fetchGuides)();
        // When the app is unloaded clear the organizationst list
        return () => organizationsStore_1.default.load([]);
    }, []);
    function clearUpgrade() {
        configStore_1.default.set('needsUpgrade', false);
    }
    function clearNewsletterConsent() {
        const flags = Object.assign(Object.assign({}, config.user.flags), { newsletter_consent_prompt: false });
        configStore_1.default.set('user', Object.assign(Object.assign({}, config.user), { flags }));
    }
    const needsUpgrade = ((_a = config.user) === null || _a === void 0 ? void 0 : _a.isSuperuser) && config.needsUpgrade;
    const newsletterConsentPrompt = (_c = (_b = config.user) === null || _b === void 0 ? void 0 : _b.flags) === null || _c === void 0 ? void 0 : _c.newsletter_consent_prompt;
    function renderBody() {
        if (needsUpgrade) {
            return (<react_1.Suspense fallback={null}>
          <InstallWizard onConfigured={clearUpgrade}/>;
        </react_1.Suspense>);
        }
        if (newsletterConsentPrompt) {
            return (<react_1.Suspense fallback={null}>
          <NewsletterConsent onSubmitSuccess={clearNewsletterConsent}/>
        </react_1.Suspense>);
        }
        return children;
    }
    // Used to restore focus to the container after closing the modal
    const mainContainerRef = (0, react_1.useRef)(null);
    return (<MainContainer tabIndex={-1} ref={mainContainerRef}>
      <globalModal_1.default onClose={() => { var _a, _b; return (_b = (_a = mainContainerRef.current) === null || _a === void 0 ? void 0 : _a.focus) === null || _b === void 0 ? void 0 : _b.call(_a); }}/>
      <systemAlerts_1.default className="messages-container"/>
      <GlobalNotifications className="notifications-container messages-container" organization={organization !== null && organization !== void 0 ? organization : undefined}/>
      <indicators_1.default className="indicators-container"/>
      <errorBoundary_1.default>{renderBody()}</errorBoundary_1.default>
    </MainContainer>);
}
exports.default = App;
const MainContainer = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  outline: none;
  padding-top: ${p => (configStore_1.default.get('demoMode') ? p.theme.demo.headerSize : 0)};
`;
//# sourceMappingURL=index.jsx.map