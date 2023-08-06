Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const qs = (0, tslib_1.__importStar)(require("query-string"));
const globalSelection_1 = require("app/actionCreators/globalSelection");
const dataZoomInside_1 = (0, tslib_1.__importDefault)(require("app/components/charts/components/dataZoomInside"));
const toolBox_1 = (0, tslib_1.__importDefault)(require("app/components/charts/components/toolBox"));
const callIfFunction_1 = require("app/utils/callIfFunction");
const dates_1 = require("app/utils/dates");
const getDate = date => date ? moment_1.default.utc(date).format(moment_1.default.HTML5_FMT.DATETIME_LOCAL_SECONDS) : null;
const ZoomPropKeys = [
    'period',
    'xAxis',
    'onChartReady',
    'onDataZoom',
    'onRestore',
    'onFinished',
];
/**
 * This is a very opinionated component that takes a render prop through `children`. It
 * will provide props to be passed to `BaseChart` to enable support of zooming without
 * eCharts' clunky zoom toolboxes.
 *
 * This also is very tightly coupled with the Global Selection Header. We can make it more
 * generic if need be in the future.
 */
class ChartZoom extends React.Component {
    constructor(props) {
        super(props);
        this.zooming = null;
        /**
         * Save current period state from period in props to be used
         * in handling chart's zoom history state
         */
        this.saveCurrentPeriod = props => {
            this.currentPeriod = {
                period: props.period,
                start: getDate(props.start),
                end: getDate(props.end),
            };
        };
        /**
         * Sets the new period due to a zoom related action
         *
         * Saves the current period to an instance property so that we
         * can control URL state when zoom history is being manipulated
         * by the chart controls.
         *
         * Saves a callback function to be called after chart animation is completed
         */
        this.setPeriod = ({ period, start, end }, saveHistory = false) => {
            const { router, onZoom, usePageDate } = this.props;
            const startFormatted = getDate(start);
            const endFormatted = getDate(end);
            // Save period so that we can revert back to it when using echarts "back" navigation
            if (saveHistory) {
                this.history.push(this.currentPeriod);
            }
            // Callback to let parent component know zoom has changed
            // This is required for some more perceived responsiveness since
            // we delay updating URL state so that chart animation can finish
            //
            // Parent container can use this to change into a loading state before
            // URL parameters are changed
            (0, callIfFunction_1.callIfFunction)(onZoom, {
                period,
                start: startFormatted,
                end: endFormatted,
            });
            this.zooming = () => {
                if (usePageDate && router) {
                    const newQuery = Object.assign(Object.assign({}, router.location.query), { pageStart: start ? (0, dates_1.getUtcDateString)(start) : undefined, pageEnd: end ? (0, dates_1.getUtcDateString)(end) : undefined, pageStatsPeriod: period !== null && period !== void 0 ? period : undefined });
                    // Only push new location if query params has changed because this will cause a heavy re-render
                    if (qs.stringify(newQuery) !== qs.stringify(router.location.query)) {
                        router.push({
                            pathname: router.location.pathname,
                            query: newQuery,
                        });
                    }
                }
                else {
                    (0, globalSelection_1.updateDateTime)({
                        period,
                        start: startFormatted
                            ? (0, dates_1.getUtcToLocalDateObject)(startFormatted)
                            : startFormatted,
                        end: endFormatted ? (0, dates_1.getUtcToLocalDateObject)(endFormatted) : endFormatted,
                    }, router);
                }
                this.saveCurrentPeriod({ period, start, end });
            };
        };
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
        /**
         * Restores the chart to initial viewport/zoom level
         *
         * Updates URL state to reflect initial params
         */
        this.handleZoomRestore = (evt, chart) => {
            if (!this.history.length) {
                return;
            }
            this.setPeriod(this.history[0]);
            // reset history
            this.history = [];
            (0, callIfFunction_1.callIfFunction)(this.props.onRestore, evt, chart);
        };
        this.handleDataZoom = (evt, chart) => {
            const model = chart.getModel();
            const { xAxis } = model.option;
            const axis = xAxis[0];
            // if `rangeStart` and `rangeEnd` are null, then we are going back
            if (axis.rangeStart === null && axis.rangeEnd === null) {
                const previousPeriod = this.history.pop();
                if (!previousPeriod) {
                    return;
                }
                this.setPeriod(previousPeriod);
            }
            else {
                const start = moment_1.default.utc(axis.rangeStart);
                // Add a day so we go until the end of the day (e.g. next day at midnight)
                const end = moment_1.default.utc(axis.rangeEnd);
                this.setPeriod({ period: null, start, end }, true);
            }
            (0, callIfFunction_1.callIfFunction)(this.props.onDataZoom, evt, chart);
        };
        /**
         * Chart event when *any* rendering+animation finishes
         *
         * `this.zooming` acts as a callback function so that
         * we can let the native zoom animation on the chart complete
         * before we update URL state and re-render
         */
        this.handleChartFinished = () => {
            if (typeof this.zooming === 'function') {
                this.zooming();
                this.zooming = null;
            }
            (0, callIfFunction_1.callIfFunction)(this.props.onFinished);
        };
        // Zoom history
        this.history = [];
        // Initialize current period instance state for zoom history
        this.saveCurrentPeriod(props);
    }
    componentDidUpdate() {
        if (this.props.disabled) {
            return;
        }
        // When component updates, make sure we sync current period state
        // for use in zoom history
        this.saveCurrentPeriod(this.props);
    }
    render() {
        const _a = this.props, { utc: _utc, start: _start, end: _end, disabled, children, xAxisIndex, router: _router, onZoom: _onZoom, onRestore: _onRestore, onChartReady: _onChartReady, onDataZoom: _onDataZoom, onFinished: _onFinished } = _a, props = (0, tslib_1.__rest)(_a, ["utc", "start", "end", "disabled", "children", "xAxisIndex", "router", "onZoom", "onRestore", "onChartReady", "onDataZoom", "onFinished"]);
        const utc = _utc !== null && _utc !== void 0 ? _utc : undefined;
        const start = _start ? (0, dates_1.getUtcToLocalDateObject)(_start) : undefined;
        const end = _end ? (0, dates_1.getUtcToLocalDateObject)(_end) : undefined;
        if (disabled) {
            return children(Object.assign({ utc,
                start,
                end }, props));
        }
        const renderProps = Object.assign({ 
            // Zooming only works when grouped by date
            isGroupedByDate: true, onChartReady: this.handleChartReady, utc,
            start,
            end, dataZoom: (0, dataZoomInside_1.default)({ xAxisIndex }), showTimeInTooltip: true, toolBox: (0, toolBox_1.default)({}, {
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
            }), onDataZoom: this.handleDataZoom, onFinished: this.handleChartFinished, onRestore: this.handleZoomRestore }, props);
        return children(renderProps);
    }
}
exports.default = ChartZoom;
//# sourceMappingURL=chartZoom.jsx.map