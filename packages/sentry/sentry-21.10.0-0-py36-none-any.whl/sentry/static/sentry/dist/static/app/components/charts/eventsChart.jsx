Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const areaChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/areaChart"));
const barChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/barChart"));
const chartZoom_1 = (0, tslib_1.__importDefault)(require("app/components/charts/chartZoom"));
const errorPanel_1 = (0, tslib_1.__importDefault)(require("app/components/charts/errorPanel"));
const lineChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/lineChart"));
const releaseSeries_1 = (0, tslib_1.__importDefault)(require("app/components/charts/releaseSeries"));
const transitionChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/transitionChart"));
const transparentLoadingMask_1 = (0, tslib_1.__importDefault)(require("app/components/charts/transparentLoadingMask"));
const utils_1 = require("app/components/charts/utils");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const utils_2 = require("app/utils");
const charts_1 = require("app/utils/discover/charts");
const fields_1 = require("app/utils/discover/fields");
const queryString_1 = require("app/utils/queryString");
const eventsRequest_1 = (0, tslib_1.__importDefault)(require("./eventsRequest"));
class Chart extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            seriesSelection: {},
            forceUpdate: false,
        };
        this.handleLegendSelectChanged = legendChange => {
            const { disableableSeries = [] } = this.props;
            const { selected } = legendChange;
            const seriesSelection = Object.keys(selected).reduce((state, key) => {
                // we only want them to be able to disable the Releases&Other series,
                // and not any of the other possible series here
                const disableable = ['Releases', 'Other'].includes(key) || disableableSeries.includes(key);
                state[key] = disableable ? selected[key] : true;
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
        if (nextProps.reloading || !nextProps.timeseriesData) {
            return false;
        }
        if ((0, isEqual_1.default)(this.props.timeseriesData, nextProps.timeseriesData) &&
            (0, isEqual_1.default)(this.props.releaseSeries, nextProps.releaseSeries) &&
            (0, isEqual_1.default)(this.props.previousTimeseriesData, nextProps.previousTimeseriesData)) {
            return false;
        }
        return true;
    }
    getChartComponent() {
        const { showDaily, timeseriesData, yAxis, chartComponent } = this.props;
        if ((0, utils_2.defined)(chartComponent)) {
            return chartComponent;
        }
        if (showDaily) {
            return barChart_1.default;
        }
        if (timeseriesData.length > 1) {
            switch ((0, fields_1.aggregateMultiPlotType)(yAxis)) {
                case 'line':
                    return lineChart_1.default;
                case 'area':
                    return areaChart_1.default;
                default:
                    throw new Error(`Unknown multi plot type for ${yAxis}`);
            }
        }
        return areaChart_1.default;
    }
    render() {
        var _a, _b, _c;
        const _d = this.props, { theme, loading: _loading, reloading: _reloading, yAxis, releaseSeries, zoomRenderProps, timeseriesData, previousTimeseriesData, showLegend, legendOptions, chartOptions: chartOptionsProp, currentSeriesNames, previousSeriesNames, seriesTransformer, previousSeriesTransformer, colors, height, timeframe, topEvents } = _d, props = (0, tslib_1.__rest)(_d, ["theme", "loading", "reloading", "yAxis", "releaseSeries", "zoomRenderProps", "timeseriesData", "previousTimeseriesData", "showLegend", "legendOptions", "chartOptions", "currentSeriesNames", "previousSeriesNames", "seriesTransformer", "previousSeriesTransformer", "colors", "height", "timeframe", "topEvents"]);
        const { seriesSelection } = this.state;
        const data = [
            ...(currentSeriesNames.length > 0 ? currentSeriesNames : [(0, locale_1.t)('Current')]),
            ...(previousSeriesNames.length > 0 ? previousSeriesNames : [(0, locale_1.t)('Previous')]),
        ];
        const releasesLegend = (0, locale_1.t)('Releases');
        const hasOther = topEvents && topEvents + 1 === timeseriesData.length;
        if (hasOther) {
            data.push('Other');
        }
        if (Array.isArray(releaseSeries)) {
            data.push(releasesLegend);
        }
        // Temporary fix to improve performance on pages with a high number of releases.
        const releases = releaseSeries && releaseSeries[0];
        const hideReleasesByDefault = Array.isArray(releaseSeries) &&
            ((_b = (_a = releases) === null || _a === void 0 ? void 0 : _a.markLine) === null || _b === void 0 ? void 0 : _b.data) &&
            releases.markLine.data.length >= utils_1.RELEASE_LINES_THRESHOLD;
        const selected = !Array.isArray(releaseSeries)
            ? seriesSelection
            : Object.keys(seriesSelection).length === 0 && hideReleasesByDefault
                ? { [releasesLegend]: false }
                : seriesSelection;
        const legend = showLegend
            ? Object.assign({ right: 16, top: 12, data,
                selected }, (legendOptions !== null && legendOptions !== void 0 ? legendOptions : {})) : undefined;
        let series = Array.isArray(releaseSeries)
            ? [...timeseriesData, ...releaseSeries]
            : timeseriesData;
        let previousSeries = previousTimeseriesData;
        if (seriesTransformer) {
            series = seriesTransformer(series);
        }
        if (previousSeriesTransformer) {
            previousSeries = previousSeries === null || previousSeries === void 0 ? void 0 : previousSeries.map(prev => previousSeriesTransformer(prev));
        }
        const chartColors = timeseriesData.length
            ? (_c = colors === null || colors === void 0 ? void 0 : colors.slice(0, series.length)) !== null && _c !== void 0 ? _c : [
                ...theme.charts.getColorPalette(timeseriesData.length - 2 - (hasOther ? 1 : 0)),
            ]
            : undefined;
        if (chartColors && chartColors.length && hasOther) {
            chartColors.push(theme.chartOther);
        }
        const chartOptions = Object.assign({ colors: chartColors, grid: {
                left: '24px',
                right: '24px',
                top: '32px',
                bottom: '12px',
            }, seriesOptions: {
                showSymbol: false,
            }, tooltip: {
                trigger: 'axis',
                truncate: 80,
                valueFormatter: (value) => (0, charts_1.tooltipFormatter)(value, yAxis),
            }, xAxis: timeframe
                ? {
                    min: timeframe.start,
                    max: timeframe.end,
                }
                : undefined, yAxis: {
                axisLabel: {
                    color: theme.chartLabel,
                    formatter: (value) => (0, charts_1.axisLabelFormatter)(value, yAxis),
                },
            } }, (chartOptionsProp !== null && chartOptionsProp !== void 0 ? chartOptionsProp : {}));
        const Component = this.getChartComponent();
        return (<Component {...props} {...zoomRenderProps} {...chartOptions} legend={legend} onLegendSelectChanged={this.handleLegendSelectChanged} series={series} previousPeriod={previousSeries ? previousSeries : undefined} height={height}/>);
    }
}
const ThemedChart = (0, react_1.withTheme)(Chart);
class EventsChart extends React.Component {
    isStacked() {
        const { topEvents, yAxis } = this.props;
        return ((typeof topEvents === 'number' && topEvents > 0) ||
            (Array.isArray(yAxis) && yAxis.length > 1));
    }
    render() {
        const _a = this.props, { api, period, utc, query, router, start, end, projects, environments, showLegend, yAxis, disablePrevious, disableReleases, emphasizeReleases, currentSeriesName: currentName, previousSeriesName: previousName, seriesTransformer, previousSeriesTransformer, field, interval, showDaily, topEvents, orderby, confirmedQuery, colors, chartHeader, legendOptions, chartOptions, preserveReleaseQueryParams, releaseQueryExtra, disableableSeries, chartComponent, usePageZoom, height, withoutZerofill } = _a, props = (0, tslib_1.__rest)(_a, ["api", "period", "utc", "query", "router", "start", "end", "projects", "environments", "showLegend", "yAxis", "disablePrevious", "disableReleases", "emphasizeReleases", "currentSeriesName", "previousSeriesName", "seriesTransformer", "previousSeriesTransformer", "field", "interval", "showDaily", "topEvents", "orderby", "confirmedQuery", "colors", "chartHeader", "legendOptions", "chartOptions", "preserveReleaseQueryParams", "releaseQueryExtra", "disableableSeries", "chartComponent", "usePageZoom", "height", "withoutZerofill"]);
        // Include previous only on relative dates (defaults to relative if no start and end)
        const includePrevious = !disablePrevious && !start && !end;
        const yAxisArray = (0, queryString_1.decodeList)(yAxis);
        const yAxisSeriesNames = yAxisArray.map(name => {
            let yAxisLabel = name && (0, fields_1.isEquation)(name) ? (0, fields_1.getEquation)(name) : name;
            if (yAxisLabel && yAxisLabel.length > 60) {
                yAxisLabel = yAxisLabel.substr(0, 60) + '...';
            }
            return yAxisLabel;
        });
        const previousSeriesNames = previousName
            ? [previousName]
            : yAxisSeriesNames.map(name => (0, locale_1.t)('previous %s', name));
        const currentSeriesNames = currentName ? [currentName] : yAxisSeriesNames;
        const intervalVal = showDaily ? '1d' : interval || (0, utils_1.getInterval)(this.props, 'high');
        let chartImplementation = ({ zoomRenderProps, releaseSeries, errored, loading, reloading, results, timeseriesData, previousTimeseriesData, timeframe, }) => {
            if (errored) {
                return (<errorPanel_1.default>
            <icons_1.IconWarning color="gray300" size="lg"/>
          </errorPanel_1.default>);
            }
            const seriesData = results ? results : timeseriesData;
            return (<transitionChart_1.default loading={loading} reloading={reloading} height={height ? `${height}px` : undefined}>
          <transparentLoadingMask_1.default visible={reloading}/>

          {React.isValidElement(chartHeader) && chartHeader}

          <ThemedChart zoomRenderProps={zoomRenderProps} loading={loading} reloading={reloading} showLegend={showLegend} releaseSeries={releaseSeries || []} timeseriesData={seriesData !== null && seriesData !== void 0 ? seriesData : []} previousTimeseriesData={previousTimeseriesData} currentSeriesNames={currentSeriesNames} previousSeriesNames={previousSeriesNames} seriesTransformer={seriesTransformer} previousSeriesTransformer={previousSeriesTransformer} stacked={this.isStacked()} yAxis={yAxisArray[0]} showDaily={showDaily} colors={colors} legendOptions={legendOptions} chartOptions={chartOptions} disableableSeries={disableableSeries} chartComponent={chartComponent} height={height} timeframe={timeframe} topEvents={topEvents}/>
        </transitionChart_1.default>);
        };
        if (!disableReleases) {
            const previousChart = chartImplementation;
            chartImplementation = chartProps => (<releaseSeries_1.default utc={utc} period={period} start={start} end={end} projects={projects} environments={environments} emphasizeReleases={emphasizeReleases} preserveQueryParams={preserveReleaseQueryParams} queryExtra={releaseQueryExtra}>
          {({ releaseSeries }) => previousChart(Object.assign(Object.assign({}, chartProps), { releaseSeries }))}
        </releaseSeries_1.default>);
        }
        return (<chartZoom_1.default router={router} period={period} start={start} end={end} utc={utc} usePageDate={usePageZoom} {...props}>
        {zoomRenderProps => (<eventsRequest_1.default {...props} api={api} period={period} project={projects} environment={environments} start={start} end={end} interval={intervalVal} query={query} includePrevious={includePrevious} currentSeriesNames={currentSeriesNames} previousSeriesNames={previousSeriesNames} yAxis={yAxis} field={field} orderby={orderby} topEvents={topEvents} confirmedQuery={confirmedQuery} partial 
            // Cannot do interpolation when stacking series
            withoutZerofill={withoutZerofill && !this.isStacked()}>
            {eventData => {
                    return chartImplementation(Object.assign(Object.assign({}, eventData), { zoomRenderProps }));
                }}
          </eventsRequest_1.default>)}
      </chartZoom_1.default>);
    }
}
exports.default = EventsChart;
//# sourceMappingURL=eventsChart.jsx.map