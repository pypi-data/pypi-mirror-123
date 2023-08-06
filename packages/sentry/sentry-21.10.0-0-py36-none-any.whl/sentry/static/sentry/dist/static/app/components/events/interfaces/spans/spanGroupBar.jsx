Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const countBy_1 = (0, tslib_1.__importDefault)(require("lodash/countBy"));
const count_1 = (0, tslib_1.__importDefault)(require("app/components/count"));
const constants_1 = require("app/components/performance/waterfall/constants");
const row_1 = require("app/components/performance/waterfall/row");
const rowBar_1 = require("app/components/performance/waterfall/rowBar");
const rowDivider_1 = require("app/components/performance/waterfall/rowDivider");
const rowTitle_1 = require("app/components/performance/waterfall/rowTitle");
const treeConnector_1 = require("app/components/performance/waterfall/treeConnector");
const utils_1 = require("app/components/performance/waterfall/utils");
const locale_1 = require("app/locale");
const utils_2 = require("app/utils");
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const DividerHandlerManager = (0, tslib_1.__importStar)(require("./dividerHandlerManager"));
const ScrollbarManager = (0, tslib_1.__importStar)(require("./scrollbarManager"));
const spanBarCursorGuide_1 = (0, tslib_1.__importDefault)(require("./spanBarCursorGuide"));
const styles_1 = require("./styles");
const utils_3 = require("./utils");
const MARGIN_LEFT = 0;
class SpanGroupBar extends React.Component {
    getSpanGroupTimestamps(spanGroup) {
        return spanGroup.reduce((acc, spanGroupItem) => {
            const { start_timestamp, timestamp } = spanGroupItem.span;
            let newStartTimestamp = acc.startTimestamp;
            let newEndTimestamp = acc.endTimestamp;
            if (start_timestamp < newStartTimestamp) {
                newStartTimestamp = start_timestamp;
            }
            if (newEndTimestamp > timestamp) {
                newEndTimestamp = timestamp;
            }
            return {
                startTimestamp: newStartTimestamp,
                endTimestamp: newEndTimestamp,
            };
        }, {
            startTimestamp: spanGroup[0].span.start_timestamp,
            endTimestamp: spanGroup[0].span.timestamp,
        });
    }
    getSpanGroupBounds(spanGroup) {
        const { generateBounds } = this.props;
        const { startTimestamp, endTimestamp } = this.getSpanGroupTimestamps(spanGroup);
        const bounds = generateBounds({
            startTimestamp,
            endTimestamp,
        });
        switch (bounds.type) {
            case 'TRACE_TIMESTAMPS_EQUAL':
            case 'INVALID_VIEW_WINDOW': {
                return {
                    warning: void 0,
                    left: void 0,
                    width: void 0,
                    isSpanVisibleInView: bounds.isSpanVisibleInView,
                };
            }
            case 'TIMESTAMPS_EQUAL': {
                return {
                    warning: void 0,
                    left: bounds.start,
                    width: 0.00001,
                    isSpanVisibleInView: bounds.isSpanVisibleInView,
                };
            }
            case 'TIMESTAMPS_REVERSED':
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
    renderGroupedSpansToggler() {
        const { spanGrouping, treeDepth, toggleSpanGroup } = this.props;
        const left = treeDepth * (treeConnector_1.TOGGLE_BORDER_BOX / 2) + MARGIN_LEFT;
        return (<treeConnector_1.TreeToggleContainer style={{ left: `${left}px` }} hasToggler>
        {this.renderSpanTreeConnector()}
        <treeConnector_1.TreeToggle disabled={false} isExpanded={false} errored={false} isSpanGroupToggler onClick={event => {
                event.stopPropagation();
                toggleSpanGroup();
            }}>
          <count_1.default value={spanGrouping.length}/>
        </treeConnector_1.TreeToggle>
      </treeConnector_1.TreeToggleContainer>);
    }
    generateGroupSpansTitle(spanGroup) {
        if (spanGroup.length === 0) {
            return '';
        }
        const operationCounts = (0, countBy_1.default)(spanGroup, enhancedSpan => (0, utils_3.getSpanOperation)(enhancedSpan.span));
        const hasOthers = Object.keys(operationCounts).length > 1;
        const [mostFrequentOperationName] = Object.entries(operationCounts).reduce((acc, [operationNameKey, count]) => {
            if (count > acc[1]) {
                return [operationNameKey, count];
            }
            return acc;
        });
        return (<strong>{`${(0, locale_1.t)('Autogrouped ')}\u2014 ${mostFrequentOperationName}${hasOthers ? (0, locale_1.t)(' and more') : ''}`}</strong>);
    }
    renderDivider(dividerHandlerChildrenProps) {
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
    renderSpanTreeConnector() {
        const { treeDepth: spanTreeDepth, continuingTreeDepths, span } = this.props;
        const connectorBars = continuingTreeDepths.map(treeDepth => {
            const depth = (0, utils_3.unwrapTreeDepth)(treeDepth);
            if (depth === 0) {
                // do not render a connector bar at depth 0,
                // if we did render a connector bar, this bar would be placed at depth -1
                // which does not exist.
                return null;
            }
            const left = ((spanTreeDepth - depth) * (treeConnector_1.TOGGLE_BORDER_BOX / 2) + 1) * -1;
            return (<treeConnector_1.ConnectorBar style={{ left }} key={`span-group-${depth}`} orphanBranch={(0, utils_3.isOrphanTreeDepth)(treeDepth)}/>);
        });
        connectorBars.push(<treeConnector_1.ConnectorBar style={{
                right: '16px',
                height: `${constants_1.ROW_HEIGHT / 2}px`,
                bottom: `-${constants_1.ROW_HEIGHT / 2}px`,
                top: 'auto',
            }} key="collapsed-span-group-row-bottom" orphanBranch={false}/>);
        return (<treeConnector_1.TreeConnector isLast hasToggler orphanBranch={(0, utils_3.isOrphanSpan)(span)}>
        {connectorBars}
      </treeConnector_1.TreeConnector>);
    }
    renderMeasurements() {
        const { event, generateBounds } = this.props;
        const measurements = (0, utils_3.getMeasurements)(event);
        return (<React.Fragment>
        {Array.from(measurements).map(([timestamp, verticalMark]) => {
                const bounds = (0, utils_3.getMeasurementBounds)(timestamp, generateBounds);
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
    render() {
        return (<ScrollbarManager.Consumer>
        {scrollbarManagerChildrenProps => (<DividerHandlerManager.Consumer>
            {(dividerHandlerChildrenProps) => {
                    const { span, generateBounds, treeDepth, spanGrouping, toggleSpanGroup, spanNumber, } = this.props;
                    const { isSpanVisibleInView: isSpanVisible } = generateBounds({
                        startTimestamp: span.start_timestamp,
                        endTimestamp: span.timestamp,
                    });
                    const { dividerPosition, addGhostDividerLineRef } = dividerHandlerChildrenProps;
                    const { generateContentSpanBarRef } = scrollbarManagerChildrenProps;
                    const left = treeDepth * (treeConnector_1.TOGGLE_BORDER_BOX / 2) + MARGIN_LEFT;
                    const bounds = this.getSpanGroupBounds(spanGrouping);
                    const durationDisplay = (0, utils_1.getDurationDisplay)(bounds);
                    const { startTimestamp, endTimestamp } = this.getSpanGroupTimestamps(spanGrouping);
                    const duration = Math.abs(endTimestamp - startTimestamp);
                    const durationString = (0, utils_1.getHumanDuration)(duration);
                    return (<row_1.Row visible={isSpanVisible} showBorder={false} data-test-id="span-row">
                  <row_1.RowCellContainer>
                    <row_1.RowCell data-type="span-row-cell" style={{
                            width: `calc(${(0, utils_1.toPercent)(dividerPosition)} - 0.5px)`,
                            paddingTop: 0,
                        }} onClick={() => {
                            toggleSpanGroup();
                        }}>
                      <rowTitle_1.RowTitleContainer ref={generateContentSpanBarRef()}>
                        {this.renderGroupedSpansToggler()}
                        <rowTitle_1.RowTitle style={{
                            left: `${left}px`,
                            width: '100%',
                        }}>
                          <rowTitle_1.SpanGroupRowTitleContent>
                            {this.generateGroupSpansTitle(spanGrouping)}
                          </rowTitle_1.SpanGroupRowTitleContent>
                        </rowTitle_1.RowTitle>
                      </rowTitle_1.RowTitleContainer>
                    </row_1.RowCell>
                    <rowDivider_1.DividerContainer>
                      {this.renderDivider(dividerHandlerChildrenProps)}
                    </rowDivider_1.DividerContainer>
                    <row_1.RowCell data-type="span-row-cell" showStriping={spanNumber % 2 !== 0} style={{
                            width: `calc(${(0, utils_1.toPercent)(1 - dividerPosition)} - 0.5px)`,
                        }} onClick={() => {
                            toggleSpanGroup();
                        }}>
                      <rowBar_1.RowRectangle spanBarHatch={false} style={{
                            backgroundColor: theme_1.default.blue300,
                            left: `min(${(0, utils_1.toPercent)(bounds.left || 0)}, calc(100% - 1px))`,
                            width: (0, utils_1.toPercent)(bounds.width || 0),
                        }}>
                        <rowBar_1.DurationPill durationDisplay={durationDisplay} showDetail={false} spanBarHatch={false}>
                          {durationString}
                        </rowBar_1.DurationPill>
                      </rowBar_1.RowRectangle>
                      {this.renderMeasurements()}
                      <spanBarCursorGuide_1.default />
                    </row_1.RowCell>
                    <rowDivider_1.DividerLineGhostContainer style={{
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
                    </rowDivider_1.DividerLineGhostContainer>
                  </row_1.RowCellContainer>
                </row_1.Row>);
                }}
          </DividerHandlerManager.Consumer>)}
      </ScrollbarManager.Consumer>);
    }
}
exports.default = SpanGroupBar;
//# sourceMappingURL=spanGroupBar.jsx.map