Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const release_1 = require("app/actionCreators/release");
const releaseStore_1 = (0, tslib_1.__importDefault)(require("app/stores/releaseStore"));
const getDisplayName_1 = (0, tslib_1.__importDefault)(require("app/utils/getDisplayName"));
function withRelease(WrappedComponent) {
    class WithRelease extends React.Component {
        constructor(props, context) {
            super(props, context);
            this.unsubscribe = releaseStore_1.default.listen(() => this.onStoreUpdate(), undefined);
            const { projectSlug, releaseVersion } = this.props;
            const releaseData = releaseStore_1.default.get(projectSlug, releaseVersion);
            this.state = Object.assign({}, releaseData);
        }
        componentDidMount() {
            this.fetchRelease();
            this.fetchDeploys();
        }
        componentWillUnmount() {
            this.unsubscribe();
        }
        fetchRelease() {
            const { api, organization, projectSlug, releaseVersion } = this.props;
            const releaseData = releaseStore_1.default.get(projectSlug, releaseVersion);
            const orgSlug = organization.slug;
            if ((!releaseData.release && !releaseData.releaseLoading) ||
                releaseData.releaseError) {
                (0, release_1.getProjectRelease)(api, { orgSlug, projectSlug, releaseVersion });
            }
        }
        fetchDeploys() {
            const { api, organization, projectSlug, releaseVersion } = this.props;
            const releaseData = releaseStore_1.default.get(projectSlug, releaseVersion);
            const orgSlug = organization.slug;
            if ((!releaseData.deploys && !releaseData.deploysLoading) ||
                releaseData.deploysError) {
                (0, release_1.getReleaseDeploys)(api, { orgSlug, projectSlug, releaseVersion });
            }
        }
        onStoreUpdate() {
            const { projectSlug, releaseVersion } = this.props;
            const releaseData = releaseStore_1.default.get(projectSlug, releaseVersion);
            this.setState(Object.assign({}, releaseData));
        }
        render() {
            return (<WrappedComponent {...this.props} {...this.state}/>);
        }
    }
    WithRelease.displayName = `withRelease(${(0, getDisplayName_1.default)(WrappedComponent)})`;
    return WithRelease;
}
exports.default = withRelease;
//# sourceMappingURL=withRelease.jsx.map