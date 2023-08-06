Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const inputField_1 = (0, tslib_1.__importDefault)(require("app/components/forms/inputField"));
const utils_1 = require("app/utils");
class RadioBooleanField extends inputField_1.default {
    constructor() {
        super(...arguments);
        this.onChange = e => {
            const value = e.target.value === 'true';
            this.setValue(value);
        };
    }
    coerceValue(props) {
        const value = super.coerceValue(props);
        return value ? true : false;
    }
    getType() {
        return 'radio';
    }
    getField() {
        const yesOption = (<div className="radio" key="yes">
        <label style={{ fontWeight: 'normal' }}>
          <input type="radio" value="true" name={this.props.name} checked={this.state.value === true} onChange={this.onChange.bind(this)} disabled={this.props.disabled}/>{' '}
          {this.props.yesLabel}
        </label>
      </div>);
        const noOption = (<div className="radio" key="no">
        <label style={{ fontWeight: 'normal' }}>
          <input type="radio" name={this.props.name} value="false" checked={this.state.value === false} onChange={this.onChange.bind(this)} disabled={this.props.disabled}/>{' '}
          {this.props.noLabel}
        </label>
      </div>);
        return (<div className="control-group radio-boolean">
        {this.props.yesFirst ? (<react_1.Fragment>
            {yesOption}
            {noOption}
          </react_1.Fragment>) : (<react_1.Fragment>
            {noOption}
            {yesOption}
          </react_1.Fragment>)}
      </div>);
    }
    render() {
        const { label, hideErrorMessage, help, style } = this.props;
        const { error } = this.state;
        const cx = this.getFinalClassNames();
        const shouldShowErrorMessage = error && !hideErrorMessage;
        return (<div style={style} className={cx}>
        <div className="controls">
          {label && (<label htmlFor={this.getId()} className="control-label">
              {label}
            </label>)}
          {(0, utils_1.defined)(help) && <p className="help-block">{help}</p>}
          {this.getField()}
          {this.renderDisabledReason()}
          {shouldShowErrorMessage && <p className="error">{error}</p>}
        </div>
      </div>);
    }
}
exports.default = RadioBooleanField;
RadioBooleanField.defaultProps = Object.assign(Object.assign({}, inputField_1.default.defaultProps), { yesLabel: 'Yes', noLabel: 'No', yesFirst: true });
//# sourceMappingURL=radioBooleanField.jsx.map