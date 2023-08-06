Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = (0, tslib_1.__importDefault)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const guideAnchor_1 = (0, tslib_1.__importDefault)(require("app/components/assistant/guideAnchor"));
const dropdownControl_1 = (0, tslib_1.__importStar)(require("app/components/dropdownControl"));
const featureBadge_1 = (0, tslib_1.__importDefault)(require("app/components/featureBadge"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const locale_1 = require("app/locale");
const utils_1 = require("app/views/issueList/utils");
const IssueListDisplayOptions = ({ onDisplayChange, display, hasSessions, hasMultipleProjectsSelected, }) => {
    const getMenuItem = (key) => {
        let tooltipText;
        let disabled = false;
        if (key === utils_1.IssueDisplayOptions.SESSIONS) {
            if (hasMultipleProjectsSelected) {
                tooltipText = (0, locale_1.t)('This option is not available when multiple projects are selected.');
                disabled = true;
            }
            else if (!hasSessions) {
                tooltipText = (0, locale_1.t)('This option is not available because there is no session data in the selected time period.');
                disabled = true;
            }
        }
        return (<dropdownControl_1.DropdownItem onSelect={onDisplayChange} eventKey={key} isActive={key === display} disabled={disabled}>
        <StyledTooltip containerDisplayMode="block" position="top" title={tooltipText} disabled={!tooltipText}>
          {(0, utils_1.getDisplayLabel)(key)}
          {key === utils_1.IssueDisplayOptions.SESSIONS && <featureBadge_1.default type="beta" noTooltip/>}
        </StyledTooltip>
      </dropdownControl_1.DropdownItem>);
    };
    return (<guideAnchor_1.default target="percentage_based_alerts" position="bottom" disabled={!hasSessions || hasMultipleProjectsSelected}>
      <StyledDropdownControl buttonProps={{
            prefix: (0, locale_1.t)('Display'),
        }} buttonTooltipTitle={display === utils_1.IssueDisplayOptions.SESSIONS
            ? (0, locale_1.t)('This shows the event count as a percent of sessions in the same time period.')
            : null} label={!hasSessions || hasMultipleProjectsSelected
            ? (0, utils_1.getDisplayLabel)(utils_1.IssueDisplayOptions.EVENTS)
            : (0, utils_1.getDisplayLabel)(display)}>
        <react_1.default.Fragment>
          {getMenuItem(utils_1.IssueDisplayOptions.EVENTS)}
          {getMenuItem(utils_1.IssueDisplayOptions.SESSIONS)}
        </react_1.default.Fragment>
      </StyledDropdownControl>
    </guideAnchor_1.default>);
};
const StyledTooltip = (0, styled_1.default)(tooltip_1.default) `
  width: 100%;
`;
const StyledDropdownControl = (0, styled_1.default)(dropdownControl_1.default) `
  z-index: ${p => p.theme.zIndex.issuesList.displayOptions};

  button {
    width: 100%;
  }

  @media (max-width: ${p => p.theme.breakpoints[2]}) {
    order: 1;
  }
`;
exports.default = IssueListDisplayOptions;
//# sourceMappingURL=displayOptions.jsx.map