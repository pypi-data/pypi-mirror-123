Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const omitBy_1 = (0, tslib_1.__importDefault)(require("lodash/omitBy"));
const events_1 = require("app/actionCreators/events");
const indicator_1 = require("app/actionCreators/indicator");
const loadingPanel_1 = (0, tslib_1.__importDefault)(require("app/components/charts/loadingPanel"));
const utils_1 = require("app/components/charts/utils");
const locale_1 = require("app/locale");
const fields_1 = require("app/utils/discover/fields");
const propNamesToIgnore = ['api', 'children', 'organization', 'loading'];
const omitIgnoredProps = (props) => (0, omitBy_1.default)(props, (_value, key) => propNamesToIgnore.includes(key));
class EventsRequest extends React.PureComponent {
    constructor() {
        super(...arguments);
        this.state = {
            reloading: !!this.props.loading,
            errored: false,
            timeseriesData: null,
            fetchedWithPrevious: false,
        };
        this.unmounting = false;
        this.fetchData = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const _a = this.props, { api, confirmedQuery, expired, name, hideError } = _a, props = (0, tslib_1.__rest)(_a, ["api", "confirmedQuery", "expired", "name", "hideError"]);
            let timeseriesData = null;
            if (confirmedQuery === false) {
                return;
            }
            this.setState(state => ({
                reloading: state.timeseriesData !== null,
                errored: false,
            }));
            if (expired) {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('%s has an invalid date range. Please try a more recent date range.', name), { append: true });
                this.setState({
                    errored: true,
                });
            }
            else {
                try {
                    api.clear();
                    timeseriesData = yield (0, events_1.doEventsRequest)(api, props);
                }
                catch (resp) {
                    if (!hideError) {
                        if (resp && resp.responseJSON && resp.responseJSON.detail) {
                            (0, indicator_1.addErrorMessage)(resp.responseJSON.detail);
                        }
                        else {
                            (0, indicator_1.addErrorMessage)((0, locale_1.t)('Error loading chart data'));
                        }
                    }
                    this.setState({
                        errored: true,
                    });
                }
            }
            if (this.unmounting) {
                return;
            }
            this.setState({
                reloading: false,
                timeseriesData,
                fetchedWithPrevious: props.includePrevious,
            });
        });
        /**
         * Retrieves data set for the current period (since data can potentially
         * contain previous period's data), as well as the previous period if
         * possible.
         *
         * Returns `null` if data does not exist
         */
        this.getData = (data) => {
            const { fetchedWithPrevious } = this.state;
            const { period, includePrevious } = this.props;
            const hasPreviousPeriod = fetchedWithPrevious || (0, utils_1.canIncludePreviousPeriod)(includePrevious, period);
            // Take the floor just in case, but data should always be divisible by 2
            const dataMiddleIndex = Math.floor(data.length / 2);
            return {
                current: hasPreviousPeriod ? data.slice(dataMiddleIndex) : data,
                previous: hasPreviousPeriod ? data.slice(0, dataMiddleIndex) : null,
            };
        };
    }
    componentDidMount() {
        this.fetchData();
    }
    componentDidUpdate(prevProps) {
        if ((0, isEqual_1.default)(omitIgnoredProps(prevProps), omitIgnoredProps(this.props))) {
            return;
        }
        this.fetchData();
    }
    componentWillUnmount() {
        this.unmounting = true;
    }
    // This aggregates all values per `timestamp`
    calculateTotalsPerTimestamp(data, getName = timestamp => timestamp * 1000) {
        return data.map(([timestamp, countArray], i) => ({
            name: getName(timestamp, countArray, i),
            value: countArray.reduce((acc, { count }) => acc + count, 0),
        }));
    }
    /**
     * Get previous period data, but transform timestamps so that data fits unto
     * the current period's data axis
     */
    transformPreviousPeriodData(current, previous, seriesName) {
        // Need the current period data array so we can take the timestamp
        // so we can be sure the data lines up
        if (!previous) {
            return null;
        }
        return {
            seriesName: seriesName !== null && seriesName !== void 0 ? seriesName : 'Previous',
            data: this.calculateTotalsPerTimestamp(previous, (_timestamp, _countArray, i) => current[i][0] * 1000),
            stack: 'previous',
        };
    }
    /**
     * Aggregate all counts for each time stamp
     */
    transformAggregatedTimeseries(data, seriesName = '') {
        return {
            seriesName,
            data: this.calculateTotalsPerTimestamp(data),
        };
    }
    /**
     * Transforms query response into timeseries data to be used in a chart
     */
    transformTimeseriesData(data, seriesName) {
        return [
            {
                seriesName: seriesName || 'Current',
                data: data.map(([timestamp, countsForTimestamp]) => ({
                    name: timestamp * 1000,
                    value: countsForTimestamp.reduce((acc, { count }) => acc + count, 0),
                })),
            },
        ];
    }
    /**
     * Transforms comparisonCount in query response into timeseries data to be used in a comparison chart for change alerts
     */
    transformComparisonTimeseriesData(data) {
        return [
            {
                seriesName: 'comparisonCount()',
                data: data.map(([timestamp, countsForTimestamp]) => ({
                    name: timestamp * 1000,
                    value: countsForTimestamp.reduce((acc, { comparisonCount }) => acc + (comparisonCount !== null && comparisonCount !== void 0 ? comparisonCount : 0), 0),
                })),
            },
        ];
    }
    processData(response, seriesIndex = 0, seriesName) {
        var _a;
        const { data, totals } = response;
        const { includeTransformedData, includeTimeAggregation, timeAggregationSeriesName, currentSeriesNames, previousSeriesNames, comparisonDelta, } = this.props;
        const { current, previous } = this.getData(data);
        const transformedData = includeTransformedData
            ? this.transformTimeseriesData(current, seriesName !== null && seriesName !== void 0 ? seriesName : currentSeriesNames === null || currentSeriesNames === void 0 ? void 0 : currentSeriesNames[seriesIndex])
            : [];
        const transformedComparisonData = includeTransformedData && comparisonDelta
            ? this.transformComparisonTimeseriesData(current)
            : [];
        const previousData = includeTransformedData
            ? this.transformPreviousPeriodData(current, previous, (_a = (seriesName ? `previous ${seriesName}` : undefined)) !== null && _a !== void 0 ? _a : previousSeriesNames === null || previousSeriesNames === void 0 ? void 0 : previousSeriesNames[seriesIndex])
            : null;
        const timeAggregatedData = includeTimeAggregation
            ? this.transformAggregatedTimeseries(current, timeAggregationSeriesName || '')
            : {};
        const timeframe = response.start && response.end
            ? !previous
                ? {
                    start: response.start * 1000,
                    end: response.end * 1000,
                }
                : {
                    // Find the midpoint of start & end since previous includes 2x data
                    start: (response.start + response.end) * 500,
                    end: response.end * 1000,
                }
            : undefined;
        return {
            data: transformedData,
            comparisonData: transformedComparisonData,
            allData: data,
            originalData: current,
            totals,
            originalPreviousData: previous,
            previousData,
            timeAggregatedData,
            timeframe,
        };
    }
    render() {
        const _a = this.props, { children, showLoading } = _a, props = (0, tslib_1.__rest)(_a, ["children", "showLoading"]);
        const { timeseriesData, reloading, errored } = this.state;
        // Is "loading" if data is null
        const loading = this.props.loading || timeseriesData === null;
        if (showLoading && loading) {
            return <loadingPanel_1.default data-test-id="events-request-loading"/>;
        }
        if ((0, utils_1.isMultiSeriesStats)(timeseriesData)) {
            // Convert multi-series results into chartable series. Multi series results
            // are created when multiple yAxis are used or a topEvents request is made.
            // Convert the timeseries data into a multi-series result set.
            // As the server will have replied with a map like:
            // {[titleString: string]: EventsStats}
            let timeframe = undefined;
            const sortedTimeseriesData = Object.keys(timeseriesData)
                .map((seriesName, index) => {
                const seriesData = timeseriesData[seriesName];
                const processedData = this.processData(seriesData, index, (0, fields_1.stripEquationPrefix)(seriesName));
                if (!timeframe) {
                    timeframe = processedData.timeframe;
                }
                return [
                    seriesData.order || 0,
                    processedData.data[0],
                    processedData.previousData,
                ];
            })
                .sort((a, b) => a[0] - b[0]);
            const results = sortedTimeseriesData.map(item => {
                return item[1];
            });
            const previousTimeseriesData = sortedTimeseriesData.some(item => item[2] === null)
                ? undefined
                : sortedTimeseriesData.map(item => {
                    return item[2];
                });
            return children(Object.assign({ loading,
                reloading,
                errored,
                results,
                timeframe,
                previousTimeseriesData }, props));
        }
        if (timeseriesData) {
            const { data: transformedTimeseriesData, comparisonData: transformedComparisonTimeseriesData, allData: allTimeseriesData, originalData: originalTimeseriesData, totals: timeseriesTotals, originalPreviousData: originalPreviousTimeseriesData, previousData: previousTimeseriesData, timeAggregatedData, timeframe, } = this.processData(timeseriesData);
            return children(Object.assign({ loading,
                reloading,
                errored, 
                // timeseries data
                timeseriesData: transformedTimeseriesData, comparisonTimeseriesData: transformedComparisonTimeseriesData, allTimeseriesData,
                originalTimeseriesData,
                timeseriesTotals,
                originalPreviousTimeseriesData, previousTimeseriesData: previousTimeseriesData
                    ? [previousTimeseriesData]
                    : previousTimeseriesData, timeAggregatedData,
                timeframe }, props));
        }
        return children(Object.assign({ loading,
            reloading,
            errored }, props));
    }
}
EventsRequest.defaultProps = {
    period: undefined,
    start: null,
    end: null,
    interval: '1d',
    comparisonDelta: undefined,
    limit: 15,
    query: '',
    includePrevious: true,
    includeTransformedData: true,
};
exports.default = EventsRequest;
//# sourceMappingURL=eventsRequest.jsx.map