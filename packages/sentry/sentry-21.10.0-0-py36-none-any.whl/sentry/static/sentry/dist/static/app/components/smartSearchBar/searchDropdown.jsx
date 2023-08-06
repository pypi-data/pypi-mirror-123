Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const types_1 = require("./types");
class SearchDropdown extends react_1.PureComponent {
    constructor() {
        super(...arguments);
        this.renderDescription = (item) => {
            const searchSubstring = this.props.searchSubstring;
            if (!searchSubstring) {
                return item.desc;
            }
            const text = item.desc;
            if (!text) {
                return null;
            }
            const idx = text.toLowerCase().indexOf(searchSubstring.toLowerCase());
            if (idx === -1) {
                return item.desc;
            }
            return (<span>
        {text.substr(0, idx)}
        <strong>{text.substr(idx, searchSubstring.length)}</strong>
        {text.substr(idx + searchSubstring.length)}
      </span>);
        };
        this.renderHeaderItem = (item) => (<SearchDropdownGroup key={item.title}>
      <SearchDropdownGroupTitle>
        {item.icon}
        {item.title && item.title}
        {item.desc && <span>{item.desc}</span>}
      </SearchDropdownGroupTitle>
    </SearchDropdownGroup>);
        this.renderItem = (item) => (<SearchListItem key={item.value || item.desc} className={item.active ? 'active' : undefined} data-test-id="search-autocomplete-item" onClick={this.props.onClick.bind(this, item.value, item)} ref={element => { var _a; return item.active && ((_a = element === null || element === void 0 ? void 0 : element.scrollIntoView) === null || _a === void 0 ? void 0 : _a.call(element, { block: 'nearest' })); }}>
      <SearchItemTitleWrapper>
        {item.title && item.title + ' · '}
        <Description>{this.renderDescription(item)}</Description>
      </SearchItemTitleWrapper>
    </SearchListItem>);
    }
    render() {
        const { className, loading, items } = this.props;
        return (<StyledSearchDropdown className={className}>
        {loading ? (<LoadingWrapper key="loading" data-test-id="search-autocomplete-loading">
            <loadingIndicator_1.default mini/>
          </LoadingWrapper>) : (<SearchItemsList>
            {items.map(item => {
                    const isEmpty = item.children && !item.children.length;
                    const invalidTag = item.type === types_1.ItemType.INVALID_TAG;
                    // Hide header if `item.children` is defined, an array, and is empty
                    return (<react_1.Fragment key={item.title}>
                  {invalidTag && <Info>{(0, locale_1.t)('Invalid tag')}</Info>}
                  {item.type === 'header' && this.renderHeaderItem(item)}
                  {item.children && item.children.map(this.renderItem)}
                  {isEmpty && !invalidTag && <Info>{(0, locale_1.t)('No items found')}</Info>}
                </react_1.Fragment>);
                })}
          </SearchItemsList>)}
      </StyledSearchDropdown>);
    }
}
SearchDropdown.defaultProps = {
    searchSubstring: '',
    onClick: function () { },
};
exports.default = SearchDropdown;
const StyledSearchDropdown = (0, styled_1.default)('div') `
  /* Container has a border that we need to account for */
  position: absolute;
  top: 100%;
  left: -1px;
  right: -1px;
  z-index: ${p => p.theme.zIndex.dropdown};
  overflow: hidden;
  background: ${p => p.theme.background};
  box-shadow: ${p => p.theme.dropShadowLight};
  border: 1px solid ${p => p.theme.border};
  border-radius: ${p => p.theme.borderRadiusBottom};
`;
const LoadingWrapper = (0, styled_1.default)('div') `
  display: flex;
  justify-content: center;
  padding: ${(0, space_1.default)(1)};
`;
const Info = (0, styled_1.default)('div') `
  display: flex;
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};
  font-size: ${p => p.theme.fontSizeLarge};
  color: ${p => p.theme.gray300};

  &:not(:last-child) {
    border-bottom: 1px solid ${p => p.theme.innerBorder};
  }
`;
const ListItem = (0, styled_1.default)('li') `
  &:not(:last-child) {
    border-bottom: 1px solid ${p => p.theme.innerBorder};
  }
`;
const SearchDropdownGroup = (0, styled_1.default)(ListItem) ``;
const SearchDropdownGroupTitle = (0, styled_1.default)('header') `
  display: flex;
  align-items: center;

  background-color: ${p => p.theme.backgroundSecondary};
  color: ${p => p.theme.gray300};
  font-weight: normal;
  font-size: ${p => p.theme.fontSizeMedium};

  margin: 0;
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};

  & > svg {
    margin-right: ${(0, space_1.default)(1)};
  }
`;
const SearchItemsList = (0, styled_1.default)('ul') `
  padding-left: 0;
  list-style: none;
  margin-bottom: 0;
`;
const SearchListItem = (0, styled_1.default)(ListItem) `
  scroll-margin: 40px 0;
  font-size: ${p => p.theme.fontSizeLarge};
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};
  cursor: pointer;

  &:hover,
  &.active {
    background: ${p => p.theme.focus};
  }
`;
const SearchItemTitleWrapper = (0, styled_1.default)('div') `
  color: ${p => p.theme.textColor};
  font-weight: normal;
  font-size: ${p => p.theme.fontSizeMedium};
  margin: 0;
  line-height: ${p => p.theme.text.lineHeightHeading};
  ${overflowEllipsis_1.default};
`;
const Description = (0, styled_1.default)('span') `
  font-size: ${p => p.theme.fontSizeSmall};
  font-family: ${p => p.theme.text.familyMono};
`;
//# sourceMappingURL=searchDropdown.jsx.map