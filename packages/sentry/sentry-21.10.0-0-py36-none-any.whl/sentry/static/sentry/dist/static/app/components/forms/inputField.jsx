Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const formField_1 = (0, tslib_1.__importDefault)(require("app/components/forms/formField"));
class InputField extends formField_1.default {
    getField() {
        return (<input id={this.getId()} // TODO(Priscila): check the reason behind this. We are getting warnings if we have 2 or more fields with the same name, for instance in the DATA PRIVACY RULES
         type={this.getType()} className="form-control" autoComplete={this.props.autoComplete} placeholder={this.props.placeholder} onChange={this.onChange} disabled={this.props.disabled} name={this.props.name} required={this.props.required} value={this.state.value} // can't pass in boolean here
         style={this.props.inputStyle} onBlur={this.props.onBlur} onFocus={this.props.onFocus} onKeyPress={this.props.onKeyPress} onKeyDown={this.props.onKeyDown} min={this.props.min}/>);
    }
    getClassName() {
        return 'control-group';
    }
    getType() {
        throw new Error('Must be implemented by child.');
    }
}
exports.default = InputField;
//# sourceMappingURL=inputField.jsx.map