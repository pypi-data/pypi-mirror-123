Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const checkbox_1 = (0, tslib_1.__importDefault)(require("app/components/checkbox"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const timePicker_1 = (0, tslib_1.__importDefault)(require("app/components/organizations/timeRangeSelector/timePicker"));
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const constants_1 = require("app/constants");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const dates_1 = require("app/utils/dates");
const getRouteStringFromRoutes_1 = (0, tslib_1.__importDefault)(require("app/utils/getRouteStringFromRoutes"));
const DateRangePicker = React.lazy(() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('./dateRangeWrapper'))));
const getTimeStringFromDate = (date) => (0, moment_1.default)(date).local().format('HH:mm');
function isRangeSelection(maybe) {
    return maybe.selection !== undefined;
}
const defaultProps = {
    showAbsolute: true,
    showRelative: false,
    /**
     * The maximum number of days in the past you can pick
     */
    maxPickableDays: constants_1.MAX_PICKABLE_DAYS,
};
class BaseDateRange extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            hasStartErrors: false,
            hasEndErrors: false,
        };
        this.handleSelectDateRange = (changeProps) => {
            if (!isRangeSelection(changeProps)) {
                return;
            }
            const { selection } = changeProps;
            const { onChange } = this.props;
            const { startDate, endDate } = selection;
            const end = endDate ? (0, dates_1.getEndOfDay)(endDate) : endDate;
            onChange({
                start: startDate,
                end,
            });
        };
        this.handleChangeStart = (e) => {
            var _a, _b;
            // Safari does not support "time" inputs, so we don't have access to
            // `e.target.valueAsDate`, must parse as string
            //
            // Time will be in 24hr e.g. "21:00"
            const start = (_a = this.props.start) !== null && _a !== void 0 ? _a : '';
            const end = (_b = this.props.end) !== null && _b !== void 0 ? _b : undefined;
            const { onChange, organization, router } = this.props;
            const startTime = e.target.value;
            if (!startTime || !(0, dates_1.isValidTime)(startTime)) {
                this.setState({ hasStartErrors: true });
                onChange({ hasDateRangeErrors: true });
                return;
            }
            const newTime = (0, dates_1.setDateToTime)(start, startTime, { local: true });
            (0, analytics_1.analytics)('dateselector.time_changed', {
                field_changed: 'start',
                time: startTime,
                path: (0, getRouteStringFromRoutes_1.default)(router.routes),
                org_id: parseInt(organization.id, 10),
            });
            onChange({
                start: newTime,
                end,
                hasDateRangeErrors: this.state.hasEndErrors,
            });
            this.setState({ hasStartErrors: false });
        };
        this.handleChangeEnd = (e) => {
            var _a, _b;
            const start = (_a = this.props.start) !== null && _a !== void 0 ? _a : undefined;
            const end = (_b = this.props.end) !== null && _b !== void 0 ? _b : '';
            const { organization, onChange, router } = this.props;
            const endTime = e.target.value;
            if (!endTime || !(0, dates_1.isValidTime)(endTime)) {
                this.setState({ hasEndErrors: true });
                onChange({ hasDateRangeErrors: true });
                return;
            }
            const newTime = (0, dates_1.setDateToTime)(end, endTime, { local: true });
            (0, analytics_1.analytics)('dateselector.time_changed', {
                field_changed: 'end',
                time: endTime,
                path: (0, getRouteStringFromRoutes_1.default)(router.routes),
                org_id: parseInt(organization.id, 10),
            });
            onChange({
                start,
                end: newTime,
                hasDateRangeErrors: this.state.hasStartErrors,
            });
            this.setState({ hasEndErrors: false });
        };
    }
    render() {
        var _a, _b;
        const { className, maxPickableDays, utc, showTimePicker, onChangeUtc, theme } = this.props;
        const start = (_a = this.props.start) !== null && _a !== void 0 ? _a : '';
        const end = (_b = this.props.end) !== null && _b !== void 0 ? _b : '';
        const startTime = getTimeStringFromDate(new Date(start));
        const endTime = getTimeStringFromDate(new Date(end));
        // Restraints on the time range that you can select
        // Can't select dates in the future b/c we're not fortune tellers (yet)
        //
        // We want `maxPickableDays` - 1 (if today is Jan 5, max is 3 days, the minDate should be Jan 3)
        // Subtract additional day  because we force the end date to be inclusive,
        // so when you pick Jan 1 the time becomes Jan 1 @ 23:59:59,
        // (or really, Jan 2 @ 00:00:00 - 1 second), while the start time is at 00:00
        const minDate = (0, dates_1.getStartOfPeriodAgo)('days', (maxPickableDays !== null && maxPickableDays !== void 0 ? maxPickableDays : constants_1.MAX_PICKABLE_DAYS) - 2);
        const maxDate = new Date();
        return (<div className={className} data-test-id="date-range">
        <React.Suspense fallback={<placeholder_1.default width="342px" height="254px">
              <loadingIndicator_1.default />
            </placeholder_1.default>}>
          <DateRangePicker rangeColors={[theme.purple300]} ranges={[
                {
                    startDate: (0, moment_1.default)(start).local().toDate(),
                    endDate: (0, moment_1.default)(end).local().toDate(),
                    key: 'selection',
                },
            ]} minDate={minDate} maxDate={maxDate} onChange={this.handleSelectDateRange}/>
        </React.Suspense>
        {showTimePicker && (<TimeAndUtcPicker>
            <timePicker_1.default start={startTime} end={endTime} onChangeStart={this.handleChangeStart} onChangeEnd={this.handleChangeEnd}/>
            <UtcPicker>
              {(0, locale_1.t)('Use UTC')}
              <checkbox_1.default onChange={onChangeUtc} checked={utc || false} style={{
                    margin: '0 0 0 0.5em',
                }}/>
            </UtcPicker>
          </TimeAndUtcPicker>)}
      </div>);
    }
}
BaseDateRange.defaultProps = defaultProps;
const DateRange = (0, styled_1.default)((0, react_1.withTheme)((0, react_router_1.withRouter)(BaseDateRange))) `
  display: flex;
  flex-direction: column;
  border-left: 1px solid ${p => p.theme.border};
`;
const TimeAndUtcPicker = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  padding: ${(0, space_1.default)(2)};
  border-top: 1px solid ${p => p.theme.innerBorder};
`;
const UtcPicker = (0, styled_1.default)('div') `
  color: ${p => p.theme.gray300};
  white-space: nowrap;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  flex: 1;
`;
exports.default = DateRange;
//# sourceMappingURL=index.jsx.map