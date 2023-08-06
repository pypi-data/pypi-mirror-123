Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const fields_1 = require("app/utils/discover/fields");
const formatters_1 = require("app/utils/formatters");
const utils_1 = require("./utils");
function getVitalStateText(vital, vitalState) {
    const unit = !Array.isArray(vital) && vital !== fields_1.WebVital.CLS ? 'ms' : '';
    switch (vitalState) {
        case utils_1.VitalState.POOR:
            return Array.isArray(vital)
                ? (0, locale_1.t)('Poor')
                : (0, locale_1.tct)('Poor: >[threshold][unit]', { threshold: utils_1.webVitalPoor[vital], unit });
        case utils_1.VitalState.MEH:
            return Array.isArray(vital)
                ? (0, locale_1.t)('Meh')
                : (0, locale_1.tct)('Meh: >[threshold][unit]', { threshold: utils_1.webVitalMeh[vital], unit });
        case utils_1.VitalState.GOOD:
            return Array.isArray(vital)
                ? (0, locale_1.t)('Good')
                : (0, locale_1.tct)('Good: <[threshold][unit]', { threshold: utils_1.webVitalMeh[vital], unit });
        default:
            return null;
    }
}
function VitalPercents(props) {
    return (<VitalSet>
      {props.percents.map(pct => {
            return (<tooltip_1.default key={pct.vitalState} title={getVitalStateText(props.vital, pct.vitalState)}>
            <VitalStatus>
              {utils_1.vitalStateIcons[pct.vitalState]}
              <span>
                {props.showVitalPercentNames && (0, locale_1.t)(`${pct.vitalState}`)}{' '}
                {(0, formatters_1.formatPercentage)(pct.percent, 0)}
              </span>
            </VitalStatus>
          </tooltip_1.default>);
        })}
    </VitalSet>);
}
exports.default = VitalPercents;
const VitalSet = (0, styled_1.default)('div') `
  display: inline-grid;
  grid-auto-flow: column;
  gap: ${(0, space_1.default)(2)};
`;
const VitalStatus = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  gap: ${(0, space_1.default)(0.5)};
  font-size: ${p => p.theme.fontSizeMedium};
`;
//# sourceMappingURL=vitalPercents.jsx.map