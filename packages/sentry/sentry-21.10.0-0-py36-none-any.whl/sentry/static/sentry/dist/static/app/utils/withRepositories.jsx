Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const repositories_1 = require("app/actionCreators/repositories");
const repositoryActions_1 = (0, tslib_1.__importDefault)(require("app/actions/repositoryActions"));
const repositoryStore_1 = (0, tslib_1.__importDefault)(require("app/stores/repositoryStore"));
const getDisplayName_1 = (0, tslib_1.__importDefault)(require("app/utils/getDisplayName"));
const INITIAL_STATE = {
    repositories: undefined,
    repositoriesLoading: undefined,
    repositoriesError: undefined,
};
function withRepositories(WrappedComponent) {
    class WithRepositories extends React.Component {
        constructor(props, context) {
            super(props, context);
            this.unsubscribe = repositoryStore_1.default.listen(() => this.onStoreUpdate(), undefined);
            const { organization } = this.props;
            const orgSlug = organization.slug;
            const repoData = repositoryStore_1.default.get();
            if (repoData.orgSlug !== orgSlug) {
                repositoryActions_1.default.resetRepositories();
            }
            this.state =
                repoData.orgSlug === orgSlug
                    ? Object.assign(Object.assign({}, INITIAL_STATE), repoData) : Object.assign({}, INITIAL_STATE);
        }
        componentDidMount() {
            // XXX(leedongwei): Do not move this function call unless you modify the
            // unit test named "prevents repeated calls"
            this.fetchRepositories();
        }
        componentWillUnmount() {
            this.unsubscribe();
        }
        fetchRepositories() {
            const { api, organization } = this.props;
            const orgSlug = organization.slug;
            const repoData = repositoryStore_1.default.get();
            // XXX(leedongwei): Do not check the orgSlug here. It would have been
            // verified at `getInitialState`. The short-circuit hack in actionCreator
            // does not update the orgSlug in the store.
            if ((!repoData.repositories && !repoData.repositoriesLoading) ||
                repoData.repositoriesError) {
                (0, repositories_1.getRepositories)(api, { orgSlug });
            }
        }
        onStoreUpdate() {
            const repoData = repositoryStore_1.default.get();
            this.setState(Object.assign({}, repoData));
        }
        render() {
            return <WrappedComponent {...this.props} {...this.state}/>;
        }
    }
    WithRepositories.displayName = `withRepositories(${(0, getDisplayName_1.default)(WrappedComponent)})`;
    return WithRepositories;
}
exports.default = withRepositories;
//# sourceMappingURL=withRepositories.jsx.map