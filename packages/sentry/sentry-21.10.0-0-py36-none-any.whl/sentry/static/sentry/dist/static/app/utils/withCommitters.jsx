Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const committers_1 = require("app/actionCreators/committers");
const committerStore_1 = (0, tslib_1.__importDefault)(require("app/stores/committerStore"));
const getDisplayName_1 = (0, tslib_1.__importDefault)(require("app/utils/getDisplayName"));
const initialState = {
    committers: [],
};
function withCommitters(WrappedComponent) {
    class WithCommitters extends React.Component {
        constructor(props, context) {
            super(props, context);
            this.unsubscribe = committerStore_1.default.listen(() => this.onStoreUpdate(), undefined);
            const { organization, project, event } = this.props;
            const repoData = committerStore_1.default.get(organization.slug, project.slug, event.id);
            this.state = Object.assign(Object.assign({}, initialState), repoData);
        }
        componentDidMount() {
            const { group } = this.props;
            // No committers if group doesn't have any releases
            if (!!(group === null || group === void 0 ? void 0 : group.firstRelease)) {
                this.fetchCommitters();
            }
        }
        componentWillUnmount() {
            this.unsubscribe();
        }
        fetchCommitters() {
            const { api, organization, project, event } = this.props;
            const repoData = committerStore_1.default.get(organization.slug, project.slug, event.id);
            if ((!repoData.committers && !repoData.committersLoading) ||
                repoData.committersError) {
                (0, committers_1.getCommitters)(api, {
                    orgSlug: organization.slug,
                    projectSlug: project.slug,
                    eventId: event.id,
                });
            }
        }
        onStoreUpdate() {
            const { organization, project, event } = this.props;
            const repoData = committerStore_1.default.get(organization.slug, project.slug, event.id);
            this.setState({ committers: repoData.committers });
        }
        render() {
            const { committers = [] } = this.state;
            // XXX: We do not pass loading/error states because the components using
            // this HOC (suggestedOwners, eventCause) do not have loading/error states
            return (<WrappedComponent {...this.props} committers={committers}/>);
        }
    }
    WithCommitters.displayName = `withCommitters(${(0, getDisplayName_1.default)(WrappedComponent)})`;
    return WithCommitters;
}
exports.default = withCommitters;
//# sourceMappingURL=withCommitters.jsx.map