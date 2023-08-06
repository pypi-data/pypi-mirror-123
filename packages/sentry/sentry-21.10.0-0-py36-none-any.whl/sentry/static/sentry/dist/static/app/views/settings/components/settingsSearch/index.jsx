Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_hotkeys_hook_1 = require("react-hotkeys-hook");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const search_1 = (0, tslib_1.__importDefault)(require("app/components/search"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const MIN_SEARCH_LENGTH = 1;
const MAX_RESULTS = 10;
function SettingsSearch() {
    const searchInput = (0, react_1.useRef)(null);
    (0, react_hotkeys_hook_1.useHotkeys)('/', e => {
        var _a;
        e.preventDefault();
        (_a = searchInput.current) === null || _a === void 0 ? void 0 : _a.focus();
    });
    return (<search_1.default entryPoint="settings_search" minSearch={MIN_SEARCH_LENGTH} maxResults={MAX_RESULTS} renderInput={({ getInputProps }) => (<SearchInputWrapper>
          <SearchInputIcon size="14px"/>
          <SearchInput {...getInputProps({ type: 'text', placeholder: (0, locale_1.t)('Search') })} ref={searchInput}/>
        </SearchInputWrapper>)}/>);
}
exports.default = SettingsSearch;
const SearchInputWrapper = (0, styled_1.default)('div') `
  position: relative;
`;
const SearchInputIcon = (0, styled_1.default)(icons_1.IconSearch) `
  color: ${p => p.theme.gray300};
  position: absolute;
  left: 10px;
  top: 8px;
`;
const SearchInput = (0, styled_1.default)('input') `
  color: ${p => p.theme.formText};
  background-color: ${p => p.theme.background};
  transition: border-color 0.15s ease;
  font-size: 14px;
  width: 260px;
  line-height: 1;
  padding: 5px 8px 4px 28px;
  border: 1px solid ${p => p.theme.border};
  border-radius: 30px;
  height: 28px;

  box-shadow: inset ${p => p.theme.dropShadowLight};

  &:focus {
    outline: none;
    border: 1px solid ${p => p.theme.border};
  }

  &::placeholder {
    color: ${p => p.theme.formPlaceholder};
  }
`;
//# sourceMappingURL=index.jsx.map