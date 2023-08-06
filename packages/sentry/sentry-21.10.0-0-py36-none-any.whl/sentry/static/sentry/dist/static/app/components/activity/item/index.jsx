Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const moment_timezone_1 = (0, tslib_1.__importDefault)(require("moment-timezone"));
const dateTime_1 = (0, tslib_1.__importDefault)(require("app/components/dateTime"));
const timeSince_1 = (0, tslib_1.__importDefault)(require("app/components/timeSince"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const text_1 = (0, tslib_1.__importDefault)(require("app/styles/text"));
const isRenderFunc_1 = require("app/utils/isRenderFunc");
const avatar_1 = (0, tslib_1.__importDefault)(require("./avatar"));
const bubble_1 = (0, tslib_1.__importDefault)(require("./bubble"));
function ActivityItem({ author, avatarSize, bubbleProps, className, children, date, interval, footer, id, header, hideDate = false, showTime = false, }) {
    const showDate = !hideDate && date && !interval;
    const showRange = !hideDate && date && interval;
    const dateEnded = showRange
        ? (0, moment_timezone_1.default)(date).add(interval, 'minutes').utc().format()
        : undefined;
    const timeOnly = Boolean(date && dateEnded && (0, moment_timezone_1.default)(date).date() === (0, moment_timezone_1.default)(dateEnded).date());
    return (<ActivityItemWrapper data-test-id="activity-item" className={className}>
      {id && <a id={id}/>}

      {author && (<StyledActivityAvatar type={author.type} user={author.user} size={avatarSize}/>)}

      <StyledActivityBubble {...bubbleProps}>
        {header && (0, isRenderFunc_1.isRenderFunc)(header) && header()}
        {header && !(0, isRenderFunc_1.isRenderFunc)(header) && (<ActivityHeader>
            <ActivityHeaderContent>{header}</ActivityHeaderContent>
            {date && showDate && !showTime && <StyledTimeSince date={date}/>}
            {date && showDate && showTime && <StyledDateTime timeOnly date={date}/>}

            {showRange && (<StyledDateTimeWindow>
                <StyledDateTime timeOnly={timeOnly} timeAndDate={!timeOnly} date={date}/>
                {' — '}
                <StyledDateTime timeOnly={timeOnly} timeAndDate={!timeOnly} date={dateEnded}/>
              </StyledDateTimeWindow>)}
          </ActivityHeader>)}

        {children && (0, isRenderFunc_1.isRenderFunc)(children) && children()}
        {children && !(0, isRenderFunc_1.isRenderFunc)(children) && (<ActivityBody>{children}</ActivityBody>)}

        {footer && (0, isRenderFunc_1.isRenderFunc)(footer) && footer()}
        {footer && !(0, isRenderFunc_1.isRenderFunc)(footer) && (<ActivityFooter>{footer}</ActivityFooter>)}
      </StyledActivityBubble>
    </ActivityItemWrapper>);
}
const ActivityItemWrapper = (0, styled_1.default)('div') `
  display: flex;
  margin-bottom: ${(0, space_1.default)(2)};
`;
const HeaderAndFooter = (0, styled_1.default)('div') `
  padding: 6px ${(0, space_1.default)(2)};
`;
const ActivityHeader = (0, styled_1.default)(HeaderAndFooter) `
  display: flex;
  border-bottom: 1px solid ${p => p.theme.border};
  font-size: ${p => p.theme.fontSizeMedium};

  &:last-child {
    border-bottom: none;
  }
`;
const ActivityHeaderContent = (0, styled_1.default)('div') `
  flex: 1;
`;
const ActivityFooter = (0, styled_1.default)(HeaderAndFooter) `
  display: flex;
  border-top: 1px solid ${p => p.theme.border};
  font-size: ${p => p.theme.fontSizeMedium};
`;
const ActivityBody = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(2)} ${(0, space_1.default)(2)};
  ${text_1.default}
`;
const StyledActivityAvatar = (0, styled_1.default)(avatar_1.default) `
  margin-right: ${(0, space_1.default)(1)};
`;
const StyledTimeSince = (0, styled_1.default)(timeSince_1.default) `
  color: ${p => p.theme.gray300};
`;
const StyledDateTime = (0, styled_1.default)(dateTime_1.default) `
  color: ${p => p.theme.gray300};
`;
const StyledDateTimeWindow = (0, styled_1.default)('div') `
  color: ${p => p.theme.gray300};
`;
const StyledActivityBubble = (0, styled_1.default)(bubble_1.default) `
  width: 75%;
  overflow-wrap: break-word;
`;
exports.default = ActivityItem;
//# sourceMappingURL=index.jsx.map