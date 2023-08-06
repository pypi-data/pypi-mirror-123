Object.defineProperty(exports, "__esModule", { value: true });
exports.Consumer = exports.Provider = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const utils_1 = require("app/components/performance/waterfall/utils");
const CursorGuideManagerContext = React.createContext({
    showCursorGuide: false,
    mouseLeft: void 0,
    traceViewMouseLeft: void 0,
    displayCursorGuide: () => { },
    hideCursorGuide: () => { },
});
class Provider extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            showCursorGuide: false,
            mouseLeft: void 0,
            traceViewMouseLeft: void 0,
        };
        this.hasInteractiveLayer = () => !!this.props.interactiveLayerRef.current;
        this.displayCursorGuide = (mousePageX) => {
            if (!this.hasInteractiveLayer()) {
                return;
            }
            const { trace, dragProps } = this.props;
            const interactiveLayer = this.props.interactiveLayerRef.current;
            const rect = (0, utils_1.rectOfContent)(interactiveLayer);
            // duration of the entire trace in seconds
            const traceDuration = trace.traceEndTimestamp - trace.traceStartTimestamp;
            const viewStart = dragProps.viewWindowStart;
            const viewEnd = dragProps.viewWindowEnd;
            const viewStartTimestamp = trace.traceStartTimestamp + viewStart * traceDuration;
            const viewEndTimestamp = trace.traceEndTimestamp - (1 - viewEnd) * traceDuration;
            const viewDuration = viewEndTimestamp - viewStartTimestamp;
            // clamp mouseLeft to be within [0, 1]
            const mouseLeft = (0, utils_1.clamp)((mousePageX - rect.x) / rect.width, 0, 1);
            const duration = mouseLeft * Math.abs(trace.traceEndTimestamp - trace.traceStartTimestamp);
            const startTimestamp = trace.traceStartTimestamp + duration;
            const start = (startTimestamp - viewStartTimestamp) / viewDuration;
            this.setState({
                showCursorGuide: true,
                mouseLeft,
                traceViewMouseLeft: start,
            });
        };
        this.hideCursorGuide = () => {
            if (!this.hasInteractiveLayer()) {
                return;
            }
            this.setState({
                showCursorGuide: false,
                mouseLeft: void 0,
                traceViewMouseLeft: void 0,
            });
        };
    }
    render() {
        const childrenProps = {
            showCursorGuide: this.state.showCursorGuide,
            mouseLeft: this.state.mouseLeft,
            traceViewMouseLeft: this.state.traceViewMouseLeft,
            displayCursorGuide: this.displayCursorGuide,
            hideCursorGuide: this.hideCursorGuide,
        };
        return (<CursorGuideManagerContext.Provider value={childrenProps}>
        {this.props.children}
      </CursorGuideManagerContext.Provider>);
    }
}
exports.Provider = Provider;
exports.Consumer = CursorGuideManagerContext.Consumer;
//# sourceMappingURL=cursorGuideHandler.jsx.map