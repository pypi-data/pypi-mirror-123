Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reflux_1 = (0, tslib_1.__importDefault)(require("reflux"));
const repositoryActions_1 = (0, tslib_1.__importDefault)(require("app/actions/repositoryActions"));
const storeConfig = {
    listenables: repositoryActions_1.default,
    state: {
        orgSlug: undefined,
        repositories: undefined,
        repositoriesLoading: undefined,
        repositoriesError: undefined,
    },
    init() {
        this.resetRepositories();
    },
    resetRepositories() {
        this.state = {
            orgSlug: undefined,
            repositories: undefined,
            repositoriesLoading: undefined,
            repositoriesError: undefined,
        };
        this.trigger(this.state);
    },
    loadRepositories(orgSlug) {
        this.state = {
            orgSlug,
            repositories: orgSlug === this.state.orgSlug ? this.state.repositories : undefined,
            repositoriesLoading: true,
            repositoriesError: undefined,
        };
        this.trigger(this.state);
    },
    loadRepositoriesError(err) {
        this.state = Object.assign(Object.assign({}, this.state), { repositories: undefined, repositoriesLoading: false, repositoriesError: err });
        this.trigger(this.state);
    },
    loadRepositoriesSuccess(data) {
        this.state = Object.assign(Object.assign({}, this.state), { repositories: data, repositoriesLoading: false, repositoriesError: undefined });
        this.trigger(this.state);
    },
    get() {
        return Object.assign({}, this.state);
    },
};
const RepositoryStore = reflux_1.default.createStore(storeConfig);
exports.default = RepositoryStore;
//# sourceMappingURL=repositoryStore.jsx.map