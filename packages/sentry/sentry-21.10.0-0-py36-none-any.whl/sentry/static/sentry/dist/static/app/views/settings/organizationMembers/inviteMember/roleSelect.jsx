Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const panels_1 = require("app/components/panels");
const radio_1 = (0, tslib_1.__importDefault)(require("app/components/radio"));
const locale_1 = require("app/locale");
const textBlock_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/text/textBlock"));
const Label = (0, styled_1.default)('label') `
  display: flex;
  flex: 1;
  align-items: center;
  margin-bottom: 0;
`;
class RoleSelect extends react_1.Component {
    render() {
        const { disabled, enforceAllowed, roleList, selectedRole } = this.props;
        return (<panels_1.Panel>
        <panels_1.PanelHeader>{(0, locale_1.t)('Role')}</panels_1.PanelHeader>

        <panels_1.PanelBody>
          {roleList.map(role => {
                const { desc, name, id, allowed } = role;
                const isDisabled = disabled || (enforceAllowed && !allowed);
                return (<panels_1.PanelItem key={id} onClick={() => !isDisabled && this.props.setRole(id)} css={!isDisabled ? {} : { color: 'grey', cursor: 'default' }}>
                <Label>
                  <radio_1.default id={id} value={name} checked={id === selectedRole} readOnly/>
                  <div style={{ flex: 1, padding: '0 16px' }}>
                    {name}
                    <textBlock_1.default noMargin>
                      <div className="help-block">{desc}</div>
                    </textBlock_1.default>
                  </div>
                </Label>
              </panels_1.PanelItem>);
            })}
        </panels_1.PanelBody>
      </panels_1.Panel>);
    }
}
exports.default = RoleSelect;
//# sourceMappingURL=roleSelect.jsx.map