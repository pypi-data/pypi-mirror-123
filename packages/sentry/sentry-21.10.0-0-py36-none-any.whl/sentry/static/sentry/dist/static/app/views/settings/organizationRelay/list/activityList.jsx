Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const dateTime_1 = (0, tslib_1.__importDefault)(require("app/components/dateTime"));
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const ActivityList = ({ activities }) => (<StyledPanelTable headers={[(0, locale_1.t)('Version'), (0, locale_1.t)('First Used'), (0, locale_1.t)('Last Used')]}>
    {activities.map(({ relayId, version, firstSeen, lastSeen }) => {
        return (<react_1.Fragment key={relayId}>
          <Version>{version}</Version>
          <dateTime_1.default date={firstSeen} seconds={false}/>
          <dateTime_1.default date={lastSeen} seconds={false}/>
        </react_1.Fragment>);
    })}
  </StyledPanelTable>);
exports.default = ActivityList;
const StyledPanelTable = (0, styled_1.default)(panels_1.PanelTable) `
  grid-template-columns: repeat(3, 2fr);

  @media (min-width: ${p => p.theme.breakpoints[2]}) {
    grid-template-columns: 2fr repeat(2, 1fr);
  }
`;
const Version = (0, styled_1.default)('div') `
  font-variant-numeric: tabular-nums;
`;
//# sourceMappingURL=activityList.jsx.map