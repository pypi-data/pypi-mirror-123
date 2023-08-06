Object.defineProperty(exports, "__esModule", { value: true });
exports.modalCss = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_2 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const search_1 = (0, tslib_1.__importDefault)(require("app/components/search"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const input_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/input"));
function CommandPalette({ Body }) {
    const theme = (0, react_2.useTheme)();
    (0, react_1.useEffect)(() => void (0, analytics_1.analytics)('omnisearch.open', {}), []);
    return (<Body>
      <react_2.ClassNames>
        {({ css: injectedCss }) => (<search_1.default entryPoint="command_palette" minSearch={1} maxResults={10} dropdownStyle={injectedCss `
                width: 100%;
                border: transparent;
                border-top-left-radius: 0;
                border-top-right-radius: 0;
                position: initial;
                box-shadow: none;
                border-top: 1px solid ${theme.border};
              `} renderInput={({ getInputProps }) => (<InputWrapper>
                <StyledInput autoFocus {...getInputProps({
                type: 'text',
                placeholder: (0, locale_1.t)('Search for projects, teams, settings, etc...'),
            })}/>
              </InputWrapper>)}/>)}
      </react_2.ClassNames>
    </Body>);
}
exports.default = CommandPalette;
exports.modalCss = (0, react_2.css) `
  [role='document'] {
    padding: 0;
  }
`;
const InputWrapper = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(0.25)};
`;
const StyledInput = (0, styled_1.default)(input_1.default) `
  width: 100%;
  padding: ${(0, space_1.default)(1)};
  border-radius: 8px;

  outline: none;
  border: none;
  box-shadow: none;

  :focus,
  :active,
  :hover {
    outline: none;
    border: none;
    box-shadow: none;
  }
`;
//# sourceMappingURL=commandPalette.jsx.map