Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const React = (0, tslib_1.__importStar)(require("react"));
const access_1 = (0, tslib_1.__importDefault)(require("app/components/acl/access"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const routeError_1 = (0, tslib_1.__importDefault)(require("app/views/routeError"));
const projectPluginRow_1 = (0, tslib_1.__importDefault)(require("./projectPluginRow"));
class ProjectPlugins extends react_1.Component {
    render() {
        const { plugins, loading, error, onChange, routes, params, project } = this.props;
        const { orgId } = this.props.params;
        const hasError = error;
        const isLoading = !hasError && loading;
        if (hasError) {
            return <routeError_1.default error={error}/>;
        }
        if (isLoading) {
            return <loadingIndicator_1.default />;
        }
        return (<panels_1.Panel>
        <panels_1.PanelHeader>
          <div>{(0, locale_1.t)('Legacy Integration')}</div>
          <div>{(0, locale_1.t)('Enabled')}</div>
        </panels_1.PanelHeader>
        <panels_1.PanelBody>
          <panels_1.PanelAlert type="warning">
            <access_1.default access={['org:integrations']}>
              {({ hasAccess }) => hasAccess
                ? (0, locale_1.tct)("Legacy Integrations must be configured per-project. It's recommended to prefer organization integrations over the legacy project integrations when available. Visit the [link:organization integrations] settings to manage them.", {
                    link: <link_1.default to={`/settings/${orgId}/integrations`}/>,
                })
                : (0, locale_1.t)("Legacy Integrations must be configured per-project. It's recommended to prefer organization integrations over the legacy project integrations when available.")}
            </access_1.default>
          </panels_1.PanelAlert>

          {plugins
                .filter(p => {
                return !p.isHidden;
            })
                .map(plugin => (<panels_1.PanelItem key={plugin.id}>
                <projectPluginRow_1.default params={params} routes={routes} project={project} {...plugin} onChange={onChange}/>
              </panels_1.PanelItem>))}
        </panels_1.PanelBody>
      </panels_1.Panel>);
    }
}
exports.default = ProjectPlugins;
//# sourceMappingURL=projectPlugins.jsx.map