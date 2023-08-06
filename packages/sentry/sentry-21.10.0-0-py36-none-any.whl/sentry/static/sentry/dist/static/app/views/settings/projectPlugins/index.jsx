Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const plugins_1 = require("app/actionCreators/plugins");
const sentryDocumentTitle_1 = (0, tslib_1.__importDefault)(require("app/components/sentryDocumentTitle"));
const locale_1 = require("app/locale");
const integrationUtil_1 = require("app/utils/integrationUtil");
const withPlugins_1 = (0, tslib_1.__importDefault)(require("app/utils/withPlugins"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const permissionAlert_1 = (0, tslib_1.__importDefault)(require("app/views/settings/project/permissionAlert"));
const projectPlugins_1 = (0, tslib_1.__importDefault)(require("./projectPlugins"));
class ProjectPluginsContainer extends React.Component {
    constructor() {
        super(...arguments);
        this.fetchData = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const plugins = yield (0, plugins_1.fetchPlugins)(this.props.params);
            const installCount = plugins.filter(plugin => plugin.hasConfiguration && plugin.enabled).length;
            (0, integrationUtil_1.trackIntegrationAnalytics)('integrations.index_viewed', {
                integrations_installed: installCount,
                view: 'legacy_integrations',
                organization: this.props.organization,
            }, { startSession: true });
        });
        this.handleChange = (pluginId, shouldEnable) => {
            const { projectId, orgId } = this.props.params;
            const actionCreator = shouldEnable ? plugins_1.enablePlugin : plugins_1.disablePlugin;
            actionCreator({ projectId, orgId, pluginId });
        };
    }
    componentDidMount() {
        this.fetchData();
    }
    render() {
        const { loading, error, plugins } = this.props.plugins || {};
        const { orgId } = this.props.params;
        const title = (0, locale_1.t)('Legacy Integrations');
        return (<React.Fragment>
        <sentryDocumentTitle_1.default title={title} orgSlug={orgId}/>
        <settingsPageHeader_1.default title={title}/>
        <permissionAlert_1.default />

        <projectPlugins_1.default {...this.props} onChange={this.handleChange} loading={loading} error={error} plugins={plugins}/>
      </React.Fragment>);
    }
}
exports.default = (0, withPlugins_1.default)(ProjectPluginsContainer);
//# sourceMappingURL=index.jsx.map