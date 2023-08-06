Object.defineProperty(exports, "__esModule", { value: true });
exports.deleteSavedSearch = exports.unpinSearch = exports.pinSearch = exports.fetchRecentSearches = exports.createSavedSearch = exports.saveRecentSearch = exports.fetchProjectSavedSearches = exports.fetchSavedSearches = exports.resetSavedSearches = void 0;
const tslib_1 = require("tslib");
const indicator_1 = require("app/actionCreators/indicator");
const savedSearchesActions_1 = (0, tslib_1.__importDefault)(require("app/actions/savedSearchesActions"));
const constants_1 = require("app/constants");
const locale_1 = require("app/locale");
const types_1 = require("app/types");
const handleXhrErrorResponse_1 = (0, tslib_1.__importDefault)(require("app/utils/handleXhrErrorResponse"));
function resetSavedSearches() {
    savedSearchesActions_1.default.resetSavedSearches();
}
exports.resetSavedSearches = resetSavedSearches;
function fetchSavedSearches(api, orgSlug) {
    const url = `/organizations/${orgSlug}/searches/`;
    savedSearchesActions_1.default.startFetchSavedSearches();
    const promise = api.requestPromise(url, {
        method: 'GET',
    });
    promise
        .then(resp => {
        savedSearchesActions_1.default.fetchSavedSearchesSuccess(resp);
    })
        .catch(err => {
        savedSearchesActions_1.default.fetchSavedSearchesError(err);
        (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to load saved searches'));
    });
    return promise;
}
exports.fetchSavedSearches = fetchSavedSearches;
function fetchProjectSavedSearches(api, orgSlug, projectId) {
    const url = `/projects/${orgSlug}/${projectId}/searches/`;
    return api.requestPromise(url, {
        method: 'GET',
    });
}
exports.fetchProjectSavedSearches = fetchProjectSavedSearches;
const getRecentSearchUrl = (orgSlug) => `/organizations/${orgSlug}/recent-searches/`;
/**
 * Saves search term for `user` + `orgSlug`
 *
 * @param api API client
 * @param orgSlug Organization slug
 * @param type Context for where search happened, 0 for issue, 1 for event
 * @param query The search term that was used
 */
function saveRecentSearch(api, orgSlug, type, query) {
    const url = getRecentSearchUrl(orgSlug);
    const promise = api.requestPromise(url, {
        method: 'POST',
        data: {
            query,
            type,
        },
    });
    promise.catch((0, handleXhrErrorResponse_1.default)('Unable to save a recent search'));
    return promise;
}
exports.saveRecentSearch = saveRecentSearch;
/**
 * Creates a saved search
 *
 * @param api API client
 * @param orgSlug Organization slug
 * @param name Saved search name
 * @param query Query to save
 */
function createSavedSearch(api, orgSlug, name, query, sort) {
    const promise = api.requestPromise(`/organizations/${orgSlug}/searches/`, {
        method: 'POST',
        data: {
            type: types_1.SavedSearchType.ISSUE,
            query,
            name,
            sort,
        },
    });
    // Need to wait for saved search to save unfortunately because we need to redirect
    // to saved search URL
    promise.then(resp => {
        savedSearchesActions_1.default.createSavedSearchSuccess(resp);
    });
    return promise;
}
exports.createSavedSearch = createSavedSearch;
/**
 * Fetches a list of recent search terms conducted by `user` for `orgSlug`
 *
 * @param api API client
 * @param orgSlug Organization slug
 * @param type Context for where search happened, 0 for issue, 1 for event
 * @param query A query term used to filter results
 *
 * @return Returns a list of objects of recent search queries performed by user
 */
function fetchRecentSearches(api, orgSlug, type, query) {
    const url = getRecentSearchUrl(orgSlug);
    const promise = api.requestPromise(url, {
        query: {
            query,
            type,
            limit: constants_1.MAX_AUTOCOMPLETE_RECENT_SEARCHES,
        },
    });
    promise.catch(resp => {
        if (resp.status !== 401 && resp.status !== 403) {
            (0, handleXhrErrorResponse_1.default)('Unable to fetch recent searches')(resp);
        }
    });
    return promise;
}
exports.fetchRecentSearches = fetchRecentSearches;
const getPinSearchUrl = (orgSlug) => `/organizations/${orgSlug}/pinned-searches/`;
function pinSearch(api, orgSlug, type, query, sort) {
    const url = getPinSearchUrl(orgSlug);
    // Optimistically update store
    savedSearchesActions_1.default.pinSearch(type, query, sort);
    const promise = api.requestPromise(url, {
        method: 'PUT',
        data: {
            query,
            type,
            sort,
        },
    });
    promise.then(savedSearchesActions_1.default.pinSearchSuccess);
    promise.catch((0, handleXhrErrorResponse_1.default)('Unable to pin search'));
    promise.catch(() => {
        savedSearchesActions_1.default.unpinSearch(type);
    });
    return promise;
}
exports.pinSearch = pinSearch;
function unpinSearch(api, orgSlug, type, pinnedSearch) {
    const url = getPinSearchUrl(orgSlug);
    // Optimistically update store
    savedSearchesActions_1.default.unpinSearch(type);
    const promise = api.requestPromise(url, {
        method: 'DELETE',
        data: {
            type,
        },
    });
    promise.catch((0, handleXhrErrorResponse_1.default)('Unable to un-pin search'));
    promise.catch(() => {
        const { type: pinnedType, query } = pinnedSearch;
        savedSearchesActions_1.default.pinSearch(pinnedType, query);
    });
    return promise;
}
exports.unpinSearch = unpinSearch;
/**
 * Send a DELETE request to remove a saved search
 *
 * @param api API client
 * @param orgSlug Organization slug
 * @param search The search to remove.
 */
function deleteSavedSearch(api, orgSlug, search) {
    const url = `/organizations/${orgSlug}/searches/${search.id}/`;
    const promise = api
        .requestPromise(url, {
        method: 'DELETE',
    })
        .then(() => savedSearchesActions_1.default.deleteSavedSearchSuccess(search))
        .catch((0, handleXhrErrorResponse_1.default)('Unable to delete a saved search'));
    return promise;
}
exports.deleteSavedSearch = deleteSavedSearch;
//# sourceMappingURL=savedSearches.jsx.map