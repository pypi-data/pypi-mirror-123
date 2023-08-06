Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const utils_1 = require("app/components/events/interfaces/spans/utils");
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const utils_2 = require("app/components/performance/waterfall/utils");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_3 = require("../utils");
const utils_4 = require("./utils");
class TransactionSummary extends react_1.Component {
    render() {
        const { baselineEvent, regressionEvent, organization, location, params } = this.props;
        const { baselineEventSlug, regressionEventSlug } = params;
        if (!(0, utils_4.isTransactionEvent)(baselineEvent) || !(0, utils_4.isTransactionEvent)(regressionEvent)) {
            return null;
        }
        const baselineTrace = (0, utils_1.parseTrace)(baselineEvent);
        const regressionTrace = (0, utils_1.parseTrace)(regressionEvent);
        const baselineDuration = Math.abs(baselineTrace.traceStartTimestamp - baselineTrace.traceEndTimestamp);
        const regressionDuration = Math.abs(regressionTrace.traceStartTimestamp - regressionTrace.traceEndTimestamp);
        return (<Container>
        <EventRow>
          <Baseline />
          <EventRowContent>
            <Content>
              <ContentTitle>{(0, locale_1.t)('Baseline Event')}</ContentTitle>
              <EventId>
                <span>{(0, locale_1.t)('ID')}: </span>
                <StyledLink to={(0, utils_3.getTransactionDetailsUrl)(organization, baselineEventSlug.trim(), baselineEvent.title, location.query)}>
                  {shortEventId(baselineEvent.eventID)}
                </StyledLink>
              </EventId>
            </Content>
            <TimeDuration>
              <span>{(0, utils_2.getHumanDuration)(baselineDuration)}</span>
            </TimeDuration>
          </EventRowContent>
        </EventRow>
        <EventRow>
          <Regression />
          <EventRowContent>
            <Content>
              <ContentTitle>{(0, locale_1.t)('This Event')}</ContentTitle>
              <EventId>
                <span>{(0, locale_1.t)('ID')}: </span>
                <StyledLink to={(0, utils_3.getTransactionDetailsUrl)(organization, regressionEventSlug.trim(), regressionEvent.title, location.query)}>
                  {shortEventId(regressionEvent.eventID)}
                </StyledLink>
              </EventId>
            </Content>
            <TimeDuration>
              <span>{(0, utils_2.getHumanDuration)(regressionDuration)}</span>
            </TimeDuration>
          </EventRowContent>
        </EventRow>
      </Container>);
    }
}
const Container = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: column;

  justify-content: space-between;
  align-content: space-between;

  padding-bottom: ${(0, space_1.default)(1)};

  > * + * {
    margin-top: ${(0, space_1.default)(0.75)};
  }
`;
const EventRow = (0, styled_1.default)('div') `
  display: flex;
`;
const Baseline = (0, styled_1.default)('div') `
  background-color: ${p => p.theme.textColor};
  height: 100%;
  width: 4px;

  margin-right: ${(0, space_1.default)(1)};
`;
const Regression = (0, styled_1.default)('div') `
  background-color: ${p => p.theme.purple200};
  height: 100%;
  width: 4px;

  margin-right: ${(0, space_1.default)(1)};
`;
const EventRowContent = (0, styled_1.default)('div') `
  flex-grow: 1;
  display: flex;
`;
const TimeDuration = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;

  font-size: ${p => p.theme.headerFontSize};
  line-height: 1.2;

  margin-left: ${(0, space_1.default)(1)};
`;
const Content = (0, styled_1.default)('div') `
  flex-grow: 1;
  width: 150px;

  font-size: ${p => p.theme.fontSizeMedium};
`;
const ContentTitle = (0, styled_1.default)('div') `
  font-weight: 600;
`;
const EventId = (0, styled_1.default)('div') `
  color: ${p => p.theme.gray300};
`;
const StyledLink = (0, styled_1.default)(link_1.default) `
  color: ${p => p.theme.gray300};
`;
function shortEventId(value) {
    return value.substring(0, 8);
}
exports.default = TransactionSummary;
//# sourceMappingURL=transactionSummary.jsx.map