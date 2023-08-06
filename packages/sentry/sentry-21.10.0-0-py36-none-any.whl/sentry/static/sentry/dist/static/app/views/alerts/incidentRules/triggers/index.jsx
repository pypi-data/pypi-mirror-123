Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const panels_1 = require("app/components/panels");
const removeAtArrayIndex_1 = require("app/utils/removeAtArrayIndex");
const replaceAtArrayIndex_1 = require("app/utils/replaceAtArrayIndex");
const actionsPanel_1 = (0, tslib_1.__importDefault)(require("app/views/alerts/incidentRules/triggers/actionsPanel"));
const form_1 = (0, tslib_1.__importDefault)(require("app/views/alerts/incidentRules/triggers/form"));
/**
 * A list of forms to add, edit, and delete triggers.
 */
class Triggers extends react_1.Component {
    constructor() {
        super(...arguments);
        this.handleDeleteTrigger = (index) => {
            const { triggers, onChange } = this.props;
            const updatedTriggers = (0, removeAtArrayIndex_1.removeAtArrayIndex)(triggers, index);
            onChange(updatedTriggers);
        };
        this.handleChangeTrigger = (triggerIndex, trigger, changeObj) => {
            const { triggers, onChange } = this.props;
            const updatedTriggers = (0, replaceAtArrayIndex_1.replaceAtArrayIndex)(triggers, triggerIndex, trigger);
            onChange(updatedTriggers, triggerIndex, changeObj);
        };
        this.handleAddAction = (triggerIndex, action) => {
            const { onChange, triggers } = this.props;
            const trigger = triggers[triggerIndex];
            const actions = [...trigger.actions, action];
            const updatedTriggers = (0, replaceAtArrayIndex_1.replaceAtArrayIndex)(triggers, triggerIndex, Object.assign(Object.assign({}, trigger), { actions }));
            onChange(updatedTriggers, triggerIndex, { actions });
        };
        this.handleChangeActions = (triggerIndex, triggers, actions) => {
            const { onChange } = this.props;
            const trigger = triggers[triggerIndex];
            const updatedTriggers = (0, replaceAtArrayIndex_1.replaceAtArrayIndex)(triggers, triggerIndex, Object.assign(Object.assign({}, trigger), { actions }));
            onChange(updatedTriggers, triggerIndex, { actions });
        };
    }
    render() {
        const { availableActions, currentProject, errors, organization, projects, triggers, disabled, aggregate, thresholdType, comparisonType, resolveThreshold, onThresholdTypeChange, onResolveThresholdChange, } = this.props;
        // Note we only support 2 triggers max
        return (<react_1.Fragment>
        <panels_1.Panel>
          <panels_1.PanelBody>
            <form_1.default disabled={disabled} errors={errors} organization={organization} projects={projects} triggers={triggers} aggregate={aggregate} resolveThreshold={resolveThreshold} thresholdType={thresholdType} comparisonType={comparisonType} onChange={this.handleChangeTrigger} onThresholdTypeChange={onThresholdTypeChange} onResolveThresholdChange={onResolveThresholdChange}/>
          </panels_1.PanelBody>
        </panels_1.Panel>

        <actionsPanel_1.default disabled={disabled} loading={availableActions === null} error={false} availableActions={availableActions} currentProject={currentProject} organization={organization} projects={projects} triggers={triggers} onChange={this.handleChangeActions} onAdd={this.handleAddAction}/>
      </react_1.Fragment>);
    }
}
exports.default = Triggers;
//# sourceMappingURL=index.jsx.map