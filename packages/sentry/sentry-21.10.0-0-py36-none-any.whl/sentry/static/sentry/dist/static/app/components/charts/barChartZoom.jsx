Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const dataZoomInside_1 = (0, tslib_1.__importDefault)(require("app/components/charts/components/dataZoomInside"));
const toolBox_1 = (0, tslib_1.__importDefault)(require("app/components/charts/components/toolBox"));
const callIfFunction_1 = require("app/utils/callIfFunction");
class BarChartZoom extends React.Component {
    constructor() {
        super(...arguments);
        /**
         * Enable zoom immediately instead of having to toggle to zoom
         */
        this.handleChartReady = chart => {
            chart.dispatchAction({
                type: 'takeGlobalCursor',
                key: 'dataZoomSelect',
                dataZoomSelectActive: true,
            });
            (0, callIfFunction_1.callIfFunction)(this.props.onChartReady, chart);
        };
        this.handleDataZoom = (evt, chart) => {
            const model = chart.getModel();
            const { xAxis } = model.option;
            const axis = xAxis[0];
            // Both of these values should not be null, but we include it just in case.
            // These values are null when the user uses the toolbox included in ECharts
            // to navigate back through zoom history, but we hide it below.
            if (axis.rangeStart !== null && axis.rangeEnd !== null) {
                const { buckets, location, paramStart, paramEnd, minZoomWidth, onHistoryPush } = this.props;
                const { start } = buckets[axis.rangeStart];
                const { end } = buckets[axis.rangeEnd];
                if (minZoomWidth === undefined || end - start > minZoomWidth) {
                    const target = {
                        pathname: location.pathname,
                        query: Object.assign(Object.assign({}, location.query), { [paramStart]: start, [paramEnd]: end }),
                    };
                    if (onHistoryPush) {
                        onHistoryPush(start, end);
                    }
                    else {
                        react_router_1.browserHistory.push(target);
                    }
                }
                else {
                    // Dispatch the restore action here to stop ECharts from zooming
                    chart.dispatchAction({ type: 'restore' });
                    (0, callIfFunction_1.callIfFunction)(this.props.onDataZoomCancelled);
                }
            }
            else {
                // Dispatch the restore action here to stop ECharts from zooming
                chart.dispatchAction({ type: 'restore' });
                (0, callIfFunction_1.callIfFunction)(this.props.onDataZoomCancelled);
            }
            (0, callIfFunction_1.callIfFunction)(this.props.onDataZoom, evt, chart);
        };
    }
    render() {
        const { children, xAxisIndex } = this.props;
        const renderProps = {
            onChartReady: this.handleChartReady,
            dataZoom: (0, dataZoomInside_1.default)({ xAxisIndex }),
            // We must include data zoom in the toolbox for the zoom to work,
            // but we do not want to show the toolbox components.
            toolBox: (0, toolBox_1.default)({}, {
                dataZoom: {
                    title: {
                        zoom: '',
                        back: '',
                    },
                    iconStyle: {
                        borderWidth: 0,
                        color: 'transparent',
                        opacity: 0,
                    },
                },
            }),
            onDataZoom: this.handleDataZoom,
        };
        return children(renderProps);
    }
}
exports.default = BarChartZoom;
//# sourceMappingURL=barChartZoom.jsx.map