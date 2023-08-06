Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_dom_1 = (0, tslib_1.__importDefault)(require("react-dom"));
const ASPECT_RATIO = 16 / 9;
class SessionStackContextType extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            showIframe: false,
        };
        this.getTitle = () => 'SessionStack';
    }
    componentDidMount() {
        // eslint-disable-next-line react/no-find-dom-node
        const domNode = react_dom_1.default.findDOMNode(this);
        this.parentNode = domNode.parentNode;
        window.addEventListener('resize', () => this.setIframeSize(), false);
        this.setIframeSize();
    }
    componentWillUnmount() {
        window.removeEventListener('resize', () => this.setIframeSize(), false);
    }
    setIframeSize() {
        if (this.state.showIframe || !this.parentNode) {
            return;
        }
        const parentWidth = this.parentNode.clientWidth;
        this.setState({
            width: parentWidth,
            height: parentWidth / ASPECT_RATIO,
        });
    }
    playSession() {
        this.setState({
            showIframe: true,
        });
        this.setIframeSize();
    }
    render() {
        const { session_url } = this.props.data;
        if (!session_url) {
            return <h4>Session not found.</h4>;
        }
        return (<div className="panel-group">
        {this.state.showIframe ? (<iframe src={session_url} sandbox="allow-scripts allow-same-origin" width={this.state.width} height={this.state.height}/>) : (<button className="btn btn-default" type="button" onClick={() => this.playSession()}>
            Play session
          </button>)}
      </div>);
    }
}
exports.default = SessionStackContextType;
//# sourceMappingURL=sessionstack.jsx.map