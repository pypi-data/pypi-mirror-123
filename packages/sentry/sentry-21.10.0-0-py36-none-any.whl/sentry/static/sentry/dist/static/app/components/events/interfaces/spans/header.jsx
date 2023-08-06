Object.defineProperty(exports, "__esModule", { value: true });
exports.SecondaryHeader = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const opsBreakdown_1 = (0, tslib_1.__importDefault)(require("app/components/events/opsBreakdown"));
const miniHeader_1 = require("app/components/performance/waterfall/miniHeader");
const utils_1 = require("app/components/performance/waterfall/utils");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const constants_1 = require("./constants");
const CursorGuideHandler = (0, tslib_1.__importStar)(require("./cursorGuideHandler"));
const DividerHandlerManager = (0, tslib_1.__importStar)(require("./dividerHandlerManager"));
const measurementsPanel_1 = (0, tslib_1.__importDefault)(require("./measurementsPanel"));
const ScrollbarManager = (0, tslib_1.__importStar)(require("./scrollbarManager"));
const types_1 = require("./types");
const utils_2 = require("./utils");
class TraceViewHeader extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            minimapWidth: undefined,
        };
    }
    componentDidMount() {
        this.fetchMinimapWidth();
    }
    componentDidUpdate() {
        this.fetchMinimapWidth();
    }
    fetchMinimapWidth() {
        const { minimapInteractiveRef } = this.props;
        if (minimapInteractiveRef.current) {
            const minimapWidth = minimapInteractiveRef.current.getBoundingClientRect().width;
            if (minimapWidth !== this.state.minimapWidth) {
                // eslint-disable-next-line react/no-did-update-set-state
                this.setState({
                    minimapWidth,
                });
            }
        }
    }
    renderCursorGuide({ cursorGuideHeight, showCursorGuide, mouseLeft, }) {
        if (!showCursorGuide || !mouseLeft) {
            return null;
        }
        return (<CursorGuide style={{
                left: (0, utils_1.toPercent)(mouseLeft),
                height: `${cursorGuideHeight}px`,
            }}/>);
    }
    renderViewHandles({ isDragging, onLeftHandleDragStart, leftHandlePosition, onRightHandleDragStart, rightHandlePosition, viewWindowStart, viewWindowEnd, }) {
        const leftHandleGhost = isDragging ? (<Handle left={viewWindowStart} onMouseDown={() => {
                // do nothing
            }} isDragging={false}/>) : null;
        const leftHandle = (<Handle left={leftHandlePosition} onMouseDown={onLeftHandleDragStart} isDragging={isDragging}/>);
        const rightHandle = (<Handle left={rightHandlePosition} onMouseDown={onRightHandleDragStart} isDragging={isDragging}/>);
        const rightHandleGhost = isDragging ? (<Handle left={viewWindowEnd} onMouseDown={() => {
                // do nothing
            }} isDragging={false}/>) : null;
        return (<React.Fragment>
        {leftHandleGhost}
        {rightHandleGhost}
        {leftHandle}
        {rightHandle}
      </React.Fragment>);
    }
    renderFog(dragProps) {
        return (<React.Fragment>
        <Fog style={{ height: '100%', width: (0, utils_1.toPercent)(dragProps.viewWindowStart) }}/>
        <Fog style={{
                height: '100%',
                width: (0, utils_1.toPercent)(1 - dragProps.viewWindowEnd),
                left: (0, utils_1.toPercent)(dragProps.viewWindowEnd),
            }}/>
      </React.Fragment>);
    }
    renderDurationGuide({ showCursorGuide, mouseLeft, }) {
        if (!showCursorGuide || !mouseLeft) {
            return null;
        }
        const interactiveLayer = this.props.minimapInteractiveRef.current;
        if (!interactiveLayer) {
            return null;
        }
        const rect = (0, utils_1.rectOfContent)(interactiveLayer);
        const { trace } = this.props;
        const duration = mouseLeft * Math.abs(trace.traceEndTimestamp - trace.traceStartTimestamp);
        const style = { top: 0, left: `calc(${mouseLeft * 100}% + 4px)` };
        const alignLeft = (1 - mouseLeft) * rect.width <= 100;
        return (<DurationGuideBox style={style} alignLeft={alignLeft}>
        <span>{(0, utils_1.getHumanDuration)(duration)}</span>
      </DurationGuideBox>);
    }
    renderTicks() {
        const { trace } = this.props;
        const { minimapWidth } = this.state;
        const duration = Math.abs(trace.traceEndTimestamp - trace.traceStartTimestamp);
        let numberOfParts = 5;
        if (minimapWidth) {
            if (minimapWidth <= 350) {
                numberOfParts = 4;
            }
            if (minimapWidth <= 280) {
                numberOfParts = 3;
            }
            if (minimapWidth <= 160) {
                numberOfParts = 2;
            }
            if (minimapWidth <= 130) {
                numberOfParts = 1;
            }
        }
        if (numberOfParts === 1) {
            return (<TickLabel key="1" duration={duration * 0.5} style={{
                    left: (0, utils_1.toPercent)(0.5),
                }}/>);
        }
        const segment = 1 / (numberOfParts - 1);
        const ticks = [];
        for (let currentPart = 0; currentPart < numberOfParts; currentPart++) {
            if (currentPart === 0) {
                ticks.push(<TickLabel key="first" align={types_1.TickAlignment.Left} hideTickMarker duration={0} style={{
                        left: (0, space_1.default)(1),
                    }}/>);
                continue;
            }
            if (currentPart === numberOfParts - 1) {
                ticks.push(<TickLabel key="last" duration={duration} align={types_1.TickAlignment.Right} hideTickMarker style={{
                        right: (0, space_1.default)(1),
                    }}/>);
                continue;
            }
            const progress = segment * currentPart;
            ticks.push(<TickLabel key={String(currentPart)} duration={duration * progress} style={{
                    left: (0, utils_1.toPercent)(progress),
                }}/>);
        }
        return ticks;
    }
    renderTimeAxis({ showCursorGuide, mouseLeft, }) {
        return (<TimeAxis>
        {this.renderTicks()}
        {this.renderCursorGuide({
                showCursorGuide,
                mouseLeft,
                cursorGuideHeight: constants_1.TIME_AXIS_HEIGHT,
            })}
        {this.renderDurationGuide({
                showCursorGuide,
                mouseLeft,
            })}
      </TimeAxis>);
    }
    renderWindowSelection(dragProps) {
        if (!dragProps.isWindowSelectionDragging) {
            return null;
        }
        const left = Math.min(dragProps.windowSelectionInitial, dragProps.windowSelectionCurrent);
        return (<WindowSelection style={{
                left: (0, utils_1.toPercent)(left),
                width: (0, utils_1.toPercent)(dragProps.windowSelectionSize),
            }}/>);
    }
    generateBounds() {
        const { dragProps, trace } = this.props;
        return (0, utils_2.boundsGenerator)({
            traceStartTimestamp: trace.traceStartTimestamp,
            traceEndTimestamp: trace.traceEndTimestamp,
            viewStart: dragProps.viewWindowStart,
            viewEnd: dragProps.viewWindowEnd,
        });
    }
    renderSecondaryHeader() {
        var _a;
        const { event } = this.props;
        const hasMeasurements = Object.keys((_a = event.measurements) !== null && _a !== void 0 ? _a : {}).length > 0;
        return (<DividerHandlerManager.Consumer>
        {dividerHandlerChildrenProps => {
                const { dividerPosition } = dividerHandlerChildrenProps;
                return (<exports.SecondaryHeader>
              <ScrollbarManager.Consumer>
                {({ virtualScrollbarRef, scrollBarAreaRef, onDragStart, onScroll }) => {
                        return (<miniHeader_1.ScrollbarContainer ref={this.props.virtualScrollBarContainerRef} style={{
                                // the width of this component is shrunk to compensate for half of the width of the divider line
                                width: `calc(${(0, utils_1.toPercent)(dividerPosition)} - 0.5px)`,
                            }} onScroll={onScroll}>
                      <div style={{
                                width: 0,
                                height: '1px',
                            }} ref={scrollBarAreaRef}/>
                      <miniHeader_1.VirtualScrollbar data-type="virtual-scrollbar" ref={virtualScrollbarRef} onMouseDown={onDragStart}>
                        <miniHeader_1.VirtualScrollbarGrip />
                      </miniHeader_1.VirtualScrollbar>
                    </miniHeader_1.ScrollbarContainer>);
                    }}
              </ScrollbarManager.Consumer>
              <miniHeader_1.DividerSpacer />
              {hasMeasurements ? (<measurementsPanel_1.default event={event} generateBounds={this.generateBounds()} dividerPosition={dividerPosition}/>) : null}
            </exports.SecondaryHeader>);
            }}
      </DividerHandlerManager.Consumer>);
    }
    render() {
        return (<HeaderContainer>
        <DividerHandlerManager.Consumer>
          {dividerHandlerChildrenProps => {
                const { dividerPosition } = dividerHandlerChildrenProps;
                return (<React.Fragment>
                <OperationsBreakdown style={{
                        width: `calc(${(0, utils_1.toPercent)(dividerPosition)} - 0.5px)`,
                    }}>
                  {this.props.event && (<opsBreakdown_1.default operationNameFilters={this.props.operationNameFilters} event={this.props.event} topN={3} hideHeader/>)}
                </OperationsBreakdown>
                <miniHeader_1.DividerSpacer style={{
                        position: 'absolute',
                        top: 0,
                        left: `calc(${(0, utils_1.toPercent)(dividerPosition)} - 0.5px)`,
                        height: `${constants_1.MINIMAP_HEIGHT + constants_1.TIME_AXIS_HEIGHT}px`,
                    }}/>
                <ActualMinimap spans={this.props.spans} generateBounds={this.props.generateBounds} dividerPosition={dividerPosition} rootSpan={this.props.rootSpan}/>
                <CursorGuideHandler.Consumer>
                  {({ displayCursorGuide, hideCursorGuide, mouseLeft, showCursorGuide, }) => (<RightSidePane ref={this.props.minimapInteractiveRef} style={{
                            width: `calc(${(0, utils_1.toPercent)(1 - dividerPosition)} - 0.5px)`,
                            left: `calc(${(0, utils_1.toPercent)(dividerPosition)} + 0.5px)`,
                        }} onMouseEnter={event => {
                            displayCursorGuide(event.pageX);
                        }} onMouseLeave={() => {
                            hideCursorGuide();
                        }} onMouseMove={event => {
                            displayCursorGuide(event.pageX);
                        }} onMouseDown={event => {
                            const target = event.target;
                            if (target instanceof Element &&
                                target.getAttribute &&
                                target.getAttribute('data-ignore')) {
                                // ignore this event if we need to
                                return;
                            }
                            this.props.dragProps.onWindowSelectionDragStart(event);
                        }}>
                      <MinimapContainer>
                        {this.renderFog(this.props.dragProps)}
                        {this.renderCursorGuide({
                            showCursorGuide,
                            mouseLeft,
                            cursorGuideHeight: constants_1.MINIMAP_HEIGHT,
                        })}
                        {this.renderViewHandles(this.props.dragProps)}
                        {this.renderWindowSelection(this.props.dragProps)}
                      </MinimapContainer>
                      {this.renderTimeAxis({
                            showCursorGuide,
                            mouseLeft,
                        })}
                    </RightSidePane>)}
                </CursorGuideHandler.Consumer>
                {this.renderSecondaryHeader()}
              </React.Fragment>);
            }}
        </DividerHandlerManager.Consumer>
      </HeaderContainer>);
    }
}
class ActualMinimap extends React.PureComponent {
    renderRootSpan() {
        const { spans, generateBounds } = this.props;
        return spans.map(payload => {
            switch (payload.type) {
                case 'root_span':
                case 'span':
                case 'span_group_chain': {
                    const { span } = payload;
                    const spanBarColor = (0, utils_1.pickBarColor)((0, utils_2.getSpanOperation)(span));
                    const bounds = generateBounds({
                        startTimestamp: span.start_timestamp,
                        endTimestamp: span.timestamp,
                    });
                    const { left: spanLeft, width: spanWidth } = this.getBounds(bounds);
                    return (<MinimapSpanBar style={{
                            backgroundColor: payload.type === 'span_group_chain' ? theme_1.default.blue300 : spanBarColor,
                            left: spanLeft,
                            width: spanWidth,
                        }}/>);
                }
                default: {
                    return null;
                }
            }
        });
    }
    getBounds(bounds) {
        switch (bounds.type) {
            case 'TRACE_TIMESTAMPS_EQUAL':
            case 'INVALID_VIEW_WINDOW': {
                return {
                    left: (0, utils_1.toPercent)(0),
                    width: '0px',
                };
            }
            case 'TIMESTAMPS_EQUAL': {
                return {
                    left: (0, utils_1.toPercent)(bounds.start),
                    width: `${bounds.width}px`,
                };
            }
            case 'TIMESTAMPS_REVERSED':
            case 'TIMESTAMPS_STABLE': {
                return {
                    left: (0, utils_1.toPercent)(bounds.start),
                    width: (0, utils_1.toPercent)(bounds.end - bounds.start),
                };
            }
            default: {
                const _exhaustiveCheck = bounds;
                return _exhaustiveCheck;
            }
        }
    }
    render() {
        const { dividerPosition } = this.props;
        return (<MinimapBackground style={{
                // the width of this component is shrunk to compensate for half of the width of the divider line
                width: `calc(${(0, utils_1.toPercent)(1 - dividerPosition)} - 0.5px)`,
                left: `calc(${(0, utils_1.toPercent)(dividerPosition)} + 0.5px)`,
            }}>
        <BackgroundSlider id="minimap-background-slider">
          {this.renderRootSpan()}
        </BackgroundSlider>
      </MinimapBackground>);
    }
}
const TimeAxis = (0, styled_1.default)('div') `
  width: 100%;
  position: absolute;
  left: 0;
  top: ${constants_1.MINIMAP_HEIGHT}px;
  border-top: 1px solid ${p => p.theme.border};
  height: ${constants_1.TIME_AXIS_HEIGHT}px;
  background-color: ${p => p.theme.background};
  color: ${p => p.theme.gray300};
  font-size: 10px;
  font-weight: 500;
  font-variant-numeric: tabular-nums;
  overflow: hidden;
`;
const TickLabelContainer = (0, styled_1.default)('div') `
  height: ${constants_1.TIME_AXIS_HEIGHT}px;
  position: absolute;
  top: 0;
  display: flex;
  align-items: center;
  user-select: none;
`;
const TickText = (0, styled_1.default)('span') `
  position: absolute;
  line-height: 1;
  white-space: nowrap;

  ${({ align }) => {
    switch (align) {
        case types_1.TickAlignment.Center: {
            return 'transform: translateX(-50%)';
        }
        case types_1.TickAlignment.Left: {
            return null;
        }
        case types_1.TickAlignment.Right: {
            return 'transform: translateX(-100%)';
        }
        default: {
            throw Error(`Invalid tick alignment: ${align}`);
        }
    }
}};
`;
const TickMarker = (0, styled_1.default)('div') `
  width: 1px;
  height: 4px;
  background-color: ${p => p.theme.gray200};
  position: absolute;
  top: 0;
  left: 0;
  transform: translateX(-50%);
`;
const TickLabel = (props) => {
    const { style, duration, hideTickMarker = false, align = types_1.TickAlignment.Center } = props;
    return (<TickLabelContainer style={style}>
      {hideTickMarker ? null : <TickMarker />}
      <TickText align={align}>{(0, utils_1.getHumanDuration)(duration)}</TickText>
    </TickLabelContainer>);
};
const DurationGuideBox = (0, styled_1.default)('div') `
  position: absolute;
  background-color: ${p => p.theme.background};
  padding: 4px;
  height: 100%;
  border-radius: 3px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  line-height: 1;
  white-space: nowrap;

  ${({ alignLeft }) => {
    if (!alignLeft) {
        return null;
    }
    return 'transform: translateX(-100%) translateX(-8px);';
}};
`;
const HeaderContainer = (0, styled_1.default)('div') `
  width: 100%;
  position: sticky;
  left: 0;
  top: ${p => (configStore_1.default.get('demoMode') ? p.theme.demo.headerSize : 0)};
  z-index: ${p => p.theme.zIndex.traceView.minimapContainer};
  background-color: ${p => p.theme.background};
  border-bottom: 1px solid ${p => p.theme.border};
  height: ${constants_1.MINIMAP_CONTAINER_HEIGHT}px;
  border-top-left-radius: ${p => p.theme.borderRadius};
  border-top-right-radius: ${p => p.theme.borderRadius};
`;
const MinimapBackground = (0, styled_1.default)('div') `
  height: ${constants_1.MINIMAP_HEIGHT}px;
  max-height: ${constants_1.MINIMAP_HEIGHT}px;
  overflow: hidden;
  position: absolute;
  top: 0;
`;
const MinimapContainer = (0, styled_1.default)('div') `
  height: ${constants_1.MINIMAP_HEIGHT}px;
  width: 100%;
  position: relative;
  left: 0;
`;
const ViewHandleContainer = (0, styled_1.default)('div') `
  position: absolute;
  top: 0;
  height: ${constants_1.MINIMAP_HEIGHT}px;
`;
const ViewHandleLine = (0, styled_1.default)('div') `
  height: ${constants_1.MINIMAP_HEIGHT - constants_1.VIEW_HANDLE_HEIGHT}px;
  width: 2px;
  background-color: ${p => p.theme.textColor};
`;
const ViewHandle = (0, styled_1.default)('div') `
  position: absolute;
  background-color: ${p => p.theme.textColor};
  cursor: col-resize;
  width: 8px;
  height: ${constants_1.VIEW_HANDLE_HEIGHT}px;
  bottom: 0;
  left: -3px;
`;
const Fog = (0, styled_1.default)('div') `
  background-color: ${p => p.theme.textColor};
  opacity: 0.1;
  position: absolute;
  top: 0;
`;
const MinimapSpanBar = (0, styled_1.default)('div') `
  position: relative;
  height: 2px;
  min-height: 2px;
  max-height: 2px;
  margin: 2px 0;
  min-width: 1px;
  border-radius: 1px;
  box-sizing: border-box;
`;
const BackgroundSlider = (0, styled_1.default)('div') `
  position: relative;
`;
const CursorGuide = (0, styled_1.default)('div') `
  position: absolute;
  top: 0;
  width: 1px;
  background-color: ${p => p.theme.red300};
  transform: translateX(-50%);
`;
const Handle = ({ left, onMouseDown, isDragging, }) => (<ViewHandleContainer style={{
        left: (0, utils_1.toPercent)(left),
    }}>
    <ViewHandleLine />
    <ViewHandle data-ignore="true" onMouseDown={onMouseDown} isDragging={isDragging} style={{
        height: `${constants_1.VIEW_HANDLE_HEIGHT}px`,
    }}/>
  </ViewHandleContainer>);
