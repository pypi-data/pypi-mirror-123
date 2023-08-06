Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const spanBar_1 = (0, tslib_1.__importDefault)(require("./spanBar"));
class SpanGroup extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            showSpanTree: true,
        };
        this.toggleSpanTree = () => {
            this.setState(state => ({
                showSpanTree: !state.showSpanTree,
            }));
        };
    }
    renderSpanChildren() {
        if (!this.state.showSpanTree) {
            return null;
        }
        return this.props.renderedSpanChildren;
    }
    render() {
        const { span, treeDepth, continuingTreeDepths, spanNumber, isLast, isRoot, numOfSpanChildren, generateBounds, } = this.props;
        return (<react_1.Fragment>
        <spanBar_1.default span={span} treeDepth={treeDepth} continuingTreeDepths={continuingTreeDepths} spanNumber={spanNumber} isLast={isLast} isRoot={isRoot} numOfSpanChildren={numOfSpanChildren} showSpanTree={this.state.showSpanTree} toggleSpanTree={this.toggleSpanTree} generateBounds={generateBounds}/>
        {this.renderSpanChildren()}
      </react_1.Fragment>);
    }
}
exports.default = SpanGroup;
//# sourceMappingURL=spanGroup.jsx.map