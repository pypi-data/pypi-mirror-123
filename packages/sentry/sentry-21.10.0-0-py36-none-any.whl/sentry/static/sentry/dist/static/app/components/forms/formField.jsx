Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const classnames_1 = (0, tslib_1.__importDefault)(require("classnames"));
const formContext_1 = (0, tslib_1.__importDefault)(require("app/components/forms/formContext"));
const questionTooltip_1 = (0, tslib_1.__importDefault)(require("app/components/questionTooltip"));
const utils_1 = require("app/utils");
class FormField extends React.PureComponent {
    constructor(props, context) {
        super(props, context);
        this.onChange = (e) => {
            const value = e.target.value;
            this.setValue(value);
        };
        this.setValue = (value) => {
            const form = (this.context || {}).form;
            this.setState({
                value,
            }, () => {
                var _a, _b;
                const finalValue = this.coerceValue(this.state.value);
                (_b = (_a = this.props).onChange) === null || _b === void 0 ? void 0 : _b.call(_a, finalValue);
                form === null || form === void 0 ? void 0 : form.onFieldChange(this.props.name, finalValue);
            });
        };
        this.state = {
            error: null,
            value: this.getValue(props, context),
        };
    }
    componentDidMount() { }
    UNSAFE_componentWillReceiveProps(nextProps, nextContext) {
        const newError = this.getError(nextProps, nextContext);
        if (newError !== this.state.error) {
            this.setState({ error: newError });
        }
        if (this.props.value !== nextProps.value || (0, utils_1.defined)(nextContext.form)) {
            const newValue = this.getValue(nextProps, nextContext);
            if (newValue !== this.state.value) {
                this.setValue(newValue);
            }
        }
    }
    componentWillUnmount() { }
    getValue(props, context) {
        const form = (context || this.context || {}).form;
        props = props || this.props;
        if ((0, utils_1.defined)(props.value)) {
            return props.value;
        }
        if (form && form.data.hasOwnProperty(props.name)) {
            return (0, utils_1.defined)(form.data[props.name]) ? form.data[props.name] : '';
        }
        return (0, utils_1.defined)(props.defaultValue) ? props.defaultValue : '';
    }
    getError(props, context) {
        const form = (context || this.context || {}).form;
        props = props || this.props;
        if ((0, utils_1.defined)(props.error)) {
            return props.error;
        }
        return (form && form.errors[props.name]) || null;
    }
    getId() {
        return `id-${this.props.name}`;
    }
    coerceValue(value) {
        return value;
    }
    getField() {
        throw new Error('Must be implemented by child.');
    }
    getClassName() {
        throw new Error('Must be implemented by child.');
    }
    getFinalClassNames() {
        const { className, required } = this.props;
        const { error } = this.state;
        return (0, classnames_1.default)(className, this.getClassName(), {
            'has-error': !!error,
            required,
        });
    }
    renderDisabledReason() {
        const { disabled, disabledReason } = this.props;
        if (!disabled) {
            return null;
        }
        if (!disabledReason) {
            return null;
        }
        return <questionTooltip_1.default title={disabledReason} position="top" size="sm"/>;
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
          {this.getField()}
          {this.renderDisabledReason()}
          {(0, utils_1.defined)(help) && <p className="help-block">{help}</p>}
          {shouldShowErrorMessage && <ErrorMessage>{error}</ErrorMessage>}
        </div>
      </div>);
    }
}
exports.default = FormField;
FormField.defaultProps = {
    hideErrorMessage: false,
    disabled: false,
    required: false,
};
FormField.contextType = formContext_1.default;
const ErrorMessage = (0, styled_1.default)('p') `
  font-size: ${p => p.theme.fontSizeMedium};
  color: ${p => p.theme.red300};
`;
//# sourceMappingURL=formField.jsx.map