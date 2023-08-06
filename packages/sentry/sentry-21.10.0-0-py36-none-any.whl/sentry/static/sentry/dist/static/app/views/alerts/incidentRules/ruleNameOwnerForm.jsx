Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const teamSelector_1 = (0, tslib_1.__importDefault)(require("app/components/forms/teamSelector"));
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const formField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/formField"));
const textField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/textField"));
class RuleNameOwnerForm extends react_1.PureComponent {
    render() {
        const { disabled, project } = this.props;
        return (<panels_1.Panel>
        <panels_1.PanelBody>
          <textField_1.default disabled={disabled} name="name" label={(0, locale_1.t)('Rule Name')} help={(0, locale_1.t)('Add a name so it’s easy to find later.')} placeholder={(0, locale_1.t)('Something really bad happened')} required/>

          <formField_1.default name="owner" label={(0, locale_1.t)('Team')} help={(0, locale_1.t)('The team that can edit this alert.')} disabled={disabled}>
            {({ model }) => {
                const owner = model.getValue('owner');
                const ownerId = owner && owner.split(':')[1];
                return (<teamSelector_1.default value={ownerId} project={project} onChange={({ value }) => {
                        const ownerValue = value && `team:${value}`;
                        model.setValue('owner', ownerValue);
                    }} teamFilter={(team) => team.isMember || team.id === ownerId} useId includeUnassigned disabled={disabled}/>);
            }}
          </formField_1.default>
        </panels_1.PanelBody>
      </panels_1.Panel>);
    }
}
exports.default = RuleNameOwnerForm;
//# sourceMappingURL=ruleNameOwnerForm.jsx.map