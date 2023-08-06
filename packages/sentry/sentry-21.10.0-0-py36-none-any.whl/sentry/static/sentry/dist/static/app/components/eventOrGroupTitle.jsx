Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const guideAnchor_1 = (0, tslib_1.__importDefault)(require("app/components/assistant/guideAnchor"));
const projectsStore_1 = (0, tslib_1.__importDefault)(require("app/stores/projectsStore"));
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const events_1 = require("app/utils/events");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const eventTitleTreeLabel_1 = (0, tslib_1.__importDefault)(require("./eventTitleTreeLabel"));
const stacktracePreview_1 = (0, tslib_1.__importDefault)(require("./stacktracePreview"));
function EventOrGroupTitle({ guideAnchorName = 'issue_title', organization, data, withStackTracePreview, hasGuideAnchor, grouping = false, className, }) {
    var _a, _b;
    const event = data;
    const groupingCurrentLevel = (_a = data.metadata) === null || _a === void 0 ? void 0 : _a.current_level;
    const hasGroupingTreeUI = !!(organization === null || organization === void 0 ? void 0 : organization.features.includes('grouping-tree-ui'));
    const hasGroupingStacktraceUI = !!(organization === null || organization === void 0 ? void 0 : organization.features.includes('grouping-stacktrace-ui'));
    const { id, eventID, groupID, projectID } = event;
    const { title, subtitle, treeLabel } = (0, events_1.getTitle)(event, organization === null || organization === void 0 ? void 0 : organization.features, grouping);
    return (<Wrapper className={className} hasGroupingTreeUI={hasGroupingTreeUI}>
      <guideAnchor_1.default disabled={!hasGuideAnchor} target={guideAnchorName} position="bottom">
        <StyledStacktracePreview organization={organization} issueId={groupID ? groupID : id} groupingCurrentLevel={groupingCurrentLevel} 
    // we need eventId and projectSlug only when hovering over Event, not Group
    // (different API call is made to get the stack trace then)
    eventId={eventID} projectSlug={eventID ? (_b = projectsStore_1.default.getById(projectID)) === null || _b === void 0 ? void 0 : _b.slug : undefined} disablePreview={!withStackTracePreview} hasGroupingStacktraceUI={hasGroupingStacktraceUI}>
          {treeLabel ? <eventTitleTreeLabel_1.default treeLabel={treeLabel}/> : title}
        </StyledStacktracePreview>
      </guideAnchor_1.default>
      {subtitle && (<react_1.Fragment>
          <Spacer />
          <Subtitle title={subtitle}>{subtitle}</Subtitle>
          <br />
        </react_1.Fragment>)}
    </Wrapper>);
}
exports.default = (0, withOrganization_1.default)(EventOrGroupTitle);
/**
 * &nbsp; is used instead of margin/padding to split title and subtitle
 * into 2 separate text nodes on the HTML AST. This allows the
 * title to be highlighted without spilling over to the subtitle.
 */
const Spacer = () => <span style={{ display: 'inline-block', width: 10 }}>&nbsp;</span>;
const Subtitle = (0, styled_1.default)('em') `
  color: ${p => p.theme.gray300};
  font-style: normal;
`;
const StyledStacktracePreview = (0, styled_1.default)(stacktracePreview_1.default) `
  ${p => p.hasGroupingStacktraceUI &&
    `
      display: inline-flex;
      overflow: hidden;
      > span:first-child {
        ${overflowEllipsis_1.default}
      }
    `}
`;
const Wrapper = (0, styled_1.default)('span') `
  ${p => p.hasGroupingTreeUI &&
    `
      display: inline-grid;
      grid-template-columns: auto max-content 1fr max-content;
      align-items: flex-end;
      line-height: 100%;

      ${Subtitle} {
        ${overflowEllipsis_1.default};
        display: inline-block;
      }
    `}
`;
//# sourceMappingURL=eventOrGroupTitle.jsx.map