Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_2 = require("@emotion/react");
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const chartZoom_1 = (0, tslib_1.__importDefault)(require("app/components/charts/chartZoom"));
const errorPanel_1 = (0, tslib_1.__importDefault)(require("app/components/charts/errorPanel"));
const lineChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/lineChart"));
const releaseSeries_1 = (0, tslib_1.__importDefault)(require("app/components/charts/releaseSeries"));
const stackedAreaChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/stackedAreaChart"));
const styles_1 = require("app/components/charts/styles");
const transitionChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/transitionChart"));
const transparentLoadingMask_1 = (0, tslib_1.__importDefault)(require("app/components/charts/transparentLoadingMask"));
const utils_1 = require("app/components/charts/utils");
const questionTooltip_1 = (0, tslib_1.__importDefault)(require("app/components/questionTooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const withGlobalSelection_1 = (0, tslib_1.__importDefault)(require("app/utils/withGlobalSelection"));
const utils_2 = require("app/views/releases/utils");
const sessionTerm_1 = require("app/views/releases/utils/sessionTerm");
const projectCharts_1 = require("../projectCharts");
const projectSessionsChartRequest_1 = (0, tslib_1.__importDefault)(require("./projectSessionsChartRequest"));
function ProjectBaseSessionsChart({ title, organization, router, selection, api, onTotalValuesChange, displayMode, help, disablePrevious, query, }) {
    const theme = (0, react_2.useTheme)();
    const { projects, environments, datetime } = selection;
    const { start, end, period, utc } = datetime;
    return (<react_1.Fragment>
      {(0, getDynamicText_1.default)({
            value: (<chartZoom_1.default router={router} period={period} start={start} end={end} utc={utc}>
            {zoomRenderProps => (<projectSessionsChartRequest_1.default api={api} selection={selection} organization={organization} onTotalValuesChange={onTotalValuesChange} displayMode={displayMode} disablePrevious={disablePrevious} query={query}>
                {({ errored, loading, reloading, timeseriesData, previousTimeseriesData, }) => (<releaseSeries_1.default utc={utc} period={period} start={start} end={end} projects={projects} environments={environments} query={query}>
                    {({ releaseSeries }) => {
                            if (errored) {
                                return (<errorPanel_1.default>
                            <icons_1.IconWarning color="gray300" size="lg"/>
                          </errorPanel_1.default>);
                            }
                            return (<transitionChart_1.default loading={loading} reloading={reloading}>
                          <transparentLoadingMask_1.default visible={reloading}/>

                          <styles_1.HeaderTitleLegend>
                            {title}
                            {help && (<questionTooltip_1.default size="sm" position="top" title={help}/>)}
                          </styles_1.HeaderTitleLegend>

                          <Chart theme={theme} zoomRenderProps={zoomRenderProps} reloading={reloading} timeSeries={timeseriesData} previousTimeSeries={previousTimeseriesData
                                    ? [previousTimeseriesData]
                                    : undefined} releaseSeries={releaseSeries} displayMode={displayMode}/>
                        </transitionChart_1.default>);
                        }}
                  </releaseSeries_1.default>)}
              </projectSessionsChartRequest_1.default>)}
          </chartZoom_1.default>),
            fixed: `${title} Chart`,
        })}
    </react_1.Fragment>);
}
class Chart extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            seriesSelection: {},
            forceUpdate: false,
        };
        // inspired by app/components/charts/eventsChart.tsx@handleLegendSelectChanged
        this.handleLegendSelectChanged = ({ selected }) => {
            const seriesSelection = Object.keys(selected).reduce((state, key) => {
                state[key] = selected[key];
                return state;
            }, {});
            // we have to force an update here otherwise ECharts will
            // update its internal state and disable the series
            this.setState({ seriesSelection, forceUpdate: true }, () => this.setState({ forceUpdate: false }));
        };
    }
    shouldComponentUpdate(nextProps, nextState) {
        if (nextState.forceUpdate) {
            return true;
        }
        if (!(0, isEqual_1.default)(this.state.seriesSelection, nextState.seriesSelection)) {
            return true;
        }
        if (nextProps.releaseSeries !== this.props.releaseSeries &&
            !nextProps.reloading &&
            !this.props.reloading) {
            return true;
        }
        if (this.props.reloading && !nextProps.reloading) {
            return true;
        }
        if (nextProps.timeSeries !== this.props.timeSeries) {
            return true;
        }
        return false;
    }
    get legend() {
        var _a, _b;
        const { theme, timeSeries, previousTimeSeries, releaseSeries } = this.props;
        const { seriesSelection } = this.state;
        const hideReleasesByDefault = ((_b = (_a = releaseSeries[0]) === null || _a === void 0 ? void 0 : _a.markLine) === null || _b === void 0 ? void 0 : _b.data.length) >= utils_1.RELEASE_LINES_THRESHOLD;
        const hideHealthyByDefault = timeSeries
            .filter(s => sessionTerm_1.sessionTerm.healthy !== s.seriesName)
            .some(s => s.data.some(d => d.value > 0));
        const selected = Object.keys(seriesSelection).length === 0 &&
            (hideReleasesByDefault || hideHealthyByDefault)
            ? {
                [(0, locale_1.t)('Releases')]: !hideReleasesByDefault,
                [sessionTerm_1.sessionTerm.healthy]: !hideHealthyByDefault,
            }
            : seriesSelection;
        return {
            right: 10,
            top: 0,
            icon: 'circle',
            itemHeight: 8,
            itemWidth: 8,
            itemGap: 12,
            align: 'left',
            textStyle: {
                color: theme.textColor,
                verticalAlign: 'top',
                fontSize: 11,
                fontFamily: theme.text.family,
            },
            data: [
                ...timeSeries.map(s => s.seriesName),
                ...(previousTimeSeries !== null && previousTimeSeries !== void 0 ? previousTimeSeries : []).map(s => s.seriesName),
                ...releaseSeries.map(s => s.seriesName),
            ],
            selected,
        };
    }
    get chartOptions() {
        const { theme, displayMode } = this.props;
        return {
            grid: { left: '10px', right: '10px', top: '40px', bottom: '0px' },
            seriesOptions: {
                showSymbol: false,
            },
            tooltip: {
                trigger: 'axis',
                truncate: 80,
                valueFormatter: (value) => {
                    if (value === null) {
                        return '\u2014';
                    }
                    if (displayMode === projectCharts_1.DisplayModes.STABILITY) {
                        return (0, utils_2.displayCrashFreePercent)(value, 0, 3);
                    }
                    return typeof value === 'number' ? value.toLocaleString() : value;
                },
            },
            yAxis: displayMode === projectCharts_1.DisplayModes.STABILITY
                ? {
                    axisLabel: {
                        color: theme.gray200,
                        formatter: (value) => (0, utils_2.displayCrashFreePercent)(value),
                    },
                    scale: true,
                    max: 100,
                }
                : { min: 0 },
        };
    }
    render() {
        const { zoomRenderProps, timeSeries, previousTimeSeries, releaseSeries, displayMode } = this.props;
        const ChartComponent = displayMode === projectCharts_1.DisplayModes.STABILITY ? lineChart_1.default : stackedAreaChart_1.default;
        return (<ChartComponent {...zoomRenderProps} {...this.chartOptions} legend={this.legend} series={Array.isArray(releaseSeries) ? [...timeSeries, ...releaseSeries] : timeSeries} previousPeriod={previousTimeSeries} onLegendSelectChanged={this.handleLegendSelectChanged} transformSinglePointToBar/>);
    }
}
exports.default = (0, withGlobalSelection_1.default)(ProjectBaseSessionsChart);
//# sourceMappingURL=projectBaseSessionsChart.jsx.map