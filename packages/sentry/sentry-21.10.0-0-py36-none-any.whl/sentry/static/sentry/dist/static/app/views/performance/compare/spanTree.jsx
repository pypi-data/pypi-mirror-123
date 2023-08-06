Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const DividerHandlerManager = (0, tslib_1.__importStar)(require("app/components/events/interfaces/spans/dividerHandlerManager"));
const spanGroup_1 = (0, tslib_1.__importDefault)(require("./spanGroup"));
const utils_1 = require("./utils");
class SpanTree extends react_1.Component {
    constructor() {
        super(...arguments);
        this.traceViewRef = (0, react_1.createRef)();
    }
    renderSpan({ span, childSpans, spanNumber, treeDepth, continuingTreeDepths, isLast, isRoot, generateBounds, }) {
        var _a;
        const spanChildren = (_a = childSpans === null || childSpans === void 0 ? void 0 : childSpans[(0, utils_1.getSpanID)(span)]) !== null && _a !== void 0 ? _a : [];
        // Mark descendents as being rendered. This is to address potential recursion issues due to malformed data.
        // For example if a span has a span_id that's identical to its parent_span_id.
        childSpans = Object.assign({}, childSpans);
        delete childSpans[(0, utils_1.getSpanID)(span)];
        const treeDepthEntry = (0, utils_1.isOrphanDiffSpan)(span)
            ? { type: 'orphan', depth: treeDepth }
            : treeDepth;
        const treeArr = isLast
            ? continuingTreeDepths
            : [...continuingTreeDepths, treeDepthEntry];
        const reduced = spanChildren.reduce((acc, spanChild, index) => {
            const key = `${(0, utils_1.getSpanID)(spanChild)}`;
            const results = this.renderSpan({
                spanNumber: acc.nextSpanNumber,
                isLast: index + 1 === spanChildren.length,
                isRoot: false,
                span: spanChild,
                childSpans,
                continuingTreeDepths: treeArr,
                treeDepth: treeDepth + 1,
                generateBounds,
            });
            acc.renderedSpanChildren.push(<react_1.Fragment key={key}>{results.spanTree}</react_1.Fragment>);
            acc.nextSpanNumber = results.nextSpanNumber;
            return acc;
        }, {
            renderedSpanChildren: [],
            nextSpanNumber: spanNumber + 1,
        });
        const spanTree = (<react_1.Fragment>
        <spanGroup_1.default spanNumber={spanNumber} span={span} renderedSpanChildren={reduced.renderedSpanChildren} treeDepth={treeDepth} continuingTreeDepths={continuingTreeDepths} isRoot={isRoot} isLast={isLast} numOfSpanChildren={spanChildren.length} generateBounds={generateBounds}/>
      </react_1.Fragment>);
        return {
            nextSpanNumber: reduced.nextSpanNumber,
            spanTree,
        };
    }
    renderRootSpans() {
        const { baselineEvent, regressionEvent } = this.props;
        const comparisonReport = (0, utils_1.diffTransactions)({
            baselineEvent,
            regressionEvent,
        });
        const { rootSpans, childSpans } = comparisonReport;
        const generateBounds = (0, utils_1.boundsGenerator)(rootSpans);
        let nextSpanNumber = 1;
        const spanTree = (<react_1.Fragment key="root-spans-tree">
        {rootSpans.map((rootSpan, index) => {
                const renderedRootSpan = this.renderSpan({
                    isLast: index + 1 === rootSpans.length,
                    isRoot: true,
                    span: rootSpan,
                    childSpans,
                    spanNumber: nextSpanNumber,
                    treeDepth: 0,
                    continuingTreeDepths: [],
                    generateBounds,
                });
                nextSpanNumber = renderedRootSpan.nextSpanNumber;
                return <react_1.Fragment key={String(index)}>{renderedRootSpan.spanTree}</react_1.Fragment>;
            })}
      </react_1.Fragment>);
        return {
            spanTree,
            nextSpanNumber,
        };
    }
    render() {
        const { spanTree } = this.renderRootSpans();
        return (<DividerHandlerManager.Provider interactiveLayerRef={this.traceViewRef}>
        <TraceViewContainer ref={this.traceViewRef}>{spanTree}</TraceViewContainer>
      </DividerHandlerManager.Provider>);
    }
}
const TraceViewContainer = (0, styled_1.default)('div') `
  overflow-x: hidden;
  border-bottom-left-radius: 3px;
  border-bottom-right-radius: 3px;
`;
exports.default = SpanTree;
//# sourceMappingURL=spanTree.jsx.map