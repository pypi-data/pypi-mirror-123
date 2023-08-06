Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const dateTime_1 = (0, tslib_1.__importDefault)(require("app/components/dateTime"));
const notAvailable_1 = (0, tslib_1.__importDefault)(require("app/components/notAvailable"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
function Details({ details }) {
    const { latestBuildVersion, latestBuildNumber, lastCheckedBuilds } = details !== null && details !== void 0 ? details : {};
    return (<Wrapper>
      {(0, locale_1.t)('Last detected version')}
      <Value>
        {latestBuildVersion ? ((0, locale_1.tct)('v[version]', { version: latestBuildVersion })) : (<notAvailable_1.default tooltip={(0, locale_1.t)('Not available')}/>)}
      </Value>

      {(0, locale_1.t)('Last detected build')}
      <Value>{latestBuildNumber !== null && latestBuildNumber !== void 0 ? latestBuildNumber : <notAvailable_1.default tooltip={(0, locale_1.t)('Not available')}/>}</Value>

      {(0, locale_1.t)('Detected last build on')}
      <Value>
        {lastCheckedBuilds ? (<dateTime_1.default date={lastCheckedBuilds}/>) : (<notAvailable_1.default tooltip={(0, locale_1.t)('Not available')}/>)}
      </Value>
    </Wrapper>);
}
exports.default = Details;
const Wrapper = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(1)};
  margin-top: ${(0, space_1.default)(0.5)};
  align-items: center;

  font-size: ${p => p.theme.fontSizeSmall};
  font-weight: 700;

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    margin-top: ${(0, space_1.default)(1)};
    grid-template-columns: max-content 1fr;
    grid-gap: ${(0, space_1.default)(1)};
    grid-row: 3/3;
    grid-column: 1/-1;
  }
`;
const Value = (0, styled_1.default)('div') `
  font-weight: 400;
  white-space: pre-wrap;
  word-break: break-all;
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(1.5)};
  font-family: ${p => p.theme.text.familyMono};
  background-color: ${p => p.theme.backgroundSecondary};

  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    :not(:last-child) {
      margin-bottom: ${(0, space_1.default)(1)};
    }
  }
`;
//# sourceMappingURL=details.jsx.map