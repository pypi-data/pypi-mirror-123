Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const guideAnchor_1 = (0, tslib_1.__importDefault)(require("app/components/assistant/guideAnchor"));
const count_1 = (0, tslib_1.__importDefault)(require("app/components/count"));
const AnchorLinkManager = (0, tslib_1.__importStar)(require("app/components/events/interfaces/spans/anchorLinkManager"));
const DividerHandlerManager = (0, tslib_1.__importStar)(require("app/components/events/interfaces/spans/dividerHandlerManager"));
const ScrollbarManager = (0, tslib_1.__importStar)(require("app/components/events/interfaces/spans/scrollbarManager"));
const projectBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge/projectBadge"));
const constants_1 = require("app/components/performance/waterfall/constants");
const row_1 = require("app/components/performance/waterfall/row");
const rowBar_1 = require("app/components/performance/waterfall/rowBar");
const rowDivider_1 = require("app/components/performance/waterfall/rowDivider");
const rowTitle_1 = require("app/components/performance/waterfall/rowTitle");
const treeConnector_1 = require("app/components/performance/waterfall/treeConnector");
const utils_1 = require("app/components/performance/waterfall/utils");
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const utils_2 = require("app/utils/performance/quickTrace/utils");
const projects_1 = (0, tslib_1.__importDefault)(require("app/utils/projects"));
const styles_1 = require("./styles");
const transactionDetail_1 = (0, tslib_1.__importDefault)(require("./transactionDetail"));
const MARGIN_LEFT = 0;
class TransactionBar extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            showDetail: false,
        };
        this.transactionRowDOMRef = React.createRef();
        this.toggleDisplayDetail = () => {
            const { transaction } = this.props;
            if ((0, utils_2.isTraceFullDetailed)(transaction)) {
                this.setState(state => ({
                    showDetail: !state.showDetail,
                }));
            }
        };
        this.scrollIntoView = () => {
            const element = this.transactionRowDOMRef.current;
            if (!element) {
                return;
            }
            const boundingRect = element.getBoundingClientRect();
            const offset = boundingRect.top + window.scrollY;
            this.setState({ showDetail: true }, () => window.scrollTo(0, offset));
        };
    }
    getCurrentOffset() {
        const { transaction } = this.props;
        const { generation } = transaction;
        return getOffset(generation);
    }
    renderConnector(hasToggle) {
        const { continuingDepths, isExpanded, isOrphan, isLast, transaction } = this.props;
        const { generation } = transaction;
        const eventId = (0, utils_2.isTraceFullDetailed)(transaction)
            ? transaction.event_id
            : transaction.traceSlug;
        if (generation === 0) {
            if (hasToggle) {
                return (<treeConnector_1.ConnectorBar style={{ right: '16px', height: '10px', bottom: '-5px', top: 'auto' }} orphanBranch={false}/>);
            }
            return null;
        }
        const connectorBars = continuingDepths.map(({ depth, isOrphanDepth }) => {
            if (generation - depth <= 1) {
                // If the difference is less than or equal to 1, then it means that the continued
                // bar is from its direct parent. In this case, do not render a connector bar
                // because the tree connector below will suffice.
                return null;
            }
            const left = -1 * getOffset(generation - depth - 1) - 1;
            return (<treeConnector_1.ConnectorBar style={{ left }} key={`${eventId}-${depth}`} orphanBranch={isOrphanDepth}/>);
        });
        if (hasToggle && isExpanded) {
            connectorBars.push(<treeConnector_1.ConnectorBar style={{
                    right: '16px',
                    height: '10px',
                    bottom: isLast ? `-${constants_1.ROW_HEIGHT / 2}px` : '0',
                    top: 'auto',
                }} key={`${eventId}-last`} orphanBranch={false}/>);
        }
        return (<treeConnector_1.TreeConnector isLast={isLast} hasToggler={hasToggle} orphanBranch={isOrphan}>
        {connectorBars}
      </treeConnector_1.TreeConnector>);
    }
    renderToggle(errored) {
        const { isExpanded, transaction, toggleExpandedState } = this.props;
        const { children, generation } = transaction;
        const left = this.getCurrentOffset();
        if (children.length <= 0) {
            return (<treeConnector_1.TreeToggleContainer style={{ left: `${left}px` }}>
          {this.renderConnector(false)}
        </treeConnector_1.TreeToggleContainer>);
        }
        const isRoot = generation === 0;
        return (<treeConnector_1.TreeToggleContainer style={{ left: `${left}px` }} hasToggler>
        {this.renderConnector(true)}
        <treeConnector_1.TreeToggle disabled={isRoot} isExpanded={isExpanded} errored={errored} onClick={event => {
                event.stopPropagation();
                if (isRoot) {
                    return;
                }
                toggleExpandedState();
            }}>
          <count_1.default value={children.length}/>
          {!isRoot && (<div>
              <treeConnector_1.TreeToggleIcon direction={isExpanded ? 'up' : 'down'}/>
            </div>)}
        </treeConnector_1.TreeToggle>
      </treeConnector_1.TreeToggleContainer>);
    }
    renderTitle(scrollbarManagerChildrenProps) {
        const { generateContentSpanBarRef } = scrollbarManagerChildrenProps;
        const { organization, transaction } = this.props;
        const left = this.getCurrentOffset();
        const errored = (0, utils_2.isTraceFullDetailed)(transaction)
            ? transaction.errors.length > 0
            : false;
        const content = (0, utils_2.isTraceFullDetailed)(transaction) ? (<React.Fragment>
        <projects_1.default orgId={organization.slug} slugs={[transaction.project_slug]}>
          {({ projects }) => {
                const project = projects.find(p => p.slug === transaction.project_slug);
                return (<styles_1.ProjectBadgeContainer>
                <tooltip_1.default title={transaction.project_slug}>
                  <projectBadge_1.default project={project ? project : { slug: transaction.project_slug }} avatarSize={16} hideName/>
                </tooltip_1.default>
              </styles_1.ProjectBadgeContainer>);
            }}
        </projects_1.default>
        <rowTitle_1.RowTitleContent errored={errored}>
          <strong>
            {transaction['transaction.op']}
            {' \u2014 '}
          </strong>
          {transaction.transaction}
        </rowTitle_1.RowTitleContent>
      </React.Fragment>) : (<rowTitle_1.RowTitleContent errored={false}>
        <strong>{'Trace \u2014 '}</strong>
        {transaction.traceSlug}
      </rowTitle_1.RowTitleContent>);
        return (<rowTitle_1.RowTitleContainer ref={generateContentSpanBarRef()}>
        {this.renderToggle(errored)}
        <rowTitle_1.RowTitle style={{
                left: `${left}px`,
                width: '100%',
            }}>
          {content}
        </rowTitle_1.RowTitle>
      </rowTitle_1.RowTitleContainer>);
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
    renderGhostDivider(dividerHandlerChildrenProps) {
        const { dividerPosition, addGhostDividerLineRef } = dividerHandlerChildrenProps;
        return (<rowDivider_1.DividerLineGhostContainer style={{
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
      </rowDivider_1.DividerLineGhostContainer>);
    }
    renderErrorBadge() {
        const { transaction } = this.props;
        if (!(0, utils_2.isTraceFullDetailed)(transaction) || !transaction.errors.length) {
            return null;
        }
        return <rowDivider_1.ErrorBadge />;
    }
    renderRectangle() {
        const { transaction, traceInfo, barColor } = this.props;
        const { showDetail } = this.state;
        // Use 1 as the difference in the event that startTimestamp === endTimestamp
        const delta = Math.abs(traceInfo.endTimestamp - traceInfo.startTimestamp) || 1;
        const startPosition = Math.abs(transaction.start_timestamp - traceInfo.startTimestamp);
        const startPercentage = startPosition / delta;
        const duration = Math.abs(transaction.timestamp - transaction.start_timestamp);
        const widthPercentage = duration / delta;
        return (<rowBar_1.RowRectangle spanBarHatch={false} style={{
                backgroundColor: barColor,
                left: `min(${(0, utils_1.toPercent)(startPercentage || 0)}, calc(100% - 1px))`,
                width: (0, utils_1.toPercent)(widthPercentage || 0),
            }}>
        <rowBar_1.DurationPill durationDisplay={(0, utils_1.getDurationDisplay)({
                left: startPercentage,
                width: widthPercentage,
            })} showDetail={showDetail} spanBarHatch={false}>
          {(0, utils_1.getHumanDuration)(duration)}
        </rowBar_1.DurationPill>
      </rowBar_1.RowRectangle>);
    }
    renderHeader({ dividerHandlerChildrenProps, scrollbarManagerChildrenProps, }) {
        const { hasGuideAnchor, index } = this.props;
        const { showDetail } = this.state;
        const { dividerPosition } = dividerHandlerChildrenProps;
        return (<row_1.RowCellContainer showDetail={showDetail}>
        <row_1.RowCell data-test-id="transaction-row-title" data-type="span-row-cell" style={{
                width: `calc(${(0, utils_1.toPercent)(dividerPosition)} - 0.5px)`,
                paddingTop: 0,
            }} showDetail={showDetail} onClick={this.toggleDisplayDetail}>
          <guideAnchor_1.default target="trace_view_guide_row" disabled={!hasGuideAnchor}>
            {this.renderTitle(scrollbarManagerChildrenProps)}
          </guideAnchor_1.default>
        </row_1.RowCell>
        <rowDivider_1.DividerContainer>
          {this.renderDivider(dividerHandlerChildrenProps)}
          {this.renderErrorBadge()}
        </rowDivider_1.DividerContainer>
        <row_1.RowCell data-test-id="transaction-row-duration" data-type="span-row-cell" showStriping={index % 2 !== 0} style={{
                width: `calc(${(0, utils_1.toPercent)(1 - dividerPosition)} - 0.5px)`,
                paddingTop: 0,
            }} showDetail={showDetail} onClick={this.toggleDisplayDetail}>
          <guideAnchor_1.default target="trace_view_guide_row_details" disabled={!hasGuideAnchor}>
            {this.renderRectangle()}
          </guideAnchor_1.default>
        </row_1.RowCell>
        {!showDetail && this.renderGhostDivider(dividerHandlerChildrenProps)}
      </row_1.RowCellContainer>);
    }
    renderDetail() {
        const { location, organization, isVisible, transaction } = this.props;
        const { showDetail } = this.state;
        return (<AnchorLinkManager.Consumer>
        {({ registerScrollFn, scrollToHash }) => {
                if (!(0, utils_2.isTraceFullDetailed)(transaction)) {
                    return null;
                }
                registerScrollFn(`#txn-${transaction.event_id}`, this.scrollIntoView);
                if (!isVisible || !showDetail) {
                    return null;
                }
                return (<transactionDetail_1.default location={location} organization={organization} transaction={transaction} scrollToHash={scrollToHash}/>);
            }}
      </AnchorLinkManager.Consumer>);
    }
    render() {
        const { isVisible, transaction } = this.props;
        const { showDetail } = this.state;
        return (<row_1.Row ref={this.transactionRowDOMRef} visible={isVisible} showBorder={showDetail} cursor={(0, utils_2.isTraceFullDetailed)(transaction) ? 'pointer' : 'default'}>
        <ScrollbarManager.Consumer>
          {scrollbarManagerChildrenProps => (<DividerHandlerManager.Consumer>
              {dividerHandlerChildrenProps => this.renderHeader({
                    dividerHandlerChildrenProps,
                    scrollbarManagerChildrenProps,
                })}
            </DividerHandlerManager.Consumer>)}
        </ScrollbarManager.Consumer>
        {this.renderDetail()}
      </row_1.Row>);
    }
}
function getOffset(generation) {
    return generation * (treeConnector_1.TOGGLE_BORDER_BOX / 2) + MARGIN_LEFT;
}
exports.default = TransactionBar;
//# sourceMappingURL=transactionBar.jsx.map