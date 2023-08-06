Object.defineProperty(exports, "__esModule", { value: true });
const react_1 = require("react");
const callIfFunction_1 = require("app/utils/callIfFunction");
class ScrollToTop extends react_1.Component {
    componentDidUpdate(prevProps) {
        const { disable, location } = this.props;
        const shouldDisable = (0, callIfFunction_1.callIfFunction)(disable, location, prevProps.location);
        if (!shouldDisable && this.props.location !== prevProps.location) {
            window.scrollTo(0, 0);
        }
    }
    render() {
        return this.props.children;
    }
}
exports.default = ScrollToTop;
//# sourceMappingURL=scrollToTop.jsx.map