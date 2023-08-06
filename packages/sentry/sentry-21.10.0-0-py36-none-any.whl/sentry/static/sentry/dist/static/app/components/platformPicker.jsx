Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const debounce_1 = (0, tslib_1.__importDefault)(require("lodash/debounce"));
const platformicons_1 = require("platformicons");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const listLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/listLink"));
const navTabs_1 = (0, tslib_1.__importDefault)(require("app/components/navTabs"));
const constants_1 = require("app/constants");
const platformCategories_1 = (0, tslib_1.__importStar)(require("app/data/platformCategories"));
const platforms_1 = (0, tslib_1.__importDefault)(require("app/data/platforms"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const input_1 = require("app/styles/input");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const trackAdvancedAnalyticsEvent_1 = (0, tslib_1.__importDefault)(require("app/utils/analytics/trackAdvancedAnalyticsEvent"));
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const PLATFORM_CATEGORIES = [...platformCategories_1.default, { id: 'all', name: (0, locale_1.t)('All') }];
const PlatformList = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(1)};
  grid-template-columns: repeat(auto-fill, 112px);
  margin-bottom: ${(0, space_1.default)(2)};
`;
class PlatformPicker extends React.Component {
    constructor() {
        var _a;
        super(...arguments);
        this.state = {
            category: (_a = this.props.defaultCategory) !== null && _a !== void 0 ? _a : PLATFORM_CATEGORIES[0].id,
            filter: this.props.noAutoFilter ? '' : (this.props.platform || '').split('-')[0],
        };
        this.logSearch = (0, debounce_1.default)(() => {
            var _a;
            if (this.state.filter) {
                (0, trackAdvancedAnalyticsEvent_1.default)('growth.platformpicker_search', {
                    search: this.state.filter.toLowerCase(),
                    num_results: this.platformList.length,
                    source: this.props.source,
                    organization: (_a = this.props.organization) !== null && _a !== void 0 ? _a : null,
                });
            }
        }, constants_1.DEFAULT_DEBOUNCE_DURATION);
    }
    get platformList() {
        const { category } = this.state;
        const currentCategory = platformCategories_1.default.find(({ id }) => id === category);
        const filter = this.state.filter.toLowerCase();
        const subsetMatch = (platform) => {
            var _a;
            return platform.id.includes(filter) ||
                platform.name.toLowerCase().includes(filter) ||
                ((_a = platformCategories_1.filterAliases[platform.id]) === null || _a === void 0 ? void 0 : _a.some(alias => alias.includes(filter)));
        };
        const categoryMatch = (platform) => {
            var _a;
            return category === 'all' ||
                ((_a = currentCategory === null || currentCategory === void 0 ? void 0 : currentCategory.platforms) === null || _a === void 0 ? void 0 : _a.includes(platform.id));
        };
        const filtered = platforms_1.default
            .filter(this.state.filter ? subsetMatch : categoryMatch)
            .sort((a, b) => a.id.localeCompare(b.id));
        return this.props.showOther ? filtered : filtered.filter(({ id }) => id !== 'other');
    }
    render() {
        const platformList = this.platformList;
        const { setPlatform, listProps, listClassName } = this.props;
        const { filter, category } = this.state;
        return (<React.Fragment>
        <NavContainer>
          <CategoryNav>
            {PLATFORM_CATEGORIES.map(({ id, name }) => (<listLink_1.default key={id} onClick={(e) => {
                    var _a;
                    (0, trackAdvancedAnalyticsEvent_1.default)('growth.platformpicker_category', {
                        category: id,
                        source: this.props.source,
                        organization: (_a = this.props.organization) !== null && _a !== void 0 ? _a : null,
                    });
                    this.setState({ category: id, filter: '' });
                    e.preventDefault();
                }} to="" isActive={() => id === (filter ? 'all' : category)}>
                {name}
              </listLink_1.default>))}
          </CategoryNav>
          <SearchBar>
            <icons_1.IconSearch size="xs"/>
            <input type="text" value={filter} placeholder={(0, locale_1.t)('Filter Platforms')} onChange={e => this.setState({ filter: e.target.value }, this.logSearch)}/>
          </SearchBar>
        </NavContainer>
        <PlatformList className={listClassName} {...listProps}>
          {platformList.map(platform => (<PlatformCard data-test-id={`platform-${platform.id}`} key={platform.id} platform={platform} selected={this.props.platform === platform.id} onClear={(e) => {
                    setPlatform(null);
                    e.stopPropagation();
                }} onClick={() => {
                    var _a;
                    (0, trackAdvancedAnalyticsEvent_1.default)('growth.select_platform', {
                        platform_id: platform.id,
                        source: this.props.source,
                        organization: (_a = this.props.organization) !== null && _a !== void 0 ? _a : null,
                    });
                    setPlatform(platform.id);
                }}/>))}
        </PlatformList>
        {platformList.length === 0 && (<emptyMessage_1.default icon={<icons_1.IconProject size="xl"/>} title={(0, locale_1.t)("We don't have an SDK for that yet!")}>
            {(0, locale_1.tct)(`Not finding your platform? You can still create your project,
              but looks like we don't have an official SDK for your platform
              yet. However, there's a rich ecosystem of community supported
              SDKs (including Perl, CFML, Clojure, and ActionScript). Try
              [search:searching for Sentry clients] or contacting support.`, {
                    search: (<externalLink_1.default href="https://github.com/search?q=-org%3Agetsentry+topic%3Asentry&type=Repositories"/>),
                })}
          </emptyMessage_1.default>)}
      </React.Fragment>);
    }
}
PlatformPicker.defaultProps = {
    showOther: true,
};
const NavContainer = (0, styled_1.default)('div') `
  margin-bottom: ${(0, space_1.default)(2)};
  display: grid;
  grid-gap: ${(0, space_1.default)(2)};
  grid-template-columns: 1fr minmax(0, 300px);
  align-items: start;
  border-bottom: 1px solid ${p => p.theme.border};
`;
const SearchBar = (0, styled_1.default)('div') `
  ${p => (0, input_1.inputStyles)(p)};
  padding: 0 8px;
  color: ${p => p.theme.subText};
  display: flex;
  align-items: center;
  font-size: 15px;
  margin-top: -${(0, space_1.default)(0.75)};

  input {
    border: none;
    background: none;
    padding: 2px 4px;
    width: 100%;
    /* Ensure a consistent line height to keep the input the desired height */
    line-height: 24px;

    &:focus {
      outline: none;
    }
  }
`;
const CategoryNav = (0, styled_1.default)(navTabs_1.default) `
  margin: 0;
  margin-top: 4px;
  white-space: nowrap;

  > li {
    float: none;
    display: inline-block;
  }
`;
const StyledPlatformIcon = (0, styled_1.default)(platformicons_1.PlatformIcon) `
  margin: ${(0, space_1.default)(2)};
`;
const ClearButton = (0, styled_1.default)(button_1.default) `
  position: absolute;
  top: -6px;
  right: -6px;
  height: 22px;
  width: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: ${p => p.theme.background};
  color: ${p => p.theme.textColor};
`;
ClearButton.defaultProps = {
    icon: <icons_1.IconClose isCircled size="xs"/>,
    borderless: true,
    size: 'xsmall',
};
const PlatformCard = (0, styled_1.default)((_a) => {
    var { platform, selected, onClear } = _a, props = (0, tslib_1.__rest)(_a, ["platform", "selected", "onClear"]);
    return (<div {...props}>
    <StyledPlatformIcon platform={platform.id} size={56} radius={5} withLanguageIcon format="lg"/>

    <h3>{platform.name}</h3>
    {selected && <ClearButton onClick={onClear}/>}
  </div>);
}) `
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0 0 14px;
  border-radius: 4px;
  cursor: pointer;
  background: ${p => p.selected && p.theme.alert.info.backgroundLight};

  &:hover {
    background: ${p => p.theme.alert.muted.backgroundLight};
  }

  h3 {
    flex-grow: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    color: ${p => (p.selected ? p.theme.textColor : p.theme.subText)};
    text-align: center;
    font-size: ${p => p.theme.fontSizeExtraSmall};
    text-transform: uppercase;
    margin: 0;
    padding: 0 ${(0, space_1.default)(0.5)};
    line-height: 1.2;
  }
`;
exports.default = PlatformPicker;
//# sourceMappingURL=platformPicker.jsx.map