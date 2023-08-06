Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const guideAnchor_1 = (0, tslib_1.__importDefault)(require("app/components/assistant/guideAnchor"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const discoverFeature_1 = (0, tslib_1.__importDefault)(require("app/components/discover/discoverFeature"));
const discoverButton_1 = (0, tslib_1.__importDefault)(require("app/components/discoverButton"));
const AnchorLinkManager = (0, tslib_1.__importStar)(require("app/components/events/interfaces/spans/anchorLinkManager"));
const DividerHandlerManager = (0, tslib_1.__importStar)(require("app/components/events/interfaces/spans/dividerHandlerManager"));
const ScrollbarManager = (0, tslib_1.__importStar)(require("app/components/events/interfaces/spans/scrollbarManager"));
const Layout = (0, tslib_1.__importStar)(require("app/components/layouts/thirds"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const messageRow_1 = require("app/components/performance/waterfall/messageRow");
const miniHeader_1 = require("app/components/performance/waterfall/miniHeader");
const utils_1 = require("app/components/performance/waterfall/utils");
const timeSince_1 = (0, tslib_1.__importDefault)(require("app/components/timeSince"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const createFuzzySearch_1 = require("app/utils/createFuzzySearch");
const formatters_1 = require("app/utils/formatters");
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const utils_2 = require("app/utils/performance/quickTrace/utils");
const breadcrumb_1 = (0, tslib_1.__importDefault)(require("app/views/performance/breadcrumb"));
const styles_1 = require("app/views/performance/transactionDetails/styles");
const styles_2 = require("./styles");
const transactionGroup_1 = (0, tslib_1.__importDefault)(require("./transactionGroup"));
const utils_3 = require("./utils");
class TraceDetailsContent extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            searchQuery: undefined,
            filteredTransactionIds: undefined,
        };
        this.traceViewRef = React.createRef();
        this.virtualScrollbarContainerRef = React.createRef();
        this.handleTransactionFilter = (searchQuery) => {
            this.setState({ searchQuery: searchQuery || undefined }, this.filterTransactions);
        };
        this.filterTransactions = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { traces } = this.props;
            const { filteredTransactionIds, searchQuery } = this.state;
            if (!searchQuery || traces === null || traces.length <= 0) {
                if (filteredTransactionIds !== undefined) {
                    this.setState({
                        filteredTransactionIds: undefined,
                    });
                }
                return;
            }
            const transformed = traces.flatMap(trace => (0, utils_2.reduceTrace)(trace, (acc, transaction) => {
                const indexed = [
                    transaction['transaction.op'],
                    transaction.transaction,
                    transaction.project_slug,
                ];
                acc.push({
                    transaction,
                    indexed,
                });
                return acc;
            }, []));
            const fuse = yield (0, createFuzzySearch_1.createFuzzySearch)(transformed, {
                keys: ['indexed'],
                includeMatches: true,
                threshold: 0.6,
                location: 0,
                distance: 100,
                maxPatternLength: 32,
            });
            const fuseMatches = fuse
                .search(searchQuery)
                /**
                 * Sometimes, there can be matches that don't include any
                 * indices. These matches are often noise, so exclude them.
                 */
                .filter(({ matches }) => matches.length)
                .map(({ item }) => item.transaction.event_id);
            /**
             * Fuzzy search on ids result in seemingly random results. So switch to
             * doing substring matches on ids to provide more meaningful results.
             */
            const idMatches = traces
                .flatMap(trace => (0, utils_2.filterTrace)(trace, ({ event_id, span_id }) => event_id.includes(searchQuery) || span_id.includes(searchQuery)))
                .map(transaction => transaction.event_id);
            this.setState({
                filteredTransactionIds: new Set([...fuseMatches, ...idMatches]),
            });
        });
        this.isTransactionVisible = (transaction) => {
            const { filteredTransactionIds } = this.state;
            return filteredTransactionIds
                ? filteredTransactionIds.has(transaction.event_id)
                : true;
        };
    }
    renderTraceLoading() {
        return <loadingIndicator_1.default />;
    }
    renderTraceRequiresDateRangeSelection() {
        return <loadingError_1.default message={(0, locale_1.t)('Trace view requires a date range selection.')}/>;
    }
    renderTraceNotFound() {
        var _a, _b;
        const { meta } = this.props;
        const transactions = (_a = meta === null || meta === void 0 ? void 0 : meta.transactions) !== null && _a !== void 0 ? _a : 0;
        const errors = (_b = meta === null || meta === void 0 ? void 0 : meta.errors) !== null && _b !== void 0 ? _b : 0;
        if (transactions === 0 && errors > 0) {
            return (<loadingError_1.default message={(0, locale_1.t)('The trace you are looking contains only errors.')}/>);
        }
        return <loadingError_1.default message={(0, locale_1.t)('The trace you are looking for was not found.')}/>;
    }
    renderSearchBar() {
        return (<styles_2.TraceSearchContainer>
        <styles_2.TraceSearchBar defaultQuery="" query={this.state.searchQuery || ''} placeholder={(0, locale_1.t)('Search for transactions')} onSearch={this.handleTransactionFilter}/>
      </styles_2.TraceSearchContainer>);
    }
    renderTraceHeader(traceInfo) {
        var _a, _b, _c;
        const { meta } = this.props;
        return (<styles_2.TraceDetailHeader>
        <guideAnchor_1.default target="trace_view_guide_breakdown">
          <styles_1.MetaData headingText={(0, locale_1.t)('Event Breakdown')} tooltipText={(0, locale_1.t)('The number of transactions and errors there are in this trace.')} bodyText={(0, locale_1.tct)('[transactions]  |  [errors]', {
                transactions: (0, locale_1.tn)('%s Transaction', '%s Transactions', (_a = meta === null || meta === void 0 ? void 0 : meta.transactions) !== null && _a !== void 0 ? _a : traceInfo.transactions.size),
                errors: (0, locale_1.tn)('%s Error', '%s Errors', (_b = meta === null || meta === void 0 ? void 0 : meta.errors) !== null && _b !== void 0 ? _b : traceInfo.errors.size),
            })} subtext={(0, locale_1.tn)('Across %s project', 'Across %s projects', (_c = meta === null || meta === void 0 ? void 0 : meta.projects) !== null && _c !== void 0 ? _c : traceInfo.projects.size)}/>
        </guideAnchor_1.default>
        <styles_1.MetaData headingText={(0, locale_1.t)('Total Duration')} tooltipText={(0, locale_1.t)('The time elapsed between the start and end of this trace.')} bodyText={(0, formatters_1.getDuration)(traceInfo.endTimestamp - traceInfo.startTimestamp, 2, true)} subtext={(0, getDynamicText_1.default)({
                value: <timeSince_1.default date={(traceInfo.endTimestamp || 0) * 1000}/>,
                fixed: '5 days ago',
            })}/>
      </styles_2.TraceDetailHeader>);
    }
    renderTraceWarnings() {
        const { traces } = this.props;
        const { roots, orphans } = (traces !== null && traces !== void 0 ? traces : []).reduce((counts, trace) => {
            if ((0, utils_3.isRootTransaction)(trace)) {
                counts.roots++;
            }
            else {
                counts.orphans++;
            }
            return counts;
        }, { roots: 0, orphans: 0 });
        let warning = null;
        if (roots === 0 && orphans > 0) {
            warning = (<alert_1.default type="info" icon={<icons_1.IconInfo size="sm"/>}>
          <externalLink_1.default href="https://docs.sentry.io/product/performance/trace-view/#orphan-traces-and-broken-subtraces">
            {(0, locale_1.t)('A root transaction is missing. Transactions linked by a dashed line have been orphaned and cannot be directly linked to the root.')}
          </externalLink_1.default>
        </alert_1.default>);
        }
        else if (roots === 1 && orphans > 0) {
            warning = (<alert_1.default type="info" icon={<icons_1.IconInfo size="sm"/>}>
          <externalLink_1.default href="https://docs.sentry.io/product/performance/trace-view/#orphan-traces-and-broken-subtraces">
            {(0, locale_1.t)('This trace has broken subtraces. Transactions linked by a dashed line have been orphaned and cannot be directly linked to the root.')}
          </externalLink_1.default>
        </alert_1.default>);
        }
        else if (roots > 1) {
            warning = (<alert_1.default type="info" icon={<icons_1.IconInfo size="sm"/>}>
          <externalLink_1.default href="https://docs.sentry.io/product/performance/trace-view/#multiple-roots">
            {(0, locale_1.t)('Multiple root transactions have been found with this trace ID.')}
          </externalLink_1.default>
        </alert_1.default>);
        }
        return warning;
    }
    renderInfoMessage({ isVisible, numberOfHiddenTransactionsAbove, }) {
        const messages = [];
        if (isVisible) {
            if (numberOfHiddenTransactionsAbove === 1) {
                messages.push(<span key="stuff">
            {(0, locale_1.tct)('[numOfTransaction] hidden transaction', {
                        numOfTransaction: <strong>{numberOfHiddenTransactionsAbove}</strong>,
                    })}
          </span>);
            }
            else if (numberOfHiddenTransactionsAbove > 1) {
                messages.push(<span key="stuff">
            {(0, locale_1.tct)('[numOfTransaction] hidden transactions', {
                        numOfTransaction: <strong>{numberOfHiddenTransactionsAbove}</strong>,
                    })}
          </span>);
            }
        }
        if (messages.length <= 0) {
            return null;
        }
        return <messageRow_1.MessageRow>{messages}</messageRow_1.MessageRow>;
    }
    renderLimitExceededMessage(traceInfo) {
        var _a;
        const { traceEventView, organization, meta } = this.props;
        const count = traceInfo.transactions.size;
        const totalTransactions = (_a = meta === null || meta === void 0 ? void 0 : meta.transactions) !== null && _a !== void 0 ? _a : count;
        if (totalTransactions === null || count >= totalTransactions) {
            return null;
        }
        const target = traceEventView.getResultsViewUrlTarget(organization.slug);
        return (<messageRow_1.MessageRow>
        {(0, locale_1.tct)('Limited to a view of [count] transactions. To view the full list, [discover].', {
                count,
                discover: (<discoverFeature_1.default>
                {({ hasFeature }) => (<link_1.default disabled={!hasFeature} to={target}>
                    Open in Discover
                  </link_1.default>)}
              </discoverFeature_1.default>),
            })}
      </messageRow_1.MessageRow>);
    }
    renderTransaction(transaction, { continuingDepths, isOrphan, isLast, index, numberOfHiddenTransactionsAbove, traceInfo, hasGuideAnchor, }) {
        const { location, organization } = this.props;
        const { children, event_id: eventId } = transaction;
        // Add 1 to the generation to make room for the "root trace"
        const generation = transaction.generation + 1;
        const isVisible = this.isTransactionVisible(transaction);
        const accumulated = children.reduce((acc, child, idx) => {
            const isLastChild = idx === children.length - 1;
            const hasChildren = child.children.length > 0;
            const result = this.renderTransaction(child, {
                continuingDepths: !isLastChild && hasChildren
                    ? [...continuingDepths, { depth: generation, isOrphanDepth: isOrphan }]
                    : continuingDepths,
                isOrphan,
                isLast: isLastChild,
                index: acc.lastIndex + 1,
                numberOfHiddenTransactionsAbove: acc.numberOfHiddenTransactionsAbove,
                traceInfo,
                hasGuideAnchor: false,
            });
            acc.lastIndex = result.lastIndex;
            acc.numberOfHiddenTransactionsAbove = result.numberOfHiddenTransactionsAbove;
            acc.renderedChildren.push(result.transactionGroup);
            return acc;
        }, {
            renderedChildren: [],
            lastIndex: index,
            numberOfHiddenTransactionsAbove: isVisible
                ? 0
                : numberOfHiddenTransactionsAbove + 1,
        });
        return {
            transactionGroup: (<React.Fragment key={eventId}>
          {this.renderInfoMessage({
                    isVisible,
                    numberOfHiddenTransactionsAbove,
                })}
          <transactionGroup_1.default location={location} organization={organization} traceInfo={traceInfo} transaction={Object.assign(Object.assign({}, transaction), { generation })} continuingDepths={continuingDepths} isOrphan={isOrphan} isLast={isLast} index={index} isVisible={isVisible} hasGuideAnchor={hasGuideAnchor} renderedChildren={accumulated.renderedChildren} barColor={(0, utils_1.pickBarColor)(transaction['transaction.op'])}/>
        </React.Fragment>),
            lastIndex: accumulated.lastIndex,
            numberOfHiddenTransactionsAbove: accumulated.numberOfHiddenTransactionsAbove,
        };
    }
    renderTraceView(traceInfo) {
        var _a;
        const sentryTransaction = (_a = Sentry.getCurrentHub().getScope()) === null || _a === void 0 ? void 0 : _a.getTransaction();
        const sentrySpan = sentryTransaction === null || sentryTransaction === void 0 ? void 0 : sentryTransaction.startChild({
            op: 'trace.render',
            description: 'trace-view-content',
        });
        const { location, organization, traces, traceSlug } = this.props;
        if (traces === null || traces.length <= 0) {
            return this.renderTraceNotFound();
        }
        const accumulator = {
            index: 1,
            numberOfHiddenTransactionsAbove: 0,
            traceInfo,
            transactionGroups: [],
        };
        const { transactionGroups, numberOfHiddenTransactionsAbove } = traces.reduce((acc, trace, index) => {
            const isLastTransaction = index === traces.length - 1;
            const hasChildren = trace.children.length > 0;
            const isNextChildOrphaned = !isLastTransaction && traces[index + 1].parent_span_id !== null;
            const result = this.renderTransaction(trace, Object.assign(Object.assign({}, acc), { 
                // if the root of a subtrace has a parent_span_idk, then it must be an orphan
                isOrphan: !(0, utils_3.isRootTransaction)(trace), isLast: isLastTransaction, continuingDepths: !isLastTransaction && hasChildren
                    ? [{ depth: 0, isOrphanDepth: isNextChildOrphaned }]
                    : [], hasGuideAnchor: index === 0 }));
            acc.index = result.lastIndex + 1;
            acc.numberOfHiddenTransactionsAbove = result.numberOfHiddenTransactionsAbove;
            acc.transactionGroups.push(result.transactionGroup);
            return acc;
        }, accumulator);
        const traceView = (<styles_2.TraceDetailBody>
        <DividerHandlerManager.Provider interactiveLayerRef={this.traceViewRef}>
          <DividerHandlerManager.Consumer>
            {({ dividerPosition }) => (<ScrollbarManager.Provider dividerPosition={dividerPosition} interactiveLayerRef={this.virtualScrollbarContainerRef}>
                <styles_2.TracePanel>
                  <styles_2.TraceViewHeaderContainer>
                    <ScrollbarManager.Consumer>
                      {({ virtualScrollbarRef, scrollBarAreaRef, onDragStart, onScroll, }) => {
                    return (<miniHeader_1.ScrollbarContainer ref={this.virtualScrollbarContainerRef} style={{
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
                  </styles_2.TraceViewHeaderContainer>
                  <styles_2.TraceViewContainer ref={this.traceViewRef}>
                    <AnchorLinkManager.Provider>
                      <transactionGroup_1.default location={location} organization={organization} traceInfo={traceInfo} transaction={{
                    traceSlug,
                    generation: 0,
                    'transaction.duration': traceInfo.endTimestamp - traceInfo.startTimestamp,
                    children: traces,
                    start_timestamp: traceInfo.startTimestamp,
                    timestamp: traceInfo.endTimestamp,
                }} continuingDepths={[]} isOrphan={false} isLast={false} index={0} isVisible hasGuideAnchor={false} renderedChildren={transactionGroups} barColor={(0, utils_1.pickBarColor)('')}/>
                    </AnchorLinkManager.Provider>
                    {this.renderInfoMessage({
                    isVisible: true,
                    numberOfHiddenTransactionsAbove,
                })}
                    {this.renderLimitExceededMessage(traceInfo)}
                  </styles_2.TraceViewContainer>
                </styles_2.TracePanel>
              </ScrollbarManager.Provider>)}
          </DividerHandlerManager.Consumer>
        </DividerHandlerManager.Provider>
      </styles_2.TraceDetailBody>);
        sentrySpan === null || sentrySpan === void 0 ? void 0 : sentrySpan.finish();
        return traceView;
    }
    renderContent() {
        const { dateSelected, isLoading, error, traces } = this.props;
        if (!dateSelected) {
            return this.renderTraceRequiresDateRangeSelection();
        }
        else if (isLoading) {
            return this.renderTraceLoading();
        }
        else if (error !== null || traces === null || traces.length <= 0) {
            return this.renderTraceNotFound();
        }
        else {
            const traceInfo = (0, utils_3.getTraceInfo)(traces);
            return (<React.Fragment>
          {this.renderTraceWarnings()}
          {this.renderTraceHeader(traceInfo)}
          {this.renderSearchBar()}
          {this.renderTraceView(traceInfo)}
        </React.Fragment>);
        }
    }
    render() {
        const { organization, location, traceEventView, traceSlug } = this.props;
        return (<React.Fragment>
        <Layout.Header>
          <Layout.HeaderContent>
            <breadcrumb_1.default organization={organization} location={location} traceSlug={traceSlug}/>
            <Layout.Title data-test-id="trace-header">
              {(0, locale_1.t)('Trace ID: %s', traceSlug)}
            </Layout.Title>
          </Layout.HeaderContent>
          <Layout.HeaderActions>
            <buttonBar_1.default gap={1}>
              <discoverButton_1.default to={traceEventView.getResultsViewUrlTarget(organization.slug)}>
                Open in Discover
              </discoverButton_1.default>
            </buttonBar_1.default>
          </Layout.HeaderActions>
        </Layout.Header>
        <Layout.Body>
          <Layout.Main fullWidth>{this.renderContent()}</Layout.Main>
        </Layout.Body>
      </React.Fragment>);
    }
}
exports.default = TraceDetailsContent;
//# sourceMappingURL=content.jsx.map