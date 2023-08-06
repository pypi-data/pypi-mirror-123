Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const rangeSlider_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/rangeSlider"));
const inputField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/inputField"));
function onChange(fieldOnChange, value, e) {
    fieldOnChange(value, e);
}
function defaultFormatMessageValue(value, props) {
    return (typeof props.formatLabel === 'function' && props.formatLabel(value)) || value;
}
function RangeField(_a) {
    var { formatMessageValue = defaultFormatMessageValue, disabled } = _a, otherProps = (0, tslib_1.__rest)(_a, ["formatMessageValue", "disabled"]);
    const resolvedDisabled = typeof disabled === 'function' ? disabled(otherProps) : disabled;
    const props = Object.assign(Object.assign({}, otherProps), { disabled: resolvedDisabled, formatMessageValue });
    return (<inputField_1.default {...props} field={(_a) => {
            var { onChange: fieldOnChange, onBlur, value } = _a, fieldProps = (0, tslib_1.__rest)(_a, ["onChange", "onBlur", "value"]);
            return (<rangeSlider_1.default {...fieldProps} value={value} onBlur={onBlur} onChange={(val, event) => onChange(fieldOnChange, val, event)}/>);
        }}/>);
}
exports.default = RangeField;
//# sourceMappingURL=rangeField.jsx.map