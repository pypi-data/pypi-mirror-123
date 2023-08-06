Object.defineProperty(exports, "__esModule", { value: true });
exports.modalCss = void 0;
const tslib_1 = require("tslib");
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const helpSearch_1 = (0, tslib_1.__importDefault)(require("app/components/helpSearch"));
const hook_1 = (0, tslib_1.__importDefault)(require("app/components/hook"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
function HelpSearchModal(_a) {
    var { Body, closeModal, organization, placeholder = (0, locale_1.t)('Search for documentation, FAQs, blog posts...') } = _a, props = (0, tslib_1.__rest)(_a, ["Body", "closeModal", "organization", "placeholder"]);
    const theme = (0, react_1.useTheme)();
    return (<Body>
      <react_1.ClassNames>
        {({ css: injectedCss }) => (<helpSearch_1.default {...props} entryPoint="sidebar_help" dropdownStyle={injectedCss `
                width: 100%;
                border: transparent;
                border-top-left-radius: 0;
                border-top-right-radius: 0;
                position: initial;
                box-shadow: none;
                border-top: 1px solid ${theme.border};
              `} renderInput={({ getInputProps }) => (<InputWrapper>
                <Input autoFocus {...getInputProps({ type: 'text', label: placeholder, placeholder })}/>
              </InputWrapper>)} resultFooter={<hook_1.default name="help-modal:footer" {...{ organization, closeModal }}/>}/>)}
      </react_1.ClassNames>
    </Body>);
}
const InputWrapper = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(0.25)};
`;
const Input = (0, styled_1.default)('input') `
  width: 100%;
  padding: ${(0, space_1.default)(1)};
  border: none;
  border-radius: 8px;
  outline: none;

  &:focus {
    outline: none;
  }
`;
exports.modalCss = (0, react_1.css) `
  [role='document'] {
    padding: 0;
  }
`;
exports.default = (0, withOrganization_1.default)(HelpSearchModal);
//# sourceMappingURL=helpSearchModal.jsx.map