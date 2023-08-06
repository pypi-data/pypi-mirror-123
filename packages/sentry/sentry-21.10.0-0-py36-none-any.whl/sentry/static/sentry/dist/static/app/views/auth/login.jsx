Object.defineProperty(exports, "__esModule", { value: true });
exports.formFooterClass = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const navTabs_1 = (0, tslib_1.__importDefault)(require("app/components/navTabs"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const loginForm_1 = (0, tslib_1.__importDefault)(require("./loginForm"));
const registerForm_1 = (0, tslib_1.__importDefault)(require("./registerForm"));
const ssoForm_1 = (0, tslib_1.__importDefault)(require("./ssoForm"));
const FORM_COMPONENTS = {
    login: loginForm_1.default,
    register: registerForm_1.default,
    sso: ssoForm_1.default,
};
class Login extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            loading: true,
            error: null,
            activeTab: 'login',
            authConfig: null,
        };
        this.handleSetTab = (activeTab, event) => {
            this.setState({ activeTab });
            event.preventDefault();
        };
        this.fetchData = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api } = this.props;
            try {
                const response = yield api.requestPromise('/auth/config/');
                const { vsts_login_link, github_login_link, google_login_link } = response, config = (0, tslib_1.__rest)(response, ["vsts_login_link", "github_login_link", "google_login_link"]);
                const authConfig = Object.assign(Object.assign({}, config), { vstsLoginLink: vsts_login_link, githubLoginLink: github_login_link, googleLoginLink: google_login_link });
                this.setState({ authConfig });
            }
            catch (e) {
                this.setState({ error: true });
            }
            this.setState({ loading: false });
        });
    }
    componentDidMount() {
        this.fetchData();
    }
    get hasAuthProviders() {
        if (this.state.authConfig === null) {
            return false;
        }
        const { githubLoginLink, googleLoginLink, vstsLoginLink } = this.state.authConfig;
        return !!(githubLoginLink || vstsLoginLink || googleLoginLink);
    }
    render() {
        const { api } = this.props;
        const { loading, error, activeTab, authConfig } = this.state;
        const FormComponent = FORM_COMPONENTS[activeTab];
        const tabs = [
            ['login', (0, locale_1.t)('Login')],
            ['sso', (0, locale_1.t)('Single Sign-On')],
            ['register', (0, locale_1.t)('Register'), !(authConfig === null || authConfig === void 0 ? void 0 : authConfig.canRegister)],
        ];
        const renderTab = ([key, label, disabled]) => !disabled && (<li key={key} className={activeTab === key ? 'active' : ''}>
          <a href="#" onClick={e => this.handleSetTab(key, e)}>
            {label}
          </a>
        </li>);
        return (<React.Fragment>
        <Header>
          <Heading>{(0, locale_1.t)('Sign in to continue')}</Heading>
          <AuthNavTabs>{tabs.map(renderTab)}</AuthNavTabs>
        </Header>
        {loading && <loadingIndicator_1.default />}
        {error && (<StyledLoadingError message={(0, locale_1.t)('Unable to load authentication configuration')} onRetry={this.fetchData}/>)}
        {!loading && authConfig !== null && !error && (<FormWrapper hasAuthProviders={this.hasAuthProviders}>
            <FormComponent {...{ api, authConfig }}/>
          </FormWrapper>)}
      </React.Fragment>);
    }
}
const StyledLoadingError = (0, styled_1.default)(loadingError_1.default) `
  margin: ${(0, space_1.default)(2)};
`;
const Header = (0, styled_1.default)('div') `
  border-bottom: 1px solid ${p => p.theme.border};
  padding: 20px 40px 0;
`;
const Heading = (0, styled_1.default)('h3') `
  font-size: 24px;
  margin: 0 0 20px 0;
`;
const AuthNavTabs = (0, styled_1.default)(navTabs_1.default) `
  margin: 0;
`;
const FormWrapper = (0, styled_1.default)('div') `
  padding: 35px;
  width: ${p => (p.hasAuthProviders ? '600px' : '490px')};
`;
const formFooterClass = `
  display: grid;
  grid-template-columns: max-content 1fr;
  grid-gap: ${(0, space_1.default)(1)};
  align-items: center;
  justify-items: end;
  border-top: none;
  margin-bottom: 0;
  padding: 0;
`;
exports.formFooterClass = formFooterClass;
exports.default = (0, withApi_1.default)(Login);
//# sourceMappingURL=login.jsx.map