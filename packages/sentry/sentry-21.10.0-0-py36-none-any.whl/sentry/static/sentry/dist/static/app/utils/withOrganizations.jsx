Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const organizationsStore_1 = (0, tslib_1.__importDefault)(require("app/stores/organizationsStore"));
const getDisplayName_1 = (0, tslib_1.__importDefault)(require("app/utils/getDisplayName"));
function withOrganizations(WrappedComponent) {
    class WithOrganizations extends React.Component {
        constructor() {
            super(...arguments);
            this.state = { organizations: organizationsStore_1.default.getAll() };
            this.unsubscribe = organizationsStore_1.default.listen((organizations) => this.setState({ organizations }), undefined);
        }
        componentWillUnmount() {
            this.unsubscribe();
        }
        render() {
            const _a = this.props, { organizationsLoading, organizations } = _a, props = (0, tslib_1.__rest)(_a, ["organizationsLoading", "organizations"]);
            return (<WrappedComponent {...Object.assign({ organizationsLoading: organizationsLoading !== null && organizationsLoading !== void 0 ? organizationsLoading : !organizationsStore_1.default.loaded, organizations: organizations !== null && organizations !== void 0 ? organizations : this.state.organizations }, props)}/>);
        }
    }
    WithOrganizations.displayName = `withOrganizations(${(0, getDisplayName_1.default)(WrappedComponent)})`;
    return WithOrganizations;
}
exports.default = withOrganizations;
//# sourceMappingURL=withOrganizations.jsx.map