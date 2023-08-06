Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const sdkUpdates_1 = require("app/actionCreators/sdkUpdates");
const sdkUpdatesStore_1 = (0, tslib_1.__importDefault)(require("app/stores/sdkUpdatesStore"));
const withApi_1 = (0, tslib_1.__importDefault)(require("./withApi"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("./withOrganization"));
function withSdkUpdates(WrappedComponent) {
    class WithProjectSdkSuggestions extends React.Component {
        constructor() {
            super(...arguments);
            this.state = { sdkUpdates: [] };
            this.unsubscribe = sdkUpdatesStore_1.default.listen(() => this.onSdkUpdatesUpdate(), undefined);
        }
        componentDidMount() {
            const orgSlug = this.props.organization.slug;
            const updates = sdkUpdatesStore_1.default.getUpdates(orgSlug);
            // Load SdkUpdates
            if (updates !== undefined) {
                this.onSdkUpdatesUpdate();
                return;
            }
            (0, sdkUpdates_1.loadSdkUpdates)(this.props.api, orgSlug);
        }
        componentWillUnmount() {
            this.unsubscribe();
        }
        onSdkUpdatesUpdate() {
            var _a;
            const sdkUpdates = (_a = sdkUpdatesStore_1.default.getUpdates(this.props.organization.slug)) !== null && _a !== void 0 ? _a : null;
            this.setState({ sdkUpdates });
        }
        render() {
            // TODO(ts) This unknown cast isn't great but Typescript complains about arbitrary
            // types being possible. I think this is related to the additional HoC wrappers causing type data to
            // be lost.
            return (<WrappedComponent {...this.props} sdkUpdates={this.state.sdkUpdates}/>);
        }
    }
    return (0, withOrganization_1.default)((0, withApi_1.default)(WithProjectSdkSuggestions));
}
exports.default = withSdkUpdates;
//# sourceMappingURL=withSdkUpdates.jsx.map