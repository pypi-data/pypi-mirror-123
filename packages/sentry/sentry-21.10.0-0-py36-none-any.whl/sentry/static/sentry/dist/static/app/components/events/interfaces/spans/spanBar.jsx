Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
require("intersection-observer"); // this is a polyfill
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const count_1 = (0, tslib_1.__importDefault)(require("app/components/count"));
const featureBadge_1 = (0, tslib_1.__importDefault)(require("app/components/featureBadge"));
const constants_1 = require("app/components/performance/waterfall/constants");
const messageRow_1 = require("app/components/performance/waterfall/messageRow");
const row_1 = require("app/components/performance/waterfall/row");
const rowBar_1 = require("app/components/performance/waterfall/rowBar");
const rowDivider_1 = require("app/components/performance/waterfall/rowDivider");
const rowTitle_1 = require("app/components/performance/waterfall/rowTitle");
const treeConnector_1 = require("app/components/performance/waterfall/treeConnector");
const utils_1 = require("app/components/performance/waterfall/utils");
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_2 = require("app/utils");
const analytics_1 = require("app/utils/analytics");
const urls_1 = require("app/utils/discover/urls");
const QuickTraceContext = (0, tslib_1.__importStar)(require("app/utils/performance/quickTrace/quickTraceContext"));
const utils_3 = require("app/utils/performance/quickTrace/utils");
const AnchorLinkManager = (0, tslib_1.__importStar)(require("./anchorLinkManager"));
const constants_2 = require("./constants");
const DividerHandlerManager = (0, tslib_1.__importStar)(require("./dividerHandlerManager"));
const ScrollbarManager = (0, tslib_1.__importStar)(require("./scrollbarManager"));
const spanBarCursorGuide_1 = (0, tslib_1.__importDefault)(require("./spanBarCursorGuide"));
const spanDetail_1 = (0, tslib_1.__importDefault)(require("./spanDetail"));
const styles_1 = require("./styles");
const utils_4 = require("./utils");
// TODO: maybe use babel-plugin-preval
// for (let i = 0; i <= 1.0; i += 0.01) {
//   INTERSECTION_THRESHOLDS.push(i);
// }
const INTERSECTION_THRESHOLDS = [
    0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14,
    0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29,
    0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44,
    0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, 0.52, 0.53, 0.54, 0.55, 0.56, 0.57, 0.58, 0.59,
    0.6, 0.61, 0.62, 0.63, 0.64, 0.65, 0.66, 0.67, 0.68, 0.69, 0.7, 0.71, 0.72, 0.73, 0.74,
    0.75, 0.76, 0.77, 0.78, 0.79, 0.8, 0.81, 0.82, 0.83, 0.84, 0.85, 0.86, 0.87, 0.88, 0.89,
    0.9, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99, 1.0,
];
const MARGIN_LEFT = 0;
class SpanBar extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            showDetail: false,
        };
        this.spanRowDOMRef = React.createRef();
        this.intersectionObserver = void 0;
        this.zoomLevel = 1; // assume initial zoomLevel is 100%
        this._mounted = false;
        this.toggleDisplayDetail = () => {
            this.setState(state => ({
                showDetail: !state.showDetail,
            }));
        };
        this.scrollIntoView = () => {
            const element = this.spanRowDOMRef.current;
            if (!element) {
                return;
            }
            const boundingRect = element.getBoundingClientRect();
            const offset = boundingRect.top + window.scrollY - constants_2.MINIMAP_CONTAINER_HEIGHT;
            this.setState({ showDetail: true }, () => window.scrollTo(0, offset));
        };
    }
    componentDidMount() {
        this._mounted = true;
        if (this.spanRowDOMRef.current) {
            this.connectObservers();
        }
    }
    componentWillUnmount() {
        this._mounted = false;
        this.disconnectObservers();
    }
    renderDetail({ isVisible, transactions, errors, }) {
        const { span, organization, isRoot, trace, event } = this.props;
        return (<AnchorLinkManager.Consumer>
        {({ registerScrollFn, scrollToHash }) => {
                if (!(0, utils_4.isGapSpan)(span)) {
                    registerScrollFn(`#span-${span.span_id}`, this.scrollIntoView);
                }
                if (!this.state.showDetail || !isVisible) {
                    return null;
                }
                return (<spanDetail_1.default span={span} organization={organization} event={event} isRoot={!!isRoot} trace={trace} childTransactions={transactions} relatedErrors={errors} scrollToHash={scrollToHash}/>);
            }}
      </AnchorLinkManager.Consumer>);
    }
    getBounds() {
        const { event, span, generateBounds } = this.props;
        const bounds = generateBounds({
            startTimestamp: span.start_timestamp,
            endTimestamp: span.timestamp,
        });
        const shouldHideSpanWarnings = (0, utils_4.isEventFromBrowserJavaScriptSDK)(event);
        switch (bounds.type) {
            case 'TRACE_TIMESTAMPS_EQUAL': {
                return {
                    warning: (0, locale_1.t)('Trace times are equal'),
                    left: void 0,
                    width: void 0,
                    isSpanVisibleInView: bounds.isSpanVisibleInView,
                };
            }
            case 'INVALID_VIEW_WINDOW': {
                return {
                    warning: (0, locale_1.t)('Invalid view window'),
                    left: void 0,
                    width: void 0,
                    isSpanVisibleInView: bounds.isSpanVisibleInView,
                };
            }
            case 'TIMESTAMPS_EQUAL': {
                const warning = shouldHideSpanWarnings &&
                    'op' in span &&
                    span.op &&
                    utils_4.durationlessBrowserOps.includes(span.op)
                    ? void 0
                    : (0, locale_1.t)('Equal start and end times');
                return {
                    warning,
                    left: bounds.start,
                    width: 0.00001,
                    isSpanVisibleInView: bounds.isSpanVisibleInView,
                };
            }
            case 'TIMESTAMPS_REVERSED': {
                return {
                    warning: (0, locale_1.t)('Reversed start and end times'),
                    left: bounds.start,
                    width: bounds.end - bounds.start,
                    isSpanVisibleInView: bounds.isSpanVisibleInView,
                };
            }
            case 'TIMESTAMPS_STABLE': {
                return {
                    warning: void 0,
                    left: bounds.start,
                    width: bounds.end - bounds.start,
                    isSpanVisibleInView: bounds.isSpanVisibleInView,
                };
            }
            default: {
                const _exhaustiveCheck = bounds;
                return _exhaustiveCheck;
            }
        }
    }
    renderMeasurements() {
        const { event, generateBounds } = this.props;
        if (this.state.showDetail) {
            return null;
        }
        const measurements = (0, utils_4.getMeasurements)(event);
        return (<React.Fragment>
        {Array.from(measurements).map(([timestamp, verticalMark]) => {
                const bounds = (0, utils_4.getMeasurementBounds)(timestamp, generateBounds);
                const shouldDisplay = (0, utils_2.defined)(bounds.left) && (0, utils_2.defined)(bounds.width);
                if (!shouldDisplay || !bounds.isSpanVisibleInView) {
                    return null;
                }
                return (<styles_1.MeasurementMarker key={String(timestamp)} style={{
                        left: `clamp(0%, ${(0, utils_1.toPercent)(bounds.left || 0)}, calc(100% - 1px))`,
                    }} failedThreshold={verticalMark.failedThreshold}/>);
            })}
      </React.Fragment>);
    }
    renderSpanTreeConnector({ hasToggler }) {
        const { isLast, isRoot, treeDepth: spanTreeDepth, continuingTreeDepths, span, showSpanTree, } = this.props;
        const spanID = (0, utils_4.getSpanID)(span);
        if (isRoot) {
            if (hasToggler) {
                return (<treeConnector_1.ConnectorBar style={{ right: '16px', height: '10px', bottom: '-5px', top: 'auto' }} key={`${spanID}-last`} orphanBranch={false}/>);
            }
            return null;
        }
        const connectorBars = continuingTreeDepths.map(treeDepth => {
            const depth = (0, utils_4.unwrapTreeDepth)(treeDepth);
            if (depth === 0) {
                // do not render a connector bar at depth 0,
                // if we did render a connector bar, this bar would be placed at depth -1
                // which does not exist.
                return null;
            }
            const left = ((spanTreeDepth - depth) * (treeConnector_1.TOGGLE_BORDER_BOX / 2) + 1) * -1;
            return (<treeConnector_1.ConnectorBar style={{ left }} key={`${spanID}-${depth}`} orphanBranch={(0, utils_4.isOrphanTreeDepth)(treeDepth)}/>);
        });
        if (hasToggler && showSpanTree) {
            // if there is a toggle button, we add a connector bar to create an attachment
            // between the toggle button and any connector bars below the toggle button
            connectorBars.push(<treeConnector_1.ConnectorBar style={{
                    right: '16px',
                    height: `${constants_1.ROW_HEIGHT / 2}px`,
                    bottom: isLast ? `-${constants_1.ROW_HEIGHT / 2}px` : '0',
                    top: 'auto',
                }} key={`${spanID}-last-bottom`} orphanBranch={false}/>);
        }
        return (<treeConnector_1.TreeConnector isLast={isLast} hasToggler={hasToggler} orphanBranch={(0, utils_4.isOrphanSpan)(span)}>
        {connectorBars}
      </treeConnector_1.TreeConnector>);
    }
    renderSpanTreeToggler({ left, errored }) {
        const { numOfSpanChildren, isRoot, showSpanTree } = this.props;
        const chevron = <treeConnector_1.TreeToggleIcon direction={showSpanTree ? 'up' : 'down'}/>;
        if (numOfSpanChildren <= 0) {
            return (<treeConnector_1.TreeToggleContainer style={{ left: `${left}px` }}>
          {this.renderSpanTreeConnector({ hasToggler: false })}
        </treeConnector_1.TreeToggleContainer>);
        }
        const chevronElement = !isRoot ? <div>{chevron}</div> : null;
        return (<treeConnector_1.TreeToggleContainer style={{ left: `${left}px` }} hasToggler>
        {this.renderSpanTreeConnector({ hasToggler: true })}
        <treeConnector_1.TreeToggle disabled={!!isRoot} isExpanded={showSpanTree} errored={errored} onClick={event => {
                event.stopPropagation();
                if (isRoot) {
                    return;
                }
                this.props.toggleSpanTree();
            }}>
          <count_1.default value={numOfSpanChildren}/>
          {chevronElement}
        </treeConnector_1.TreeToggle>
      </treeConnector_1.TreeToggleContainer>);
    }
    renderTitle(scrollbarManagerChildrenProps, errors) {
        var _a;
        const { generateContentSpanBarRef } = scrollbarManagerChildrenProps;
        const { span, treeDepth, toggleSpanGroup } = this.props;
        let titleFragments = [];
        if (typeof toggleSpanGroup === 'function') {
            titleFragments.push(<Regroup onClick={event => {
                    event.stopPropagation();
                    event.preventDefault();
                    toggleSpanGroup();
                }}>
          <a href="#regroup" onClick={event => {
                    event.preventDefault();
                }}>
            {(0, locale_1.t)('Regroup')}
          </a>
        </Regroup>);
        }
        const spanOperationName = (0, utils_4.getSpanOperation)(span);
        if (spanOperationName) {
            titleFragments.push(spanOperationName);
        }
        titleFragments = titleFragments.flatMap(current => [current, ' \u2014 ']);
        const description = (_a = span === null || span === void 0 ? void 0 : span.description) !== null && _a !== void 0 ? _a : (0, utils_4.getSpanID)(span);
        const left = treeDepth * (treeConnector_1.TOGGLE_BORDER_BOX / 2) + MARGIN_LEFT;
        const errored = Boolean(errors && errors.length > 0);
        return (<rowTitle_1.RowTitleContainer data-debug-id="SpanBarTitleContainer" ref={generateContentSpanBarRef()}>
        {this.renderSpanTreeToggler({ left, errored })}
        <rowTitle_1.RowTitle style={{
                left: `${left}px`,
                width: '100%',
            }}>
          <rowTitle_1.RowTitleContent errored={errored}>
            <strong>{titleFragments}</strong>
            {description}
          </rowTitle_1.RowTitleContent>
        </rowTitle_1.RowTitle>
      </rowTitle_1.RowTitleContainer>);
    }
    connectObservers() {
        if (!this.spanRowDOMRef.current) {
            return;
        }
        this.disconnectObservers();
        /**
    
        We track intersections events between the span bar's DOM element
        and the viewport's (root) intersection area. the intersection area is sized to
        exclude the minimap. See below.
    
        By default, the intersection observer's root intersection is the viewport.
        We adjust the margins of this root intersection area to exclude the minimap's
        height. The minimap's height is always fixed.
    
          VIEWPORT (ancestor element used for the intersection events)
        +--+-------------------------+--+
        |  |                         |  |
        |  |       MINIMAP           |  |
        |  |                         |  |
        |  +-------------------------+  |  ^
        |  |                         |  |  |
        |  |       SPANS             |  |  | ROOT
        |  |                         |  |  | INTERSECTION
        |  |                         |  |  | OBSERVER
        |  |                         |  |  | HEIGHT
        |  |                         |  |  |
        |  |                         |  |  |
        |  |                         |  |  |
        |  +-------------------------+  |  |
        |                               |  |
        +-------------------------------+  v
    
         */
        this.intersectionObserver = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (!this._mounted) {
                    return;
                }
                const shouldMoveMinimap = this.props.numOfSpans > constants_2.NUM_OF_SPANS_FIT_IN_MINI_MAP;
                if (!shouldMoveMinimap) {
                    return;
                }
                const spanNumber = this.props.spanNumber;
                const minimapSlider = document.getElementById('minimap-background-slider');
                if (!minimapSlider) {
                    return;
                }
                // NOTE: THIS IS HACKY.
                //
                // IntersectionObserver.rootMargin is un-affected by the browser's zoom level.
                // The margins of the intersection area needs to be adjusted.
                // Thus, IntersectionObserverEntry.rootBounds may not be what we expect.
                //
                // We address this below.
                //
                // Note that this function was called whenever an intersection event occurred wrt
                // the thresholds.
                //
                if (entry.rootBounds) {
                    // After we create the IntersectionObserver instance with rootMargin set as:
                    // -${MINIMAP_CONTAINER_HEIGHT * this.zoomLevel}px 0px 0px 0px
                    //
                    // we can introspect the rootBounds to infer the zoomlevel.
                    //
                    // we always expect entry.rootBounds.top to equal MINIMAP_CONTAINER_HEIGHT
                    const actualRootTop = Math.ceil(entry.rootBounds.top);
                    if (actualRootTop !== constants_2.MINIMAP_CONTAINER_HEIGHT && actualRootTop > 0) {
                        // we revert the actualRootTop value by the current zoomLevel factor
                        const normalizedActualTop = actualRootTop / this.zoomLevel;
                        const zoomLevel = constants_2.MINIMAP_CONTAINER_HEIGHT / normalizedActualTop;
                        this.zoomLevel = zoomLevel;
                        // we reconnect the observers; the callback functions may be invoked
                        this.connectObservers();
                        // NOTE: since we cannot guarantee that the callback function is invoked on
                        //       the newly connected observers, we continue running this function.
                    }
                }
                // root refers to the root intersection rectangle used for the IntersectionObserver
                const rectRelativeToRoot = entry.boundingClientRect;
                const bottomYCoord = rectRelativeToRoot.y + rectRelativeToRoot.height;
                // refers to if the rect is out of view from the viewport
                const isOutOfViewAbove = rectRelativeToRoot.y < 0 && bottomYCoord < 0;
                if (isOutOfViewAbove) {
                    return;
                }
                const relativeToMinimap = {
                    top: rectRelativeToRoot.y - constants_2.MINIMAP_CONTAINER_HEIGHT,
                    bottom: bottomYCoord - constants_2.MINIMAP_CONTAINER_HEIGHT,
                };
                const rectBelowMinimap = relativeToMinimap.top > 0 && relativeToMinimap.bottom > 0;
                if (rectBelowMinimap) {
                    // if the first span is below the minimap, we scroll the minimap
                    // to the top. this addresses spurious scrolling to the top of the page
                    if (spanNumber <= 1) {
                        minimapSlider.style.top = '0px';
                        return;
                    }
                    return;
                }
                const inAndAboveMinimap = relativeToMinimap.bottom <= 0;
                if (inAndAboveMinimap) {
                    return;
                }
                // invariant: spanNumber >= 1
                const numberOfMovedSpans = spanNumber - 1;
                const totalHeightOfHiddenSpans = numberOfMovedSpans * constants_2.MINIMAP_SPAN_BAR_HEIGHT;
                const currentSpanHiddenRatio = 1 - entry.intersectionRatio;
                const panYPixels = totalHeightOfHiddenSpans + currentSpanHiddenRatio * constants_2.MINIMAP_SPAN_BAR_HEIGHT;
                // invariant: this.props.numOfSpans - spanNumberToStopMoving + 1 = NUM_OF_SPANS_FIT_IN_MINI_MAP
                const spanNumberToStopMoving = this.props.numOfSpans + 1 - constants_2.NUM_OF_SPANS_FIT_IN_MINI_MAP;
                if (spanNumber > spanNumberToStopMoving) {
                    // if the last span bar appears on the minimap, we do not want the minimap
                    // to keep panning upwards
                    minimapSlider.style.top = `-${spanNumberToStopMoving * constants_2.MINIMAP_SPAN_BAR_HEIGHT}px`;
                    return;
                }
                minimapSlider.style.top = `-${panYPixels}px`;
            });
        }, {
            threshold: INTERSECTION_THRESHOLDS,
            rootMargin: `-${constants_2.MINIMAP_CONTAINER_HEIGHT * this.zoomLevel}px 0px 0px 0px`,
        });
        this.intersectionObserver.observe(this.spanRowDOMRef.current);
    }
    disconnectObservers() {
        if (this.intersectionObserver) {
            this.intersectionObserver.disconnect();
        }
    }
    renderDivider(dividerHandlerChildrenProps) {
        if (this.state.showDetail) {
            // Mock component to preserve layout spacing
            return (<rowDivider_1.DividerLine showDetail style={{
                    position: 'absolute',
                }}/>);
        }
        const { addDividerLineRef } = dividerHandlerChildrenProps;
        return (<rowDivider_1.DividerLine ref={addDividerLineRef()} style={{
                position: 'absolute',
            }} onMouseEnter={() => {
                dividerHandlerChildrenProps.setHover(true);
            }} onMouseLeave={() => {
                dividerHandlerChildrenProps.setHover(false);
            }} onMouseOver={() => {
                dividerHandlerChildrenProps.setHover(true);
            }} onMouseDown={dividerHandlerChildrenProps.onDragStart} onClick={event => {
                // we prevent the propagation of the clicks from this component to prevent
                // the span detail from being opened.
                event.stopPropagation();
            }}/>);
    }
    getRelatedErrors(quickTrace) {
        if (!quickTrace) {
            return null;
        }
        const { span } = this.props;
        const { currentEvent } = quickTrace;
        if ((0, utils_4.isGapSpan)(span) || !currentEvent || !(0, utils_3.isTraceFull)(currentEvent)) {
            return null;
        }
        return currentEvent.errors.filter(error => error.span === span.span_id);
    }
    getChildTransactions(quickTrace) {
        if (!quickTrace) {
            return null;
        }
        const { span } = this.props;
        const { trace } = quickTrace;
        if ((0, utils_4.isGapSpan)(span) || !trace) {
            return null;
        }
        return trace.filter(({ parent_span_id }) => parent_span_id === span.span_id);
    }
    renderErrorBadge(errors) {
        return (errors === null || errors === void 0 ? void 0 : errors.length) ? <rowDivider_1.ErrorBadge /> : null;
    }
    renderEmbeddedTransactionsBadge(transactions) {
        const { toggleEmbeddedChildren, organization, showEmbeddedChildren } = this.props;
        if (!organization.features.includes('unified-span-view')) {
            return null;
        }
        if (transactions && transactions.length === 1) {
            const transaction = transactions[0];
            return (<tooltip_1.default title={<span>
              {showEmbeddedChildren
                        ? (0, locale_1.t)('This span is showing a direct child. Remove transaction to hide')
                        : (0, locale_1.t)('This span has a direct child. Add transaction to view')}
              <featureBadge_1.default type="new" noTooltip/>
            </span>} position="top" containerDisplayMode="block">
          <rowDivider_1.EmbeddedTransactionBadge expanded={showEmbeddedChildren} onClick={() => {
                    if (toggleEmbeddedChildren) {
                        if (showEmbeddedChildren) {
                            (0, analytics_1.trackAnalyticsEvent)({
                                eventKey: 'span_view.embedded_child.hide',
                                eventName: 'Span View: Hide Embedded Transaction',
                                organization_id: parseInt(organization.id, 10),
                            });
                        }
                        else {
                            (0, analytics_1.trackAnalyticsEvent)({
                                eventKey: 'span_view.embedded_child.show',
                                eventName: 'Span View: Show Embedded Transaction',
                                organization_id: parseInt(organization.id, 10),
                            });
                        }
                        toggleEmbeddedChildren({
                            orgSlug: organization.slug,
                            eventSlug: (0, urls_1.generateEventSlug)({
                                id: transaction.event_id,
                                project: transaction.project_slug,
                            }),
                        });
                    }
                }}/>
        </tooltip_1.default>);
        }
        return null;
    }
    renderWarningText({ warningText } = {}) {
        if (!warningText) {
            return null;
        }
        return (<tooltip_1.default containerDisplayMode="flex" title={warningText}>
        <StyledIconWarning size="xs"/>
      </tooltip_1.default>);
    }
    renderHeader({ scrollbarManagerChildrenProps, dividerHandlerChildrenProps, errors, transactions, }) {
        const { span, spanBarColor, spanBarHatch, spanNumber } = this.props;
        const startTimestamp = span.start_timestamp;
        const endTimestamp = span.timestamp;
        const duration = Math.abs(endTimestamp - startTimestamp);
        const durationString = (0, utils_1.getHumanDuration)(duration);
        const bounds = this.getBounds();
        const { dividerPosition, addGhostDividerLineRef } = dividerHandlerChildrenProps;
        const displaySpanBar = (0, utils_2.defined)(bounds.left) && (0, utils_2.defined)(bounds.width);
        const durationDisplay = (0, utils_1.getDurationDisplay)(bounds);
        return (<row_1.RowCellContainer showDetail={this.state.showDetail}>
        <row_1.RowCell data-type="span-row-cell" showDetail={this.state.showDetail} style={{
                width: `calc(${(0, utils_1.toPercent)(dividerPosition)} - 0.5px)`,
                paddingTop: 0,
            }} onClick={() => {
                this.toggleDisplayDetail();
            }}>
          {this.renderTitle(scrollbarManagerChildrenProps, errors)}
        </row_1.RowCell>
        <rowDivider_1.DividerContainer>
          {this.renderDivider(dividerHandlerChildrenProps)}
          {this.renderErrorBadge(errors)}
          {this.renderEmbeddedTransactionsBadge(transactions)}
        </rowDivider_1.DividerContainer>
        <row_1.RowCell data-type="span-row-cell" showDetail={this.state.showDetail} showStriping={spanNumber % 2 !== 0} style={{
                width: `calc(${(0, utils_1.toPercent)(1 - dividerPosition)} - 0.5px)`,
            }} onClick={() => {
                this.toggleDisplayDetail();
            }}>
          {displaySpanBar && (<rowBar_1.RowRectangle spanBarHatch={!!spanBarHatch} style={{
                    backgroundColor: spanBarColor,
                    left: `min(${(0, utils_1.toPercent)(bounds.left || 0)}, calc(100% - 1px))`,
                    width: (0, utils_1.toPercent)(bounds.width || 0),
                }}>
              <rowBar_1.DurationPill durationDisplay={durationDisplay} showDetail={this.state.showDetail} spanBarHatch={!!spanBarHatch}>
                {durationString}
                {this.renderWarningText({ warningText: bounds.warning })}
              </rowBar_1.DurationPill>
            </rowBar_1.RowRectangle>)}
          {this.renderMeasurements()}
          <spanBarCursorGuide_1.default />
        </row_1.RowCell>
        {!this.state.showDetail && (<rowDivider_1.DividerLineGhostContainer style={{
                    width: `calc(${(0, utils_1.toPercent)(dividerPosition)} + 0.5px)`,
                    display: 'none',
                }}>
            <rowDivider_1.DividerLine ref={addGhostDividerLineRef()} style={{
                    right: 0,
                }} className="hovering" onClick={event => {
                    // the ghost divider line should not be interactive.
                    // we prevent the propagation of the clicks from this component to prevent
                    // the span detail from being opened.
                    event.stopPropagation();
                }}/>
          </rowDivider_1.DividerLineGhostContainer>)}
      </row_1.RowCellContainer>);
    }
    renderEmbeddedChildrenState() {
        const { fetchEmbeddedChildrenState } = this.props;
        switch (fetchEmbeddedChildrenState) {
            case 'loading_embedded_transactions': {
                return (<messageRow_1.MessageRow>
            <span>{(0, locale_1.t)('Loading embedded transaction')}</span>
          </messageRow_1.MessageRow>);
            }
            case 'error_fetching_embedded_transactions': {
                return (<messageRow_1.MessageRow>
            <span>{(0, locale_1.t)('Error loading embedded transaction')}</span>
          </messageRow_1.MessageRow>);
            }
            default:
                return null;
        }
    }
    render() {
        const bounds = this.getBounds();
        const { isSpanVisibleInView } = bounds;
        return (<React.Fragment>
        <row_1.Row ref={this.spanRowDOMRef} visible={isSpanVisibleInView} showBorder={this.state.showDetail} data-test-id="span-row">
          <QuickTraceContext.Consumer>
            {quickTrace => {
                const errors = this.getRelatedErrors(quickTrace);
                const transactions = this.getChildTransactions(quickTrace);
                return (<React.Fragment>
                  <ScrollbarManager.Consumer>
                    {scrollbarManagerChildrenProps => (<DividerHandlerManager.Consumer>
                        {(dividerHandlerChildrenProps) => this.renderHeader({
                            dividerHandlerChildrenProps,
                            scrollbarManagerChildrenProps,
                            errors,
                            transactions,
                        })}
                      </DividerHandlerManager.Consumer>)}
                  </ScrollbarManager.Consumer>
                  {this.renderDetail({
                        isVisible: isSpanVisibleInView,
                        transactions,
                        errors,
                    })}
                </React.Fragment>);
            }}
          </QuickTraceContext.Consumer>
        </row_1.Row>
        {this.renderEmbeddedChildrenState()}
      </React.Fragment>);
    }
}
const StyledIconWarning = (0, styled_1.default)(icons_1.IconWarning) `
  margin-left: ${(0, space_1.default)(0.25)};
  margin-bottom: ${(0, space_1.default)(0.25)};
`;
const Regroup = (0, styled_1.default)('span') ``;
exports.default = SpanBar;
//# sourceMappingURL=spanBar.jsx.map