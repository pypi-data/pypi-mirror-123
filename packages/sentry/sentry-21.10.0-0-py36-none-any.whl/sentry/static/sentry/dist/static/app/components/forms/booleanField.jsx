Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const inputField_1 = (0, tslib_1.__importDefault)(require("app/components/forms/inputField"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const utils_1 = require("app/utils");
class BooleanField extends inputField_1.default {
    constructor() {
        super(...arguments);
        this.onChange = (e) => {
            const value = e.target.checked;
            this.setValue(value);
        };
    }
    coerceValue(initialValue) {
        const value = super.coerceValue(initialValue);
        return value ? true : false;
    }
    getField() {
        return (<input id={this.getId()} type={this.getType()} checked={this.state.value} onChange={this.onChange.bind(this)} disabled={this.props.disabled}/>);
    }
    render() {
        const { error } = this.state;
        let className = this.getClassName();
        if (error) {
            className += ' has-error';
        }
        return (<div className={className}>
        <div className="controls">
          <label className="control-label">
            {this.getField()}
            {this.props.label}
            {this.props.disabled && this.props.disabledReason && (<tooltip_1.default title={this.props.disabledReason}>
                <icons_1.IconQuestion size="xs"/>
              </tooltip_1.default>)}
          </label>
          {(0, utils_1.defined)(this.props.help) && <p className="help-block">{this.props.help}</p>}
          {error && <p className="error">{error}</p>}
        </div>
      </div>);
    }
    getClassName() {
        return 'control-group checkbox';
    }
    getType() {
        return 'checkbox';
    }
}
exports.default = BooleanField;
//# sourceMappingURL=booleanField.jsx.map