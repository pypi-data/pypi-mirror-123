Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const count_1 = (0, tslib_1.__importDefault)(require("app/components/count"));
const DividerHandlerManager = (0, tslib_1.__importStar)(require("app/components/events/interfaces/spans/dividerHandlerManager"));
const utils_1 = require("app/components/events/interfaces/spans/utils");
const constants_1 = require("app/components/performance/waterfall/constants");
const row_1 = require("app/components/performance/waterfall/row");
const rowDivider_1 = require("app/components/performance/waterfall/rowDivider");
const rowTitle_1 = require("app/components/performance/waterfall/rowTitle");
const treeConnector_1 = require("app/components/performance/waterfall/treeConnector");
const utils_2 = require("app/components/performance/waterfall/utils");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const spanDetail_1 = (0, tslib_1.__importDefault)(require("./spanDetail"));
const styles_1 = require("./styles");
const utils_3 = require("./utils");
class SpanBar extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            showDetail: false,
        };
        this.renderDivider = (dividerHandlerChildrenProps) => {
            const { theme } = this.props;
            if (this.state.showDetail) {
                // Mock component to preserve layout spacing
                return (<rowDivider_1.DividerLine style={{
                        position: 'relative',
                        backgroundColor: (0, utils_2.getBackgroundColor)({
                            theme,
                            showDetail: true,
                        }),
                    }}/>);
            }
            const { addDividerLineRef } = dividerHandlerChildrenProps;
            return (<rowDivider_1.DividerLine ref={addDividerLineRef()} style={{
                    position: 'relative',
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
        };
        this.toggleDisplayDetail = () => {
            this.setState(state => ({
                showDetail: !state.showDetail,
            }));
        };
    }
    renderSpanTreeConnector({ hasToggler }) {
        const { isLast, isRoot, treeDepth: spanTreeDepth, continuingTreeDepths, span, showSpanTree, } = this.props;
        const spanID = (0, utils_3.getSpanID)(span);
        if (isRoot) {
            if (hasToggler) {
                return (<treeConnector_1.ConnectorBar style={{ right: '16px', height: '10px', bottom: '-5px', top: 'auto' }} key={`${spanID}-last`} orphanBranch={false}/>);
            }
            return null;
        }
        const connectorBars = continuingTreeDepths.map(treeDepth => {
            const depth = (0, utils_1.unwrapTreeDepth)(treeDepth);
            if (depth === 0) {
                // do not render a connector bar at depth 0,
                // if we did render a connector bar, this bar would be placed at depth -1
                // which does not exist.
                return null;
            }
            const left = ((spanTreeDepth - depth) * (treeConnector_1.TOGGLE_BORDER_BOX / 2) + 1) * -1;
            return (<treeConnector_1.ConnectorBar style={{ left }} key={`${spanID}-${depth}`} orphanBranch={(0, utils_1.isOrphanTreeDepth)(treeDepth)}/>);
        });
        if (hasToggler && showSpanTree) {
            // if there is a toggle button, we add a connector bar to create an attachment
            // between the toggle button and any connector bars below the toggle button
            connectorBars.push(<treeConnector_1.ConnectorBar style={{
                    right: '16px',
                    height: '10px',
                    bottom: isLast ? `-${constants_1.ROW_HEIGHT / 2}px` : '0',
                    top: 'auto',
                }} key={`${spanID}-last`} orphanBranch={false}/>);
        }
        return (<treeConnector_1.TreeConnector isLast={isLast} hasToggler={hasToggler} orphanBranch={(0, utils_3.isOrphanDiffSpan)(span)}>
        {connectorBars}
      </treeConnector_1.TreeConnector>);
    }
    renderSpanTreeToggler({ left }) {
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
        <treeConnector_1.TreeToggle disabled={!!isRoot} isExpanded={this.props.showSpanTree} errored={false} onClick={event => {
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
    renderTitle() {
        var _a;
        const { span, treeDepth } = this.props;
        const operationName = (0, utils_3.getSpanOperation)(span) ? (<strong>
        {(0, utils_3.getSpanOperation)(span)}
        {' \u2014 '}
      </strong>) : ('');
        const description = (_a = (0, utils_3.getSpanDescription)(span)) !== null && _a !== void 0 ? _a : (span.comparisonResult === 'matched' ? (0, locale_1.t)('matched') : (0, utils_3.getSpanID)(span));
        const left = treeDepth * (treeConnector_1.TOGGLE_BORDER_BOX / 2);
        return (<rowTitle_1.RowTitleContainer>
        {this.renderSpanTreeToggler({ left })}
        <rowTitle_1.RowTitle style={{
                left: `${left}px`,
                width: '100%',
            }}>
          <span>
            {operationName}
            {description}
          </span>
        </rowTitle_1.RowTitle>
      </rowTitle_1.RowTitleContainer>);
    }
    getSpanBarStyles() {
        const { theme, span, generateBounds } = this.props;
        const bounds = generateBounds(span);
        function normalizePadding(width) {
            if (!width) {
                return undefined;
            }
            return `max(1px, ${width})`;
        }
        switch (span.comparisonResult) {
            case 'matched': {
                const baselineDuration = (0, utils_3.getSpanDuration)(span.baselineSpan);
                const regressionDuration = (0, utils_3.getSpanDuration)(span.regressionSpan);
                if (baselineDuration === regressionDuration) {
                    return {
                        background: {
                            color: undefined,
                            width: normalizePadding((0, utils_3.generateCSSWidth)(bounds.background)),
                            hatch: true,
                        },
                        foreground: undefined,
                    };
                }
                if (baselineDuration > regressionDuration) {
                    return {
                        background: {
                            // baseline
                            color: theme.textColor,
                            width: normalizePadding((0, utils_3.generateCSSWidth)(bounds.background)),
                        },
                        foreground: {
                            // regression
                            color: undefined,
                            width: normalizePadding((0, utils_3.generateCSSWidth)(bounds.foreground)),
                            hatch: true,
                        },
                    };
                }
                // case: baselineDuration < regressionDuration
                return {
                    background: {
                        // regression
                        color: theme.purple200,
                        width: normalizePadding((0, utils_3.generateCSSWidth)(bounds.background)),
                    },
                    foreground: {
                        // baseline
                        color: undefined,
                        width: normalizePadding((0, utils_3.generateCSSWidth)(bounds.foreground)),
                        hatch: true,
                    },
                };
            }
            case 'regression': {
                return {
                    background: {
                        color: theme.purple200,
                        width: normalizePadding((0, utils_3.generateCSSWidth)(bounds.background)),
                    },
                    foreground: undefined,
                };
            }
            case 'baseline': {
                return {
                    background: {
                        color: theme.textColor,
                        width: normalizePadding((0, utils_3.generateCSSWidth)(bounds.background)),
                    },
                    foreground: undefined,
                };
            }
            default: {
                const _exhaustiveCheck = span;
                return _exhaustiveCheck;
            }
        }
    }
    renderComparisonReportLabel() {
        const { span } = this.props;
        switch (span.comparisonResult) {
            case 'matched': {
                const baselineDuration = (0, utils_3.getSpanDuration)(span.baselineSpan);
                const regressionDuration = (0, utils_3.getSpanDuration)(span.regressionSpan);
                let label;
                if (baselineDuration === regressionDuration) {
                    label = <ComparisonLabel>{(0, locale_1.t)('No change')}</ComparisonLabel>;
                }
                if (baselineDuration > regressionDuration) {
                    const duration = (0, utils_2.getHumanDuration)(Math.abs(baselineDuration - regressionDuration));
                    label = (<NotableComparisonLabel>{(0, locale_1.t)('- %s faster', duration)}</NotableComparisonLabel>);
                }
                if (baselineDuration < regressionDuration) {
                    const duration = (0, utils_2.getHumanDuration)(Math.abs(baselineDuration - regressionDuration));
                    label = (<NotableComparisonLabel>{(0, locale_1.t)('+ %s slower', duration)}</NotableComparisonLabel>);
                }
                return label;
            }
            case 'baseline': {
                return <ComparisonLabel>{(0, locale_1.t)('Only in baseline')}</ComparisonLabel>;
            }
            case 'regression': {
                return <ComparisonLabel>{(0, locale_1.t)('Only in this event')}</ComparisonLabel>;
            }
            default: {
                const _exhaustiveCheck = span;
                return _exhaustiveCheck;
            }
        }
    }
    renderHeader(dividerHandlerChildrenProps) {
        var _a, _b;
        const { dividerPosition, addGhostDividerLineRef } = dividerHandlerChildrenProps;
        const { spanNumber, span } = this.props;
        const isMatched = span.comparisonResult === 'matched';
        const hideSpanBarColumn = this.state.showDetail && isMatched;
        const spanBarStyles = this.getSpanBarStyles();
        const foregroundSpanBar = spanBarStyles.foreground ? (<ComparisonSpanBarRectangle spanBarHatch={(_a = spanBarStyles.foreground.hatch) !== null && _a !== void 0 ? _a : false} style={{
                backgroundColor: spanBarStyles.foreground.color,
                width: spanBarStyles.foreground.width,
                display: hideSpanBarColumn ? 'none' : 'block',
            }}/>) : null;
        return (<row_1.RowCellContainer showDetail={this.state.showDetail}>
        <row_1.RowCell data-type="span-row-cell" showDetail={this.state.showDetail} style={{
                width: `calc(${(0, utils_2.toPercent)(dividerPosition)} - 0.5px)`,
            }} onClick={() => {
                this.toggleDisplayDetail();
            }}>
          {this.renderTitle()}
        </row_1.RowCell>
        {this.renderDivider(dividerHandlerChildrenProps)}
        <row_1.RowCell data-type="span-row-cell" showDetail={this.state.showDetail} showStriping={spanNumber % 2 !== 0} style={{
                width: `calc(${(0, utils_2.toPercent)(1 - dividerPosition)} - 0.5px)`,
            }} onClick={() => {
                this.toggleDisplayDetail();
            }}>
          <SpanContainer>
            <ComparisonSpanBarRectangle spanBarHatch={(_b = spanBarStyles.background.hatch) !== null && _b !== void 0 ? _b : false} style={{
                backgroundColor: spanBarStyles.background.color,
                width: spanBarStyles.background.width,
                display: hideSpanBarColumn ? 'none' : 'block',
            }}/>
            {foregroundSpanBar}
          </SpanContainer>
          {this.renderComparisonReportLabel()}
        </row_1.RowCell>
        {!this.state.showDetail && (<rowDivider_1.DividerLineGhostContainer style={{
                    width: `calc(${(0, utils_2.toPercent)(dividerPosition)} + 0.5px)`,
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
    renderDetail() {
        if (!this.state.showDetail) {
            return null;
        }
        const { span, generateBounds } = this.props;
        return <spanDetail_1.default span={this.props.span} bounds={generateBounds(span)}/>;
    }
    render() {
        return (<row_1.Row visible data-test-id="span-row">
        <DividerHandlerManager.Consumer>
          {(dividerHandlerChildrenProps) => this.renderHeader(dividerHandlerChildrenProps)}
        </DividerHandlerManager.Consumer>
        {this.renderDetail()}
      </row_1.Row>);
    }
}
const ComparisonSpanBarRectangle = (0, styled_1.default)(styles_1.SpanBarRectangle) `
  position: absolute;
  left: 0;
  height: 16px;
  ${p => (0, utils_2.getHatchPattern)(p, p.theme.purple200, p.theme.gray500)}
`;
const ComparisonLabel = (0, styled_1.default)('div') `
  position: absolute;
  user-select: none;
  right: ${(0, space_1.default)(1)};
  line-height: ${constants_1.ROW_HEIGHT - 2 * constants_1.ROW_PADDING}px;
  top: ${constants_1.ROW_PADDING}px;
  font-size: ${p => p.theme.fontSizeExtraSmall};
`;
const SpanContainer = (0, styled_1.default)('div') `
  position: relative;
  margin-right: 120px;
`;
const NotableComparisonLabel = (0, styled_1.default)(ComparisonLabel) `
  font-weight: bold;
`;
exports.default = (0, react_1.withTheme)(SpanBar);
//# sourceMappingURL=spanBar.jsx.map