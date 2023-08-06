Object.defineProperty(exports, "__esModule", { value: true });
exports.initializeApp = void 0;
const tslib_1 = require("tslib");
require("./legacyTwitterBootstrap");
require("./exportGlobals");
const routes_1 = (0, tslib_1.__importDefault)(require("app/routes"));
const analytics_1 = require("app/utils/analytics");
const commonInitialization_1 = require("./commonInitialization");
const initializeSdk_1 = require("./initializeSdk");
const processInitQueue_1 = require("./processInitQueue");
const renderMain_1 = require("./renderMain");
const renderOnDomReady_1 = require("./renderOnDomReady");
function initializeApp(config) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        (0, commonInitialization_1.commonInitialization)(config);
        (0, initializeSdk_1.initializeSdk)(config, { routes: routes_1.default });
        // Used for operational metrics to determine that the application js
        // bundle was loaded by browser.
        analytics_1.metric.mark({ name: 'sentry-app-init' });
        (0, renderOnDomReady_1.renderOnDomReady)(renderMain_1.renderMain);
        (0, processInitQueue_1.processInitQueue)();
    });
}
exports.initializeApp = initializeApp;
//# sourceMappingURL=initializeApp.jsx.map