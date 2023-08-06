Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const classnames_1 = (0, tslib_1.__importDefault)(require("classnames"));
const formField_1 = (0, tslib_1.__importDefault)(require("app/components/forms/formField"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const utils_1 = require("app/utils");
class MultipleCheckboxField extends formField_1.default {
    constructor() {
        super(...arguments);
        this.onChange = (e, _value) => {
            const value = _value; // Casting here to allow _value to be optional, which it has to be since it's overloaded.
            let allValues = this.state.values;
            if (e.target.checked) {
                if (allValues) {
                    allValues = [...allValues, value];
                }
                else {
                    allValues = [value];
                }
            }
            else {
                allValues = allValues.filter(v => v !== value);
            }
            this.setValues(allValues);
        };
    }
    setValues(values) {
        const form = (this.context || {}).form;
        this.setState({
            values,
        }, () => {
            const finalValue = this.coerceValue(this.state.values);
            this.props.onChange && this.props.onChange(finalValue);
            form && form.onFieldChange(this.props.name, finalValue);
        });
    }
    render() {
        const { required, className, disabled, disabledReason, label, help, choices, hideLabelDivider, style, } = this.props;
        const { error } = this.state;
        const cx = (0, classnames_1.default)(className, 'control-group', {
            'has-error': error,
        });
        // Hacky, but this isn't really a form label vs the checkbox labels, but
        // we want to treat it as one (i.e. for "required" indicator)
        const labelCx = (0, classnames_1.default)({
            required,
        });
        const shouldShowDisabledReason = disabled && disabledReason;
        return (<div style={style} className={cx}>
        <div className={labelCx}>
          <div className="controls">
            <label className="control-label" style={{
                display: 'block',
                marginBottom: !hideLabelDivider ? 10 : undefined,
                borderBottom: !hideLabelDivider ? '1px solid #f1eff3' : undefined,
            }}>
              {label}
              {shouldShowDisabledReason && (<tooltip_1.default title={disabledReason}>
                  <span className="disabled-indicator">
                    <icons_1.IconQuestion size="xs"/>
                  </span>
                </tooltip_1.default>)}
            </label>
            {help && <p className="help-block">{help}</p>}
            {error && <p className="error">{error}</p>}
          </div>
        </div>

        <div className="control-list">
          {choices.map(([value, choiceLabel]) => (<label className="checkbox" key={value}>
              <input type="checkbox" value={value} onChange={e => this.onChange(e, value)} disabled={disabled} checked={(0, utils_1.defined)(this.state.values) && this.state.values.indexOf(value) !== -1}/>
              {choiceLabel}
            </label>))}
        </div>
      </div>);
    }
}
exports.default = MultipleCheckboxField;
//# sourceMappingURL=multipleCheckboxField.jsx.map