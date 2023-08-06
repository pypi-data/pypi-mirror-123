Object.defineProperty(exports, "__esModule", { value: true });
exports.initializePipelineView = void 0;
const analytics_1 = require("app/utils/analytics");
const commonInitialization_1 = require("./commonInitialization");
const initializeSdk_1 = require("./initializeSdk");
const renderOnDomReady_1 = require("./renderOnDomReady");
const renderPipelineView_1 = require("./renderPipelineView");
function initializePipelineView(config) {
    (0, commonInitialization_1.commonInitialization)(config);
    /**
     * XXX: Note we do not include routingInstrumentation because importing
     * `app/routes` significantly increases bundle size.
     *
     * A potential solution would be to use dynamic imports here to import
     * `app/routes` to pass to `initializeSdk()`
     */
    (0, initializeSdk_1.initializeSdk)(config);
    // Used for operational metrics to determine that the application js
    // bundle was loaded by browser.
    analytics_1.metric.mark({ name: 'sentry-pipeline-init' });
    (0, renderOnDomReady_1.renderOnDomReady)(renderPipelineView_1.renderPipelineView);
}
exports.initializePipelineView = initializePipelineView;
//# sourceMappingURL=initializePipelineView.jsx.map