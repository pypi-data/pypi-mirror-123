Object.defineProperty(exports, "__esModule", { value: true });
exports.disablePlugin = exports.enablePlugin = exports.fetchPlugins = void 0;
const tslib_1 = require("tslib");
const indicator_1 = require("app/actionCreators/indicator");
const pluginActions_1 = (0, tslib_1.__importDefault)(require("app/actions/pluginActions"));
const api_1 = require("app/api");
const locale_1 = require("app/locale");
const activeFetch = {};
// PluginsStore always exists, so api client should be independent of component lifecycle
const api = new api_1.Client();
function doUpdate(_a) {
    var { orgId, projectId, pluginId, update } = _a, params = (0, tslib_1.__rest)(_a, ["orgId", "projectId", "pluginId", "update"]);
    pluginActions_1.default.update(pluginId, update);
    const request = api.requestPromise(`/projects/${orgId}/${projectId}/plugins/${pluginId}/`, Object.assign({}, params));
    // This is intentionally not chained because we want the unhandled promise to be returned
    request
        .then(() => {
        pluginActions_1.default.updateSuccess(pluginId, update);
    })
        .catch(resp => {
        const err = resp && resp.responseJSON && typeof resp.responseJSON.detail === 'string'
            ? new Error(resp.responseJSON.detail)
            : new Error('Unable to update plugin');
        pluginActions_1.default.updateError(pluginId, update, err);
    });
    return request;
}
/**
 * Fetches list of available plugins for a project
 */
function fetchPlugins({ orgId, projectId }, options) {
    const path = `/projects/${orgId}/${projectId}/plugins/`;
    // Make sure we throttle fetches
    if (activeFetch[path]) {
        return activeFetch[path];
    }
    pluginActions_1.default.fetchAll(options);
    const request = api.requestPromise(path, {
        method: 'GET',
        includeAllArgs: true,
    });
    activeFetch[path] = request;
    // This is intentionally not chained because we want the unhandled promise to be returned
    request
        .then(([data, _, resp]) => {
        pluginActions_1.default.fetchAllSuccess(data, { pageLinks: resp === null || resp === void 0 ? void 0 : resp.getResponseHeader('Link') });
        return data;
    })
        .catch(err => {
        pluginActions_1.default.fetchAllError(err);
        throw new Error('Unable to fetch plugins');
    })
        .then(() => (activeFetch[path] = null));
    return request;
}
exports.fetchPlugins = fetchPlugins;
/**
 * Enables a plugin
 */
function enablePlugin(params) {
    (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Enabling...'));
    return doUpdate(Object.assign(Object.assign({}, params), { update: { enabled: true }, method: 'POST' }))
        .then(() => (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Plugin was enabled')))
        .catch(() => (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to enable plugin')));
}
exports.enablePlugin = enablePlugin;
/**
 * Disables a plugin
 */
function disablePlugin(params) {
    (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Disabling...'));
    return doUpdate(Object.assign(Object.assign({}, params), { update: { enabled: false }, method: 'DELETE' }))
        .then(() => (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Plugin was disabled')))
        .catch(() => (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to disable plugin')));
}
exports.disablePlugin = disablePlugin;
//# sourceMappingURL=plugins.jsx.map