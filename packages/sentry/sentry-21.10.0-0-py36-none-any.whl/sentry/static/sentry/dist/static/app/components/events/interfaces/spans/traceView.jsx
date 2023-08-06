Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const mobx_react_1 = require("mobx-react");
const emptyStateWarning_1 = (0, tslib_1.__importDefault)(require("app/components/emptyStateWarning"));
const locale_1 = require("app/locale");
const CursorGuideHandler = (0, tslib_1.__importStar)(require("./cursorGuideHandler"));
const DividerHandlerManager = (0, tslib_1.__importStar)(require("./dividerHandlerManager"));
const dragManager_1 = (0, tslib_1.__importDefault)(require("./dragManager"));
const header_1 = (0, tslib_1.__importDefault)(require("./header"));
const ScrollbarManager = (0, tslib_1.__importStar)(require("./scrollbarManager"));
const spanTree_1 = (0, tslib_1.__importDefault)(require("./spanTree"));
const utils_1 = require("./utils");
class TraceView extends react_1.PureComponent {
    constructor() {
        super(...arguments);
        this.traceViewRef = (0, react_1.createRef)();
        this.virtualScrollBarContainerRef = (0, react_1.createRef)();
        this.minimapInteractiveRef = (0, react_1.createRef)();
        this.renderHeader = (dragProps) => (<mobx_react_1.Observer>
      {() => {
                const { waterfallModel } = this.props;
                return (<header_1.default organization={this.props.organization} minimapInteractiveRef={this.minimapInteractiveRef} dragProps={dragProps} trace={waterfallModel.parsedTrace} event={waterfallModel.event} virtualScrollBarContainerRef={this.virtualScrollBarContainerRef} operationNameFilters={waterfallModel.operationNameFilters} rootSpan={waterfallModel.rootSpan.span} spans={waterfallModel.getWaterfall({
                        viewStart: 0,
                        viewEnd: 1,
                    })} generateBounds={waterfallModel.generateBounds({
                        viewStart: 0,
                        viewEnd: 1,
                    })}/>);
            }}
    </mobx_react_1.Observer>);
    }
    render() {
        const { organization, waterfallModel } = this.props;
        if (!(0, utils_1.getTraceContext)(waterfallModel.event)) {
            return (<emptyStateWarning_1.default>
          <p>{(0, locale_1.t)('There is no trace for this transaction')}</p>
        </emptyStateWarning_1.default>);
        }
        return (<dragManager_1.default interactiveLayerRef={this.minimapInteractiveRef}>
        {(dragProps) => (<mobx_react_1.Observer>
            {() => {
                    const parsedTrace = waterfallModel.parsedTrace;
                    return (<CursorGuideHandler.Provider interactiveLayerRef={this.minimapInteractiveRef} dragProps={dragProps} trace={parsedTrace}>
                  <DividerHandlerManager.Provider interactiveLayerRef={this.traceViewRef}>
                    <DividerHandlerManager.Consumer>
                      {dividerHandlerChildrenProps => {
                            return (<ScrollbarManager.Provider dividerPosition={dividerHandlerChildrenProps.dividerPosition} interactiveLayerRef={this.virtualScrollBarContainerRef} dragProps={dragProps}>
                            {this.renderHeader(dragProps)}
                            <mobx_react_1.Observer>
                              {() => {
                                    return (<spanTree_1.default traceViewRef={this.traceViewRef} dragProps={dragProps} organization={organization} waterfallModel={waterfallModel} filterSpans={waterfallModel.filterSpans} spans={waterfallModel.getWaterfall({
                                            viewStart: dragProps.viewWindowStart,
                                            viewEnd: dragProps.viewWindowEnd,
                                        })}/>);
                                }}
                            </mobx_react_1.Observer>
                          </ScrollbarManager.Provider>);
                        }}
                    </DividerHandlerManager.Consumer>
                  </DividerHandlerManager.Provider>
                </CursorGuideHandler.Provider>);
                }}
          </mobx_react_1.Observer>)}
      </dragManager_1.default>);
    }
}
exports.default = TraceView;
//# sourceMappingURL=traceView.jsx.map