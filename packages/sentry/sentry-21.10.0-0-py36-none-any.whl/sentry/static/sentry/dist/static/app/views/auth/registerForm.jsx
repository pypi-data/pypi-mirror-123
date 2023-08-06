Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const react_2 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const form_1 = (0, tslib_1.__importDefault)(require("app/components/forms/form"));
const passwordField_1 = (0, tslib_1.__importDefault)(require("app/components/forms/passwordField"));
const radioBooleanField_1 = (0, tslib_1.__importDefault)(require("app/components/forms/radioBooleanField"));
const textField_1 = (0, tslib_1.__importDefault)(require("app/components/forms/textField"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const locale_1 = require("app/locale");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const login_1 = require("app/views/auth/login");
const SubscribeField = () => (<radioBooleanField_1.default name="subscribe" yesLabel={(0, locale_1.t)('Yes, I would like to receive updates via email')} noLabel={(0, locale_1.t)("No, I'd prefer not to receive these updates")} help={(0, locale_1.tct)(`We'd love to keep you updated via email with product and feature
           announcements, promotions, educational materials, and events. Our
           updates focus on relevant information, and we'll never sell your data
           to third parties. See our [link] for more details.`, {
        link: <a href="https://sentry.io/privacy/">Privacy Policy</a>,
    })}/>);
class RegisterForm extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            errorMessage: null,
            errors: {},
        };
        this.handleSubmit = (data, onSuccess, onError) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api } = this.props;
            try {
                const response = yield api.requestPromise('/auth/register/', {
                    method: 'POST',
                    data,
                });
                onSuccess(data);
                // TODO(epurkhiser): There is more we need to do to setup the user. but
                // definitely primarily we need to init our user.
                configStore_1.default.set('user', response.user);
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
        const { hasNewsletter } = this.props.authConfig;
        const { errorMessage, errors } = this.state;
        return (<react_2.ClassNames>
        {({ css }) => (<form_1.default initialData={{ subscribe: true }} submitLabel={(0, locale_1.t)('Continue')} onSubmit={this.handleSubmit} footerClass={css `
              ${login_1.formFooterClass}
            `} errorMessage={errorMessage} extraButton={<PrivacyPolicyLink href="https://sentry.io/privacy/">
                {(0, locale_1.t)('Privacy Policy')}
              </PrivacyPolicyLink>}>
            <textField_1.default name="name" placeholder={(0, locale_1.t)('Jane Bloggs')} label={(0, locale_1.t)('Name')} error={errors.name} required/>
            <textField_1.default name="username" placeholder={(0, locale_1.t)('you@example.com')} label={(0, locale_1.t)('Email')} error={errors.username} required/>
            <passwordField_1.default name="password" placeholder={(0, locale_1.t)('something super secret')} label={(0, locale_1.t)('Password')} error={errors.password} required/>
            {hasNewsletter && <SubscribeField />}
          </form_1.default>)}
      </react_2.ClassNames>);
    }
}
const PrivacyPolicyLink = (0, styled_1.default)(externalLink_1.default) `
  color: ${p => p.theme.gray300};

  &:hover {
    color: ${p => p.theme.textColor};
  }
`;
exports.default = RegisterForm;
//# sourceMappingURL=registerForm.jsx.map