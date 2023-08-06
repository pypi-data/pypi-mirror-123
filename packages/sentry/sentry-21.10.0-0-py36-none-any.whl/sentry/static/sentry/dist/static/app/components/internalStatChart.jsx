Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const miniBarChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/miniBarChart"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
class InternalStatChart extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            error: false,
            loading: true,
            data: null,
        };
        this.fetchData = () => {
            this.setState({ loading: true });
            this.props.api.request('/internal/stats/', {
                method: 'GET',
                data: {
                    since: this.props.since,
                    resolution: this.props.resolution,
                    key: this.props.stat,
                },
                success: data => this.setState({
                    data,
                    loading: false,
                    error: false,
                }),
                error: () => this.setState({ error: true, loading: false }),
            });
        };
    }
    componentDidMount() {
        this.fetchData();
    }
    shouldComponentUpdate(_nextProps, nextState) {
        return this.state.loading !== nextState.loading;
    }
    componentDidUpdate(prevProps) {
        if (prevProps.since !== this.props.since ||
            prevProps.stat !== this.props.stat ||
            prevProps.resolution !== this.props.resolution) {
            this.fetchData();
        }
    }
    render() {
        var _a;
        const { loading, error, data } = this.state;
        const { label, height } = this.props;
        if (loading) {
            return <loadingIndicator_1.default />;
        }
        else if (error) {
            return <loadingError_1.default onRetry={this.fetchData}/>;
        }
        const series = {
            seriesName: label,
            data: (_a = data === null || data === void 0 ? void 0 : data.map(([timestamp, value]) => ({
                name: timestamp * 1000,
                value,
            }))) !== null && _a !== void 0 ? _a : [],
        };
        return (<miniBarChart_1.default height={height !== null && height !== void 0 ? height : 150} series={[series]} isGroupedByDate showTimeInTooltip labelYAxisExtents/>);
    }
}
exports.default = (0, withApi_1.default)(InternalStatChart);
//# sourceMappingURL=internalStatChart.jsx.map