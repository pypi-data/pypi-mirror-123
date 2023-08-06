Object.defineProperty(exports, "__esModule", { value: true });
exports.processInitQueue = void 0;
const tslib_1 = require("tslib");
const exportGlobals_1 = (0, tslib_1.__importDefault)(require("app/bootstrap/exportGlobals"));
const types_1 = require("app/types");
const renderDom_1 = require("./renderDom");
const renderOnDomReady_1 = require("./renderOnDomReady");
const COMPONENT_MAP = {
    [types_1.SentryInitRenderReactComponent.INDICATORS]: () => Promise.resolve().then(() => (0, tslib_1.__importStar)(require(/* webpackChunkName: "Indicators" */ 'app/components/indicators'))),
    [types_1.SentryInitRenderReactComponent.SYSTEM_ALERTS]: () => Promise.resolve().then(() => (0, tslib_1.__importStar)(require(/* webpackChunkName: "SystemAlerts" */ 'app/views/app/systemAlerts'))),
    [types_1.SentryInitRenderReactComponent.SETUP_WIZARD]: () => Promise.resolve().then(() => (0, tslib_1.__importStar)(require(/* webpackChunkName: "SetupWizard" */ 'app/views/setupWizard'))),
    [types_1.SentryInitRenderReactComponent.U2F_SIGN]: () => Promise.resolve().then(() => (0, tslib_1.__importStar)(require(/* webpackChunkName: "U2fSign" */ 'app/components/u2f/u2fsign'))),
};
function processItem(initConfig) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        /**
         * Allows our auth pages to dynamically attach a client side password
         * strength indicator The password strength component is very
         * heavyweight as it includes the zxcvbn, a relatively byte-heavy
         * password strength estimation library. Load it on demand.
         */
        if (initConfig.name === 'passwordStrength') {
            const { input, element } = initConfig;
            if (!input || !element) {
                return;
            }
            const passwordStrength = yield Promise.resolve().then(() => (0, tslib_1.__importStar)(require(
            /* webpackChunkName: "PasswordStrength" */ 'app/components/passwordStrength')));
            passwordStrength.attachTo({
                input: document.querySelector(input),
                element: document.querySelector(element),
            });
            return;
        }
        /**
         * Allows server rendered templates to render a React component to DOM
         * without exposing the component globally.
         */
        if (initConfig.name === 'renderReact') {
            if (!COMPONENT_MAP.hasOwnProperty(initConfig.component)) {
                return;
            }
            const { default: Component } = yield COMPONENT_MAP[initConfig.component]();
            (0, renderOnDomReady_1.renderOnDomReady)(() => 
            // TODO(ts): Unsure how to type this, complains about u2fsign's required props
            (0, renderDom_1.renderDom)(Component, initConfig.container, initConfig.props));
        }
        /**
         * Callback for when js bundle is loaded. Provide library + component references
         * for downstream consumers to use.
         */
        if (initConfig.name === 'onReady' && typeof initConfig.onReady === 'function') {
            initConfig.onReady(exportGlobals_1.default);
        }
    });
}
/**
 * This allows server templates to push "tasks" to be run after application has initialized.
 * The global `window.__onSentryInit` is used for this.
 *
 * Be careful here as we can not guarantee type safety on `__onSentryInit` as
 * these will be defined in server rendered templates
 */
function processInitQueue() {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        // Currently, this is run *before* anything is queued in
        // `window.__onSentryInit`. We want to provide a migration path for potential
        // custom plugins that rely on `window.SentryApp` so they can start migrating
        // their plugins ASAP, as `SentryApp` will be loaded async and will require
        // callbacks to access it, instead of via `window` global.
        if (typeof window.__onSentryInit !== 'undefined' &&
            !Array.isArray(window.__onSentryInit)) {
            return;
        }
        const queued = window.__onSentryInit;
        // Stub future calls of `window.__onSentryInit.push` so that it is
        // processed immediately (since bundle is loaded at this point and no
        // longer needs to act as a queue)
        //
        window.__onSentryInit = {
            push: processItem,
        };
        if (Array.isArray(queued)) {
            // These are all side-effects, so no need to return a value, but allow consumer to
            // wait for all initialization to finish
            yield Promise.all(queued.map(processItem));
        }
    });
}
exports.processInitQueue = processInitQueue;
//# sourceMappingURL=processInitQueue.jsx.map