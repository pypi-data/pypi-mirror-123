Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const areaChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/areaChart"));
const eventsChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/eventsChart"));
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const panels_1 = require("app/components/panels");
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const locale_1 = require("app/locale");
const dates_1 = require("app/utils/dates");
const types_1 = require("app/utils/discover/types");
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const queryString_1 = require("app/utils/queryString");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const chartFooter_1 = (0, tslib_1.__importDefault)(require("./chartFooter"));
class ResultsChart extends react_1.Component {
    shouldComponentUpdate(nextProps) {
        const _a = this.props, { eventView } = _a, restProps = (0, tslib_1.__rest)(_a, ["eventView"]);
        const { eventView: nextEventView } = nextProps, restNextProps = (0, tslib_1.__rest)(nextProps, ["eventView"]);
        if (!eventView.isEqualTo(nextEventView)) {
            return true;
        }
        return !(0, isEqual_1.default)(restProps, restNextProps);
    }
    render() {
        const { api, eventView, location, organization, router, confirmedQuery, yAxisValue } = this.props;
        const hasPerformanceChartInterpolation = organization.features.includes('performance-chart-interpolation');
        const hasConnectDiscoverAndDashboards = organization.features.includes('connect-discover-and-dashboards');
        const hasTopEvents = organization.features.includes('discover-top-events');
        const globalSelection = eventView.getGlobalSelection();
        const start = globalSelection.datetime.start
            ? (0, dates_1.getUtcToLocalDateObject)(globalSelection.datetime.start)
            : null;
        const end = globalSelection.datetime.end
            ? (0, dates_1.getUtcToLocalDateObject)(globalSelection.datetime.end)
            : null;
        const { utc } = (0, getParams_1.getParams)(location.query);
        const apiPayload = eventView.getEventsAPIPayload(location);
        const display = eventView.getDisplayMode();
        const isTopEvents = display === types_1.DisplayModes.TOP5 || display === types_1.DisplayModes.DAILYTOP5;
        const isPeriod = display === types_1.DisplayModes.DEFAULT || display === types_1.DisplayModes.TOP5;
        const isDaily = display === types_1.DisplayModes.DAILYTOP5 || display === types_1.DisplayModes.DAILY;
        const isPrevious = display === types_1.DisplayModes.PREVIOUS;
        const referrer = `api.discover.${display}-chart`;
        const topEvents = hasTopEvents && eventView.topEvents ? parseInt(eventView.topEvents, 10) : types_1.TOP_N;
        return (<react_1.Fragment>
        {(0, getDynamicText_1.default)({
                value: (<eventsChart_1.default api={api} router={router} query={apiPayload.query} organization={organization} showLegend yAxis={yAxisValue} projects={globalSelection.projects} environments={globalSelection.environments} start={start} end={end} period={globalSelection.datetime.period} disablePrevious={!isPrevious} disableReleases={!isPeriod} field={isTopEvents ? apiPayload.field : undefined} interval={eventView.interval} showDaily={isDaily} topEvents={isTopEvents ? topEvents : undefined} orderby={isTopEvents ? (0, queryString_1.decodeScalar)(apiPayload.sort) : undefined} utc={utc === 'true'} confirmedQuery={confirmedQuery} withoutZerofill={hasPerformanceChartInterpolation} chartComponent={hasConnectDiscoverAndDashboards && yAxisValue.length > 1 && !isDaily
                        ? areaChart_1.default
                        : undefined} referrer={referrer}/>),
                fixed: <placeholder_1.default height="200px" testId="skeleton-ui"/>,
            })}
      </react_1.Fragment>);
    }
}
class ResultsChartContainer extends react_1.Component {
    shouldComponentUpdate(nextProps) {
        const _a = this.props, { eventView } = _a, restProps = (0, tslib_1.__rest)(_a, ["eventView"]);
        const { eventView: nextEventView } = nextProps, restNextProps = (0, tslib_1.__rest)(nextProps, ["eventView"]);
        if (!eventView.isEqualTo(nextEventView) ||
            this.props.confirmedQuery !== nextProps.confirmedQuery) {
            return true;
        }
        return !(0, isEqual_1.default)(restProps, restNextProps);
    }
    render() {
        var _a;
        const { api, eventView, location, router, total, onAxisChange, onDisplayChange, onTopEventsChange, organization, confirmedQuery, yAxis, } = this.props;
        const hasQueryFeature = organization.features.includes('discover-query');
        const hasConnectDiscoverAndDashboards = organization.features.includes('connect-discover-and-dashboards');
        const hasTopEvents = organization.features.includes('discover-top-events');
        const displayOptions = eventView
            .getDisplayOptions()
            .filter(opt => {
            // top5 modes are only available with larger packages in saas.
            // We remove instead of disable here as showing tooltips in dropdown
            // menus is clunky.
            if ([types_1.DisplayModes.TOP5, types_1.DisplayModes.DAILYTOP5].includes(opt.value) &&
                !hasQueryFeature) {
                return false;
            }
            return true;
        })
            .map(opt => {
            // Can only use default display or total daily with multi y axis
            if (hasTopEvents &&
                [types_1.DisplayModes.TOP5, types_1.DisplayModes.DAILYTOP5].includes(opt.value)) {
                opt.label = types_1.DisplayModes.TOP5 === opt.value ? 'Top Period' : 'Top Daily';
            }
            if (yAxis.length > 1 &&
                ![types_1.DisplayModes.DEFAULT, types_1.DisplayModes.DAILY, types_1.DisplayModes.PREVIOUS].includes(opt.value)) {
                return Object.assign(Object.assign({}, opt), { disabled: true, tooltip: (0, locale_1.t)('Change the Y-Axis dropdown to display only 1 function to use this view.') });
            }
            return opt;
        });
        const yAxisValue = hasConnectDiscoverAndDashboards ? yAxis : [eventView.getYAxis()];
        return (<StyledPanel>
        {(yAxisValue.length > 0 && (<ResultsChart api={api} eventView={eventView} location={location} organization={organization} router={router} confirmedQuery={confirmedQuery} yAxisValue={yAxisValue}/>)) || <NoChartContainer>{(0, locale_1.t)('No Y-Axis selected.')}</NoChartContainer>}
        <chartFooter_1.default organization={organization} total={total} yAxisValue={yAxisValue} yAxisOptions={eventView.getYAxisOptions()} onAxisChange={onAxisChange} displayOptions={displayOptions} displayMode={eventView.getDisplayMode()} onDisplayChange={onDisplayChange} onTopEventsChange={onTopEventsChange} topEvents={(_a = eventView.topEvents) !== null && _a !== void 0 ? _a : types_1.TOP_N.toString()}/>
      </StyledPanel>);
    }
}
exports.default = (0, withApi_1.default)(ResultsChartContainer);
const StyledPanel = (0, styled_1.default)(panels_1.Panel) `
  @media (min-width: ${p => p.theme.breakpoints[1]}) {
    margin: 0;
  }
`;
const NoChartContainer = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

  flex: 1;
  flex-shrink: 0;
  overflow: hidden;
  height: ${p => p.height || '200px'};
  position: relative;
  border-color: transparent;
  margin-bottom: 0;
  color: ${p => p.theme.gray300};
  font-size: ${p => p.theme.fontSizeExtraLarge};
`;
//# sourceMappingURL=resultsChart.jsx.map