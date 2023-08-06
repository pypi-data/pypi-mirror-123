Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const account_1 = require("app/actionCreators/account");
const api_1 = require("app/api");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
class NarrowLayout extends react_1.Component {
    constructor() {
        super(...arguments);
        this.api = new api_1.Client();
        this.handleLogout = () => {
            (0, account_1.logout)(this.api).then(() => window.location.assign('/auth/login'));
        };
    }
    UNSAFE_componentWillMount() {
        document.body.classList.add('narrow');
    }
    componentWillUnmount() {
        this.api.clear();
        document.body.classList.remove('narrow');
    }
    render() {
        return (<div className="app">
        <div className="pattern-bg"/>
        <div className="container" style={{ maxWidth: this.props.maxWidth }}>
          <div className="box box-modal">
            <div className="box-header">
              <a href="/">
                <icons_1.IconSentry size="lg"/>
              </a>
              {this.props.showLogout && (<a className="logout pull-right" onClick={this.handleLogout}>
                  <Logout>{(0, locale_1.t)('Sign out')}</Logout>
                </a>)}
            </div>
            <div className="box-content with-padding">{this.props.children}</div>
          </div>
        </div>
      </div>);
    }
}
const Logout = (0, styled_1.default)('span') `
  font-size: 16px;
`;
exports.default = NarrowLayout;
//# sourceMappingURL=narrowLayout.jsx.map