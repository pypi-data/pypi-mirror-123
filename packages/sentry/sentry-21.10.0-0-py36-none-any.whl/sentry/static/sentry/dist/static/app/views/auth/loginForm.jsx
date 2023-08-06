Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const react_2 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const form_1 = (0, tslib_1.__importDefault)(require("app/components/forms/form"));
const passwordField_1 = (0, tslib_1.__importDefault)(require("app/components/forms/passwordField"));
const textField_1 = (0, tslib_1.__importDefault)(require("app/components/forms/textField"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const login_1 = require("app/views/auth/login");
// TODO(epurkhiser): The abstraction here would be much nicer if we just
// exposed a configuration object telling us what auth providers there are.
const LoginProviders = ({ vstsLoginLink, githubLoginLink, googleLoginLink, }) => (<ProviderWrapper>
    <ProviderHeading>{(0, locale_1.t)('External Account Login')}</ProviderHeading>
    {googleLoginLink && (<button_1.default align="left" size="small" icon={<icons_1.IconGoogle size="xs"/>} href={googleLoginLink}>
        {(0, locale_1.t)('Sign in with Google')}
      </button_1.default>)}
    {githubLoginLink && (<button_1.default align="left" size="small" icon={<icons_1.IconGithub size="xs"/>} href={githubLoginLink}>
        {(0, locale_1.t)('Sign in with GitHub')}
      </button_1.default>)}
    {vstsLoginLink && (<button_1.default align="left" size="small" icon={<icons_1.IconVsts size="xs"/>} href={vstsLoginLink}>
        {(0, locale_1.t)('Sign in with Azure DevOps')}
      </button_1.default>)}
  </ProviderWrapper>);
class LoginForm extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            errorMessage: null,
            errors: {},
        };
        this.handleSubmit = (data, onSuccess, onError) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            try {
                const response = yield this.props.api.requestPromise('/auth/login/', {
                    method: 'POST',
                    data,
                });
                onSuccess(data);
                // TODO(epurkhiser): There is likely more that needs to happen to update
                // the application state after user login.
                configStore_1.default.set('user', response.user);
                // TODO(epurkhiser): Reconfigure sentry SDK identity
                react_router_1.browserHistory.push({ pathname: response.nextUri });
            }
            catch (e) {
                if (!e.responseJSON || !e.responseJSON.errors) {
                    onError(e);
                    return;
                }
                let message = e.responseJSON.detail;
                if (e.responseJSON.errors.__all__) {
                    message = e.responseJSON.errors.__all__;
                }
                this.setState({
                    errorMessage: message,
                    errors: e.responseJSON.errors || {},
                });
                onError(e);
            }
        });
    }
    render() {
        const { errorMessage, errors } = this.state;
        const { githubLoginLink, vstsLoginLink } = this.props.authConfig;
        const hasLoginProvider = !!(githubLoginLink || vstsLoginLink);
        return (<react_2.ClassNames>
        {({ css }) => (<FormWrapper hasLoginProvider={hasLoginProvider}>
            <form_1.default submitLabel={(0, locale_1.t)('Continue')} onSubmit={this.handleSubmit} footerClass={css `
                ${login_1.formFooterClass}
              `} errorMessage={errorMessage} extraButton={<LostPasswordLink to="/account/recover/">
                  {(0, locale_1.t)('Lost your password?')}
                </LostPasswordLink>}>
              <textField_1.default name="username" placeholder={(0, locale_1.t)('username or email')} label={(0, locale_1.t)('Account')} error={errors.username} required/>
              <passwordField_1.default name="password" placeholder={(0, locale_1.t)('password')} label={(0, locale_1.t)('Password')} error={errors.password} required/>
            </form_1.default>
            {hasLoginProvider && <LoginProviders {...{ vstsLoginLink, githubLoginLink }}/>}
          </FormWrapper>)}
      </react_2.ClassNames>);
    }
}
const FormWrapper = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: 60px;
  grid-template-columns: ${p => (p.hasLoginProvider ? '1fr 0.8fr' : '1fr')};
`;
const ProviderHeading = (0, styled_1.default)('div') `
  margin: 0;
  font-size: 15px;
  font-weight: bold;
  line-height: 24px;
`;
const ProviderWrapper = (0, styled_1.default)('div') `
  position: relative;
  display: grid;
  grid-auto-rows: max-content;
  grid-gap: ${(0, space_1.default)(1.5)};

  &:before {
    position: absolute;
    display: block;
    content: '';
    top: 0;
    bottom: 0;
    left: -30px;
    border-left: 1px solid ${p => p.theme.border};
  }
`;
const LostPasswordLink = (0, styled_1.default)(link_1.default) `
  color: ${p => p.theme.gray300};

  &:hover {
    color: ${p => p.theme.textColor};
  }
`;
exports.default = LoginForm;
//# sourceMappingURL=loginForm.jsx.map