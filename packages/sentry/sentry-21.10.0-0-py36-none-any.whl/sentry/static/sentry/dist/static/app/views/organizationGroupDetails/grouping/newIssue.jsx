Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const eventOrGroupHeader_1 = (0, tslib_1.__importDefault)(require("app/components/eventOrGroupHeader"));
const timeSince_1 = (0, tslib_1.__importDefault)(require("app/components/timeSince"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
function NewIssue({ sampleEvent, eventCount, organization }) {
    return (<react_1.Fragment>
      <EventDetails>
        <eventOrGroupHeader_1.default data={sampleEvent} organization={organization} grouping hideIcons hideLevel/>
        <ExtraInfo>
          <TimeWrapper>
            <StyledIconClock size="11px"/>
            <timeSince_1.default date={sampleEvent.dateCreated
            ? sampleEvent.dateCreated
            : sampleEvent.dateReceived} suffix={(0, locale_1.t)('old')}/>
          </TimeWrapper>
        </ExtraInfo>
      </EventDetails>
      <EventCount>{eventCount}</EventCount>
    </react_1.Fragment>);
}
exports.default = NewIssue;
const EventDetails = (0, styled_1.default)('div') `
  overflow: hidden;
  line-height: 1.1;
`;
const ExtraInfo = (0, styled_1.default)('div') `
  display: grid;
  grid-auto-flow: column;
  grid-gap: ${(0, space_1.default)(2)};
  justify-content: flex-start;
`;
const TimeWrapper = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(0.5)};
  grid-template-columns: max-content 1fr;
  align-items: center;
  font-size: ${p => p.theme.fontSizeSmall};
`;
const EventCount = (0, styled_1.default)('div') `
  align-items: center;
  font-variant-numeric: tabular-nums;
  line-height: 1.1;
`;
const StyledIconClock = (0, styled_1.default)(icons_1.IconClock) `
  color: ${p => p.theme.subText};
`;
//# sourceMappingURL=newIssue.jsx.map