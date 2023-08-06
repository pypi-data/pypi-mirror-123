Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const radioGroup_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/radioGroup"));
const inputField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/inputField"));
class RadioField extends React.Component {
    constructor() {
        super(...arguments);
        this.onChange = (id, onChange, onBlur, e) => {
            onChange(id, e);
            onBlur(id, e);
        };
    }
    render() {
        return (<inputField_1.default {...this.props} field={(_a) => {
                var { onChange, onBlur, value, disabled, orientInline } = _a, props = (0, tslib_1.__rest)(_a, ["onChange", "onBlur", "value", "disabled", "orientInline"]);
                return (<radioGroup_1.default choices={props.choices} disabled={disabled} orientInline={orientInline} value={value === '' ? null : value} label={props.label} onChange={(id, e) => this.onChange(id, onChange, onBlur, e)}/>);
            }}/>);
    }
}
exports.default = RadioField;
//# sourceMappingURL=radioField.jsx.map