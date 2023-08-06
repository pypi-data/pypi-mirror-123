Object.defineProperty(exports, "__esModule", { value: true });
exports.initializeSdk = void 0;
const tslib_1 = require("tslib");
const react_router_1 = require("react-router");
const integrations_1 = require("@sentry/integrations");
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const rrweb_1 = (0, tslib_1.__importDefault)(require("@sentry/rrweb"));
const tracing_1 = require("@sentry/tracing");
const utils_1 = require("@sentry/utils");
const constants_1 = require("app/constants");
const apiSentryClient_1 = require("app/utils/apiSentryClient");
/**
 * We accept a routes argument here because importing `app/routes`
 * is expensive in regards to bundle size. Some entrypoints may opt to forgo
 * having routing instrumentation in order to have a smaller bundle size.
 * (e.g.  `app/views/integrationPipeline`)
 */
function getSentryIntegrations(hasReplays = false, routes) {
    const integrations = [
        new integrations_1.ExtraErrorData({
            // 6 is arbitrary, seems like a nice number
            depth: 6,
        }),
        new tracing_1.Integrations.BrowserTracing(Object.assign(Object.assign({}, (typeof routes === 'function'
            ? {
                routingInstrumentation: Sentry.reactRouterV3Instrumentation(react_router_1.browserHistory, (0, react_router_1.createRoutes)(routes()), react_router_1.match),
            }
            : {})), { idleTimeout: 5000, _metricOptions: {
                _reportAllChanges: true,
            } })),
    ];
    if (hasReplays) {
        // eslint-disable-next-line no-console
        console.log('[sentry] Instrumenting session with rrweb');
        // TODO(ts): The type returned by SentryRRWeb seems to be somewhat
        // incompatible. It's a newer plugin, so this can be expected, but we
        // should fix.
        integrations.push(new rrweb_1.default({
            checkoutEveryNms: 60 * 1000, // 60 seconds
        }));
    }
    return integrations;
}
/**
 * Initialize the Sentry SDK
 *
 * If `routes` is passed, we will instrument react-router. Not all
 * entrypoints require this.
 */
function initializeSdk(config, { routes } = {}) {
    if (config.dsn_requests) {
        (0, apiSentryClient_1.init)(config.dsn_requests);
    }
    const { apmSampling, sentryConfig, userIdentity } = config;
    const tracesSampleRate = apmSampling !== null && apmSampling !== void 0 ? apmSampling : 0;
    const hasReplays = (userIdentity === null || userIdentity === void 0 ? void 0 : userIdentity.isStaff) && !constants_1.DISABLE_RR_WEB;
    Sentry.init(Object.assign(Object.assign({}, sentryConfig), { 
        /**
         * For SPA mode, we need a way to overwrite the default DSN from backend
         * as well as `whitelistUrls`
         */
        dsn: constants_1.SPA_DSN || (sentryConfig === null || sentryConfig === void 0 ? void 0 : sentryConfig.dsn), 
        /**
         * Frontend can be built with a `SENTRY_RELEASE_VERSION` environment variable for release string, useful if frontend is
         * deployed separately from backend.
         */
        release: constants_1.SENTRY_RELEASE_VERSION !== null && constants_1.SENTRY_RELEASE_VERSION !== void 0 ? constants_1.SENTRY_RELEASE_VERSION : sentryConfig === null || sentryConfig === void 0 ? void 0 : sentryConfig.release, whitelistUrls: constants_1.SPA_DSN
            ? ['localhost', 'dev.getsentry.net', 'sentry.dev', 'webpack-internal://']
            : sentryConfig === null || sentryConfig === void 0 ? void 0 : sentryConfig.whitelistUrls, integrations: getSentryIntegrations(hasReplays, routes), tracesSampleRate, 
        /**
         * There is a bug in Safari, that causes `AbortError` when fetch is aborted, and you are in the middle of reading the response.
         * In Chrome and other browsers, it is handled gracefully, where in Safari, it produces additional error, that is jumping
         * outside of the original Promise chain and bubbles up to the `unhandledRejection` handler, that we then captures as error.
         * Ref: https://bugs.webkit.org/show_bug.cgi?id=215771
         */
        ignoreErrors: ['AbortError: Fetch is aborted'] }));
    // Track timeOrigin Selection by the SDK to see if it improves transaction durations
    Sentry.addGlobalEventProcessor((event, _hint) => {
        event.tags = event.tags || {};
        event.tags['timeOrigin.mode'] = utils_1._browserPerformanceTimeOriginMode;
        return event;
    });
    if (userIdentity) {
        Sentry.setUser(userIdentity);
    }
    if (window.__SENTRY__VERSION) {
        Sentry.setTag('sentry_version', window.__SENTRY__VERSION);
    }
    Sentry.setTag('rrweb.active', hasReplays ? 'yes' : 'no');
}
exports.initializeSdk = initializeSdk;
//# sourceMappingURL=initializeSdk.jsx.map