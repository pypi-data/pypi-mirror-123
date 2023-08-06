Object.defineProperty(exports, "__esModule", { value: true });
exports.extractAnalyticsQueryFields = exports.getAnalyticsCreateEventKeyName = exports.handleDeleteQuery = exports.handleUpdateQueryName = exports.handleUpdateQuery = exports.handleCreateQuery = void 0;
const discoverSavedQueries_1 = require("app/actionCreators/discoverSavedQueries");
const indicator_1 = require("app/actionCreators/indicator");
const locale_1 = require("app/locale");
const analytics_1 = require("app/utils/analytics");
function handleCreateQuery(api, organization, eventView, yAxis, 
// True if this is a brand new query being saved
// False if this is a modification from a saved query
isNewQuery = true) {
    const payload = eventView.toNewQuery();
    payload.yAxis = yAxis;
    (0, analytics_1.trackAnalyticsEvent)(Object.assign(Object.assign(Object.assign({}, getAnalyticsCreateEventKeyName(isNewQuery, 'request')), { organization_id: parseInt(organization.id, 10) }), extractAnalyticsQueryFields(payload)));
    const promise = (0, discoverSavedQueries_1.createSavedQuery)(api, organization.slug, payload);
    promise
        .then((savedQuery) => {
        (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Query saved'));
        (0, analytics_1.trackAnalyticsEvent)(Object.assign(Object.assign(Object.assign({}, getAnalyticsCreateEventKeyName(isNewQuery, 'success')), { organization_id: parseInt(organization.id, 10) }), extractAnalyticsQueryFields(payload)));
        return savedQuery;
    })
        .catch((err) => {
        (0, indicator_1.addErrorMessage)((0, locale_1.t)('Query not saved'));
        (0, analytics_1.trackAnalyticsEvent)(Object.assign(Object.assign(Object.assign(Object.assign({}, getAnalyticsCreateEventKeyName(isNewQuery, 'failed')), { organization_id: parseInt(organization.id, 10) }), extractAnalyticsQueryFields(payload)), { error: (err && err.message) ||
                `Could not save a ${isNewQuery ? 'new' : 'existing'} query` }));
    });
    return promise;
}
exports.handleCreateQuery = handleCreateQuery;
const EVENT_NAME_EXISTING_MAP = {
    request: 'Discoverv2: Request to save a saved query as a new query',
    success: 'Discoverv2: Successfully saved a saved query as a new query',
    failed: 'Discoverv2: Failed to save a saved query as a new query',
};
const EVENT_NAME_NEW_MAP = {
    request: 'Discoverv2: Request to save a new query',
    success: 'Discoverv2: Successfully saved a new query',
    failed: 'Discoverv2: Failed to save a new query',
};
function handleUpdateQuery(api, organization, eventView, yAxis) {
    const payload = eventView.toNewQuery();
    payload.yAxis = yAxis;
    if (!eventView.name) {
        (0, indicator_1.addErrorMessage)((0, locale_1.t)('Please name your query'));
        return Promise.reject();
    }
    (0, analytics_1.trackAnalyticsEvent)(Object.assign({ eventKey: 'discover_v2.update_query_request', eventName: 'Discoverv2: Request to update a saved query', organization_id: parseInt(organization.id, 10) }, extractAnalyticsQueryFields(payload)));
    const promise = (0, discoverSavedQueries_1.updateSavedQuery)(api, organization.slug, payload);
    promise
        .then((savedQuery) => {
        (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Query updated'));
        (0, analytics_1.trackAnalyticsEvent)(Object.assign({ eventKey: 'discover_v2.update_query_success', eventName: 'Discoverv2: Successfully updated a saved query', organization_id: parseInt(organization.id, 10) }, extractAnalyticsQueryFields(payload)));
        // NOTE: there is no need to convert _saved into an EventView and push it
        //       to the browser history, since this.props.eventView already
        //       derives from location.
        return savedQuery;
    })
        .catch((err) => {
        (0, indicator_1.addErrorMessage)((0, locale_1.t)('Query not updated'));
        (0, analytics_1.trackAnalyticsEvent)(Object.assign(Object.assign({ eventKey: 'discover_v2.update_query_failed', eventName: 'Discoverv2: Failed to update a saved query', organization_id: parseInt(organization.id, 10) }, extractAnalyticsQueryFields(payload)), { error: (err && err.message) || 'Failed to update a query' }));
    });
    return promise;
}
exports.handleUpdateQuery = handleUpdateQuery;
/**
 * Essentially the same as handleUpdateQuery, but specifically for changing the
 * name of the query
 */
function handleUpdateQueryName(api, organization, eventView) {
    const payload = eventView.toNewQuery();
    (0, analytics_1.trackAnalyticsEvent)(Object.assign({ eventKey: 'discover_v2.update_query_name_request', eventName: "Discoverv2: Request to update a saved query's name", organization_id: parseInt(organization.id, 10) }, extractAnalyticsQueryFields(payload)));
    const promise = (0, discoverSavedQueries_1.updateSavedQuery)(api, organization.slug, payload);
    promise
        .then(_saved => {
        (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Query name saved'));
        (0, analytics_1.trackAnalyticsEvent)(Object.assign({ eventKey: 'discover_v2.update_query_name_success', eventName: "Discoverv2: Successfully updated a saved query's name", organization_id: parseInt(organization.id, 10) }, extractAnalyticsQueryFields(payload)));
    })
        .catch((err) => {
        (0, indicator_1.addErrorMessage)((0, locale_1.t)('Query name not saved'));
        (0, analytics_1.trackAnalyticsEvent)(Object.assign(Object.assign({ eventKey: 'discover_v2.update_query_failed', eventName: "Discoverv2: Failed to update a saved query's name", organization_id: parseInt(organization.id, 10) }, extractAnalyticsQueryFields(payload)), { error: (err && err.message) || 'Failed to update a query name' }));
    });
    return promise;
}
exports.handleUpdateQueryName = handleUpdateQueryName;
function handleDeleteQuery(api, organization, eventView) {
    (0, analytics_1.trackAnalyticsEvent)(Object.assign({ eventKey: 'discover_v2.delete_query_request', eventName: 'Discoverv2: Request to delete a saved query', organization_id: parseInt(organization.id, 10) }, extractAnalyticsQueryFields(eventView.toNewQuery())));
    const promise = (0, discoverSavedQueries_1.deleteSavedQuery)(api, organization.slug, eventView.id);
    promise
        .then(() => {
        (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Query deleted'));
        (0, analytics_1.trackAnalyticsEvent)(Object.assign({ eventKey: 'discover_v2.delete_query_success', eventName: 'Discoverv2: Successfully deleted a saved query', organization_id: parseInt(organization.id, 10) }, extractAnalyticsQueryFields(eventView.toNewQuery())));
    })
        .catch((err) => {
        (0, indicator_1.addErrorMessage)((0, locale_1.t)('Query not deleted'));
        (0, analytics_1.trackAnalyticsEvent)(Object.assign(Object.assign({ eventKey: 'discover_v2.delete_query_failed', eventName: 'Discoverv2: Failed to delete a saved query', organization_id: parseInt(organization.id, 10) }, extractAnalyticsQueryFields(eventView.toNewQuery())), { error: (err && err.message) || 'Failed to delete query' }));
    });
    return promise;
}
exports.handleDeleteQuery = handleDeleteQuery;
function getAnalyticsCreateEventKeyName(
// True if this is a brand new query being saved
// False if this is a modification from a saved query
isNewQuery, type) {
    const eventKey = isNewQuery
        ? 'discover_v2.save_new_query_' + type
        : 'discover_v2.save_existing_query_' + type;
    const eventName = isNewQuery ? EVENT_NAME_NEW_MAP[type] : EVENT_NAME_EXISTING_MAP[type];
    return {
        eventKey,
        eventName,
    };
}
exports.getAnalyticsCreateEventKeyName = getAnalyticsCreateEventKeyName;
/**
 * Takes in a DiscoverV2 NewQuery object and returns a Partial containing
 * the desired fields to populate into reload analytics
 */
function extractAnalyticsQueryFields(payload) {
    const { projects, fields, query } = payload;
    return {
        projects,
        fields,
        query,
    };
}
exports.extractAnalyticsQueryFields = extractAnalyticsQueryFields;
//# sourceMappingURL=utils.jsx.map