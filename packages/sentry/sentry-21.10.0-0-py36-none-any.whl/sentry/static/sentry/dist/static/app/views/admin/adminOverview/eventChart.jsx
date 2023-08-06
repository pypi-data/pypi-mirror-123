Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const miniBarChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/miniBarChart"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const locale_1 = require("app/locale");
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const initialState = {
    error: false,
    loading: true,
    rawData: {
        'events.total': [],
        'events.dropped': [],
    },
    stats: { received: [], rejected: [] },
};
class EventChart extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = initialState;
        this.fetchData = () => {
            const statNameList = ['events.total', 'events.dropped'];
            statNameList.forEach(statName => {
                // query the organization stats via a separate call as its possible the project stats
                // are too heavy
                this.props.api.request('/internal/stats/', {
                    method: 'GET',
                    data: {
                        since: this.props.since,
                        resolution: this.props.resolution,
                        key: statName,
                    },
                    success: data => {
                        this.setState(prevState => {
                            const rawData = prevState.rawData;
                            rawData[statName] = data;
                            return {
                                rawData,
                            };
                        }, this.requestFinished);
                    },
                    error: () => {
                        this.setState({
                            error: true,
                        });
                    },
                });
            });
        };
    }
    componentWillMount() {
        this.fetchData();
    }
    componentWillReceiveProps(nextProps) {
        if (this.props.since !== nextProps.since) {
            this.setState(initialState, this.fetchData);
        }
    }
    requestFinished() {
        const { rawData } = this.state;
        if (rawData['events.total'] && rawData['events.dropped']) {
            this.processOrgData();
        }
    }
    processOrgData() {
        const { rawData } = this.state;
        const sReceived = {};
        const sRejected = {};
        const aReceived = [0, 0]; // received, points
        rawData['events.total'].forEach((point, idx) => {
            var _a;
            const dReceived = point[1];
            const dRejected = (_a = rawData['events.dropped'][idx]) === null || _a === void 0 ? void 0 : _a[1];
            const ts = point[0];
            if (sReceived[ts] === undefined) {
                sReceived[ts] = dReceived;
                sRejected[ts] = dRejected;
            }
            else {
                sReceived[ts] += dReceived;
                sRejected[ts] += dRejected;
            }
            if (dReceived > 0) {
                aReceived[0] += dReceived;
                aReceived[1] += 1;
            }
        });
        this.setState({
            stats: {
                rejected: Object.keys(sRejected).map(ts => ({
                    name: parseInt(ts, 10) * 1000,
                    value: sRejected[ts] || 0,
                })),
                accepted: Object.keys(sReceived).map(ts => 
                // total number of events accepted (received - rejected)
                ({ name: parseInt(ts, 10) * 1000, value: sReceived[ts] - sRejected[ts] })),
            },
            loading: false,
        });
    }
    getChartSeries() {
        const { stats } = this.state;
        return [
            {
                seriesName: (0, locale_1.t)('Accepted'),
                data: stats.accepted,
                color: theme_1.default.blue300,
            },
            {
                seriesName: (0, locale_1.t)('Dropped'),
                data: stats.rejected,
                color: theme_1.default.red200,
            },
        ];
    }
    render() {
        const { loading, error } = this.state;
        if (loading) {
            return <loadingIndicator_1.default />;
        }
        else if (error) {
            return <loadingError_1.default onRetry={this.fetchData}/>;
        }
        const series = this.getChartSeries();
        const colors = series.map(({ color }) => color);
        return (<miniBarChart_1.default series={series} colors={colors} height={110} stacked isGroupedByDate showTimeInTooltip labelYAxisExtents/>);
    }
}
exports.default = (0, withApi_1.default)(EventChart);
//# sourceMappingURL=eventChart.jsx.map