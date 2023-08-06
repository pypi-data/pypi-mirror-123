Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const inputField_1 = (0, tslib_1.__importDefault)(require("app/components/forms/inputField"));
class TextareaField extends inputField_1.default {
    getField() {
        return (<textarea id={this.getId()} className="form-control" value={this.state.value} disabled={this.props.disabled} required={this.props.required} placeholder={this.props.placeholder} onChange={this.onChange.bind(this)}/>);
    }
}
exports.default = TextareaField;
//# sourceMappingURL=textareaField.jsx.map