Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reflux_1 = (0, tslib_1.__importDefault)(require("reflux"));
const environmentActions_1 = (0, tslib_1.__importDefault)(require("app/actions/environmentActions"));
const environment_1 = require("app/utils/environment");
const storeConfig = {
    state: {
        environments: null,
        error: null,
    },
    init() {
        this.state = { environments: null, error: null };
        this.listenTo(environmentActions_1.default.fetchEnvironments, this.onFetchEnvironments);
        this.listenTo(environmentActions_1.default.fetchEnvironmentsSuccess, this.onFetchEnvironmentsSuccess);
        this.listenTo(environmentActions_1.default.fetchEnvironmentsError, this.onFetchEnvironmentsError);
    },
    makeEnvironment(item) {
        return {
            id: item.id,
            name: item.name,
            get displayName() {
                return (0, environment_1.getDisplayName)(item);
            },
            get urlRoutingName() {
                return (0, environment_1.getUrlRoutingName)(item);
            },
        };
    },
    onFetchEnvironments() {
        this.state = { environments: null, error: null };
        this.trigger(this.state);
    },
    onFetchEnvironmentsSuccess(environments) {
        this.state = { error: null, environments: environments.map(this.makeEnvironment) };
        this.trigger(this.state);
    },
    onFetchEnvironmentsError(error) {
        this.state = { error, environments: null };
        this.trigger(this.state);
    },
    get() {
        return this.state;
    },
};
const OrganizationEnvironmentsStore = reflux_1.default.createStore(storeConfig);
exports.default = OrganizationEnvironmentsStore;
//# sourceMappingURL=organizationEnvironmentsStore.jsx.map