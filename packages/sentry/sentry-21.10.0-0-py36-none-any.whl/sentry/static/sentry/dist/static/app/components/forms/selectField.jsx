Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const utils_1 = require("app/utils");
const form_1 = require("./form");
const formField_1 = (0, tslib_1.__importDefault)(require("./formField"));
const selectControl_1 = (0, tslib_1.__importDefault)(require("./selectControl"));
class SelectField extends formField_1.default {
    constructor() {
        super(...arguments);
        this.onChange = opt => {
            // Changing this will most likely break react-select (e.g. you won't be able to select
            // a menu option that is from an async request, or a multi select).
            this.setValue(opt);
        };
    }
    UNSAFE_componentWillReceiveProps(nextProps, nextContext) {
        const newError = this.getError(nextProps, nextContext);
        if (newError !== this.state.error) {
            this.setState({ error: newError });
        }
        if (this.props.value !== nextProps.value || (0, utils_1.defined)(nextContext.form)) {
            const newValue = this.getValue(nextProps, nextContext);
            // This is the only thing that is different from parent, we compare newValue against coerced value in state
            // To remain compatible with react-select, we need to store the option object that
            // includes `value` and `label`, but when we submit the format, we need to coerce it
            // to just return `value`. Also when field changes, it propagates the coerced value up
            const coercedValue = this.coerceValue(this.state.value);
            // newValue can be empty string because of `getValue`, while coerceValue needs to return null (to differentiate
            // empty string from cleared item). We could use `!=` to compare, but lets be a bit more explicit with strict equality
            //
            // This can happen when this is apart of a field, and it re-renders onChange for a different field,
            // there will be a mismatch between this component's state.value and `this.getValue` result above
            if (newValue !== coercedValue && !!newValue !== !!coercedValue) {
                this.setValue(newValue);
            }
        }
    }
    // Overriding this so that we can support `multi` fields through property
    getValue(props, context) {
        const form = (context || this.context || {}).form;
        props = props || this.props;
        // Don't use `isMultiple` here because we're taking props from args as well
        const defaultValue = this.isMultiple(props) ? [] : '';
        if ((0, utils_1.defined)(props.value)) {
            return props.value;
        }
        if (form && form.data.hasOwnProperty(props.name)) {
            return (0, utils_1.defined)(form.data[props.name]) ? form.data[props.name] : defaultValue;
        }
        return (0, utils_1.defined)(props.defaultValue) ? props.defaultValue : defaultValue;
    }
    // We need this to get react-select's `Creatable` to work properly
    // Otherwise, when you hit "enter" to create a new item, the "selected value" does
    // not update with new value (and also new value is not displayed in dropdown)
    //
    // This is also needed to get `multi` select working since we need the {label, value} object
    // for react-select (but forms expect just the value to be propagated)
    coerceValue(value) {
        if (!value) {
            return '';
        }
        if (this.isMultiple()) {
            return value.map(v => v.value);
        }
        else if (value.hasOwnProperty('value')) {
            return value.value;
        }
        return value;
    }
    isMultiple(props) {
        props = props || this.props;
        // this is to maintain compatibility with the 'multi' prop
        return props.multi || props.multiple;
    }
    getClassName() {
        return '';
    }
    getField() {
        const { options, clearable, creatable, choices, placeholder, disabled, name, isLoading, } = this.props;
        return (<StyledSelectControl creatable={creatable} id={this.getId()} choices={choices} options={options} placeholder={placeholder} disabled={disabled} value={this.state.value} onChange={this.onChange} clearable={clearable} multiple={this.isMultiple()} name={name} isLoading={isLoading}/>);
    }
}
exports.default = SelectField;
SelectField.defaultProps = Object.assign(Object.assign({}, formField_1.default.defaultProps), { clearable: true, multiple: false });
// This is to match other fields that are wrapped by a `div.control-group`
const StyledSelectControl = (0, styled_1.default)(selectControl_1.default) `
  ${form_1.StyledForm} &, .form-stacked & {
    .control-group & {
      margin-bottom: 0;
    }

    margin-bottom: 15px;
  }
`;
//# sourceMappingURL=selectField.jsx.map