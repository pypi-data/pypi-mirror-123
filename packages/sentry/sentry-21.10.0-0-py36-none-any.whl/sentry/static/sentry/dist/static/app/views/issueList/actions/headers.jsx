Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const toolbarHeader_1 = (0, tslib_1.__importDefault)(require("app/components/toolbarHeader"));
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
function Headers({ selection, statsPeriod, onSelectStatsPeriod, isReprocessingQuery, }) {
    return (<react_1.Fragment>
      {isReprocessingQuery ? (<react_1.Fragment>
          <StartedColumn>{(0, locale_1.t)('Started')}</StartedColumn>
          <EventsReprocessedColumn>{(0, locale_1.t)('Events Reprocessed')}</EventsReprocessedColumn>
          <ProgressColumn>{(0, locale_1.t)('Progress')}</ProgressColumn>
        </react_1.Fragment>) : (<react_1.Fragment>
          <GraphHeaderWrapper className="hidden-xs hidden-sm hidden-md">
            <GraphHeader>
              <StyledToolbarHeader>{(0, locale_1.t)('Graph:')}</StyledToolbarHeader>
              {selection.datetime.period !== '24h' && (<GraphToggle active={statsPeriod === '24h'} onClick={() => onSelectStatsPeriod('24h')}>
                  {(0, locale_1.t)('24h')}
                </GraphToggle>)}
              <GraphToggle active={statsPeriod === 'auto'} onClick={() => onSelectStatsPeriod('auto')}>
                {selection.datetime.period || (0, locale_1.t)('Custom')}
              </GraphToggle>
            </GraphHeader>
          </GraphHeaderWrapper>
          <EventsOrUsersLabel>{(0, locale_1.t)('Events')}</EventsOrUsersLabel>
          <EventsOrUsersLabel>{(0, locale_1.t)('Users')}</EventsOrUsersLabel>
          <AssigneesLabel className="hidden-xs hidden-sm">
            <toolbarHeader_1.default>{(0, locale_1.t)('Assignee')}</toolbarHeader_1.default>
          </AssigneesLabel>
        </react_1.Fragment>)}
    </react_1.Fragment>);
}
exports.default = Headers;
const GraphHeaderWrapper = (0, styled_1.default)('div') `
  width: 160px;
  margin-left: ${(0, space_1.default)(2)};
  margin-right: ${(0, space_1.default)(2)};
  animation: 0.25s FadeIn linear forwards;

  @keyframes FadeIn {
    0% {
      opacity: 0;
    }
    100% {
      opacity: 1;
    }
  }
`;
const GraphHeader = (0, styled_1.default)('div') `
  display: flex;
`;
const StyledToolbarHeader = (0, styled_1.default)(toolbarHeader_1.default) `
  flex: 1;
`;
const GraphToggle = (0, styled_1.default)('a') `
  font-size: 13px;
  padding-left: ${(0, space_1.default)(1)};

  &,
  &:hover,
  &:focus,
  &:active {
    color: ${p => (p.active ? p.theme.textColor : p.theme.disabled)};
  }
`;
const EventsOrUsersLabel = (0, styled_1.default)(toolbarHeader_1.default) `
  display: inline-grid;
  align-items: center;
  justify-content: flex-end;
  text-align: right;
  width: 60px;
  margin: 0 ${(0, space_1.default)(2)};

  @media (min-width: ${p => p.theme.breakpoints[3]}) {
    width: 80px;
  }
`;
const AssigneesLabel = (0, styled_1.default)('div') `
  justify-content: flex-end;
  text-align: right;
  width: 80px;
  margin-left: ${(0, space_1.default)(2)};
  margin-right: ${(0, space_1.default)(2)};
`;
// Reprocessing
const StartedColumn = (0, styled_1.default)(toolbarHeader_1.default) `
  margin: 0 ${(0, space_1.default)(2)};
  ${overflowEllipsis_1.default};
  width: 85px;

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    width: 140px;
  }
`;
const EventsReprocessedColumn = (0, styled_1.default)(toolbarHeader_1.default) `
  margin: 0 ${(0, space_1.default)(2)};
  ${overflowEllipsis_1.default};
  width: 75px;

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    width: 140px;
  }
`;
const ProgressColumn = (0, styled_1.default)(toolbarHeader_1.default) `
  margin: 0 ${(0, space_1.default)(2)};

  display: none;

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    display: block;
    width: 160px;
  }
`;
//# sourceMappingURL=headers.jsx.map