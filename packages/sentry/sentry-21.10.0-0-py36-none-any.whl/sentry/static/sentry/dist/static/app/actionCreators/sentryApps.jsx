Object.defineProperty(exports, "__esModule", { value: true });
exports.removeSentryApp = void 0;
const indicator_1 = require("app/actionCreators/indicator");
const locale_1 = require("app/locale");
/**
 * Remove a Sentry Application
 *
 * @param {Object} client ApiClient
 * @param {Object} app SentryApp
 */
function removeSentryApp(client, app) {
    (0, indicator_1.addLoadingMessage)();
    const promise = client.requestPromise(`/sentry-apps/${app.slug}/`, {
        method: 'DELETE',
    });
    promise.then(() => {
        (0, indicator_1.addSuccessMessage)((0, locale_1.t)('%s successfully removed.', app.slug));
    }, () => {
        (0, indicator_1.clearIndicators)();
        (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to remove %s integration', app.slug));
    });
    return promise;
}
exports.removeSentryApp = removeSentryApp;
//# sourceMappingURL=sentryApps.jsx.map