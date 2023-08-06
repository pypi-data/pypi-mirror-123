Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const pieSeries_1 = (0, tslib_1.__importDefault)(require("./series/pieSeries"));
const baseChart_1 = (0, tslib_1.__importDefault)(require("./baseChart"));
class PieChart extends React.Component {
    constructor() {
        super(...arguments);
        this.isInitialSelected = true;
        this.selected = 0;
        this.chart = React.createRef();
        // Select a series to highlight (e.g. shows details of series)
        // This is the same event as when you hover over a series in the chart
        this.highlight = dataIndex => {
            if (!this.chart.current) {
                return;
            }
            this.chart.current.getEchartsInstance().dispatchAction({
                type: 'highlight',
                seriesIndex: 0,
                dataIndex,
            });
        };
        // Opposite of `highlight`
        this.downplay = dataIndex => {
            if (!this.chart.current) {
                return;
            }
            this.chart.current.getEchartsInstance().dispatchAction({
                type: 'downplay',
                seriesIndex: 0,
                dataIndex,
            });
        };
        // echarts Legend does not have access to percentages (but tooltip does :/)
        this.getSeriesPercentages = series => {
            const total = series.data.reduce((acc, { value }) => acc + value, 0);
            return series.data
                .map(({ name, value }) => [name, Math.round((value / total) * 10000) / 100])
                .reduce((acc, [name, value]) => (Object.assign(Object.assign({}, acc), { [name]: value })), {});
        };
    }
    componentDidMount() {
        const { selectOnRender } = this.props;
        if (!selectOnRender) {
            return;
        }
        // Timeout is because we need to wait for rendering animation to complete
        // And I haven't found a callback for this
        setTimeout(() => this.highlight(0), 1000);
    }
    render() {
        const _a = this.props, { series } = _a, props = (0, tslib_1.__rest)(_a, ["series"]);
        if (!series || !series.length) {
            return null;
        }
        if (series.length > 1) {
            // eslint-disable-next-line no-console
            console.warn('PieChart only uses the first series!');
        }
        // Note, we only take the first series unit!
        const [firstSeries] = series;
        const seriesPercentages = this.getSeriesPercentages(firstSeries);
        return (<baseChart_1.default ref={this.chart} colors={firstSeries &&
                firstSeries.data && [...theme_1.default.charts.getColorPalette(firstSeries.data.length)]} 
        // when legend highlights it does NOT pass dataIndex :(
        onHighlight={({ name }) => {
                if (!this.isInitialSelected ||
                    !name ||
                    firstSeries.data[this.selected].name === name) {
                    return;
                }
                // Unhighlight if not initial "highlight" event and
                // if name exists (i.e. not dispatched from cDM) and
                // highlighted series name is different than the initially selected series name
                this.downplay(this.selected);
                this.isInitialSelected = false;
            }} onMouseOver={({ dataIndex }) => {
                if (!this.isInitialSelected) {
                    return;
                }
                if (dataIndex === this.selected) {
                    return;
                }
                this.downplay(this.selected);
                this.isInitialSelected = false;
            }} {...props} options={{
                legend: {
                    orient: 'vertical',
                    align: 'left',
                    show: true,
                    left: 10,
                    top: 10,
                    bottom: 10,
                    formatter: name => `${name} ${typeof seriesPercentages[name] !== 'undefined'
                        ? `(${seriesPercentages[name]}%)`
                        : ''}`,
                },
            }} series={[
                (0, pieSeries_1.default)({
                    name: firstSeries.seriesName,
                    data: firstSeries.data,
                    avoidLabelOverlap: false,
                    label: {
                        normal: {
                            formatter: ({ name, percent }) => `${name}\n${percent}%`,
                            show: false,
                            position: 'center',
                        },
                        emphasis: {
                            show: true,
                            textStyle: {
                                fontSize: '18',
                            },
                        },
                    },
                    itemStyle: {
                        normal: {
                            label: {
                                show: false,
                            },
                            labelLine: {
                                show: false,
                            },
                        },
                    },
                }),
            ]} xAxis={null} yAxis={null}/>);
    }
}
exports.default = PieChart;
//# sourceMappingURL=pieChart.jsx.map