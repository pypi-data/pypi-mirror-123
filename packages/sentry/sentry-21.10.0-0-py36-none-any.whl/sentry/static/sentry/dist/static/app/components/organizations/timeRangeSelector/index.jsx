Object.defineProperty(exports, "__esModule", { value: true });
exports.TimeRangeRoot = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const moment_timezone_1 = (0, tslib_1.__importDefault)(require("moment-timezone"));
const dropdownMenu_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownMenu"));
const hookOrDefault_1 = (0, tslib_1.__importDefault)(require("app/components/hookOrDefault"));
const headerItem_1 = (0, tslib_1.__importDefault)(require("app/components/organizations/headerItem"));
const multipleSelectorSubmitRow_1 = (0, tslib_1.__importDefault)(require("app/components/organizations/multipleSelectorSubmitRow"));
const dateRange_1 = (0, tslib_1.__importDefault)(require("app/components/organizations/timeRangeSelector/dateRange"));
const selectorItems_1 = (0, tslib_1.__importDefault)(require("app/components/organizations/timeRangeSelector/dateRange/selectorItems"));
const dateSummary_1 = (0, tslib_1.__importDefault)(require("app/components/organizations/timeRangeSelector/dateSummary"));
const utils_1 = require("app/components/organizations/timeRangeSelector/utils");
const constants_1 = require("app/constants");
const icons_1 = require("app/icons");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_2 = require("app/utils");
const analytics_1 = require("app/utils/analytics");
const dates_1 = require("app/utils/dates");
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const getRouteStringFromRoutes_1 = (0, tslib_1.__importDefault)(require("app/utils/getRouteStringFromRoutes"));
// Strips timezone from local date, creates a new moment date object with timezone
// Then returns as a Date object
const getDateWithTimezoneInUtc = (date, utc) => moment_timezone_1.default
    .tz((0, moment_timezone_1.default)(date).local().format('YYYY-MM-DD HH:mm:ss'), utc ? 'UTC' : (0, dates_1.getUserTimezone)())
    .utc()
    .toDate();
