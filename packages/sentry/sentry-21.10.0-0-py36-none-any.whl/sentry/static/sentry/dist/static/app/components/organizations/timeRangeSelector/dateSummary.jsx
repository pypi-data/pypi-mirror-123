Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
/**
 * Displays and formats absolute DateTime ranges
 */
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const dates_1 = require("app/utils/dates");
class DateSummary extends react_1.Component {
    getFormattedDate(date, format) {
        return (0, moment_1.default)(date).local().format(format);
    }
    formatDate(date) {
        return this.getFormattedDate(date, 'll');
    }
    formatTime(date, withSeconds = false) {
        return this.getFormattedDate(date, `HH:mm${withSeconds ? ':ss' : ''}`);
    }
    render() {
        const { start, end } = this.props;
        const startTimeFormatted = this.formatTime(start, true);
        const endTimeFormatted = this.formatTime(end, true);
        // Show times if either start or end date contain a time that is not midnight
        const shouldShowTimes = startTimeFormatted !== dates_1.DEFAULT_DAY_START_TIME ||
            endTimeFormatted !== dates_1.DEFAULT_DAY_END_TIME;
        return (<DateGroupWrapper hasTime={shouldShowTimes}>
        <DateGroup>
          <Date hasTime={shouldShowTimes}>
            {this.formatDate(start)}
            {shouldShowTimes && <Time>{this.formatTime(start)}</Time>}
          </Date>
        </DateGroup>
        <react_1.Fragment>
          <DateRangeDivider>{(0, locale_1.t)('to')}</DateRangeDivider>

          <DateGroup>
            <Date hasTime={shouldShowTimes}>
              {this.formatDate(end)}
              {shouldShowTimes && <Time>{this.formatTime(end)}</Time>}
            </Date>
          </DateGroup>
        </react_1.Fragment>
      </DateGroupWrapper>);
    }
}
const DateGroupWrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  transform: translateY(${p => (p.hasTime ? '-5px' : '0')});
`;
const DateGroup = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 110px;
`;
const Date = (0, styled_1.default)('div') `
  ${p => p.hasTime && 'margin-top: 9px'};
  display: flex;
  flex-direction: column;
  align-items: flex-end;
`;
const Time = (0, styled_1.default)('div') `
  font-size: 0.7em;
  line-height: 0.7em;
  opacity: 0.5;
`;
const DateRangeDivider = (0, styled_1.default)('span') `
  margin: 0 ${(0, space_1.default)(0.5)};
`;
exports.default = DateSummary;
//# sourceMappingURL=dateSummary.jsx.map