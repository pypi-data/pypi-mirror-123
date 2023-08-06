Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const selectControl_1 = (0, tslib_1.__importDefault)(require("app/components/forms/selectControl"));
const teamSelector_1 = (0, tslib_1.__importDefault)(require("app/components/forms/teamSelector"));
const selectMembers_1 = (0, tslib_1.__importDefault)(require("app/components/selectMembers"));
const types_1 = require("app/views/alerts/incidentRules/types");
const input_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/input"));
const getPlaceholderForType = (type) => {
    switch (type) {
        case types_1.ActionType.SLACK:
            return '@username or #channel';
        case types_1.ActionType.MSTEAMS:
            // no prefixes for msteams
            return 'username or channel';
        case types_1.ActionType.PAGERDUTY:
            return 'service';
        default:
            throw Error('Not implemented');
    }
};
function ActionTargetSelector(props) {
    const { action, availableAction, disabled, loading, onChange, organization, project } = props;
    const handleChangeTargetIdentifier = (value) => {
        onChange(value.value);
    };
    const handleChangeSpecificTargetIdentifier = (e) => {
        onChange(e.target.value);
    };
    switch (action.targetType) {
        case types_1.TargetType.TEAM:
        case types_1.TargetType.USER:
            const isTeam = action.targetType === types_1.TargetType.TEAM;
            return isTeam ? (<teamSelector_1.default disabled={disabled} key="team" project={project} value={action.targetIdentifier} onChange={handleChangeTargetIdentifier} useId/>) : (<selectMembers_1.default disabled={disabled} key="member" project={project} organization={organization} value={action.targetIdentifier} onChange={handleChangeTargetIdentifier}/>);
        case types_1.TargetType.SPECIFIC:
            return (availableAction === null || availableAction === void 0 ? void 0 : availableAction.options) ? (<selectControl_1.default isDisabled={disabled || loading} value={action.targetIdentifier} options={availableAction.options} onChange={handleChangeTargetIdentifier}/>) : (<input_1.default type="text" autoComplete="off" disabled={disabled} key={action.type} value={action.targetIdentifier || ''} onChange={handleChangeSpecificTargetIdentifier} placeholder={getPlaceholderForType(action.type)}/>);
        default:
            return null;
    }
}
exports.default = ActionTargetSelector;
//# sourceMappingURL=actionTargetSelector.jsx.map