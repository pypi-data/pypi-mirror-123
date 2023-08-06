Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const switchButton_1 = (0, tslib_1.__importDefault)(require("app/components/switchButton"));
const inputField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/inputField"));
class BooleanField extends React.Component {
    constructor() {
        super(...arguments);
        this.handleChange = (value, onChange, onBlur, e) => {
            // We need to toggle current value because Switch is not an input
            const newValue = this.coerceValue(!value);
            onChange(newValue, e);
            onBlur(newValue, e);
        };
    }
    coerceValue(value) {
        return !!value;
    }
    render() {
        const _a = this.props, { confirm } = _a, fieldProps = (0, tslib_1.__rest)(_a, ["confirm"]);
        return (<inputField_1.default {...fieldProps} resetOnError field={(_a) => {
                var { onChange, onBlur, value, disabled } = _a, props = (0, tslib_1.__rest)(_a, ["onChange", "onBlur", "value", "disabled"]);
                // Create a function with required args bound
                const handleChange = this.handleChange.bind(this, value, onChange, onBlur);
                const switchProps = Object.assign(Object.assign({}, props), { size: 'lg', isActive: !!value, isDisabled: disabled, toggle: handleChange });
                if (confirm) {
                    return (<confirm_1.default renderMessage={() => confirm[(!value).toString()]} onConfirm={() => handleChange({})}>
                {({ open }) => (<switchButton_1.default {...switchProps} toggle={(e) => {
                                // If we have a `confirm` prop and enabling switch
                                // Then show confirm dialog, otherwise propagate change as normal
                                if (confirm[(!value).toString()]) {
                                    // Open confirm modal
                                    open();
                                    return;
                                }
                                handleChange(e);
                            }}/>)}
              </confirm_1.default>);
                }
                return <switchButton_1.default {...switchProps}/>;
            }}/>);
    }
}
exports.default = BooleanField;
//# sourceMappingURL=booleanField.jsx.map