const getInternalDate = (date, utc) => {
    if (utc) {
        return (0, dates_1.getUtcToSystem)(date);
    }
    else {
        return new Date(moment_timezone_1.default.tz(moment_timezone_1.default.utc(date), (0, dates_1.getUserTimezone)()).format('YYYY/MM/DD HH:mm:ss'));
    }
};
const DateRangeHook = (0, hookOrDefault_1.default)({
    hookName: 'component:header-date-range',
    defaultComponent: dateRange_1.default,
});
const SelectorItemsHook = (0, hookOrDefault_1.default)({
    hookName: 'component:header-selector-items',
    defaultComponent: selectorItems_1.default,
});
const defaultProps = {
    /**
     * Show absolute date selectors
     */
    showAbsolute: true,
    /**
     * Show relative date selectors
     */
    showRelative: true,
    /**
     * When the default period is selected, it is visually dimmed and
     * makes the selector unclearable.
     */
    defaultPeriod: constants_1.DEFAULT_STATS_PERIOD,
    /**
     * Callback when value changes
     */
    onChange: (() => { }),
};
class TimeRangeSelector extends React.PureComponent {
    constructor(props) {
        super(props);
        this.callCallback = (callback, datetime) => {
            if (typeof callback !== 'function') {
                return;
            }
            if (!datetime.start && !datetime.end) {
                callback(datetime);
                return;
            }
            // Change local date into either UTC or local time (local time defined by user preference)
            callback(Object.assign(Object.assign({}, datetime), { start: getDateWithTimezoneInUtc(datetime.start, this.state.utc), end: getDateWithTimezoneInUtc(datetime.end, this.state.utc) }));
        };
        this.handleCloseMenu = () => {
            const { relative, start, end, utc } = this.state;
            if (this.state.hasChanges) {
                // Only call update if we close when absolute date is selected
                this.handleUpdate({ relative, start, end, utc });
            }
            else {
                this.setState({ isOpen: false });
            }
        };
        this.handleUpdate = (datetime) => {
            const { onUpdate } = this.props;
            this.setState({
                isOpen: false,
                hasChanges: false,
            }, () => {
                this.callCallback(onUpdate, datetime);
            });
        };
        this.handleAbsoluteClick = () => {
            const { relative, onChange, defaultPeriod } = this.props;
            // Set default range to equivalent of last relative period,
            // or use default stats period
            const newDateTime = {
                relative: null,
                start: (0, dates_1.getPeriodAgo)('hours', (0, dates_1.parsePeriodToHours)(relative || defaultPeriod || constants_1.DEFAULT_STATS_PERIOD)).toDate(),
                end: new Date(),
            };
            if ((0, utils_2.defined)(this.props.utc)) {
                newDateTime.utc = this.state.utc;
            }
            this.setState(Object.assign(Object.assign({ hasChanges: true }, newDateTime), { start: newDateTime.start, end: newDateTime.end }));
            this.callCallback(onChange, newDateTime);
        };
        this.handleSelectRelative = (value) => {
            const { onChange } = this.props;
            const newDateTime = {
                relative: value,
                start: undefined,
                end: undefined,
            };
            this.setState(newDateTime);
            this.callCallback(onChange, newDateTime);
            this.handleUpdate(newDateTime);
        };
        this.handleClear = () => {
            const { onChange, defaultPeriod } = this.props;
            const newDateTime = {
                relative: defaultPeriod || constants_1.DEFAULT_STATS_PERIOD,
                start: undefined,
                end: undefined,
                utc: null,
            };
            this.setState(newDateTime);
            this.callCallback(onChange, newDateTime);
            this.handleUpdate(newDateTime);
        };
        this.handleSelectDateRange = ({ start, end, hasDateRangeErrors = false, }) => {
            if (hasDateRangeErrors) {
                this.setState({ hasDateRangeErrors });
                return;
            }
            const { onChange } = this.props;
            const newDateTime = {
                relative: null,
                start,
                end,
            };
            if ((0, utils_2.defined)(this.props.utc)) {
                newDateTime.utc = this.state.utc;
            }
            this.setState(Object.assign({ hasChanges: true, hasDateRangeErrors }, newDateTime));
            this.callCallback(onChange, newDateTime);
        };
        this.handleUseUtc = () => {
            const { onChange, router } = this.props;
            let { start, end } = this.props;
            this.setState(state => {
                const utc = !state.utc;
                if (!start) {
                    start = getDateWithTimezoneInUtc(state.start, state.utc);
                }
                if (!end) {
                    end = getDateWithTimezoneInUtc(state.end, state.utc);
                }
                (0, analytics_1.analytics)('dateselector.utc_changed', {
                    utc,
                    path: (0, getRouteStringFromRoutes_1.default)(router.routes),
                    org_id: parseInt(this.props.organization.id, 10),
                });
                const newDateTime = {
                    relative: null,
                    start: utc ? (0, dates_1.getLocalToSystem)(start) : (0, dates_1.getUtcToSystem)(start),
                    end: utc ? (0, dates_1.getLocalToSystem)(end) : (0, dates_1.getUtcToSystem)(end),
                    utc,
                };
                this.callCallback(onChange, newDateTime);
                return Object.assign({ hasChanges: true }, newDateTime);
            });
        };
        this.handleOpen = () => {
            this.setState({ isOpen: true });
            // Start loading react-date-picker
            Promise.resolve().then(() => (0, tslib_1.__importStar)(require('../timeRangeSelector/dateRange/index')));
        };
        let start = undefined;
        let end = undefined;
        if (props.start && props.end) {
            start = getInternalDate(props.start, props.utc);
            end = getInternalDate(props.end, props.utc);
        }
        this.state = {
            // if utc is not null and not undefined, then use value of `props.utc` (it can be false)
            // otherwise if no value is supplied, the default should be the user's timezone preference
            utc: (0, utils_2.defined)(props.utc) ? props.utc : (0, dates_1.getUserTimezone)() === 'UTC',
            isOpen: false,
            hasChanges: false,
            hasDateRangeErrors: false,
            start,
            end,
            relative: props.relative,
        };
    }
    componentDidUpdate(_prevProps, prevState) {
        const { onToggleSelector } = this.props;
        const currState = this.state;
        if (onToggleSelector && prevState.isOpen !== currState.isOpen) {
            onToggleSelector(currState.isOpen);
        }
    }
    render() {
        const { defaultPeriod, showAbsolute, showRelative, organization, hint, label, relativeOptions, } = this.props;
        const { start, end, relative } = this.state;
        const shouldShowAbsolute = showAbsolute;
        const shouldShowRelative = showRelative;
        const isAbsoluteSelected = !!start && !!end;
        const summary = isAbsoluteSelected && start && end ? (<dateSummary_1.default start={start} end={end}/>) : ((0, utils_1.getRelativeSummary)(relative || defaultPeriod || constants_1.DEFAULT_STATS_PERIOD, relativeOptions));
        const relativeSelected = isAbsoluteSelected
            ? ''
            : relative || defaultPeriod || constants_1.DEFAULT_STATS_PERIOD;
        return (<dropdownMenu_1.default isOpen={this.state.isOpen} onOpen={this.handleOpen} onClose={this.handleCloseMenu} keepMenuOpen>
        {({ isOpen, getRootProps, getActorProps, getMenuProps }) => (<TimeRangeRoot {...getRootProps()}>
            <StyledHeaderItem data-test-id="global-header-timerange-selector" icon={label !== null && label !== void 0 ? label : <icons_1.IconCalendar />} isOpen={isOpen} hasSelected={(!!this.props.relative && this.props.relative !== defaultPeriod) ||
                    isAbsoluteSelected} hasChanges={this.state.hasChanges} onClear={this.handleClear} allowClear hint={hint} {...getActorProps()}>
              {(0, getDynamicText_1.default)({ value: summary, fixed: 'start to end' })}
            </StyledHeaderItem>
            {isOpen && (<Menu {...getMenuProps()} isAbsoluteSelected={isAbsoluteSelected}>
                <SelectorList isAbsoluteSelected={isAbsoluteSelected}>
                  <SelectorItemsHook handleSelectRelative={this.handleSelectRelative} handleAbsoluteClick={this.handleAbsoluteClick} isAbsoluteSelected={isAbsoluteSelected} relativeSelected={relativeSelected} relativePeriods={relativeOptions} shouldShowAbsolute={shouldShowAbsolute} shouldShowRelative={shouldShowRelative}/>
                </SelectorList>
                {isAbsoluteSelected && (<div>
                    <DateRangeHook start={start !== null && start !== void 0 ? start : null} end={end !== null && end !== void 0 ? end : null} organization={organization} showTimePicker utc={this.state.utc} onChange={this.handleSelectDateRange} onChangeUtc={this.handleUseUtc}/>
                    <SubmitRow>
                      <multipleSelectorSubmitRow_1.default onSubmit={this.handleCloseMenu} disabled={!this.state.hasChanges || this.state.hasDateRangeErrors}/>
                    </SubmitRow>
                  </div>)}
              </Menu>)}
          </TimeRangeRoot>)}
      </dropdownMenu_1.default>);
    }
}
TimeRangeSelector.defaultProps = defaultProps;
const TimeRangeRoot = (0, styled_1.default)('div') `
  position: relative;
`;
exports.TimeRangeRoot = TimeRangeRoot;
const StyledHeaderItem = (0, styled_1.default)(headerItem_1.default) `
  height: 100%;
`;
const Menu = (0, styled_1.default)('div') `
  ${p => !p.isAbsoluteSelected && 'left: -1px'};
  ${p => p.isAbsoluteSelected && 'right: -1px'};

  display: flex;
  background: ${p => p.theme.background};
  border: 1px solid ${p => p.theme.border};
  position: absolute;
  top: 100%;
  min-width: 100%;
  z-index: ${p => p.theme.zIndex.dropdown};
  box-shadow: ${p => p.theme.dropShadowLight};
  border-radius: ${p => p.theme.borderRadiusBottom};
  font-size: 0.8em;
  overflow: hidden;
`;
const SelectorList = (0, styled_1.default)('div') `
  display: flex;
  flex: 1;
  flex-direction: column;
  flex-shrink: 0;
  min-width: ${p => (p.isAbsoluteSelected ? '160px' : '220px')};
  min-height: 305px;
`;
const SubmitRow = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(0.5)} ${(0, space_1.default)(1)};
  border-top: 1px solid ${p => p.theme.innerBorder};
  border-left: 1px solid ${p => p.theme.border};
`;
exports.default = (0, react_router_1.withRouter)(TimeRangeSelector);
//# sourceMappingURL=index.jsx.map