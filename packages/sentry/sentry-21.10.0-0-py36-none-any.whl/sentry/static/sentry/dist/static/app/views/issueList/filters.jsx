Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const guideAnchor_1 = (0, tslib_1.__importDefault)(require("app/components/assistant/guideAnchor"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const displayOptions_1 = (0, tslib_1.__importDefault)(require("./displayOptions"));
const searchBar_1 = (0, tslib_1.__importDefault)(require("./searchBar"));
const sortOptions_1 = (0, tslib_1.__importDefault)(require("./sortOptions"));
class IssueListFilters extends React.Component {
    render() {
        const { organization, savedSearch, query, isSearchDisabled, sort, display, hasSessions, selectedProjects, onSidebarToggle, onSearch, onSortChange, onDisplayChange, tagValueLoader, tags, } = this.props;
        const isAssignedQuery = /\bassigned:/.test(query);
        const hasIssuePercentDisplay = organization.features.includes('issue-percent-display');
        return (<SearchContainer hasIssuePercentDisplay={hasIssuePercentDisplay}>
        <react_1.ClassNames>
          {({ css }) => (<guideAnchor_1.default target="assigned_or_suggested_query" disabled={!isAssignedQuery} containerClassName={css `
                width: 100%;
              `}>
              <searchBar_1.default organization={organization} query={query || ''} sort={sort} onSearch={onSearch} disabled={isSearchDisabled} excludeEnvironment supportedTags={tags} tagValueLoader={tagValueLoader} savedSearch={savedSearch} onSidebarToggle={onSidebarToggle}/>
            </guideAnchor_1.default>)}
        </react_1.ClassNames>

        <DropdownsWrapper hasIssuePercentDisplay={hasIssuePercentDisplay}>
          {hasIssuePercentDisplay && (<displayOptions_1.default onDisplayChange={onDisplayChange} display={display} hasSessions={hasSessions} hasMultipleProjectsSelected={selectedProjects.length !== 1 || selectedProjects[0] === -1}/>)}
          <sortOptions_1.default sort={sort} query={query} onSelect={onSortChange}/>
        </DropdownsWrapper>
      </SearchContainer>);
    }
}
const SearchContainer = (0, styled_1.default)('div') `
  display: inline-grid;
  grid-gap: ${(0, space_1.default)(1)};
  margin-bottom: ${(0, space_1.default)(2)};
  width: 100%;

  @media (min-width: ${p => p.theme.breakpoints[p.hasIssuePercentDisplay ? 1 : 0]}) {
    grid-template-columns: 1fr auto;
  }

  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    grid-template-columns: 1fr;
  }
`;
const DropdownsWrapper = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(1)};
  grid-template-columns: 1fr ${p => (p.hasIssuePercentDisplay ? '1fr' : '')};
  align-items: start;

  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    grid-template-columns: 1fr;
  }
`;
exports.default = IssueListFilters;
//# sourceMappingURL=filters.jsx.map