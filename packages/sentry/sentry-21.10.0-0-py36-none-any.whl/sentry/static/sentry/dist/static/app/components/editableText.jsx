Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const textOverflow_1 = (0, tslib_1.__importDefault)(require("app/components/textOverflow"));
const iconEdit_1 = require("app/icons/iconEdit");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const useKeyPress_1 = (0, tslib_1.__importDefault)(require("app/utils/useKeyPress"));
const useOnClickOutside_1 = (0, tslib_1.__importDefault)(require("app/utils/useOnClickOutside"));
const input_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/input"));
function EditableText({ value, onChange, name, errorMessage, successMessage, isDisabled = false, }) {
    const [isEditing, setIsEditing] = (0, react_1.useState)(false);
    const [inputValue, setInputValue] = (0, react_1.useState)(value);
    const isEmpty = !inputValue.trim();
    const innerWrapperRef = (0, react_1.useRef)(null);
    const labelRef = (0, react_1.useRef)(null);
    const inputRef = (0, react_1.useRef)(null);
    const enter = (0, useKeyPress_1.default)('Enter');
    const esc = (0, useKeyPress_1.default)('Escape');
    function revertValueAndCloseEditor() {
        if (value !== inputValue) {
            setInputValue(value);
        }
        if (isEditing) {
            setIsEditing(false);
        }
    }
    // check to see if the user clicked outside of this component
    (0, useOnClickOutside_1.default)(innerWrapperRef, () => {
        if (!isEditing) {
            return;
        }
        if (isEmpty) {
            displayStatusMessage('error');
            return;
        }
        if (inputValue !== value) {
            onChange(inputValue);
            displayStatusMessage('success');
        }
        setIsEditing(false);
    });
    const onEnter = (0, react_1.useCallback)(() => {
        if (enter) {
            if (isEmpty) {
                displayStatusMessage('error');
                return;
            }
            if (inputValue !== value) {
                onChange(inputValue);
                displayStatusMessage('success');
            }
            setIsEditing(false);
        }
    }, [enter, inputValue, onChange]);
    const onEsc = (0, react_1.useCallback)(() => {
        if (esc) {
            revertValueAndCloseEditor();
        }
    }, [esc]);
    (0, react_1.useEffect)(() => {
        revertValueAndCloseEditor();
    }, [isDisabled, value]);
    // focus the cursor in the input field on edit start
    (0, react_1.useEffect)(() => {
        if (isEditing) {
            const inputElement = inputRef.current;
            if ((0, utils_1.defined)(inputElement)) {
                inputElement.focus();
            }
        }
    }, [isEditing]);
    (0, react_1.useEffect)(() => {
        if (isEditing) {
            // if Enter is pressed, save the value and close the editor
            onEnter();
            // if Escape is pressed, revert the value and close the editor
            onEsc();
        }
    }, [onEnter, onEsc, isEditing]); // watch the Enter and Escape key presses
    function displayStatusMessage(status) {
        if (status === 'error') {
            if (errorMessage) {
                (0, indicator_1.addErrorMessage)(errorMessage);
            }
            return;
        }
        if (successMessage) {
            (0, indicator_1.addSuccessMessage)(successMessage);
        }
    }
    function handleInputChange(event) {
        setInputValue(event.target.value);
    }
    function handleEditClick() {
        setIsEditing(true);
    }
    return (<Wrapper isDisabled={isDisabled} isEditing={isEditing}>
      {isEditing ? (<InputWrapper ref={innerWrapperRef} isEmpty={isEmpty} data-test-id="editable-text-input">
          <StyledInput name={name} ref={inputRef} value={inputValue} onChange={handleInputChange}/>
          <InputLabel>{inputValue}</InputLabel>
        </InputWrapper>) : (<Label onClick={isDisabled ? undefined : handleEditClick} ref={labelRef} data-test-id="editable-text-label">
          <InnerLabel>{inputValue}</InnerLabel>
          {!isDisabled && <iconEdit_1.IconEdit />}
        </Label>)}
    </Wrapper>);
}
exports.default = EditableText;
const Label = (0, styled_1.default)('div') `
  display: grid;
  grid-auto-flow: column;
  align-items: center;
  gap: ${(0, space_1.default)(1)};
  cursor: pointer;
`;
const InnerLabel = (0, styled_1.default)(textOverflow_1.default) `
  border-top: 1px solid transparent;
  border-bottom: 1px dotted ${p => p.theme.gray200};
`;
const InputWrapper = (0, styled_1.default)('div') `
  display: inline-block;
  background: ${p => p.theme.gray100};
  border-radius: ${p => p.theme.borderRadius};
  margin: -${(0, space_1.default)(0.5)} -${(0, space_1.default)(1)};
  max-width: calc(100% + ${(0, space_1.default)(2)});
`;
const StyledInput = (0, styled_1.default)(input_1.default) `
  border: none !important;
  background: transparent;
  height: auto;
  min-height: 34px;
  padding: ${(0, space_1.default)(0.5)} ${(0, space_1.default)(1)};
  &,
  &:focus,
  &:active,
  &:hover {
    box-shadow: none;
  }
`;
const InputLabel = (0, styled_1.default)('div') `
  height: 0;
  opacity: 0;
  white-space: pre;
  padding: 0 ${(0, space_1.default)(1)};
`;
const Wrapper = (0, styled_1.default)('div') `
  display: flex;

  ${p => p.isDisabled &&
    `
      ${InnerLabel} {
        border-bottom-color: transparent;
      }
    `}
`;
//# sourceMappingURL=editableText.jsx.map