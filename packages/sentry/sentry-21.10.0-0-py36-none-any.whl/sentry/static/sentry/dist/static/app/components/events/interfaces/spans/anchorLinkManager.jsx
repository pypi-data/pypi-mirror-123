Object.defineProperty(exports, "__esModule", { value: true });
exports.Consumer = exports.Provider = void 0;
const tslib_1 = require("tslib");
const react_1 = (0, tslib_1.__importDefault)(require("react"));
const AnchorLinkManagerContext = react_1.default.createContext({
    registerScrollFn: () => () => undefined,
    scrollToHash: () => undefined,
});
class Provider extends react_1.default.Component {
    constructor() {
        super(...arguments);
        this.scrollFns = new Map();
        this.scrollToHash = (hash) => {
            var _a;
            (_a = this.scrollFns.get(hash)) === null || _a === void 0 ? void 0 : _a();
        };
        this.registerScrollFn = (hash, fn) => {
            this.scrollFns.set(hash, fn);
        };
    }
    componentDidMount() {
        this.scrollToHash(location.hash);
    }
    render() {
        const childrenProps = {
            registerScrollFn: this.registerScrollFn,
            scrollToHash: this.scrollToHash,
        };
        return (<AnchorLinkManagerContext.Provider value={childrenProps}>
        {this.props.children}
      </AnchorLinkManagerContext.Provider>);
    }
}
exports.Provider = Provider;
exports.Consumer = AnchorLinkManagerContext.Consumer;
//# sourceMappingURL=anchorLinkManager.jsx.map