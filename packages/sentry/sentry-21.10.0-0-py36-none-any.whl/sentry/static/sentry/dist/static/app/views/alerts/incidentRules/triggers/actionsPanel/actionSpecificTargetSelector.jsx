Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const locale_1 = require("app/locale");
const types_1 = require("app/views/alerts/incidentRules/types");
const input_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/input"));
function ActionSpecificTargetSelector({ action, disabled, onChange }) {
    const handleChangeSpecificTargetIdentifier = (e) => {
        onChange(e.target.value);
    };
    if (action.targetType !== types_1.TargetType.SPECIFIC || action.type !== types_1.ActionType.SLACK) {
        return null;
    }
    return (<input_1.default type="text" autoComplete="off" disabled={disabled} key="inputChannelId" value={action.inputChannelId || ''} onChange={handleChangeSpecificTargetIdentifier} placeholder={(0, locale_1.t)('optional: channel ID or user ID')}/>);
}
exports.default = ActionSpecificTargetSelector;
//# sourceMappingURL=actionSpecificTargetSelector.jsx.map