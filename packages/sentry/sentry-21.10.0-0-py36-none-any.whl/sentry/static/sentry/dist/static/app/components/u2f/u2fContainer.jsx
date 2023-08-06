Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const u2fsign_1 = (0, tslib_1.__importDefault)(require("./u2fsign"));
class U2fContainer extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            authenticators: [],
        };
    }
    componentDidMount() {
        this.getAuthenticators();
    }
    getAuthenticators() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api } = this.props;
            try {
                const authenticators = yield api.requestPromise('/authenticators/');
                this.setState({ authenticators: authenticators !== null && authenticators !== void 0 ? authenticators : [] });
            }
            catch (_a) {
                // ignore errors
            }
        });
    }
    render() {
        const { className } = this.props;
        const { authenticators } = this.state;
        if (!authenticators.length) {
            return null;
        }
        return (<div className={className}>
        {authenticators.map(auth => auth.id === 'u2f' && auth.challenge ? (<u2fsign_1.default key={auth.id} {...this.props} challengeData={auth.challenge}/>) : null)}
      </div>);
    }
}
exports.default = (0, withApi_1.default)(U2fContainer);
//# sourceMappingURL=u2fContainer.jsx.map