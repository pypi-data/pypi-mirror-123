Object.defineProperty(exports, "__esModule", { value: true });
exports.markBroadcastsAsSeen = exports.getAllBroadcasts = void 0;
function getAllBroadcasts(api, orgSlug) {
    return api.requestPromise(`/organizations/${orgSlug}/broadcasts/`, { method: 'GET' });
}
exports.getAllBroadcasts = getAllBroadcasts;
function markBroadcastsAsSeen(api, idList) {
    return api.requestPromise('/broadcasts/', {
        method: 'PUT',
        query: { id: idList },
        data: { hasSeen: '1' },
    });
}
exports.markBroadcastsAsSeen = markBroadcastsAsSeen;
//# sourceMappingURL=broadcasts.jsx.map