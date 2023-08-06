Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const selectControl_1 = (0, tslib_1.__importDefault)(require("app/components/forms/selectControl"));
const teamSelector_1 = (0, tslib_1.__importDefault)(require("app/components/forms/teamSelector"));
const panels_1 = require("app/components/panels");
const selectMembers_1 = (0, tslib_1.__importDefault)(require("app/components/selectMembers"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
class MemberTeamFields extends React.Component {
    constructor() {
        super(...arguments);
        this.handleChange = (attribute, newValue) => {
            const { onChange, ruleData } = this.props;
            if (newValue === ruleData[attribute]) {
                return;
            }
            const newData = Object.assign(Object.assign({}, ruleData), { [attribute]: newValue });
            /**
             * TargetIdentifiers between the targetTypes are not unique, and may wrongly map to something that has not been
             * selected. E.g. A member and project can both have the `targetIdentifier`, `'2'`. Hence we clear the identifier.
             **/
            if (attribute === 'targetType') {
                newData.targetIdentifier = '';
            }
            onChange(newData);
        };
        this.handleChangeActorType = (optionRecord) => {
            this.handleChange('targetType', optionRecord.value);
        };
        this.handleChangeActorId = (optionRecord) => {
            this.handleChange('targetIdentifier', optionRecord.value);
        };
    }
    render() {
        const { disabled, loading, project, organization, ruleData, memberValue, teamValue, options, } = this.props;
        const teamSelected = ruleData.targetType === teamValue;
        const memberSelected = ruleData.targetType === memberValue;
        const selectControlStyles = {
            control: provided => (Object.assign(Object.assign({}, provided), { minHeight: '28px', height: '28px' })),
        };
        return (<PanelItemGrid>
        <selectControl_1.default isClearable={false} isDisabled={disabled || loading} value={ruleData.targetType} styles={selectControlStyles} options={options} onChange={this.handleChangeActorType}/>
        {teamSelected ? (<teamSelector_1.default disabled={disabled} key={teamValue} project={project} 
            // The value from the endpoint is of type `number`, `SelectMembers` require value to be of type `string`
            value={`${ruleData.targetIdentifier}`} styles={selectControlStyles} onChange={this.handleChangeActorId} useId/>) : memberSelected ? (<selectMembers_1.default disabled={disabled} key={teamSelected ? teamValue : memberValue} project={project} organization={organization} 
            // The value from the endpoint is of type `number`, `SelectMembers` require value to be of type `string`
            value={`${ruleData.targetIdentifier}`} styles={selectControlStyles} onChange={this.handleChangeActorId}/>) : null}
      </PanelItemGrid>);
    }
}
const PanelItemGrid = (0, styled_1.default)(panels_1.PanelItem) `
  display: grid;
  grid-template-columns: 200px 200px;
  padding: 0;
  align-items: center;
  grid-gap: ${(0, space_1.default)(2)};
`;
exports.default = MemberTeamFields;
//# sourceMappingURL=memberTeamFields.jsx.map