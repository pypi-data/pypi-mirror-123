Object.defineProperty(exports, "__esModule", { value: true });
exports.removeSentryAppToken = exports.addSentryAppToken = void 0;
const tslib_1 = require("tslib");
const indicator_1 = require("app/actionCreators/indicator");
const locale_1 = require("app/locale");
/**
 * Install a sentry application
 *
 * @param {Object} client ApiClient
 * @param {Object} app SentryApp
 */
function addSentryAppToken(client, app) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        (0, indicator_1.addLoadingMessage)();
        try {
            const token = yield client.requestPromise(`/sentry-apps/${app.slug}/api-tokens/`, {
                method: 'POST',
            });
            (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Token successfully added.'));
            return token;
        }
        catch (err) {
            (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to create token'));
            throw err;
        }
    });
}
exports.addSentryAppToken = addSentryAppToken;
/**
 * Uninstall a sentry application
 *
 * @param {Object} client ApiClient
 * @param {Object} app SentryApp
 * @param {String} token Token string
 */
function removeSentryAppToken(client, app, token) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        (0, indicator_1.addLoadingMessage)();
        try {
            yield client.requestPromise(`/sentry-apps/${app.slug}/api-tokens/${token}/`, {
                method: 'DELETE',
            });
            (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Token successfully deleted.'));
            return;
        }
        catch (err) {
            (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to delete token'));
            throw err;
        }
    });
}
exports.removeSentryAppToken = removeSentryAppToken;
//# sourceMappingURL=sentryAppTokens.jsx.map