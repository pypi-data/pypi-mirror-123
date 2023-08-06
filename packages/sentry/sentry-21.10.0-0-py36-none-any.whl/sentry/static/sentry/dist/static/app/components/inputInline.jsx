Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const icons_1 = require("app/icons");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const callIfFunction_1 = require("app/utils/callIfFunction");
/**
 * InputInline is a cool pattern and @doralchan has confirmed that this has more
 * than 50% chance of being reused elsewhere in the app. However, adding it as a
 * form component has too much overhead for Discover2, so it'll be kept outside
 * for now.
 *
 * The props for this component take some cues from InputField.tsx
 *
 * The implementation uses HTMLDivElement with `contentEditable="true"`. This is
 * because we need the width to expand along with the content inside. There
 * isn't a way to easily do this with HTMLInputElement, especially with fonts
 * which are not fixed-width.
 *
 * If you are expecting the usual HTMLInputElement, this may have some quirky
 * behaviours that'll need your help to improve.
 *
 * TODO(leedongwei): Add to storybook
 * TODO(leedongwei): Add some tests
 */
class InputInline extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            isFocused: false,
            isHovering: false,
        };
        this.refInput = React.createRef();
        /**
         * Used by the parent to blur/focus on the Input
         */
        this.blur = () => {
            if (this.refInput.current) {
                this.refInput.current.blur();
            }
        };
        /**
         * Used by the parent to blur/focus on the Input
         */
        this.focus = () => {
            if (this.refInput.current) {
                this.refInput.current.focus();
                document.execCommand('selectAll', false, undefined);
            }
        };
        this.onBlur = (event) => {
            this.setState({
                isFocused: false,
                isHovering: false,
            });
            (0, callIfFunction_1.callIfFunction)(this.props.onBlur, InputInline.setValueOnEvent(event));
        };
        this.onFocus = (event) => {
            this.setState({ isFocused: true });
            (0, callIfFunction_1.callIfFunction)(this.props.onFocus, InputInline.setValueOnEvent(event));
            // Wait for the next event loop so that the content region has focus.
            window.setTimeout(() => document.execCommand('selectAll', false, undefined), 1);
        };
        /**
         * HACK(leedongwei): ContentEditable is not a Form element, and as such it
         * does not emit `onChange` events. This method using `onInput` and capture the
         * inner value to be passed along to an onChange function.
         */
        this.onChangeUsingOnInput = (event) => {
            (0, callIfFunction_1.callIfFunction)(this.props.onChange, InputInline.setValueOnEvent(event));
        };
        this.onKeyDown = (event) => {
            // Might make sense to add Form submission here too
            if (event.key === 'Enter') {
                // Prevents the Enter key from inserting a line-break
                event.preventDefault();
                if (this.refInput.current) {
                    this.refInput.current.blur();
                }
            }
            (0, callIfFunction_1.callIfFunction)(this.props.onKeyUp, InputInline.setValueOnEvent(event));
        };
        this.onKeyUp = (event) => {
            if (event.key === 'Escape' && this.refInput.current) {
                this.refInput.current.blur();
            }
            (0, callIfFunction_1.callIfFunction)(this.props.onKeyUp, InputInline.setValueOnEvent(event));
        };
        this.onMouseEnter = () => {
            this.setState({ isHovering: !this.props.disabled });
        };
        this.onMouseMove = () => {
            this.setState({ isHovering: !this.props.disabled });
        };
        this.onMouseLeave = () => {
            this.setState({ isHovering: false });
        };
        this.onClickIcon = (event) => {
            if (this.props.disabled) {
                return;
            }
            if (this.refInput.current) {
                this.refInput.current.focus();
                document.execCommand('selectAll', false, undefined);
            }
            (0, callIfFunction_1.callIfFunction)(this.props.onClick, InputInline.setValueOnEvent(event));
        };
    }
    /**
     * HACK(leedongwei): ContentEditable does not have the property `value`. We
     * coerce its `innerText` to `value` so it will have similar behaviour as a
     * HTMLInputElement
     *
     * We probably need to attach this to every DOMAttribute event...
     */
    static setValueOnEvent(event) {
        const text = event.target.innerText ||
            event.currentTarget.innerText;
        event.target.value = text;
        event.currentTarget.value = text;
        return event;
    }
    render() {
        const { value, placeholder, disabled } = this.props;
        const { isFocused } = this.state;
        const innerText = value || placeholder || '';
        return (<Wrapper style={this.props.style} onMouseEnter={this.onMouseEnter} onMouseMove={this.onMouseMove} onMouseLeave={this.onMouseLeave}>
        <Input {...this.props} // Pass DOMAttributes props first, extend/overwrite below
         ref={this.refInput} suppressContentEditableWarning contentEditable={!this.props.disabled} isHovering={this.state.isHovering} isDisabled={this.props.disabled} onBlur={this.onBlur} onFocus={this.onFocus} onInput={this.onChangeUsingOnInput} onChange={this.onChangeUsingOnInput} // Overwrite onChange too, just to be 100% sure
         onKeyDown={this.onKeyDown} onKeyUp={this.onKeyUp}>
          {innerText}
        </Input>

        {!isFocused && !disabled && (<div onClick={this.onClickIcon}>
            <StyledIconEdit />
          </div>)}
      </Wrapper>);
    }
}
const Wrapper = (0, styled_1.default)('div') `
  display: inline-flex;
  align-items: center;

  vertical-align: text-bottom;
`;
const Input = (0, styled_1.default)('div') `
  min-width: 40px;
  margin: 0;
  border: 1px solid ${p => (p.isHovering ? p.theme.border : 'transparent')};
  outline: none;

  line-height: inherit;
  border-radius: ${(0, space_1.default)(0.5)};
  background: transparent;
  padding: 1px;

  &:focus,
  &:active {
    border: 1px solid ${p => (p.isDisabled ? 'transparent' : p.theme.border)};
    background-color: ${p => (p.isDisabled ? 'transparent' : p.theme.gray200)};
  }
`;
const StyledIconEdit = (0, styled_1.default)(icons_1.IconEdit) `
  color: ${p => p.theme.gray300};
  margin-left: ${(0, space_1.default)(0.5)};

  &:hover {
    cursor: pointer;
  }
`;
exports.default = InputInline;
//# sourceMappingURL=inputInline.jsx.map