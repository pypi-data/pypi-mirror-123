Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const plugins_1 = require("app/actionCreators/plugins");
const inactivePlugins_1 = (0, tslib_1.__importDefault)(require("app/components/inactivePlugins"));
const pluginConfig_1 = (0, tslib_1.__importDefault)(require("app/components/pluginConfig"));
const locale_1 = require("app/locale");
const panels_1 = require("./panels");
const PluginList = ({ organization, project, pluginList, onDisablePlugin = () => { }, onEnablePlugin = () => { }, }) => {
    const handleEnablePlugin = (plugin) => {
        (0, plugins_1.enablePlugin)({
            projectId: project.slug,
            orgId: organization.slug,
            pluginId: plugin.slug,
        });
        onEnablePlugin(plugin);
    };
    const handleDisablePlugin = (plugin) => {
        (0, plugins_1.disablePlugin)({
            projectId: project.slug,
            orgId: organization.slug,
            pluginId: plugin.slug,
        });
        onDisablePlugin(plugin);
    };
    if (!pluginList.length) {
        return (<panels_1.Panel>
        <panels_1.PanelItem>
          {(0, locale_1.t)("Oops! Looks like there aren't any available integrations installed.")}
        </panels_1.PanelItem>
      </panels_1.Panel>);
    }
    return (<div>
      {pluginList
            .filter(p => p.enabled)
            .map(data => (<pluginConfig_1.default data={data} organization={organization} project={project} key={data.id} onDisablePlugin={handleDisablePlugin}/>))}

      <inactivePlugins_1.default plugins={pluginList.filter(p => !p.enabled && !p.isHidden)} onEnablePlugin={handleEnablePlugin}/>
    </div>);
};
exports.default = PluginList;
//# sourceMappingURL=pluginList.jsx.map