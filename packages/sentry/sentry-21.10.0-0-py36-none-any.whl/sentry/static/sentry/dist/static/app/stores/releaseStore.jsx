Object.defineProperty(exports, "__esModule", { value: true });
exports.getReleaseStoreKey = void 0;
const tslib_1 = require("tslib");
const reflux_1 = (0, tslib_1.__importDefault)(require("reflux"));
const organizationActions_1 = (0, tslib_1.__importDefault)(require("app/actions/organizationActions"));
const releaseActions_1 = (0, tslib_1.__importDefault)(require("app/actions/releaseActions"));
const getReleaseStoreKey = (projectSlug, releaseVersion) => `${projectSlug}${releaseVersion}`;
exports.getReleaseStoreKey = getReleaseStoreKey;
const storeConfig = {
    state: {
        orgSlug: undefined,
        release: new Map(),
        releaseLoading: new Map(),
        releaseError: new Map(),
        deploys: new Map(),
        deploysLoading: new Map(),
        deploysError: new Map(),
    },
    listenables: releaseActions_1.default,
    init() {
        this.listenTo(organizationActions_1.default.update, this.updateOrganization);
        this.reset();
    },
    reset() {
        this.state = {
            orgSlug: undefined,
            release: new Map(),
            releaseLoading: new Map(),
            releaseError: new Map(),
            deploys: new Map(),
            deploysLoading: new Map(),
            deploysError: new Map(),
        };
        this.trigger(this.state);
    },
    updateOrganization(org) {
        this.reset();
        this.state.orgSlug = org.slug;
        this.trigger(this.state);
    },
    loadRelease(orgSlug, projectSlug, releaseVersion) {
        // Wipe entire store if the user switched organizations
        if (!this.orgSlug || this.orgSlug !== orgSlug) {
            this.reset();
            this.orgSlug = orgSlug;
        }
        const releaseKey = (0, exports.getReleaseStoreKey)(projectSlug, releaseVersion);
        const _a = this.state, { releaseLoading, releaseError } = _a, state = (0, tslib_1.__rest)(_a, ["releaseLoading", "releaseError"]);
        this.state = Object.assign(Object.assign({}, state), { releaseLoading: Object.assign(Object.assign({}, releaseLoading), { [releaseKey]: true }), releaseError: Object.assign(Object.assign({}, releaseError), { [releaseKey]: undefined }) });
        this.trigger(this.state);
    },
    loadReleaseError(projectSlug, releaseVersion, error) {
        const releaseKey = (0, exports.getReleaseStoreKey)(projectSlug, releaseVersion);
        const _a = this.state, { releaseLoading, releaseError } = _a, state = (0, tslib_1.__rest)(_a, ["releaseLoading", "releaseError"]);
        this.state = Object.assign(Object.assign({}, state), { releaseLoading: Object.assign(Object.assign({}, releaseLoading), { [releaseKey]: false }), releaseError: Object.assign(Object.assign({}, releaseError), { [releaseKey]: error }) });
        this.trigger(this.state);
    },
    loadReleaseSuccess(projectSlug, releaseVersion, data) {
        const releaseKey = (0, exports.getReleaseStoreKey)(projectSlug, releaseVersion);
        const _a = this.state, { release, releaseLoading, releaseError } = _a, state = (0, tslib_1.__rest)(_a, ["release", "releaseLoading", "releaseError"]);
        this.state = Object.assign(Object.assign({}, state), { release: Object.assign(Object.assign({}, release), { [releaseKey]: data }), releaseLoading: Object.assign(Object.assign({}, releaseLoading), { [releaseKey]: false }), releaseError: Object.assign(Object.assign({}, releaseError), { [releaseKey]: undefined }) });
        this.trigger(this.state);
    },
    loadDeploys(orgSlug, projectSlug, releaseVersion) {
        // Wipe entire store if the user switched organizations
        if (!this.orgSlug || this.orgSlug !== orgSlug) {
            this.reset();
            this.orgSlug = orgSlug;
        }
        const releaseKey = (0, exports.getReleaseStoreKey)(projectSlug, releaseVersion);
        const _a = this.state, { deploysLoading, deploysError } = _a, state = (0, tslib_1.__rest)(_a, ["deploysLoading", "deploysError"]);
        this.state = Object.assign(Object.assign({}, state), { deploysLoading: Object.assign(Object.assign({}, deploysLoading), { [releaseKey]: true }), deploysError: Object.assign(Object.assign({}, deploysError), { [releaseKey]: undefined }) });
        this.trigger(this.state);
    },
    loadDeploysError(projectSlug, releaseVersion, error) {
        const releaseKey = (0, exports.getReleaseStoreKey)(projectSlug, releaseVersion);
        const _a = this.state, { deploysLoading, deploysError } = _a, state = (0, tslib_1.__rest)(_a, ["deploysLoading", "deploysError"]);
        this.state = Object.assign(Object.assign({}, state), { deploysLoading: Object.assign(Object.assign({}, deploysLoading), { [releaseKey]: false }), deploysError: Object.assign(Object.assign({}, deploysError), { [releaseKey]: error }) });
        this.trigger(this.state);
    },
    loadDeploysSuccess(projectSlug, releaseVersion, data) {
        const releaseKey = (0, exports.getReleaseStoreKey)(projectSlug, releaseVersion);
        const _a = this.state, { deploys, deploysLoading, deploysError } = _a, state = (0, tslib_1.__rest)(_a, ["deploys", "deploysLoading", "deploysError"]);
        this.state = Object.assign(Object.assign({}, state), { deploys: Object.assign(Object.assign({}, deploys), { [releaseKey]: data }), deploysLoading: Object.assign(Object.assign({}, deploysLoading), { [releaseKey]: false }), deploysError: Object.assign(Object.assign({}, deploysError), { [releaseKey]: undefined }) });
        this.trigger(this.state);
    },
    get(projectSlug, releaseVersion) {
        const releaseKey = (0, exports.getReleaseStoreKey)(projectSlug, releaseVersion);
        return {
            release: this.state.release[releaseKey],
            releaseLoading: this.state.releaseLoading[releaseKey],
            releaseError: this.state.releaseError[releaseKey],
            deploys: this.state.deploys[releaseKey],
            deploysLoading: this.state.deploysLoading[releaseKey],
            deploysError: this.state.deploysError[releaseKey],
        };
    },
};
const ReleaseStore = reflux_1.default.createStore(storeConfig);
exports.default = ReleaseStore;
//# sourceMappingURL=releaseStore.jsx.map