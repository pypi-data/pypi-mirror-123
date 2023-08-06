Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const areaChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/areaChart"));
const barChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/barChart"));
const eventsRequest_1 = (0, tslib_1.__importDefault)(require("app/components/charts/eventsRequest"));
const lineChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/lineChart"));
const utils_1 = require("app/components/charts/utils");
const loadingContainer_1 = (0, tslib_1.__importDefault)(require("app/components/loading/loadingContainer"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const icons_1 = require("app/icons");
const dates_1 = require("app/utils/dates");
const charts_1 = require("app/utils/discover/charts");
const types_1 = require("app/utils/discover/types");
const queryString_1 = require("app/utils/queryString");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
class MiniGraph extends React.Component {
    shouldComponentUpdate(nextProps) {
        // We pay for the cost of the deep comparison here since it is cheaper
        // than the cost for rendering the graph, which can take ~200ms to ~300ms to
        // render.
        return !(0, isEqual_1.default)(this.getRefreshProps(this.props), this.getRefreshProps(nextProps));
    }
    getRefreshProps(props) {
        // get props that are relevant to the API payload for the graph
        const { organization, location, eventView, yAxis } = props;
        const apiPayload = eventView.getEventsAPIPayload(location);
        const query = apiPayload.query;
        const start = apiPayload.start ? (0, dates_1.getUtcToLocalDateObject)(apiPayload.start) : null;
        const end = apiPayload.end ? (0, dates_1.getUtcToLocalDateObject)(apiPayload.end) : null;
        const period = apiPayload.statsPeriod;
        const display = eventView.getDisplayMode();
        const isTopEvents = display === types_1.DisplayModes.TOP5 || display === types_1.DisplayModes.DAILYTOP5;
        const isDaily = display === types_1.DisplayModes.DAILYTOP5 || display === types_1.DisplayModes.DAILY;
        const field = isTopEvents ? apiPayload.field : undefined;
        const topEvents = isTopEvents ? types_1.TOP_N : undefined;
        const orderby = isTopEvents ? (0, queryString_1.decodeScalar)(apiPayload.sort) : undefined;
        const interval = isDaily ? '1d' : (0, utils_1.getInterval)({ start, end, period }, 'high');
        return {
            organization,
            apiPayload,
            query,
            start,
            end,
            period,
            interval,
            project: eventView.project,
            environment: eventView.environment,
            yAxis: yAxis !== null && yAxis !== void 0 ? yAxis : eventView.getYAxis(),
            field,
            topEvents,
            orderby,
            showDaily: isDaily,
            expired: eventView.expired,
            name: eventView.name,
        };
    }
    getChartType({ showDaily, }) {
        if (showDaily) {
            return 'bar';
        }
        return 'area';
    }
    getChartComponent(chartType) {
        switch (chartType) {
            case 'bar':
                return barChart_1.default;
            case 'line':
                return lineChart_1.default;
            case 'area':
                return areaChart_1.default;
            default:
                throw new Error(`Unknown multi plot type for ${chartType}`);
        }
    }
    render() {
        const { theme, api, referrer } = this.props;
        const { query, start, end, period, interval, organization, project, environment, yAxis, field, topEvents, orderby, showDaily, expired, name, } = this.getRefreshProps(this.props);
        return (<eventsRequest_1.default organization={organization} api={api} query={query} start={start} end={end} period={period} interval={interval} project={project} environment={environment} includePrevious={false} yAxis={yAxis} field={field} topEvents={topEvents} orderby={orderby} expired={expired} name={name} referrer={referrer} partial>
        {({ loading, timeseriesData, results, errored }) => {
                var _a;
                if (errored) {
                    return (<StyledGraphContainer>
                <icons_1.IconWarning color="gray300" size="md"/>
              </StyledGraphContainer>);
                }
                if (loading) {
                    return (<StyledGraphContainer>
                <loadingIndicator_1.default mini/>
              </StyledGraphContainer>);
                }
                const allSeries = (_a = timeseriesData !== null && timeseriesData !== void 0 ? timeseriesData : results) !== null && _a !== void 0 ? _a : [];
                const chartType = this.getChartType({
                    showDaily,
                    yAxis: Array.isArray(yAxis) ? yAxis[0] : yAxis,
                    timeseriesData: allSeries,
                });
                const data = allSeries.map(series => (Object.assign(Object.assign({}, series), { lineStyle: {
                        opacity: chartType === 'line' ? 1 : 0,
                    }, smooth: true })));
                const hasOther = topEvents && topEvents + 1 === allSeries.length;
                const chartColors = allSeries.length
                    ? [...theme.charts.getColorPalette(allSeries.length - 2 - (hasOther ? 1 : 0))]
                    : undefined;
                if (chartColors && chartColors.length && hasOther) {
                    chartColors.push(theme.chartOther);
                }
                const chartOptions = {
                    colors: chartColors,
                    height: 100,
                    series: [...data],
                    xAxis: {
                        show: false,
                        axisPointer: {
                            show: false,
                        },
                    },
                    yAxis: {
                        show: true,
                        axisLine: {
                            show: false,
                        },
                        axisLabel: {
                            color: theme.chartLabel,
                            fontFamily: theme.text.family,
                            fontSize: 12,
                            formatter: (value) => (0, charts_1.axisLabelFormatter)(value, Array.isArray(yAxis) ? yAxis[0] : yAxis, true),
                            inside: true,
                            showMinLabel: false,
                            showMaxLabel: false,
                        },
                        splitNumber: 3,
                        splitLine: {
                            show: false,
                        },
                        zlevel: theme.zIndex.header,
                    },
                    tooltip: {
                        show: false,
                    },
                    toolBox: {
                        show: false,
                    },
                    grid: {
                        left: 0,
                        top: 0,
                        right: 0,
                        bottom: 0,
                        containLabel: false,
                    },
                    stacked: (typeof topEvents === 'number' && topEvents > 0) ||
                        (Array.isArray(yAxis) && yAxis.length > 1),
                };
                const Component = this.getChartComponent(chartType);
                return <Component {...chartOptions}/>;
            }}
      </eventsRequest_1.default>);
    }
}
const StyledGraphContainer = (0, styled_1.default)(props => (<loadingContainer_1.default {...props} maskBackgroundColor="transparent"/>)) `
  height: 100px;

  display: flex;
  justify-content: center;
  align-items: center;
`;
exports.default = (0, withApi_1.default)((0, react_1.withTheme)(MiniGraph));
//# sourceMappingURL=miniGraph.jsx.map