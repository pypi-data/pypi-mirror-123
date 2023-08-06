Object.defineProperty(exports, "__esModule", { value: true });
exports.uninstallSentryApp = exports.installSentryApp = void 0;
const indicator_1 = require("app/actionCreators/indicator");
const locale_1 = require("app/locale");
/**
 * Install a sentry application
 *
 * @param {Object} client ApiClient
 * @param {String} orgId Organization Slug
 * @param {Object} app SentryApp
 */
function installSentryApp(client, orgId, app) {
    (0, indicator_1.addLoadingMessage)();
    const promise = client.requestPromise(`/organizations/${orgId}/sentry-app-installations/`, {
        method: 'POST',
        data: { slug: app.slug },
    });
    promise.then(() => (0, indicator_1.clearIndicators)(), () => (0, indicator_1.addErrorMessage)((0, locale_1.t)(`Unable to install ${app.name}`)));
    return promise;
}
exports.installSentryApp = installSentryApp;
/**
 * Uninstall a sentry application
 *
 * @param {Object} client ApiClient
 * @param {Object} install SentryAppInstallation
 */
function uninstallSentryApp(client, install) {
    (0, indicator_1.addLoadingMessage)();
    const promise = client.requestPromise(`/sentry-app-installations/${install.uuid}/`, {
        method: 'DELETE',
    });
    promise.then(() => {
        (0, indicator_1.addSuccessMessage)((0, locale_1.t)(`${install.app.slug} successfully uninstalled.`));
    }, () => (0, indicator_1.clearIndicators)());
    return promise;
}
exports.uninstallSentryApp = uninstallSentryApp;
//# sourceMappingURL=sentryAppInstallations.jsx.map