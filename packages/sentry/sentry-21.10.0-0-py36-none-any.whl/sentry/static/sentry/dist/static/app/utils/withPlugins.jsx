Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const plugins_1 = require("app/actionCreators/plugins");
const pluginsStore_1 = (0, tslib_1.__importDefault)(require("app/stores/pluginsStore"));
const utils_1 = require("app/utils");
const getDisplayName_1 = (0, tslib_1.__importDefault)(require("app/utils/getDisplayName"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const withProject_1 = (0, tslib_1.__importDefault)(require("app/utils/withProject"));
/**
 * Higher order component that fetches list of plugins and
 * passes PluginsStore to component as `plugins`
 */
function withPlugins(WrappedComponent) {
    class WithPlugins extends React.Component {
        constructor() {
            super(...arguments);
            this.state = { plugins: [], loading: true };
            this.unsubscribe = pluginsStore_1.default.listen(({ plugins, loading }) => {
                // State is destructured as store updates contain additional keys
                // that are not exposed by this HoC
                this.setState({ plugins, loading });
            }, undefined);
        }
        componentDidMount() {
            this.fetchPlugins();
        }
        componentDidUpdate(prevProps, _prevState, prevContext) {
            const { organization, project } = this.props;
            // Only fetch plugins when a org slug or project slug has changed
            const prevOrg = prevProps.organization || (prevContext === null || prevContext === void 0 ? void 0 : prevContext.organization);
            const prevProject = prevProps.project || (prevContext === null || prevContext === void 0 ? void 0 : prevContext.project);
            // If previous org/project is undefined then it means:
            // the HoC has mounted, `fetchPlugins` has been called (via cDM), and
            // store was updated. We don't need to fetchPlugins again (or it will cause an infinite loop)
            //
            // This is for the unusual case where component is mounted and receives a new org/project prop
            // e.g. when switching projects via breadcrumbs in settings.
            if (!(0, utils_1.defined)(prevProject) || !(0, utils_1.defined)(prevOrg)) {
                return;
            }
            const isOrgSame = prevOrg.slug === organization.slug;
            const isProjectSame = prevProject.slug === (project === null || project === void 0 ? void 0 : project.slug);
            // Don't do anything if org and project are the same
            if (isOrgSame && isProjectSame) {
                return;
            }
            this.fetchPlugins();
        }
        componentWillUnmount() {
            this.unsubscribe();
        }
        fetchPlugins() {
            const { organization, project } = this.props;
            if (!project || !organization) {
                return;
            }
            (0, plugins_1.fetchPlugins)({ projectId: project.slug, orgId: organization.slug });
        }
        render() {
            return (<WrappedComponent {...this.props} plugins={this.state}/>);
        }
    }
    WithPlugins.displayName = `withPlugins(${(0, getDisplayName_1.default)(WrappedComponent)})`;
    return (0, withOrganization_1.default)((0, withProject_1.default)(WithPlugins));
}
exports.default = withPlugins;
//# sourceMappingURL=withPlugins.jsx.map