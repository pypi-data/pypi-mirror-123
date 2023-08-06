Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const miniBarChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/miniBarChart"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const initialState = {
    error: false,
    loading: true,
    rawData: {
        'client-api.all-versions.responses.2xx': [],
        'client-api.all-versions.responses.4xx': [],
        'client-api.all-versions.responses.5xx': [],
    },
};
class ApiChart extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = initialState;
        this.fetchData = () => {
            const statNameList = [
                'client-api.all-versions.responses.2xx',
                'client-api.all-versions.responses.4xx',
                'client-api.all-versions.responses.5xx',
            ];
            statNameList.forEach(statName => {
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
        this.requestFinished = () => {
            const { rawData } = this.state;
            if (rawData['client-api.all-versions.responses.2xx'] &&
                rawData['client-api.all-versions.responses.4xx'] &&
                rawData['client-api.all-versions.responses.5xx']) {
                this.setState({
                    loading: false,
                });
            }
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
    processRawSeries(series) {
        return series.map(item => ({ name: item[0] * 1000, value: item[1] }));
    }
    getChartSeries() {
        const { rawData } = this.state;
        return [
            {
                seriesName: '2xx',
                data: this.processRawSeries(rawData['client-api.all-versions.responses.2xx']),
                color: theme_1.default.green200,
            },
            {
                seriesName: '4xx',
                data: this.processRawSeries(rawData['client-api.all-versions.responses.4xx']),
                color: theme_1.default.blue300,
            },
            {
                seriesName: '5xx',
                data: this.processRawSeries(rawData['client-api.all-versions.responses.5xx']),
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
exports.default = (0, withApi_1.default)(ApiChart);
//# sourceMappingURL=apiChart.jsx.map