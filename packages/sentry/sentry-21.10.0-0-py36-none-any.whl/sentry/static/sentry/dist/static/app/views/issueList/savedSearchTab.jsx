Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const badge_1 = (0, tslib_1.__importDefault)(require("app/components/badge"));
const dropdownLink_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownLink"));
const queryCount_1 = (0, tslib_1.__importDefault)(require("app/components/queryCount"));
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const savedSearchMenu_1 = (0, tslib_1.__importDefault)(require("./savedSearchMenu"));
function SavedSearchTab({ isActive, organization, savedSearchList, onSavedSearchSelect, onSavedSearchDelete, query, queryCount, sort, }) {
    const savedSearch = savedSearchList.find(search => search.query === query && search.sort === sort);
    const title = (<TitleWrapper>
      {isActive ? (<react_1.Fragment>
          <TitleTextOverflow>
            {savedSearch ? savedSearch.name : (0, locale_1.t)('Custom Search')}{' '}
          </TitleTextOverflow>
          {queryCount !== undefined && queryCount > 0 && (<div>
              <badge_1.default>
                <queryCount_1.default hideParens count={queryCount} max={1000}/>
              </badge_1.default>
            </div>)}
        </react_1.Fragment>) : ((0, locale_1.t)('Saved Searches'))}
    </TitleWrapper>);
    return (<TabWrapper isActive={isActive} className="saved-search-tab">
      <StyledDropdownLink alwaysRenderMenu={false} anchorMiddle caret title={title} isActive={isActive}>
        <savedSearchMenu_1.default organization={organization} savedSearchList={savedSearchList} onSavedSearchSelect={onSavedSearchSelect} onSavedSearchDelete={onSavedSearchDelete} query={query} sort={sort}/>
      </StyledDropdownLink>
    </TabWrapper>);
}
exports.default = SavedSearchTab;
const TabWrapper = (0, styled_1.default)('li') `
  /* Color matches nav-tabs - overwritten using dark mode class saved-search-tab */
  border-bottom: ${p => (p.isActive ? `4px solid #6c5fc7` : 0)};
  /* Reposition menu under caret */
  & > span {
    display: block;
  }
  & > span > .dropdown-menu {
    padding: 0;
    margin-top: ${(0, space_1.default)(1)};
    min-width: 20vw;
    max-width: 25vw;
    z-index: ${p => p.theme.zIndex.globalSelectionHeader};

    :after {
      border-bottom-color: ${p => p.theme.backgroundSecondary};
    }
  }

  @media (max-width: ${p => p.theme.breakpoints[4]}) {
    & > span > .dropdown-menu {
      max-width: 30vw;
    }
  }

  @media (max-width: ${p => p.theme.breakpoints[1]}) {
    & > span > .dropdown-menu {
      max-width: 50vw;
    }
  }
`;
const TitleWrapper = (0, styled_1.default)('span') `
  margin-right: ${(0, space_1.default)(0.5)};
  user-select: none;
  display: flex;
  align-items: center;
`;
const TitleTextOverflow = (0, styled_1.default)('span') `
  margin-right: ${(0, space_1.default)(0.5)};
  max-width: 150px;
  ${overflowEllipsis_1.default};
`;
const StyledDropdownLink = (0, styled_1.default)(dropdownLink_1.default) `
  position: relative;
  display: block;
  padding: ${(0, space_1.default)(1)} 0;
  /* Important to override a media query from .nav-tabs */
  font-size: ${p => p.theme.fontSizeLarge} !important;
  text-align: center;
  text-transform: capitalize;
  /* TODO(scttcper): Replace hex color when nav-tabs is replaced */
  color: ${p => (p.isActive ? p.theme.textColor : '#7c6a8e')};

  :hover {
    color: #2f2936;
  }
`;
//# sourceMappingURL=savedSearchTab.jsx.map