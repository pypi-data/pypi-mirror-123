Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const mobx_react_1 = require("mobx-react");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const panelAlert_1 = (0, tslib_1.__importDefault)(require("app/components/panels/panelAlert"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const sanitizeQuerySelector_1 = require("app/utils/sanitizeQuerySelector");
const field_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field"));
const fieldControl_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field/fieldControl"));
const fieldErrorReason_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field/fieldErrorReason"));
const formContext_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/formContext"));
const controlState_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/formField/controlState"));
const model_1 = require("app/views/settings/components/forms/model");
const returnButton_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/returnButton"));
/**
 * Some fields don't need to implement their own onChange handlers, in
 * which case we will receive an Event, but if they do we should handle
 * the case where they return a value as the first argument.
 */
const getValueFromEvent = (valueOrEvent, e) => {
    var _a;
    const event = e || valueOrEvent;
    const value = (0, utils_1.defined)(e) ? valueOrEvent : (_a = event === null || event === void 0 ? void 0 : event.target) === null || _a === void 0 ? void 0 : _a.value;
    return { value, event };
};
/**
 * This is a list of field properties that can accept a function taking the
 * form model, that will be called to determine the value of the prop upon an
 * observed change in the model.
 *
 * This uses mobx's observation of the models observable fields.
 */
const propsToObserver = ['help', 'inline', 'highlighted', 'visible', 'disabled'];
class FormField extends React.Component {
    constructor() {
        super(...arguments);
        this.input = null;
        /**
         * Attempts to autofocus input field if field's name is in url hash.
         *
         * The ref must be forwared for this to work.
         */
        this.handleInputMount = (node) => {
            var _a;
            if (node && !this.input) {
                // TODO(mark) Clean this up. FormContext could include the location
                const hash = (_a = window.location) === null || _a === void 0 ? void 0 : _a.hash;
                if (!hash) {
                    return;
                }
                if (hash !== `#${this.props.name}`) {
                    return;
                }
                // Not all form fields have this (e.g. Select fields)
                if (typeof node.focus === 'function') {
                    node.focus();
                }
            }
            this.input = node;
        };
        /**
         * Update field value in form model
         */
        this.handleChange = (...args) => {
            const { name, onChange } = this.props;
            const { value, event } = getValueFromEvent(...args);
            const model = this.getModel();
            if (onChange) {
                onChange(value, event);
            }
            model.setValue(name, value);
        };
        /**
         * Notify model of a field being blurred
         */
        this.handleBlur = (...args) => {
            const { name, onBlur } = this.props;
            const { value, event } = getValueFromEvent(...args);
            const model = this.getModel();
            if (onBlur) {
                onBlur(value, event);
            }
            // Always call this, so model can decide what to do
            model.handleBlurField(name, value);
        };
        /**
         * Handle keydown to trigger a save on Enter
         */
        this.handleKeyDown = (...args) => {
            const { onKeyDown, name } = this.props;
            const { value, event } = getValueFromEvent(...args);
            const model = this.getModel();
            if (event.key === 'Enter') {
                model.handleBlurField(name, value);
            }
            if (onKeyDown) {
                onKeyDown(value, event);
            }
        };
        /**
         * Handle saving an individual field via UI button
         */
        this.handleSaveField = () => {
            const { name } = this.props;
            const model = this.getModel();
            model.handleSaveField(name, model.getValue(name));
        };
        this.handleCancelField = () => {
            const { name } = this.props;
            const model = this.getModel();
            model.handleCancelSaveField(name);
        };
    }
    componentDidMount() {
        // Tell model about this field's props
        this.getModel().setFieldDescriptor(this.props.name, this.props);
    }
    componentWillUnmount() {
        this.getModel().removeField(this.props.name);
    }
    getError() {
        return this.getModel().getError(this.props.name);
    }
    getId() {
        return (0, sanitizeQuerySelector_1.sanitizeQuerySelector)(this.props.name);
    }
    getModel() {
        return this.context.form !== undefined
            ? this.context.form
            : new model_1.MockModel(this.props);
    }
    render() {
        const _a = this.props, { className, name, hideErrorMessage, flexibleControlStateSize, saveOnBlur, saveMessage, saveMessageAlertType, selectionInfoFunction, hideControlState, 
        // Don't pass `defaultValue` down to input fields, will be handled in
        // form model
        defaultValue: _defaultValue } = _a, otherProps = (0, tslib_1.__rest)(_a, ["className", "name", "hideErrorMessage", "flexibleControlStateSize", "saveOnBlur", "saveMessage", "saveMessageAlertType", "selectionInfoFunction", "hideControlState", "defaultValue"]);
        const id = this.getId();
        const model = this.getModel();
        const saveOnBlurFieldOverride = typeof saveOnBlur !== 'undefined' && !saveOnBlur;
        const makeField = (resolvedObservedProps) => {
            const props = Object.assign(Object.assign({}, otherProps), resolvedObservedProps);
            return (<React.Fragment>
          <field_1.default id={id} className={className} flexibleControlStateSize={flexibleControlStateSize} {...props}>
            {({ alignRight, inline, disabled, disabledReason }) => (<fieldControl_1.default disabled={disabled} disabledReason={disabledReason} inline={inline} alignRight={alignRight} flexibleControlStateSize={flexibleControlStateSize} hideControlState={hideControlState} controlState={<controlState_1.default model={model} name={name}/>} errorState={<mobx_react_1.Observer>
                    {() => {
                            const error = this.getError();
                            const shouldShowErrorMessage = error && !hideErrorMessage;
                            if (!shouldShowErrorMessage) {
                                return null;
                            }
                            return <fieldErrorReason_1.default>{error}</fieldErrorReason_1.default>;
                        }}
                  </mobx_react_1.Observer>}>
                <mobx_react_1.Observer>
                  {() => {
                        const error = this.getError();
                        const value = model.getValue(name);
                        const showReturnButton = model.getFieldState(name, 'showReturnButton');
                        return (<React.Fragment>
                        {this.props.children(Object.assign(Object.assign({ ref: this.handleInputMount }, props), { model,
                                name,
                                id, onKeyDown: this.handleKeyDown, onChange: this.handleChange, onBlur: this.handleBlur, 
                                // Fixes react warnings about input switching from controlled to uncontrolled
                                // So force to empty string for null values
                                value: value === null ? '' : value, error,
                                disabled, initialData: model.initialData }))}
                        {showReturnButton && <StyledReturnButton />}
                      </React.Fragment>);
                    }}
                </mobx_react_1.Observer>
              </fieldControl_1.default>)}
          </field_1.default>
          {selectionInfoFunction && (<mobx_react_1.Observer>
              {() => {
                        const error = this.getError();
                        const value = model.getValue(name);
                        const isVisible = typeof props.visible === 'function'
                            ? props.visible(Object.assign(Object.assign({}, this.props), props))
                            : true;
                        return (<React.Fragment>
                    {isVisible ? selectionInfoFunction(Object.assign(Object.assign({}, props), { error, value })) : null}
                  </React.Fragment>);
                    }}
            </mobx_react_1.Observer>)}
          {saveOnBlurFieldOverride && (<mobx_react_1.Observer>
              {() => {
                        const showFieldSave = model.getFieldState(name, 'showSave');
                        const value = model.getValue(name);
                        if (!showFieldSave) {
                            return null;
                        }
                        return (<panelAlert_1.default type={saveMessageAlertType}>
                    <MessageAndActions>
                      <div>
                        {typeof saveMessage === 'function'
                                ? saveMessage(Object.assign(Object.assign({}, props), { value }))
                                : saveMessage}
                      </div>
                      <buttonBar_1.default gap={1}>
                        <button_1.default onClick={this.handleCancelField}>{(0, locale_1.t)('Cancel')}</button_1.default>
                        <button_1.default priority="primary" type="button" onClick={this.handleSaveField}>
                          {(0, locale_1.t)('Save')}
                        </button_1.default>
                      </buttonBar_1.default>
                    </MessageAndActions>
                  </panelAlert_1.default>);
                    }}
            </mobx_react_1.Observer>)}
        </React.Fragment>);
        };
        const observedProps = propsToObserver
            .filter(p => typeof this.props[p] === 'function')
            .map(p => [
            p,
            () => this.props[p](Object.assign(Object.assign({}, this.props), { model })),
        ]);
        // This field has no properties that require observation to compute their
        // value, this field is static and will not be re-rendered.
        if (observedProps.length === 0) {
            return makeField();
        }
        const resolveObservedProps = (props, [propName, resolve]) => (Object.assign(Object.assign({}, props), { [propName]: resolve() }));
        return (<mobx_react_1.Observer>
        {() => makeField(observedProps.reduce(resolveObservedProps, {}))}
      </mobx_react_1.Observer>);
    }
}
FormField.defaultProps = {
    hideErrorMessage: false,
    flexibleControlStateSize: false,
};
FormField.contextType = formContext_1.default;
exports.default = FormField;
const MessageAndActions = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: 1fr max-content;
  grid-gap: ${(0, space_1.default)(2)};
  align-items: flex-start;
`;
const StyledReturnButton = (0, styled_1.default)(returnButton_1.default) `
  position: absolute;
  right: 0;
  top: 0;
`;
//# sourceMappingURL=index.jsx.map