const WindowSelection = (0, styled_1.default)('div') `
  position: absolute;
  top: 0;
  height: ${constants_1.MINIMAP_HEIGHT}px;
  background-color: ${p => p.theme.textColor};
  opacity: 0.1;
`;
exports.SecondaryHeader = (0, styled_1.default)('div') `
  position: absolute;
  top: ${constants_1.MINIMAP_HEIGHT + constants_1.TIME_AXIS_HEIGHT}px;
  left: 0;
  height: ${constants_1.TIME_AXIS_HEIGHT}px;
  width: 100%;
  background-color: ${p => p.theme.backgroundSecondary};
  display: flex;
  border-top: 1px solid ${p => p.theme.border};
  overflow: hidden;
`;
const OperationsBreakdown = (0, styled_1.default)('div') `
  height: ${constants_1.MINIMAP_HEIGHT + constants_1.TIME_AXIS_HEIGHT}px;
  position: absolute;
  left: 0;
  top: 0;
  overflow: hidden;
`;
const RightSidePane = (0, styled_1.default)('div') `
  height: ${constants_1.MINIMAP_HEIGHT + constants_1.TIME_AXIS_HEIGHT}px;
  position: absolute;
  top: 0;
`;
exports.default = TraceViewHeader;
//# sourceMappingURL=header.jsx.map