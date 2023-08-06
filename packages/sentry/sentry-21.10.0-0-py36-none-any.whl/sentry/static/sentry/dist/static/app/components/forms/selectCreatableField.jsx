Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const form_1 = require("app/components/forms/form");
const selectControl_1 = (0, tslib_1.__importDefault)(require("app/components/forms/selectControl"));
const selectField_1 = (0, tslib_1.__importDefault)(require("app/components/forms/selectField"));
const utils_1 = require("app/utils");
const convertFromSelect2Choices_1 = (0, tslib_1.__importDefault)(require("app/utils/convertFromSelect2Choices"));
/**
 * This is a <SelectField> that allows the user to create new options if one does't exist.
 *
 * This is used in some integrations
 */
class SelectCreatableField extends selectField_1.default {
    constructor(props, context) {
        super(props, context);
        // We only want to parse options once because react-select relies
        // on `options` mutation when you create a new option
        //
        // Otherwise you will not get the created option in the dropdown menu
        this.options = this.getOptions(props);
    }
    UNSAFE_componentWillReceiveProps(nextProps, nextContext) {
        const newError = this.getError(nextProps, nextContext);
        if (newError !== this.state.error) {
            this.setState({ error: newError });
        }
        if (this.props.value !== nextProps.value || (0, utils_1.defined)(nextContext.form)) {
            const newValue = this.getValue(nextProps, nextContext);
            // This is the only thing that is different from parent, we compare newValue against coerved value in state
            // To remain compatible with react-select, we need to store the option object that
            // includes `value` and `label`, but when we submit the format, we need to coerce it
            // to just return `value`. Also when field changes, it propagates the coerced value up
            const coercedValue = this.coerceValue(this.state.value);
            // newValue can be empty string because of `getValue`, while coerceValue needs to return null (to differentiate
            // empty string from cleared item). We could use `!=` to compare, but lets be a bit more explicit with strict equality
            //
            // This can happen when this is apart of a field, and it re-renders onChange for a different field,
            // there will be a mismatch between this component's state.value and `this.getValue` result above
            if (newValue !== coercedValue &&
                !!newValue !== !!coercedValue &&
                newValue !== this.state.value) {
                this.setValue(newValue);
            }
        }
    }
    getOptions(props) {
        return (0, convertFromSelect2Choices_1.default)(props.choices) || props.options;
    }
    getField() {
        const { placeholder, disabled, clearable, name } = this.props;
        return (<StyledSelectControl creatable id={this.getId()} options={this.options} placeholder={placeholder} disabled={disabled} value={this.state.value} onChange={this.onChange} clearable={clearable} multiple={this.isMultiple()} name={name}/>);
    }
}
exports.default = SelectCreatableField;
// This is because we are removing `control-group` class name which provides margin-bottom
const StyledSelectControl = (0, styled_1.default)(selectControl_1.default) `
  ${form_1.StyledForm} &, .form-stacked & {
    .control-group & {
      margin-bottom: 0;
    }

    margin-bottom: 15px;
  }
`;
//# sourceMappingURL=selectCreatableField.jsx.map