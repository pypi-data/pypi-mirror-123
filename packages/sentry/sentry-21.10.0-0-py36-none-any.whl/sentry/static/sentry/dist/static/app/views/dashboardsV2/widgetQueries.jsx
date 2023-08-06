Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const events_1 = require("app/actionCreators/events");
const utils_1 = require("app/components/charts/utils");
const utils_2 = require("app/components/organizations/globalSelectionHeader/utils");
const locale_1 = require("app/locale");
const dates_1 = require("app/utils/dates");
const fields_1 = require("app/utils/discover/fields");
const genericDiscoverQuery_1 = require("app/utils/discover/genericDiscoverQuery");
const types_1 = require("app/utils/discover/types");
const utils_3 = require("./utils");
// Don't fetch more than 4000 bins as we're plotting on a small area.
const MAX_BIN_COUNT = 4000;
function getWidgetInterval(widget, datetimeObj) {
    // Bars charts are daily totals to aligned with discover. It also makes them
    // usefully different from line/area charts until we expose the interval control, or remove it.
    let interval = widget.displayType === 'bar' ? '1d' : widget.interval;
    if (!interval) {
        // Default to 5 minutes
        interval = '5m';
    }
    const desiredPeriod = (0, dates_1.parsePeriodToHours)(interval);
    const selectedRange = (0, utils_1.getDiffInMinutes)(datetimeObj);
    if (selectedRange / desiredPeriod > MAX_BIN_COUNT) {
        return (0, utils_1.getInterval)(datetimeObj, 'high');
    }
    return interval;
}
function transformSeries(stats, seriesName) {
    return {
        seriesName,
        data: stats.data.map(([timestamp, counts]) => ({
            name: timestamp * 1000,
            value: counts.reduce((acc, { count }) => acc + count, 0),
        })),
    };
}
function transformResult(query, result) {
    let output = [];
    const seriesNamePrefix = query.name;
    if ((0, utils_1.isMultiSeriesStats)(result)) {
        // Convert multi-series results into chartable series. Multi series results
        // are created when multiple yAxis are used. Convert the timeseries
        // data into a multi-series result set.  As the server will have
        // replied with a map like: {[titleString: string]: EventsStats}
        const transformed = Object.keys(result)
            .map((seriesName) => {
            const prefixedName = seriesNamePrefix
                ? `${seriesNamePrefix} : ${seriesName}`
                : seriesName;
            const seriesData = result[seriesName];
            return [seriesData.order || 0, transformSeries(seriesData, prefixedName)];
        })
            .sort((a, b) => a[0] - b[0])
            .map(item => item[1]);
        output = output.concat(transformed);
    }
    else {
        const field = query.fields[0];
        const prefixedName = seriesNamePrefix ? `${seriesNamePrefix} : ${field}` : field;
        const transformed = transformSeries(result, prefixedName);
        output.push(transformed);
    }
    return output;
}
class WidgetQueries extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            loading: true,
            queryFetchID: undefined,
            errorMessage: undefined,
            timeseriesResults: undefined,
            rawResults: undefined,
            tableResults: undefined,
        };
    }
    componentDidMount() {
        this.fetchData();
    }
    componentDidUpdate(prevProps) {
        var _a;
        const { selection, widget } = this.props;
        // We do not fetch data whenever the query name changes.
        // Also don't count empty fields when checking for field changes
        const [prevWidgetQueryNames, prevWidgetQueries] = prevProps.widget.queries
            .map((query) => {
            query.fields = query.fields.filter(field => !!field);
            return query;
        })
            .reduce(([names, queries], _a) => {
            var { name } = _a, rest = (0, tslib_1.__rest)(_a, ["name"]);
            names.push(name);
            queries.push(rest);
            return [names, queries];
        }, [[], []]);
        const [widgetQueryNames, widgetQueries] = widget.queries
            .map((query) => {
            query.fields = query.fields.filter(field => !!field && field !== 'equation|');
            return query;
        })
            .reduce(([names, queries], _a) => {
            var { name } = _a, rest = (0, tslib_1.__rest)(_a, ["name"]);
            names.push(name);
            queries.push(rest);
            return [names, queries];
        }, [[], []]);
        if (!(0, isEqual_1.default)(widget.displayType, prevProps.widget.displayType) ||
            !(0, isEqual_1.default)(widget.interval, prevProps.widget.interval) ||
            !(0, isEqual_1.default)(widgetQueries, prevWidgetQueries) ||
            !(0, isEqual_1.default)(widget.displayType, prevProps.widget.displayType) ||
            !(0, utils_2.isSelectionEqual)(selection, prevProps.selection)) {
            this.fetchData();
            return;
        }
        if (!this.state.loading &&
            !(0, isEqual_1.default)(prevWidgetQueryNames, widgetQueryNames) &&
            ((_a = this.state.rawResults) === null || _a === void 0 ? void 0 : _a.length) === widget.queries.length) {
            // If the query names has changed, then update timeseries labels
            // eslint-disable-next-line react/no-did-update-set-state
            this.setState(prevState => {
                const timeseriesResults = widget.queries.reduce((acc, query, index) => {
                    return acc.concat(transformResult(query, prevState.rawResults[index]));
                }, []);
                return Object.assign(Object.assign({}, prevState), { timeseriesResults });
            });
        }
    }
    fetchEventData(queryFetchID) {
        const { selection, api, organization, widget } = this.props;
        let tableResults = [];
        // Table, world map, and stat widgets use table results and need
        // to do a discover 'table' query instead of a 'timeseries' query.
        this.setState({ tableResults: [] });
        const promises = widget.queries.map(query => {
            const eventView = (0, utils_3.eventViewFromWidget)(widget.title, query, selection);
            let url = '';
            const params = {
                per_page: 5,
                noPagination: true,
            };
            if (widget.displayType === 'table') {
                url = `/organizations/${organization.slug}/eventsv2/`;
                params.referrer = 'api.dashboards.tablewidget';
            }
            else if (widget.displayType === 'big_number') {
                url = `/organizations/${organization.slug}/eventsv2/`;
                params.per_page = 1;
                params.referrer = 'api.dashboards.bignumberwidget';
            }
            else if (widget.displayType === 'world_map') {
                url = `/organizations/${organization.slug}/events-geo/`;
                delete params.per_page;
                params.referrer = 'api.dashboards.worldmapwidget';
            }
            else {
                throw Error('Expected widget displayType to be either big_number, table or world_map');
            }
            return (0, genericDiscoverQuery_1.doDiscoverQuery)(api, url, Object.assign(Object.assign({}, eventView.generateQueryStringObject()), params));
        });
        let completed = 0;
        promises.forEach((promise, i) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            var _a, _b, _c;
            try {
                const [data] = yield promise;
                // Cast so we can add the title.
                const tableData = data;
                tableData.title = (_b = (_a = widget.queries[i]) === null || _a === void 0 ? void 0 : _a.name) !== null && _b !== void 0 ? _b : '';
                // Overwrite the local var to work around state being stale in tests.
                tableResults = [...tableResults, tableData];
                this.setState(prevState => {
                    if (prevState.queryFetchID !== queryFetchID) {
                        // invariant: a different request was initiated after this request
                        return prevState;
                    }
                    return Object.assign(Object.assign({}, prevState), { tableResults });
                });
            }
            catch (err) {
                const errorMessage = ((_c = err === null || err === void 0 ? void 0 : err.responseJSON) === null || _c === void 0 ? void 0 : _c.detail) || (0, locale_1.t)('An unknown error occurred.');
                this.setState({ errorMessage });
            }
            finally {
                completed++;
                this.setState(prevState => {
                    if (prevState.queryFetchID !== queryFetchID) {
                        // invariant: a different request was initiated after this request
                        return prevState;
                    }
                    return Object.assign(Object.assign({}, prevState), { loading: completed === promises.length ? false : true });
                });
            }
        }));
    }
    fetchTimeseriesData(queryFetchID, displayType) {
        const { selection, api, organization, widget } = this.props;
        this.setState({ timeseriesResults: [], rawResults: [] });
        const { environments, projects } = selection;
        const { start, end, period: statsPeriod } = selection.datetime;
        const interval = getWidgetInterval(widget, {
            start,
            end,
            period: statsPeriod,
        });
        const promises = widget.queries.map(query => {
            let requestData;
            if (widget.displayType === 'top_n') {
                requestData = {
                    organization,
                    interval,
                    start,
                    end,
                    project: projects,
                    environment: environments,
                    period: statsPeriod,
                    query: query.conditions,
                    yAxis: (0, fields_1.getAggregateFields)(query.fields)[0],
                    includePrevious: false,
                    referrer: `api.dashboards.widget.${displayType}-chart`,
                    partial: true,
                    topEvents: types_1.TOP_N,
                    field: query.fields,
                };
                if (query.orderby) {
                    requestData.orderby = query.orderby;
                }
            }
            else {
                requestData = {
                    organization,
                    interval,
                    start,
                    end,
                    project: projects,
                    environment: environments,
                    period: statsPeriod,
                    query: query.conditions,
                    yAxis: query.fields,
                    orderby: query.orderby,
                    includePrevious: false,
                    referrer: `api.dashboards.widget.${displayType}-chart`,
                    partial: true,
                };
            }
            return (0, events_1.doEventsRequest)(api, requestData);
        });
        let completed = 0;
        promises.forEach((promise, i) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            var _a;
            try {
                const rawResults = yield promise;
                this.setState(prevState => {
                    var _a, _b;
                    if (prevState.queryFetchID !== queryFetchID) {
                        // invariant: a different request was initiated after this request
                        return prevState;
                    }
                    const timeseriesResults = ((_a = prevState.timeseriesResults) !== null && _a !== void 0 ? _a : []).concat(transformResult(widget.queries[i], rawResults));
                    return Object.assign(Object.assign({}, prevState), { timeseriesResults, rawResults: ((_b = prevState.rawResults) !== null && _b !== void 0 ? _b : []).concat(rawResults) });
                });
            }
            catch (err) {
                const errorMessage = ((_a = err === null || err === void 0 ? void 0 : err.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) || (0, locale_1.t)('An unknown error occurred.');
                this.setState({ errorMessage });
            }
            finally {
                completed++;
                this.setState(prevState => {
                    if (prevState.queryFetchID !== queryFetchID) {
                        // invariant: a different request was initiated after this request
                        return prevState;
                    }
                    return Object.assign(Object.assign({}, prevState), { loading: completed === promises.length ? false : true });
                });
            }
        }));
    }
    fetchData() {
        const { widget } = this.props;
        const queryFetchID = Symbol('queryFetchID');
        this.setState({ loading: true, errorMessage: undefined, queryFetchID });
        if (['table', 'world_map', 'big_number'].includes(widget.displayType)) {
            this.fetchEventData(queryFetchID);
        }
        else {
            this.fetchTimeseriesData(queryFetchID, widget.displayType);
        }
    }
    render() {
        const { children } = this.props;
        const { loading, timeseriesResults, tableResults, errorMessage } = this.state;
        return children({ loading, timeseriesResults, tableResults, errorMessage });
    }
}
exports.default = WidgetQueries;
//# sourceMappingURL=widgetQueries.jsx.map