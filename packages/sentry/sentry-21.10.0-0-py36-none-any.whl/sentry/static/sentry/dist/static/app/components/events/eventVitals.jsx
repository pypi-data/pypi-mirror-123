Object.defineProperty(exports, "__esModule", { value: true });
exports.EventVitalContainer = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const styles_1 = require("app/components/charts/styles");
const panels_1 = require("app/components/panels");
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const index_1 = require("app/utils/measurements/index");
const constants_1 = require("app/utils/performance/vitals/constants");
function isOutdatedSdk(event) {
    var _a;
    if (!((_a = event.sdk) === null || _a === void 0 ? void 0 : _a.version)) {
        return false;
    }
    const sdkVersion = event.sdk.version;
    return (sdkVersion.startsWith('5.26.') ||
        sdkVersion.startsWith('5.27.0') ||
        sdkVersion.startsWith('5.27.1') ||
        sdkVersion.startsWith('5.27.2'));
}
function EventVitals({ event }) {
    return (<react_1.Fragment>
      <WebVitals event={event}/>
      <MobileVitals event={event}/>
    </react_1.Fragment>);
}
exports.default = EventVitals;
function WebVitals({ event }) {
    var _a;
    const measurementNames = Object.keys((_a = event.measurements) !== null && _a !== void 0 ? _a : {})
        .filter(name => Boolean(constants_1.WEB_VITAL_DETAILS[`measurements.${name}`]))
        .sort();
    if (measurementNames.length === 0) {
        return null;
    }
    return (<Container>
      <styles_1.SectionHeading>
        {(0, locale_1.t)('Web Vitals')}
        {isOutdatedSdk(event) && (<WarningIconContainer size="sm">
            <tooltip_1.default title={(0, locale_1.t)('These vitals were collected using an outdated SDK version and may not be accurate. To ensure accurate web vitals in new transaction events, please update your SDK to the latest version.')} position="top" containerDisplayMode="inline-block">
              <icons_1.IconWarning size="sm"/>
            </tooltip_1.default>
          </WarningIconContainer>)}
      </styles_1.SectionHeading>
      <Measurements>
        {measurementNames.map(name => {
            // Measurements are referred to by their full name `measurements.<name>`
            // here but are stored using their abbreviated name `<name>`. Make sure
            // to convert it appropriately.
            const measurement = `measurements.${name}`;
            const vital = constants_1.WEB_VITAL_DETAILS[measurement];
            return <EventVital key={name} event={event} name={name} vital={vital}/>;
        })}
      </Measurements>
    </Container>);
}
function MobileVitals({ event }) {
    var _a;
    const measurementNames = Object.keys((_a = event.measurements) !== null && _a !== void 0 ? _a : {})
        .filter(name => Boolean(constants_1.MOBILE_VITAL_DETAILS[`measurements.${name}`]))
        .sort();
    if (measurementNames.length === 0) {
        return null;
    }
    return (<Container>
      <styles_1.SectionHeading>{(0, locale_1.t)('Mobile Vitals')}</styles_1.SectionHeading>
      <Measurements>
        {measurementNames.map(name => {
            // Measurements are referred to by their full name `measurements.<name>`
            // here but are stored using their abbreviated name `<name>`. Make sure
            // to convert it appropriately.
            const measurement = `measurements.${name}`;
            const vital = constants_1.MOBILE_VITAL_DETAILS[measurement];
            return <EventVital key={name} event={event} name={name} vital={vital}/>;
        })}
      </Measurements>
    </Container>);
}
function EventVital({ event, name, vital }) {
    var _a, _b, _c, _d;
    const value = (_b = (_a = event.measurements) === null || _a === void 0 ? void 0 : _a[name].value) !== null && _b !== void 0 ? _b : null;
    if (value === null || !vital) {
        return null;
    }
    const failedThreshold = (0, utils_1.defined)(vital.poorThreshold) && value >= vital.poorThreshold;
    const currentValue = (0, index_1.formattedValue)(vital, value);
    const thresholdValue = (0, index_1.formattedValue)(vital, (_c = vital === null || vital === void 0 ? void 0 : vital.poorThreshold) !== null && _c !== void 0 ? _c : 0);
    return (<exports.EventVitalContainer>
      <StyledPanel failedThreshold={failedThreshold}>
        <Name>{(_d = vital.name) !== null && _d !== void 0 ? _d : name}</Name>
        <ValueRow>
          {failedThreshold ? (<FireIconContainer size="sm">
              <tooltip_1.default title={(0, locale_1.t)('Fails threshold at %s.', thresholdValue)} position="top" containerDisplayMode="inline-block">
                <icons_1.IconFire size="sm"/>
              </tooltip_1.default>
            </FireIconContainer>) : null}
          <Value failedThreshold={failedThreshold}>{currentValue}</Value>
        </ValueRow>
      </StyledPanel>
    </exports.EventVitalContainer>);
}
const Measurements = (0, styled_1.default)('div') `
  display: grid;
  grid-column-gap: ${(0, space_1.default)(1)};
`;
const Container = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeMedium};
  margin-bottom: ${(0, space_1.default)(4)};
`;
const StyledPanel = (0, styled_1.default)(panels_1.Panel) `
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(1.5)};
  margin-bottom: ${(0, space_1.default)(1)};
  ${p => p.failedThreshold && `border: 1px solid ${p.theme.red300};`}
`;
const Name = (0, styled_1.default)('div') ``;
const ValueRow = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
`;
const WarningIconContainer = (0, styled_1.default)('span') `
  display: inline-block;
  height: ${p => { var _a; return (_a = p.theme.iconSizes[p.size]) !== null && _a !== void 0 ? _a : p.size; }};
  line-height: ${p => { var _a; return (_a = p.theme.iconSizes[p.size]) !== null && _a !== void 0 ? _a : p.size; }};
  margin-left: ${(0, space_1.default)(0.5)};
  color: ${p => p.theme.red300};
`;
const FireIconContainer = (0, styled_1.default)('span') `
  display: inline-block;
  height: ${p => { var _a; return (_a = p.theme.iconSizes[p.size]) !== null && _a !== void 0 ? _a : p.size; }};
  line-height: ${p => { var _a; return (_a = p.theme.iconSizes[p.size]) !== null && _a !== void 0 ? _a : p.size; }};
  margin-right: ${(0, space_1.default)(0.5)};
  color: ${p => p.theme.red300};
`;
const Value = (0, styled_1.default)('span') `
  font-size: ${p => p.theme.fontSizeExtraLarge};
  ${p => p.failedThreshold && `color: ${p.theme.red300};`}
`;
exports.EventVitalContainer = (0, styled_1.default)('div') ``;
//# sourceMappingURL=eventVitals.jsx.map