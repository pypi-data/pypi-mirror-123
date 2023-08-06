Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const icons_1 = require("app/icons");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const DropdownButton = (_a) => {
    var { children, forwardedRef, prefix, isOpen = false, showChevron = false, hideBottomBorder = true, disabled = false, priority = 'form' } = _a, props = (0, tslib_1.__rest)(_a, ["children", "forwardedRef", "prefix", "isOpen", "showChevron", "hideBottomBorder", "disabled", "priority"]);
    return (<StyledButton {...props} type="button" disabled={disabled} priority={priority} isOpen={isOpen} hideBottomBorder={hideBottomBorder} ref={forwardedRef}>
      {prefix && <LabelText>{prefix}</LabelText>}
      {children}
      {showChevron && <StyledChevron size="10px" direction={isOpen ? 'up' : 'down'}/>}
    </StyledButton>);
};
DropdownButton.defaultProps = {
    showChevron: true,
};
const StyledChevron = (0, styled_1.default)(icons_1.IconChevron) `
  margin-left: 0.33em;
`;
const StyledButton = (0, styled_1.default)(button_1.default) `
  border-bottom-right-radius: ${p => (p.isOpen ? 0 : p.theme.borderRadius)};
  border-bottom-left-radius: ${p => (p.isOpen ? 0 : p.theme.borderRadius)};
  position: relative;
  z-index: 2;
  box-shadow: ${p => (p.isOpen || p.disabled ? 'none' : p.theme.dropShadowLight)};
  &,
  &:active,
  &:focus,
  &:hover {
    border-bottom-color: ${p => p.isOpen && p.hideBottomBorder
    ? 'transparent'
    : p.theme.button[p.priority].borderActive};
  }
`;
const LabelText = (0, styled_1.default)('span') `
  &:after {
    content: ':';
  }

  font-weight: 400;
  padding-right: ${(0, space_1.default)(0.75)};
`;
exports.default = React.forwardRef((props, ref) => (<DropdownButton forwardedRef={ref} {...props}/>));
//# sourceMappingURL=dropdownButton.jsx.map