Object.defineProperty(exports, "__esModule", { value: true });
exports.fetchTagValues = exports.fetchOrganizationTags = exports.loadOrganizationTags = void 0;
const tslib_1 = require("tslib");
const alertActions_1 = (0, tslib_1.__importDefault)(require("app/actions/alertActions"));
const tagActions_1 = (0, tslib_1.__importDefault)(require("app/actions/tagActions"));
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const locale_1 = require("app/locale");
const tagStore_1 = (0, tslib_1.__importDefault)(require("app/stores/tagStore"));
const MAX_TAGS = 1000;
function tagFetchSuccess(tags) {
    // We occasionally get undefined passed in when APIs are having a bad time.
    tags = tags || [];
    const trimmedTags = tags.slice(0, MAX_TAGS);
    if (tags.length > MAX_TAGS) {
        alertActions_1.default.addAlert({
            message: (0, locale_1.t)('You have too many unique tags and some have been truncated'),
            type: 'warn',
        });
    }
    tagActions_1.default.loadTagsSuccess(trimmedTags);
}
/**
 * Load an organization's tags based on a global selection value.
 */
function loadOrganizationTags(api, orgId, selection) {
    tagStore_1.default.reset();
    const url = `/organizations/${orgId}/tags/`;
    const query = selection.datetime ? Object.assign({}, (0, getParams_1.getParams)(selection.datetime)) : {};
    query.use_cache = '1';
    if (selection.projects) {
        query.project = selection.projects.map(String);
    }
    const promise = api.requestPromise(url, {
        method: 'GET',
        query,
    });
    promise.then(tagFetchSuccess, tagActions_1.default.loadTagsError);
    return promise;
}
exports.loadOrganizationTags = loadOrganizationTags;
/**
 * Fetch tags for an organization or a subset or projects.
 */
function fetchOrganizationTags(api, orgId, projectIds = null) {
    tagStore_1.default.reset();
    const url = `/organizations/${orgId}/tags/`;
    const query = { use_cache: '1' };
    if (projectIds) {
        query.project = projectIds;
    }
    const promise = api.requestPromise(url, {
        method: 'GET',
        query,
    });
    promise.then(tagFetchSuccess, tagActions_1.default.loadTagsError);
    return promise;
}
exports.fetchOrganizationTags = fetchOrganizationTags;
/**
 * Fetch tag values for an organization.
 * The `projectIds` argument can be used to subset projects.
 */
function fetchTagValues(api, orgId, tagKey, search = null, projectIds = null, endpointParams = null, includeTransactions = false) {
    const url = `/organizations/${orgId}/tags/${tagKey}/values/`;
    const query = {};
    if (search) {
        query.query = search;
    }
    if (projectIds) {
        query.project = projectIds;
    }
    if (endpointParams) {
        if (endpointParams.start) {
            query.start = endpointParams.start;
        }
        if (endpointParams.end) {
            query.end = endpointParams.end;
        }
        if (endpointParams.statsPeriod) {
            query.statsPeriod = endpointParams.statsPeriod;
        }
    }
    if (includeTransactions) {
        query.includeTransactions = '1';
    }
    return api.requestPromise(url, {
        method: 'GET',
        query,
    });
}
exports.fetchTagValues = fetchTagValues;
//# sourceMappingURL=tags.jsx.map