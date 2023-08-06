Object.defineProperty(exports, "__esModule", { value: true });
exports.StyledForm = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const formContext_1 = (0, tslib_1.__importDefault)(require("app/components/forms/formContext"));
const state_1 = (0, tslib_1.__importDefault)(require("app/components/forms/state"));
const locale_1 = require("app/locale");
class Form extends React.Component {
    constructor(props, context) {
        super(props, context);
        this.onSubmit = (e) => {
            e.preventDefault();
            if (!this.props.onSubmit) {
                throw new Error('onSubmit is a required prop');
            }
            this.props.onSubmit(this.state.data, this.onSubmitSuccess, this.onSubmitError);
        };
        this.onSubmitSuccess = (data) => {
            this.setState({
                state: state_1.default.READY,
                errors: {},
                initialData: Object.assign(Object.assign({}, this.state.data), (data || {})),
            });
            this.props.onSubmitSuccess && this.props.onSubmitSuccess(data);
        };
        this.onSubmitError = error => {
            this.setState({
                state: state_1.default.ERROR,
                errors: error.responseJSON,
            });
            if (this.props.resetOnError) {
                this.setState({
                    initialData: {},
                });
            }
            this.props.onSubmitError && this.props.onSubmitError(error);
        };
        this.onFieldChange = (name, value) => {
            this.setState(state => ({
                data: Object.assign(Object.assign({}, state.data), { [name]: value }),
            }));
        };
        this.state = {
            data: Object.assign({}, this.props.initialData),
            errors: {},
            initialData: Object.assign({}, this.props.initialData),
            state: state_1.default.READY,
        };
    }
    getContext() {
        const { data, errors } = this.state;
        return {
            form: {
                data,
                errors,
                onFieldChange: this.onFieldChange,
            },
        };
    }
    render() {
        const isSaving = this.state.state === state_1.default.SAVING;
        const { initialData, data } = this.state;
        const { errorMessage, hideErrors, requireChanges } = this.props;
        const hasChanges = requireChanges
            ? Object.keys(data).length && !(0, isEqual_1.default)(data, initialData)
            : true;
        const isError = this.state.state === state_1.default.ERROR;
        const nonFieldErrors = this.state.errors && this.state.errors.non_field_errors;
        return (<formContext_1.default.Provider value={this.getContext()}>
        <exports.StyledForm onSubmit={this.onSubmit} className={this.props.className}>
          {isError && !hideErrors && (<div className="alert alert-error alert-block">
              {nonFieldErrors ? (<div>
                  <p>
                    {(0, locale_1.t)('Unable to save your changes. Please correct the following errors try again.')}
                  </p>
                  <ul>
                    {nonFieldErrors.map((e, i) => (<li key={i}>{e}</li>))}
                  </ul>
                </div>) : (errorMessage)}
            </div>)}
          {this.props.children}
          <div className={this.props.footerClass} style={{ marginTop: 25 }}>
            <button_1.default priority="primary" disabled={isSaving || this.props.submitDisabled || !hasChanges} type="submit">
              {this.props.submitLabel}
            </button_1.default>
            {this.props.onCancel && (<button_1.default type="button" disabled={isSaving} onClick={this.props.onCancel} style={{ marginLeft: 5 }}>
                {this.props.cancelLabel}
              </button_1.default>)}
            {this.props.extraButton}
          </div>
        </exports.StyledForm>
      </formContext_1.default.Provider>);
    }
}
Form.defaultProps = {
    cancelLabel: (0, locale_1.t)('Cancel'),
    submitLabel: (0, locale_1.t)('Save Changes'),
    submitDisabled: false,
    footerClass: 'form-actions align-right',
    className: 'form-stacked',
    requireChanges: false,
    hideErrors: false,
    resetOnError: false,
    errorMessage: (0, locale_1.t)('Unable to save your changes. Please ensure all fields are valid and try again.'),
};
// Note: this is so we can use this as a selector for SelectField
// We need to keep `Form` as a React Component because ApiForm extends it :/
exports.StyledForm = (0, styled_1.default)('form') ``;
exports.default = Form;
//# sourceMappingURL=form.jsx.map