Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const locale_1 = require("app/locale");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
class SetupWizard extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            finished: false,
        };
    }
    UNSAFE_componentWillMount() {
        this.pollFinished();
    }
    pollFinished() {
        return new Promise(resolve => {
            this.props.api.request(`/wizard/${this.props.hash}/`, {
                method: 'GET',
                success: () => {
                    setTimeout(() => this.pollFinished(), 1000);
                },
                error: () => {
                    resolve();
                    this.setState({ finished: true });
                    setTimeout(() => window.close(), 10000);
                },
            });
        });
    }
    renderSuccess() {
        return (<div className="row">
        <h5>{(0, locale_1.t)('Return to your terminal to complete your setup')}</h5>
        <h5>{(0, locale_1.t)('(This window will close in 10 seconds)')}</h5>
        <button className="btn btn-default" onClick={() => window.close()}>
          Close browser tab
        </button>
      </div>);
    }
    renderLoading() {
        return (<div className="row">
        <h5>{(0, locale_1.t)('Waiting for wizard to connect')}</h5>
      </div>);
    }
    render() {
        const { finished } = this.state;
        return (<div className="container">
        <loadingIndicator_1.default style={{ margin: '2em auto' }} finished={finished}>
          {finished ? this.renderSuccess() : this.renderLoading()}
        </loadingIndicator_1.default>
      </div>);
    }
}
SetupWizard.defaultProps = {
    hash: false,
};
exports.default = (0, withApi_1.default)(SetupWizard);
//# sourceMappingURL=index.jsx.map