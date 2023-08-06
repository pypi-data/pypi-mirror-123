Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const panels_1 = require("app/components/panels");
const timeSince_1 = (0, tslib_1.__importDefault)(require("app/components/timeSince"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("./utils");
function SessionRow({ ipAddress, lastSeen, firstSeen, countryCode, regionCode, }) {
    return (<SessionPanelItem>
      <IpAndLocation>
        <IpAddress>{ipAddress}</IpAddress>
        {countryCode && regionCode && (<CountryCode>{`${countryCode} (${regionCode})`}</CountryCode>)}
      </IpAndLocation>
      <StyledTimeSince date={firstSeen}/>
      <StyledTimeSince date={lastSeen}/>
    </SessionPanelItem>);
}
exports.default = SessionRow;
const IpAddress = (0, styled_1.default)('div') `
  margin-bottom: ${(0, space_1.default)(0.5)};
  font-weight: bold;
`;
const CountryCode = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeRelativeSmall};
`;
const StyledTimeSince = (0, styled_1.default)(timeSince_1.default) `
  font-size: ${p => p.theme.fontSizeRelativeSmall};
`;
const IpAndLocation = (0, styled_1.default)('div') `
  flex: 1;
`;
const SessionPanelItem = (0, styled_1.default)(panels_1.PanelItem) `
  ${utils_1.tableLayout};
`;
//# sourceMappingURL=sessionRow.jsx.map