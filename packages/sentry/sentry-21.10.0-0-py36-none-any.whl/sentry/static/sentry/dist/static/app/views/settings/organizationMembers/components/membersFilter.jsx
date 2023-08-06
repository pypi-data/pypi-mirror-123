Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const checkbox_1 = (0, tslib_1.__importDefault)(require("app/components/checkbox"));
const switchButton_1 = (0, tslib_1.__importDefault)(require("app/components/switchButton"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const tokenizeSearch_1 = require("app/utils/tokenizeSearch");
const getBoolean = (list) => Array.isArray(list) && list.length
    ? list && list.map(v => v.toLowerCase()).includes('true')
    : null;
const MembersFilter = ({ className, roles, query, onChange }) => {
    const search = new tokenizeSearch_1.MutableSearch(query);
    const filters = {
        roles: search.getFilterValues('role') || [],
        isInvited: getBoolean(search.getFilterValues('isInvited')),
        ssoLinked: getBoolean(search.getFilterValues('ssoLinked')),
        has2fa: getBoolean(search.getFilterValues('has2fa')),
    };
    const handleRoleFilter = (id) => () => {
        const roleList = new Set(search.getFilterValues('role') ? [...search.getFilterValues('role')] : []);
        if (roleList.has(id)) {
            roleList.delete(id);
        }
        else {
            roleList.add(id);
        }
        const newSearch = search.copy();
        newSearch.setFilterValues('role', [...roleList]);
        onChange(newSearch.formatString());
    };
    const handleBoolFilter = (key) => (value) => {
        const newQueryObject = search.copy();
        newQueryObject.removeFilter(key);
        if (value !== null) {
            newQueryObject.setFilterValues(key, [Boolean(value).toString()]);
        }
        onChange(newQueryObject.formatString());
    };
    return (<FilterContainer className={className}>
      <FilterHeader>{(0, locale_1.t)('Filter By')}</FilterHeader>

      <FilterLists>
        <FilterList>
          <h3>{(0, locale_1.t)('User Role')}</h3>
          {roles.map(({ id, name }) => (<label key={id}>
              <checkbox_1.default data-test-id={`filter-role-${id}`} checked={filters.roles.includes(id)} onChange={handleRoleFilter(id)}/>
              {name}
            </label>))}
        </FilterList>

        <FilterList>
          <h3>{(0, locale_1.t)('Status')}</h3>
          <BooleanFilter data-test-id="filter-isInvited" onChange={handleBoolFilter('isInvited')} value={filters.isInvited}>
            {(0, locale_1.t)('Invited')}
          </BooleanFilter>
          <BooleanFilter data-test-id="filter-has2fa" onChange={handleBoolFilter('has2fa')} value={filters.has2fa}>
            {(0, locale_1.t)('2FA')}
          </BooleanFilter>
          <BooleanFilter data-test-id="filter-ssoLinked" onChange={handleBoolFilter('ssoLinked')} value={filters.ssoLinked}>
            {(0, locale_1.t)('SSO Linked')}
          </BooleanFilter>
        </FilterList>
      </FilterLists>
    </FilterContainer>);
};
const BooleanFilter = ({ onChange, value, children }) => (<label>
    <checkbox_1.default checked={value !== null} onChange={() => onChange(value === null ? true : null)}/>
    {children}
    <switchButton_1.default isDisabled={value === null} isActive={value === true} toggle={() => onChange(!value)}/>
  </label>);
const FilterContainer = (0, styled_1.default)('div') `
  border-radius: 4px;
  background: ${p => p.theme.background};
  box-shadow: ${p => p.theme.dropShadowLight};
  border: 1px solid ${p => p.theme.border};
`;
const FilterHeader = (0, styled_1.default)('h2') `
  border-top-left-radius: 4px;
  border-top-right-radius: 4px;
  border-bottom: 1px solid ${p => p.theme.border};
  background: ${p => p.theme.backgroundSecondary};
  color: ${p => p.theme.subText};
  text-transform: uppercase;
  font-size: ${p => p.theme.fontSizeExtraSmall};
  padding: ${(0, space_1.default)(1)};
  margin: 0;
`;
const FilterLists = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: 100px max-content;
  grid-gap: ${(0, space_1.default)(3)};
  margin: ${(0, space_1.default)(1.5)};
  margin-top: ${(0, space_1.default)(0.75)};
`;
const FilterList = (0, styled_1.default)('div') `
  display: grid;
  grid-template-rows: repeat(auto-fit, minmax(0, max-content));
  grid-gap: ${(0, space_1.default)(1)};
  font-size: ${p => p.theme.fontSizeMedium};

  h3 {
    color: #000;
    font-size: ${p => p.theme.fontSizeSmall};
    text-transform: uppercase;
    margin: ${(0, space_1.default)(1)} 0;
  }

  label {
    display: grid;
    grid-template-columns: max-content 1fr max-content;
    grid-gap: ${(0, space_1.default)(0.75)};
    align-items: center;
    font-weight: normal;
    white-space: nowrap;
    height: ${(0, space_1.default)(2)};
  }

  input,
  label {
    margin: 0;
  }
`;
exports.default = MembersFilter;
//# sourceMappingURL=membersFilter.jsx.map