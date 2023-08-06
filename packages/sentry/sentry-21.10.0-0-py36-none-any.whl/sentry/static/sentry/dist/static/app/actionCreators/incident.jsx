Object.defineProperty(exports, "__esModule", { value: true });
exports.markIncidentAsSeen = exports.updateIncidentNote = exports.deleteIncidentNote = exports.createIncidentNote = exports.fetchIncidentActivities = void 0;
const tslib_1 = require("tslib");
const indicator_1 = require("app/actionCreators/indicator");
const locale_1 = require("app/locale");
/**
 * Fetches a list of activities for an incident
 */
function fetchIncidentActivities(api, orgId, alertId) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        return api.requestPromise(`/organizations/${orgId}/incidents/${alertId}/activity/`);
    });
}
exports.fetchIncidentActivities = fetchIncidentActivities;
/**
 * Creates a note for an incident
 */
function createIncidentNote(api, orgId, alertId, note) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        try {
            const result = yield api.requestPromise(`/organizations/${orgId}/incidents/${alertId}/comments/`, {
                method: 'POST',
                data: {
                    mentions: note.mentions,
                    comment: note.text,
                },
            });
            return result;
        }
        catch (err) {
            (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to post comment'));
            throw err;
        }
    });
}
exports.createIncidentNote = createIncidentNote;
/**
 * Deletes a note for an incident
 */
function deleteIncidentNote(api, orgId, alertId, noteId) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        try {
            const result = yield api.requestPromise(`/organizations/${orgId}/incidents/${alertId}/comments/${noteId}/`, {
                method: 'DELETE',
            });
            return result;
        }
        catch (err) {
            (0, indicator_1.addErrorMessage)((0, locale_1.t)('Failed to delete comment'));
            throw err;
        }
    });
}
exports.deleteIncidentNote = deleteIncidentNote;
/**
 * Updates a note for an incident
 */
function updateIncidentNote(api, orgId, alertId, noteId, note) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        try {
            const result = yield api.requestPromise(`/organizations/${orgId}/incidents/${alertId}/comments/${noteId}/`, {
                method: 'PUT',
                data: {
                    mentions: note.mentions,
                    comment: note.text,
                },
            });
            (0, indicator_1.clearIndicators)();
            return result;
        }
        catch (err) {
            (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to update comment'));
            throw err;
        }
    });
}
exports.updateIncidentNote = updateIncidentNote;
// This doesn't return anything because you shouldn't need to do anything with
// the result success or fail
function markIncidentAsSeen(api, orgId, incident) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        if (!incident || incident.hasSeen) {
            return;
        }
        try {
            yield api.requestPromise(`/organizations/${orgId}/incidents/${incident.identifier}/seen/`, {
                method: 'POST',
                data: {
                    hasSeen: true,
                },
            });
        }
        catch (err) {
            // do nothing
        }
    });
}
exports.markIncidentAsSeen = markIncidentAsSeen;
//# sourceMappingURL=incident.jsx.map