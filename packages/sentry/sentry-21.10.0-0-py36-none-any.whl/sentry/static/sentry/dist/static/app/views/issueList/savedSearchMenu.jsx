Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const access_1 = (0, tslib_1.__importDefault)(require("app/components/acl/access"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const menuItem_1 = (0, tslib_1.__importDefault)(require("app/components/menuItem"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("./utils");
function SavedSearchMenuItem({ organization, onSavedSearchSelect, onSavedSearchDelete, search, query, sort, isLast, }) {
    return (<tooltip_1.default title={<react_1.Fragment>
          {`${search.name} \u2022 `}
          <TooltipSearchQuery>{search.query}</TooltipSearchQuery>
          {` \u2022 `}
          {(0, locale_1.t)('Sort: ')}
          {(0, utils_1.getSortLabel)(search.sort)}
        </react_1.Fragment>} containerDisplayMode="block" delay={1000}>
      <StyledMenuItem isActive={search.query === query && search.sort === sort} isLast={isLast}>
        <MenuItemLink tabIndex={-1} onClick={() => onSavedSearchSelect(search)}>
          <SearchTitle>{search.name}</SearchTitle>
          <SearchQueryContainer>
            <SearchQuery>{search.query}</SearchQuery>
            <SearchSort>
              {(0, locale_1.t)('Sort: ')}
              {(0, utils_1.getSortLabel)(search.sort)}
            </SearchSort>
          </SearchQueryContainer>
        </MenuItemLink>
        {search.isGlobal === false && search.isPinned === false && (<access_1.default organization={organization} access={['org:write']} renderNoAccessMessage={false}>
            <confirm_1.default onConfirm={() => onSavedSearchDelete(search)} message={(0, locale_1.t)('Are you sure you want to delete this saved search?')} stopPropagation>
              <DeleteButton borderless title={(0, locale_1.t)('Delete this saved search')} icon={<icons_1.IconDelete />} label={(0, locale_1.t)('delete')} size="zero"/>
            </confirm_1.default>
          </access_1.default>)}
      </StyledMenuItem>
    </tooltip_1.default>);
}
function SavedSearchMenu(_a) {
    var { savedSearchList } = _a, props = (0, tslib_1.__rest)(_a, ["savedSearchList"]);
    const savedSearches = savedSearchList.filter(search => !search.isGlobal);
    let globalSearches = savedSearchList.filter(search => search.isGlobal);
    // Hide "Unresolved Issues" since they have a unresolved tab
    globalSearches = globalSearches.filter(search => !search.isPinned && search.query !== 'is:unresolved');
    return (<react_1.Fragment>
      <MenuHeader>{(0, locale_1.t)('Saved Searches')}</MenuHeader>
      {savedSearches.length === 0 ? (<EmptyItem>{(0, locale_1.t)('No saved searches yet.')}</EmptyItem>) : (savedSearches.map((search, index) => (<SavedSearchMenuItem key={search.id} search={search} isLast={index === savedSearches.length - 1} {...props}/>)))}
      <SecondaryMenuHeader>{(0, locale_1.t)('Recommended Searches')}</SecondaryMenuHeader>
      {/* Could only happen on self-hosted */}
      {globalSearches.length === 0 ? (<EmptyItem>{(0, locale_1.t)('No recommended searches yet.')}</EmptyItem>) : (globalSearches.map((search, index) => (<SavedSearchMenuItem key={search.id} search={search} isLast={index === globalSearches.length - 1} {...props}/>)))}
    </react_1.Fragment>);
}
exports.default = SavedSearchMenu;
const SearchTitle = (0, styled_1.default)('div') `
  color: ${p => p.theme.textColor};
  ${overflowEllipsis_1.default}
`;
const SearchQueryContainer = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeExtraSmall};
  ${overflowEllipsis_1.default}
`;
const SearchQuery = (0, styled_1.default)('code') `
  color: ${p => p.theme.subText};
  font-size: ${p => p.theme.fontSizeExtraSmall};
  padding: 0;
  background: inherit;
`;
const SearchSort = (0, styled_1.default)('span') `
  color: ${p => p.theme.subText};
  font-size: ${p => p.theme.fontSizeExtraSmall};
  &:before {
    font-size: ${p => p.theme.fontSizeExtraSmall};
    color: ${p => p.theme.textColor};
    content: ' \u2022 ';
  }
`;
const TooltipSearchQuery = (0, styled_1.default)('span') `
  color: ${p => p.theme.gray200};
  font-weight: normal;
  font-family: ${p => p.theme.text.familyMono};
`;
const DeleteButton = (0, styled_1.default)(button_1.default) `
  color: ${p => p.theme.gray200};
  background: transparent;
  flex-shrink: 0;
  padding: ${(0, space_1.default)(1)} 0;

  &:hover {
    background: transparent;
    color: ${p => p.theme.blue300};
  }
`;
const MenuHeader = (0, styled_1.default)('div') `
  align-items: center;
  color: ${p => p.theme.gray400};
  background: ${p => p.theme.backgroundSecondary};
  line-height: 0.75;
  padding: ${(0, space_1.default)(1.5)} ${(0, space_1.default)(2)};
  border-bottom: 1px solid ${p => p.theme.innerBorder};
  border-radius: ${p => p.theme.borderRadius} ${p => p.theme.borderRadius} 0 0;
`;
const SecondaryMenuHeader = (0, styled_1.default)(MenuHeader) `
  border-top: 1px solid ${p => p.theme.innerBorder};
  border-radius: 0;
`;
const StyledMenuItem = (0, styled_1.default)(menuItem_1.default) `
  border-bottom: ${p => (!p.isLast ? `1px solid ${p.theme.innerBorder}` : null)};
  font-size: ${p => p.theme.fontSizeMedium};

  & > span {
    padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};
  }

  ${p => p.isActive &&
    `
  ${SearchTitle}, ${SearchQuery}, ${SearchSort} {
    color: ${p.theme.white};
  }
  ${SearchSort}:before {
    color: ${p.theme.white};
  }
  &:hover {
    ${SearchTitle}, ${SearchQuery}, ${SearchSort} {
      color: ${p.theme.black};
    }
    ${SearchSort}:before {
      color: ${p.theme.black};
    }
  }
  `}
`;
const MenuItemLink = (0, styled_1.default)('a') `
  display: block;
  flex-grow: 1;
  /* Nav tabs style override */
  border: 0;

  ${overflowEllipsis_1.default}
`;
const EmptyItem = (0, styled_1.default)('li') `
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(1.5)};
  color: ${p => p.theme.subText};
`;
//# sourceMappingURL=savedSearchMenu.jsx.map