Object.defineProperty(exports, "__esModule", { value: true });
exports.getCommitterStoreKey = exports.storeConfig = void 0;
const tslib_1 = require("tslib");
const reflux_1 = (0, tslib_1.__importDefault)(require("reflux"));
const committerActions_1 = (0, tslib_1.__importDefault)(require("app/actions/committerActions"));
exports.storeConfig = {
    listenables: committerActions_1.default,
    state: {},
    init() {
        this.reset();
    },
    reset() {
        this.state = {};
        this.trigger(this.state);
    },
    load(orgSlug, projectSlug, eventId) {
        const key = getCommitterStoreKey(orgSlug, projectSlug, eventId);
        this.state = Object.assign(Object.assign({}, this.state), { [key]: {
                committers: undefined,
                committersLoading: true,
                committersError: undefined,
            } });
        this.trigger(this.state);
    },
    loadError(orgSlug, projectSlug, eventId, err) {
        const key = getCommitterStoreKey(orgSlug, projectSlug, eventId);
        this.state = Object.assign(Object.assign({}, this.state), { [key]: {
                committers: undefined,
                committersLoading: false,
                committersError: err,
            } });
        this.trigger(this.state);
    },
    loadSuccess(orgSlug, projectSlug, eventId, data) {
        const key = getCommitterStoreKey(orgSlug, projectSlug, eventId);
        this.state = Object.assign(Object.assign({}, this.state), { [key]: {
                committers: data,
                committersLoading: false,
                committersError: undefined,
            } });
        this.trigger(this.state);
    },
    get(orgSlug, projectSlug, eventId) {
        const key = getCommitterStoreKey(orgSlug, projectSlug, eventId);
        return Object.assign({}, this.state[key]);
    },
};
function getCommitterStoreKey(orgSlug, projectSlug, eventId) {
    return `${orgSlug} ${projectSlug} ${eventId}`;
}
exports.getCommitterStoreKey = getCommitterStoreKey;
const CommitterStore = reflux_1.default.createStore(exports.storeConfig);
exports.default = CommitterStore;
//# sourceMappingURL=committerStore.jsx.map