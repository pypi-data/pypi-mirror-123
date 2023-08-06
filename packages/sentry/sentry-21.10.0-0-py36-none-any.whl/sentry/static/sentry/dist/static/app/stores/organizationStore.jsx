Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reflux_1 = (0, tslib_1.__importDefault)(require("reflux"));
const organizationActions_1 = (0, tslib_1.__importDefault)(require("app/actions/organizationActions"));
const constants_1 = require("app/constants");
const storeConfig = {
    init() {
        this.reset();
        this.listenTo(organizationActions_1.default.update, this.onUpdate);
        this.listenTo(organizationActions_1.default.reset, this.reset);
        this.listenTo(organizationActions_1.default.fetchOrgError, this.onFetchOrgError);
    },
    reset() {
        this.loading = true;
        this.error = null;
        this.errorType = null;
        this.organization = null;
        this.dirty = false;
        this.trigger(this.get());
    },
    onUpdate(updatedOrg, { replace = false } = {}) {
        this.loading = false;
        this.error = null;
        this.errorType = null;
        this.organization = replace ? updatedOrg : Object.assign(Object.assign({}, this.organization), updatedOrg);
        this.dirty = false;
        this.trigger(this.get());
    },
    onFetchOrgError(err) {
        this.organization = null;
        this.errorType = null;
        switch (err === null || err === void 0 ? void 0 : err.status) {
            case 401:
                this.errorType = constants_1.ORGANIZATION_FETCH_ERROR_TYPES.ORG_NO_ACCESS;
                break;
            case 404:
                this.errorType = constants_1.ORGANIZATION_FETCH_ERROR_TYPES.ORG_NOT_FOUND;
                break;
            default:
        }
        this.loading = false;
        this.error = err;
        this.dirty = false;
        this.trigger(this.get());
    },
    get() {
        return {
            organization: this.organization,
            error: this.error,
            loading: this.loading,
            errorType: this.errorType,
            dirty: this.dirty,
        };
    },
    getState() {
        return this.get();
    },
};
const OrganizationStore = reflux_1.default.createStore(storeConfig);
exports.default = OrganizationStore;
//# sourceMappingURL=organizationStore.jsx.map