Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const dropdownButton_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownButton"));
const dropdownControl_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownControl"));
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const savedSearchMenu_1 = (0, tslib_1.__importDefault)(require("./savedSearchMenu"));
function SavedSearchSelector({ savedSearchList, onSavedSearchDelete, onSavedSearchSelect, organization, query, sort, }) {
    function getTitle() {
        const savedSearch = savedSearchList.find(search => search.query === query && search.sort === sort);
        return savedSearch ? savedSearch.name : (0, locale_1.t)('Custom Search');
    }
    return (<dropdownControl_1.default menuWidth="35vw" blendWithActor button={({ isOpen, getActorProps }) => (<StyledDropdownButton {...getActorProps()} isOpen={isOpen}>
          <ButtonTitle>{getTitle()}</ButtonTitle>
        </StyledDropdownButton>)}>
      <savedSearchMenu_1.default organization={organization} savedSearchList={savedSearchList} onSavedSearchSelect={onSavedSearchSelect} onSavedSearchDelete={onSavedSearchDelete} query={query} sort={sort}/>
    </dropdownControl_1.default>);
}
exports.default = SavedSearchSelector;
const StyledDropdownButton = (0, styled_1.default)(dropdownButton_1.default) `
  color: ${p => p.theme.textColor};
  background-color: ${p => p.theme.background};
  border-right: 0;
  border-color: ${p => p.theme.border};
  z-index: ${p => p.theme.zIndex.dropdownAutocomplete.actor};
  border-radius: ${p => p.isOpen
    ? `${p.theme.borderRadius} 0 0 0`
    : `${p.theme.borderRadius} 0 0 ${p.theme.borderRadius}`};
  white-space: nowrap;
  max-width: 200px;
  margin-right: 0;

  &:hover,
  &:focus,
  &:active {
    border-color: ${p => p.theme.border};
    border-right: 0;
  }
`;
const ButtonTitle = (0, styled_1.default)('span') `
  ${overflowEllipsis_1.default}
`;
//# sourceMappingURL=savedSearchSelector.jsx.map