Object.defineProperty(exports, "__esModule", { value: true });
exports.getSortTooltip = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const dropdownControl_1 = (0, tslib_1.__importStar)(require("app/components/dropdownControl"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const locale_1 = require("app/locale");
const utils_1 = require("app/views/issueList/utils");
function getSortTooltip(key) {
    switch (key) {
        case utils_1.IssueSortOptions.INBOX:
            return (0, locale_1.t)('When the issue was flagged for review.');
        case utils_1.IssueSortOptions.NEW:
            return (0, locale_1.t)('When the issue was first seen in the selected time period.');
        case utils_1.IssueSortOptions.PRIORITY:
            return (0, locale_1.t)('Issues trending upward recently.');
        case utils_1.IssueSortOptions.FREQ:
            return (0, locale_1.t)('Number of events in the time selected.');
        case utils_1.IssueSortOptions.USER:
            return (0, locale_1.t)('Number of users affected in the time selected.');
        case utils_1.IssueSortOptions.TREND:
            return (0, locale_1.t)('% change in event count over the time selected.');
        case utils_1.IssueSortOptions.DATE:
        default:
            return (0, locale_1.t)('When the issue was last seen in the selected time period.');
    }
}
exports.getSortTooltip = getSortTooltip;
const IssueListSortOptions = ({ onSelect, sort, query }) => {
    const sortKey = sort || utils_1.IssueSortOptions.DATE;
    const getMenuItem = (key) => (<dropdownControl_1.DropdownItem onSelect={onSelect} eventKey={key} isActive={sortKey === key}>
      <StyledTooltip containerDisplayMode="block" position="top" delay={500} title={getSortTooltip(key)}>
        {(0, utils_1.getSortLabel)(key)}
      </StyledTooltip>
    </dropdownControl_1.DropdownItem>);
    return (<StyledDropdownControl buttonProps={{ prefix: (0, locale_1.t)('Sort by') }} label={(0, utils_1.getSortLabel)(sortKey)}>
      <React.Fragment>
        {query === utils_1.Query.FOR_REVIEW && getMenuItem(utils_1.IssueSortOptions.INBOX)}
        {getMenuItem(utils_1.IssueSortOptions.DATE)}
        {getMenuItem(utils_1.IssueSortOptions.NEW)}
        {getMenuItem(utils_1.IssueSortOptions.PRIORITY)}
        {getMenuItem(utils_1.IssueSortOptions.FREQ)}
        {getMenuItem(utils_1.IssueSortOptions.USER)}
        <feature_1.default features={['issue-list-trend-sort']}>
          {getMenuItem(utils_1.IssueSortOptions.TREND)}
        </feature_1.default>
      </React.Fragment>
    </StyledDropdownControl>);
};
exports.default = IssueListSortOptions;
const StyledTooltip = (0, styled_1.default)(tooltip_1.default) `
  width: 100%;
`;
const StyledDropdownControl = (0, styled_1.default)(dropdownControl_1.default) `
  z-index: ${p => p.theme.zIndex.issuesList.sortOptions};

  button {
    width: 100%;
  }

  @media (max-width: ${p => p.theme.breakpoints[2]}) {
    order: 2;
  }
`;
//# sourceMappingURL=sortOptions.jsx.map