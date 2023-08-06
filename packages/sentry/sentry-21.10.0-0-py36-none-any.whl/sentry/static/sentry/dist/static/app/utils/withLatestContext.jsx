Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const latestContextStore_1 = (0, tslib_1.__importDefault)(require("app/stores/latestContextStore"));
const getDisplayName_1 = (0, tslib_1.__importDefault)(require("app/utils/getDisplayName"));
const withOrganizations_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganizations"));
const fallbackContext = {
    organization: null,
    project: null,
    lastRoute: null,
};
function withLatestContext(WrappedComponent) {
    class WithLatestContext extends React.Component {
        constructor() {
            super(...arguments);
            this.state = {
                latestContext: latestContextStore_1.default.get(),
            };
            this.unsubscribe = latestContextStore_1.default.listen((latestContext) => this.setState({ latestContext }), undefined);
        }
        componentWillUmount() {
            this.unsubscribe();
        }
        render() {
            const { organizations } = this.props;
            const { latestContext } = this.state;
            const { organization, project, lastRoute } = latestContext || fallbackContext;
            // Even though org details exists in LatestContextStore,
            // fetch organization from OrganizationsStore so that we can
            // expect consistent data structure because OrganizationsStore has a list
            // of orgs but not full org details
            const latestOrganization = organization ||
                (organizations && organizations.length
                    ? organizations.find(({ slug }) => slug === configStore_1.default.get('lastOrganization')) || organizations[0]
                    : null);
            // TODO(billy): Below is going to be wrong if component is passed project, it will override
            // project from `latestContext`
            return (<WrappedComponent project={project} lastRoute={lastRoute} {...this.props} organization={(this.props.organization || latestOrganization)}/>);
        }
    }
    WithLatestContext.displayName = `withLatestContext(${(0, getDisplayName_1.default)(WrappedComponent)})`;
    return (0, withOrganizations_1.default)(WithLatestContext);
}
exports.default = withLatestContext;
//# sourceMappingURL=withLatestContext.jsx.map