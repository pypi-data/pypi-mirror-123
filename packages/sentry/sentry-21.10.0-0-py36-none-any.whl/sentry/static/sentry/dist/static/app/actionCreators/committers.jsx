Object.defineProperty(exports, "__esModule", { value: true });
exports.getCommitters = void 0;
const tslib_1 = require("tslib");
const committerActions_1 = (0, tslib_1.__importDefault)(require("app/actions/committerActions"));
const committerStore_1 = (0, tslib_1.__importStar)(require("app/stores/committerStore"));
function getCommitters(api, params) {
    const { orgSlug, projectSlug, eventId } = params;
    const path = `/projects/${orgSlug}/${projectSlug}/events/${eventId}/committers/`;
    // HACK(leedongwei): Actions fired by the ActionCreators are queued to
    // the back of the event loop, allowing another getRepo for the same
    // repo to be fired before the loading state is updated in store.
    // This hack short-circuits that and update the state immediately.
    const storeKey = (0, committerStore_1.getCommitterStoreKey)(orgSlug, projectSlug, eventId);
    committerStore_1.default.state[storeKey] = Object.assign(Object.assign({}, committerStore_1.default.state[storeKey]), { committersLoading: true });
    committerActions_1.default.load(orgSlug, projectSlug, eventId);
    return api
        .requestPromise(path, {
        method: 'GET',
    })
        .then((res) => {
        committerActions_1.default.loadSuccess(orgSlug, projectSlug, eventId, res.committers);
    })
        .catch(err => {
        // NOTE: Do not captureException here as EventFileCommittersEndpoint returns
        // 404 Not Found if the project did not setup Releases or Commits
        committerActions_1.default.loadError(orgSlug, projectSlug, eventId, err);
    });
}
exports.getCommitters = getCommitters;
//# sourceMappingURL=committers.jsx.map