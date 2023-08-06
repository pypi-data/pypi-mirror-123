Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const confirm_1 = require("app/components/confirm");
const selectControl_1 = (0, tslib_1.__importDefault)(require("app/components/forms/selectControl"));
const locale_1 = require("app/locale");
const inputField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/inputField"));
function getChoices(props) {
    const choices = props.choices;
    if (typeof choices === 'function') {
        return choices(props);
    }
    if (choices === undefined) {
        return [];
    }
    return choices;
}
/**
 * Required to type guard for OptionsType<T> which is a readonly Array
 */
function isArray(maybe) {
    return Array.isArray(maybe);
}
class SelectField extends React.Component {
    constructor() {
        super(...arguments);
        this.handleChange = (onBlur, onChange, optionObj) => {
            let value = undefined;
            // If optionObj is empty, then it probably means that the field was "cleared"
            if (!optionObj) {
                value = optionObj;
            }
            else if (this.props.multiple && isArray(optionObj)) {
                // List of optionObjs
                value = optionObj.map(({ value: val }) => val);
            }
            else if (!isArray(optionObj)) {
                value = optionObj.value;
            }
            onChange === null || onChange === void 0 ? void 0 : onChange(value, {});
            onBlur === null || onBlur === void 0 ? void 0 : onBlur(value, {});
        };
    }
    render() {
        const _a = this.props, { allowClear, confirm, multiple, small } = _a, otherProps = (0, tslib_1.__rest)(_a, ["allowClear", "confirm", "multiple", "small"]);
        return (<inputField_1.default {...otherProps} alignRight={small} field={(_a) => {
                var { onChange, onBlur, required: _required } = _a, props = (0, tslib_1.__rest)(_a, ["onChange", "onBlur", "required"]);
                return (<selectControl_1.default {...props} clearable={allowClear} multiple={multiple} onChange={val => {
                        var _a, _b, _c;
                        if (!confirm) {
                            this.handleChange(onBlur, onChange, val);
                            return;
                        }
                        // Support 'confirming' selections. This only works with
                        // `val` objects that use the new-style options format
                        const previousValue = (_a = props.value) === null || _a === void 0 ? void 0 : _a.toString();
                        // `val` may be null if clearing the select for an optional field
                        const newValue = (_b = val === null || val === void 0 ? void 0 : val.value) === null || _b === void 0 ? void 0 : _b.toString();
                        // Value not marked for confirmation, or hasn't changed
                        if (!confirm[newValue] || previousValue === newValue) {
                            this.handleChange(onBlur, onChange, val);
                            return;
                        }
                        (0, confirm_1.openConfirmModal)({
                            onConfirm: () => this.handleChange(onBlur, onChange, val),
                            message: (_c = confirm[val === null || val === void 0 ? void 0 : val.value]) !== null && _c !== void 0 ? _c : (0, locale_1.t)('Continue with these changes?'),
                        });
                    }}/>);
            }}/>);
    }
}
exports.default = SelectField;
SelectField.defaultProps = {
    allowClear: false,
    allowEmpty: false,
    placeholder: '--',
    escapeMarkup: true,
    multiple: false,
    small: false,
    formatMessageValue: (value, props) => (getChoices(props).find(choice => choice[0] === value) || [null, value])[1],
};
//# sourceMappingURL=selectField.jsx.map