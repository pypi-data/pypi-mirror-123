Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const panels_1 = require("app/components/panels");
const textOverflow_1 = (0, tslib_1.__importDefault)(require("app/components/textOverflow"));
const locale_1 = require("app/locale");
const pluginIcon_1 = (0, tslib_1.__importDefault)(require("app/plugins/components/pluginIcon"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const InactivePlugins = ({ plugins, onEnablePlugin }) => {
    if (plugins.length === 0) {
        return null;
    }
    return (<panels_1.Panel>
      <panels_1.PanelHeader>{(0, locale_1.t)('Inactive Integrations')}</panels_1.PanelHeader>

      <panels_1.PanelBody>
        <Plugins>
          {plugins.map(plugin => (<IntegrationButton key={plugin.id} onClick={() => onEnablePlugin(plugin)} className={`ref-plugin-enable-${plugin.id}`}>
              <Label>
                <StyledPluginIcon pluginId={plugin.id}/>
                <textOverflow_1.default>{plugin.shortName || plugin.name}</textOverflow_1.default>
              </Label>
            </IntegrationButton>))}
        </Plugins>
      </panels_1.PanelBody>
    </panels_1.Panel>);
};
const Plugins = (0, styled_1.default)('div') `
  display: flex;
  padding: ${(0, space_1.default)(1)};
  flex: 1;
  flex-wrap: wrap;
`;
const IntegrationButton = (0, styled_1.default)('button') `
  margin: ${(0, space_1.default)(1)};
  width: 175px;
  text-align: center;
  font-size: ${p => p.theme.fontSizeSmall};
  color: #889ab0;
  letter-spacing: 0.1px;
  font-weight: 600;
  text-transform: uppercase;
  border: 1px solid #eee;
  background: inherit;
  border-radius: ${p => p.theme.borderRadius};
  padding: 10px;

  &:hover {
    border-color: #ccc;
  }
`;
const Label = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  justify-content: center;
`;
const StyledPluginIcon = (0, styled_1.default)(pluginIcon_1.default) `
  margin-right: ${(0, space_1.default)(1)};
`;
exports.default = InactivePlugins;
//# sourceMappingURL=inactivePlugins.jsx.map