Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const mobx_react_1 = require("mobx-react");
const state_1 = (0, tslib_1.__importDefault)(require("app/components/forms/state"));
const controlState_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field/controlState"));
/**
 * ControlState (i.e. loading/error icons) for connected form components
 */
const FormFieldControlState = ({ model, name }) => (<mobx_react_1.Observer>
    {() => {
        const isSaving = model.getFieldState(name, state_1.default.SAVING);
        const isSaved = model.getFieldState(name, state_1.default.READY);
        const error = model.getError(name);
        return <controlState_1.default isSaving={isSaving} isSaved={isSaved} error={error}/>;
    }}
  </mobx_react_1.Observer>);
exports.default = FormFieldControlState;
//# sourceMappingURL=controlState.jsx.map