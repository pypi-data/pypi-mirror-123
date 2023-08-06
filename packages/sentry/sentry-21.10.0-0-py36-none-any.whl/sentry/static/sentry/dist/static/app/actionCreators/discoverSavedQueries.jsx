Object.defineProperty(exports, "__esModule", { value: true });
exports.deleteSavedQuery = exports.updateSavedQueryVisit = exports.updateSavedQuery = exports.createSavedQuery = exports.fetchSavedQuery = exports.fetchSavedQueries = void 0;
const indicator_1 = require("app/actionCreators/indicator");
const api_1 = require("app/api");
const locale_1 = require("app/locale");
function fetchSavedQueries(api, orgId, query = '') {
    const promise = api.requestPromise(`/organizations/${orgId}/discover/saved/`, {
        method: 'GET',
        query: { query: `version:2 ${query}`.trim() },
    });
    promise.catch(() => {
        (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to load saved queries'));
    });
    return promise;
}
exports.fetchSavedQueries = fetchSavedQueries;
function fetchSavedQuery(api, orgId, queryId) {
    const promise = api.requestPromise(`/organizations/${orgId}/discover/saved/${queryId}/`, {
        method: 'GET',
    });
    promise.catch(() => {
        (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to load saved query'));
    });
    return promise;
}
exports.fetchSavedQuery = fetchSavedQuery;
function createSavedQuery(api, orgId, query) {
    const promise = api.requestPromise(`/organizations/${orgId}/discover/saved/`, {
        method: 'POST',
        data: query,
    });
    promise.catch(() => {
        (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to create your saved query'));
    });
    return promise;
}
exports.createSavedQuery = createSavedQuery;
function updateSavedQuery(api, orgId, query) {
    const promise = api.requestPromise(`/organizations/${orgId}/discover/saved/${query.id}/`, {
        method: 'PUT',
        data: query,
    });
    promise.catch(() => {
        (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to update your saved query'));
    });
    return promise;
}
exports.updateSavedQuery = updateSavedQuery;
function updateSavedQueryVisit(orgId, queryId) {
    // Create a new client so the request is not cancelled
    const api = new api_1.Client();
    const promise = api.requestPromise(`/organizations/${orgId}/discover/saved/${queryId}/visit/`, {
        method: 'POST',
    });
    return promise;
}
exports.updateSavedQueryVisit = updateSavedQueryVisit;
function deleteSavedQuery(api, orgId, queryId) {
    const promise = api.requestPromise(`/organizations/${orgId}/discover/saved/${queryId}/`, { method: 'DELETE' });
    promise.catch(() => {
        (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to delete the saved query'));
    });
    return promise;
}
exports.deleteSavedQuery = deleteSavedQuery;
//# sourceMappingURL=discoverSavedQueries.jsx.map