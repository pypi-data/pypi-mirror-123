Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const progressBar_1 = (0, tslib_1.__importDefault)(require("app/components/progressBar"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
function ReprocessingProgress({ totalEvents, pendingEvents }) {
    const remainingEventsToReprocess = totalEvents - pendingEvents;
    const remainingEventsToReprocessPercent = (0, utils_1.percent)(remainingEventsToReprocess, totalEvents);
    return (<Wrapper>
      <Inner>
        <Header>
          <Title>{(0, locale_1.t)('Reprocessing\u2026')}</Title>
          {(0, locale_1.t)('Once the events in this issue have been reprocessed, you’ll be able to make changes and view any new issues that may have been created.')}
        </Header>
        <Content>
          <progressBar_1.default value={remainingEventsToReprocessPercent} variant="large"/>
          {(0, locale_1.tct)('[remainingEventsToReprocess]/[totalEvents] [event] reprocessed', {
            remainingEventsToReprocess,
            totalEvents,
            event: (0, locale_1.tn)('event', 'events', totalEvents),
        })}
        </Content>
      </Inner>
    </Wrapper>);
}
exports.default = ReprocessingProgress;
const Wrapper = (0, styled_1.default)('div') `
  margin: ${(0, space_1.default)(4)} 40px;
  flex: 1;
  text-align: center;

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    margin: 40px;
  }
`;
const Content = (0, styled_1.default)('div') `
  color: ${p => p.theme.gray300};
  font-size: ${p => p.theme.fontSizeMedium};
  display: grid;
  grid-gap: ${(0, space_1.default)(1.5)};
  justify-items: center;
  max-width: 402px;
  width: 100%;
`;
const Inner = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(3)};
  justify-items: center;
`;
const Header = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(1)};
  color: ${p => p.theme.textColor};
  max-width: 557px;
`;
const Title = (0, styled_1.default)('h3') `
  font-size: ${p => p.theme.headerFontSize};
  font-weight: 600;
  margin-bottom: 0;
`;
//# sourceMappingURL=reprocessingProgress.jsx.map