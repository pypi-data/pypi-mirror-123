Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const GroupListHeader = ({ withChart = true, narrowGroups = false }) => (<panels_1.PanelHeader disablePadding>
    <IssueWrapper>{(0, locale_1.t)('Issue')}</IssueWrapper>
    {withChart && (<ChartWrapper className={`hidden-xs hidden-sm ${narrowGroups ? 'hidden-md' : ''}`}>
        {(0, locale_1.t)('Graph')}
      </ChartWrapper>)}
    <EventUserWrapper>{(0, locale_1.t)('events')}</EventUserWrapper>
    <EventUserWrapper>{(0, locale_1.t)('users')}</EventUserWrapper>
    <AssigneeWrapper className="hidden-xs hidden-sm toolbar-header">
      {(0, locale_1.t)('Assignee')}
    </AssigneeWrapper>
  </panels_1.PanelHeader>);
exports.default = GroupListHeader;
const Heading = (0, styled_1.default)('div') `
  display: flex;
  align-self: center;
  margin: 0 ${(0, space_1.default)(2)};
`;
const IssueWrapper = (0, styled_1.default)(Heading) `
  flex: 1;
  width: 66.66%;

  @media (min-width: ${p => p.theme.breakpoints[1]}) {
    width: 50%;
  }
`;
const EventUserWrapper = (0, styled_1.default)(Heading) `
  justify-content: flex-end;
  width: 60px;

  @media (min-width: ${p => p.theme.breakpoints[3]}) {
    width: 80px;
  }
`;
const ChartWrapper = (0, styled_1.default)(Heading) `
  justify-content: space-between;
  width: 160px;
`;
const AssigneeWrapper = (0, styled_1.default)(Heading) `
  justify-content: flex-end;
  width: 80px;
`;
//# sourceMappingURL=groupListHeader.jsx.map