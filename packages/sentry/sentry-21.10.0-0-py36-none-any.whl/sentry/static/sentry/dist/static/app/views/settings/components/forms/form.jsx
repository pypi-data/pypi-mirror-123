Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const mobx_react_1 = require("mobx-react");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const panel_1 = (0, tslib_1.__importDefault)(require("app/components/panels/panel"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const isRenderFunc_1 = require("app/utils/isRenderFunc");
const formContext_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/formContext"));
const model_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/model"));
class Form extends React.Component {
    constructor(props, context) {
        super(props, context);
        this.model = this.props.model || new model_1.default();
        this.onSubmit = e => {
            var _a, _b;
            !this.props.skipPreventDefault && e.preventDefault();
            if (this.model.isSaving) {
                return;
            }
            (_b = (_a = this.props).onPreSubmit) === null || _b === void 0 ? void 0 : _b.call(_a);
            if (this.props.onSubmit) {
                this.props.onSubmit(this.model.getData(), this.onSubmitSuccess, this.onSubmitError, e, this.model);
            }
            else {
                this.model.saveForm();
            }
        };
        this.onSubmitSuccess = data => {
            const { onSubmitSuccess } = this.props;
            this.model.submitSuccess(data);
            if (onSubmitSuccess) {
                onSubmitSuccess(data, this.model);
            }
        };
        this.onSubmitError = error => {
            const { onSubmitError } = this.props;
            this.model.submitError(error);
            if (onSubmitError) {
                onSubmitError(error, this.model);
            }
        };
        const { saveOnBlur, apiEndpoint, apiMethod, resetOnError, onSubmitSuccess, onSubmitError, onFieldChange, initialData, allowUndo, } = props;
        this.model.setInitialData(initialData);
        this.model.setFormOptions({
            resetOnError,
            allowUndo,
            onFieldChange,
            onSubmitSuccess,
            onSubmitError,
            saveOnBlur,
            apiEndpoint,
            apiMethod,
        });
    }
    componentWillUnmount() {
        this.model.reset();
    }
    contextData() {
        return {
            saveOnBlur: this.props.saveOnBlur,
            form: this.model,
        };
    }
    render() {
        const { className, children, footerClass, footerStyle, submitDisabled, submitLabel, submitPriority, cancelLabel, onCancel, extraButton, requireChanges, saveOnBlur, hideFooter, } = this.props;
        const shouldShowFooter = typeof hideFooter !== 'undefined' ? !hideFooter : !saveOnBlur;
        return (<formContext_1.default.Provider value={this.contextData()}>
        <form onSubmit={this.onSubmit} className={className !== null && className !== void 0 ? className : 'form-stacked'} data-test-id={this.props['data-test-id']}>
          <div>
            {(0, isRenderFunc_1.isRenderFunc)(children)
                ? children({ model: this.model })
                : children}
          </div>

          {shouldShowFooter && (<StyledFooter className={footerClass} style={footerStyle} saveOnBlur={saveOnBlur}>
              {extraButton}
              <DefaultButtons>
                {onCancel && (<mobx_react_1.Observer>
                    {() => (<button_1.default type="button" disabled={this.model.isSaving} onClick={onCancel} style={{ marginLeft: 5 }}>
                        {cancelLabel !== null && cancelLabel !== void 0 ? cancelLabel : (0, locale_1.t)('Cancel')}
                      </button_1.default>)}
                  </mobx_react_1.Observer>)}

                <mobx_react_1.Observer>
                  {() => (<button_1.default data-test-id="form-submit" priority={submitPriority !== null && submitPriority !== void 0 ? submitPriority : 'primary'} disabled={this.model.isError ||
                        this.model.isSaving ||
                        submitDisabled ||
                        (requireChanges ? !this.model.formChanged : false)} type="submit">
                      {submitLabel !== null && submitLabel !== void 0 ? submitLabel : (0, locale_1.t)('Save Changes')}
                    </button_1.default>)}
                </mobx_react_1.Observer>
              </DefaultButtons>
            </StyledFooter>)}
        </form>
      </formContext_1.default.Provider>);
    }
}
exports.default = Form;
const StyledFooter = (0, styled_1.default)('div') `
  display: flex;
  justify-content: flex-end;
  margin-top: 25px;
  border-top: 1px solid ${p => p.theme.innerBorder};
  background: none;
  padding: 16px 0 0;
  margin-bottom: 16px;

  ${p => !p.saveOnBlur &&
    `
  ${panel_1.default} & {
    margin-top: 0;
    padding-right: 36px;
  }

  /* Better padding with form inside of a modal */
  [role='document'] & {
    padding-right: 30px;
    margin-left: -30px;
    margin-right: -30px;
    margin-bottom: -30px;
    margin-top: 16px;
    padding-bottom: 16px;
  }
  `};
`;
const DefaultButtons = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(1)};
  grid-auto-flow: column;
  justify-content: flex-end;
  flex: 1;
`;
//# sourceMappingURL=form.jsx.map