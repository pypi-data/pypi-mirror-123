Object.defineProperty(exports, "__esModule", { value: true });
const analytics_1 = require("app/utils/analytics");
const hasAnalyticsDebug = () => { var _a; return ((_a = window.localStorage) === null || _a === void 0 ? void 0 : _a.getItem('DEBUG_ANALYTICS')) === '1'; };
/**
 * Generates functions used to track an event for analytics.
 * Each function can only handle the event types specified by the
 * generic for EventParameters and the events in eventKeyToNameMap.
 * Can specifcy default options with the defaultOptions argument as well.
 * Can make orgnization required with the second generic.
 */
function makeAnalyticsFunction(eventKeyToNameMap, defaultOptions) {
    /**
     * Function used for analytics of specifc types determined from factory function
     * Uses the current session ID or generates a new one if startSession == true.
     * An analytics session corresponds to a single action funnel such as installation.
     * Tracking by session allows us to track individual funnel attempts for a single user.
     */
    return (eventKey, analyticsParams, options) => {
        const eventName = eventKeyToNameMap[eventKey];
        const params = Object.assign({ eventKey,
            eventName }, analyticsParams);
        if (hasAnalyticsDebug()) {
            // eslint-disable-next-line no-console
            console.log('analyticsEvent', params);
        }
        // only apply options if required to make mock assertions easier
        if (options || defaultOptions) {
            options = Object.assign(Object.assign({}, defaultOptions), options);
            (0, analytics_1.trackAnalyticsEventV2)(params, options);
        }
        else {
            (0, analytics_1.trackAnalyticsEventV2)(params);
        }
    };
}
exports.default = makeAnalyticsFunction;
//# sourceMappingURL=makeAnalyticsFunction.jsx.map