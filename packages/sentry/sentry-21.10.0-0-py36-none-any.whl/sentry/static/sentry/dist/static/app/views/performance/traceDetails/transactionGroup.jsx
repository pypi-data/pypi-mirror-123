Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const scrollbarManager_1 = require("app/components/events/interfaces/spans/scrollbarManager");
const transactionBar_1 = (0, tslib_1.__importDefault)(require("./transactionBar"));
class TransactionGroup extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            isExpanded: true,
        };
        this.toggleExpandedState = () => {
            this.setState(({ isExpanded }) => ({ isExpanded: !isExpanded }));
        };
    }
    componentDidUpdate(_prevProps, prevState) {
        if (prevState.isExpanded !== this.state.isExpanded) {
            this.props.updateScrollState();
        }
    }
    render() {
        const { location, organization, transaction, traceInfo, continuingDepths, isOrphan, isLast, index, isVisible, hasGuideAnchor, renderedChildren, barColor, } = this.props;
        const { isExpanded } = this.state;
        return (<React.Fragment>
        <transactionBar_1.default location={location} organization={organization} index={index} transaction={transaction} traceInfo={traceInfo} continuingDepths={continuingDepths} isOrphan={isOrphan} isLast={isLast} isExpanded={isExpanded} toggleExpandedState={this.toggleExpandedState} isVisible={isVisible} hasGuideAnchor={hasGuideAnchor} barColor={barColor}/>
        {isExpanded && renderedChildren}
      </React.Fragment>);
    }
}
exports.default = (0, scrollbarManager_1.withScrollbarManager)(TransactionGroup);
//# sourceMappingURL=transactionGroup.jsx.map