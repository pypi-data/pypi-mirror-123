Object.defineProperty(exports, "__esModule", { value: true });
exports.metric = exports.analytics = exports.trackDeprecated = exports.logExperiment = exports.trackAdhocEvent = exports.trackAnalyticsEvent = exports.trackAnalyticsEventV2 = void 0;
const tslib_1 = require("tslib");
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const hookStore_1 = (0, tslib_1.__importDefault)(require("app/stores/hookStore"));
/**
 * Analytics and metric tracking functionality.
 *
 * These are primarily driven through hooks provided through the hookstore. For
 * sentry.io these are currently mapped to our in-house analytics backend
 * 'Reload' and the Amplitude service.
 *
 * NOTE: sentry.io contributors, you will need to ensure that the eventKey
 *       passed exists as an event key in the Reload events.py configuration:
 *
 *       https://github.com/getsentry/reload/blob/master/reload_app/events.py
 *
 * NOTE: sentry.io contributors, if you are using `gauge` or `increment` the
 *       name must be added to the Reload metrics module:
 *
 *       https://github.com/getsentry/reload/blob/master/reload_app/metrics/__init__.py
 */
/**
 * This should be with all analytics events regardless of the analytics destination
 * which includes Reload, Amplitude, and Google Analytics.
 * All events go to Reload. If eventName is defined, events also go to Amplitude.
 * For more details, refer to the API defined in hooks.
 *
 * Shold NOT be used directly.
 * Instead, use makeAnalyticsFunction to generate an analytics function.
 */
const trackAnalyticsEventV2 = (data, options) => hookStore_1.default.get('analytics:track-event-v2').forEach(cb => cb(data, options));
exports.trackAnalyticsEventV2 = trackAnalyticsEventV2;
/**
 * @deprecated Use a method generated from makeAnalyticsFunction
 */
const trackAnalyticsEvent = options => hookStore_1.default.get('analytics:track-event').forEach(cb => cb(options));
exports.trackAnalyticsEvent = trackAnalyticsEvent;
/**
 * @deprecated Use a method generated from makeAnalyticsFunction
 */
const trackAdhocEvent = options => hookStore_1.default.get('analytics:track-adhoc-event').forEach(cb => cb(options));
exports.trackAdhocEvent = trackAdhocEvent;
/**
 * This should be used to log when a `organization.experiments` experiment
 * variant is checked in the application.
 *
 * Refer for the backend implementation provided through HookStore for more
 * details.
 */
const logExperiment = options => hookStore_1.default.get('analytics:log-experiment').forEach(cb => cb(options));
exports.logExperiment = logExperiment;
/**
 * Helper function for `trackAnalyticsEvent` to generically track usage of deprecated features
 *
 * @param feature A name to identify the feature you are tracking
 * @param orgId The organization id
 * @param url [optional] The URL
 */
const trackDeprecated = (feature, orgId, url = '') => (0, exports.trackAdhocEvent)({
    eventKey: 'deprecated.feature',
    feature,
    url,
    org_id: orgId && Number(orgId),
});
exports.trackDeprecated = trackDeprecated;
/**
 * Legacy analytics tracking.
 *
 * @deprecated Prefer `trackAnalyticsEvent` and `trackAdhocEvent`.
 */
const analytics = (name, data) => hookStore_1.default.get('analytics:event').forEach(cb => cb(name, data));
exports.analytics = analytics;
/**
 * Used to pass data between metric.mark() and metric.measure()
 */
const metricDataStore = new Map();
/**
 * Record metrics.
 */
const metric = (name, value, tags) => hookStore_1.default.get('metrics:event').forEach(cb => cb(name, value, tags));
exports.metric = metric;
// JSDOM implements window.performance but not window.performance.mark
const CAN_MARK = window.performance &&
    typeof window.performance.mark === 'function' &&
    typeof window.performance.measure === 'function' &&
    typeof window.performance.getEntriesByName === 'function' &&
    typeof window.performance.clearMeasures === 'function';
exports.metric.mark = function metricMark({ name, data = {} }) {
    // Just ignore if browser is old enough that it doesn't support this
    if (!CAN_MARK) {
        return;
    }
    if (!name) {
        throw new Error('Invalid argument provided to `metric.mark`');
    }
    window.performance.mark(name);
    metricDataStore.set(name, data);
};
/**
 * Performs a measurement between `start` and `end` (or now if `end` is not
 * specified) Calls `metric` with `name` and the measured time difference.
 */
exports.metric.measure = function metricMeasure({ name, start, end, data = {}, noCleanup } = {}) {
    // Just ignore if browser is old enough that it doesn't support this
    if (!CAN_MARK) {
        return;
    }
    if (!name || !start) {
        throw new Error('Invalid arguments provided to `metric.measure`');
    }
    let endMarkName = end;
    // Can't destructure from performance
    const { performance } = window;
    // NOTE: Edge REQUIRES an end mark if it is given a start mark
    // If we don't have an end mark, create one now.
    if (!end) {
        endMarkName = `${start}-end`;
        performance.mark(endMarkName);
    }
    // Check if starting mark exists
    if (!performance.getEntriesByName(start, 'mark').length) {
        return;
    }
    performance.measure(name, start, endMarkName);
    const startData = metricDataStore.get(start) || {};
    // Retrieve measurement entries
    performance
        .getEntriesByName(name, 'measure')
        .forEach(measurement => (0, exports.metric)(measurement.name, measurement.duration, Object.assign(Object.assign({}, startData), data)));
    // By default, clean up measurements
    if (!noCleanup) {
        performance.clearMeasures(name);
        performance.clearMarks(start);
        performance.clearMarks(endMarkName);
        metricDataStore.delete(start);
    }
};
/**
 * Used to pass data between startTransaction and endTransaction
 */
const transactionDataStore = new Map();
const getCurrentTransaction = () => {
    var _a;
    return (_a = Sentry.getCurrentHub().getScope()) === null || _a === void 0 ? void 0 : _a.getTransaction();
};
exports.metric.startTransaction = ({ name, traceId, op }) => {
    var _a;
    if (!traceId) {
        traceId = (_a = getCurrentTransaction()) === null || _a === void 0 ? void 0 : _a.traceId;
    }
    const transaction = Sentry.startTransaction({ name, op, traceId });
    transactionDataStore[name] = transaction;
    return transaction;
};
exports.metric.endTransaction = ({ name }) => {
    const transaction = transactionDataStore[name];
    if (transaction) {
        transaction.finish();
    }
};
//# sourceMappingURL=analytics.jsx.map