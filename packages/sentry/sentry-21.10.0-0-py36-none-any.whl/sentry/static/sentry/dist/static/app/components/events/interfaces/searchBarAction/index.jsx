Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const searchBar_1 = (0, tslib_1.__importDefault)(require("app/components/searchBar"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
function SearchBarAction({ onChange, query, placeholder, filter, className }) {
    return (<Wrapper className={className}>
      {filter}
      <StyledSearchBar onChange={onChange} query={query} placeholder={placeholder} blendWithFilter={!!filter}/>
    </Wrapper>);
}
exports.default = SearchBarAction;
const Wrapper = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(2)};
  width: 100%;
  margin-top: ${(0, space_1.default)(1)};
  position: relative;

  @media (min-width: ${props => props.theme.breakpoints[0]}) {
    margin-top: 0;
    grid-gap: 0;
    grid-template-columns: ${p => p.children && react_1.Children.toArray(p.children).length === 1
    ? '1fr'
    : 'max-content 1fr'};
    justify-content: flex-end;
  }

  @media (min-width: ${props => props.theme.breakpoints[1]}) {
    width: 400px;
  }

  @media (min-width: ${props => props.theme.breakpoints[3]}) {
    width: 600px;
  }
`;
// TODO(matej): remove this once we refactor SearchBar to not use css classes
// - it could accept size as a prop
const StyledSearchBar = (0, styled_1.default)(searchBar_1.default) `
  width: 100%;
  position: relative;
  .search-input {
    height: 32px;
  }
  .search-clear-form,
  .search-input-icon {
    height: 32px;
    display: flex;
    align-items: center;
  }

  @media (min-width: ${props => props.theme.breakpoints[0]}) {
    ${p => p.blendWithFilter &&
    `
        .search-input,
        .search-input:focus {
          border-top-left-radius: 0;
          border-bottom-left-radius: 0;
        }
      `}
  }
`;
//# sourceMappingURL=index.jsx.map