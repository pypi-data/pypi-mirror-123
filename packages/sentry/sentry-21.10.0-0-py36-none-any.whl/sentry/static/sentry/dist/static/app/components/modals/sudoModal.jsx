Object.defineProperty(exports, "__esModule", { value: true });
exports.SudoModal = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const u2fContainer_1 = (0, tslib_1.__importDefault)(require("app/components/u2f/u2fContainer"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const inputField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/inputField"));
const textBlock_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/text/textBlock"));
class SudoModal extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            error: false,
            busy: false,
        };
        this.handleSuccess = () => {
            const { closeModal, superuser, location, router, retryRequest } = this.props;
            if (!retryRequest) {
                closeModal();
                return;
            }
            if (superuser) {
                router.replace({ pathname: location.pathname, state: { forceUpdate: new Date() } });
                return;
            }
            this.setState({ busy: true }, () => {
                retryRequest().then(() => {
                    this.setState({ busy: false }, closeModal);
                });
            });
        };
        this.handleError = () => {
            this.setState({ busy: false, error: true });
        };
        this.handleU2fTap = (data) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            this.setState({ busy: true });
            const { api } = this.props;
            try {
                yield api.requestPromise('/auth/', { method: 'PUT', data });
                this.handleSuccess();
            }
            catch (err) {
                this.setState({ busy: false });
                // u2fInterface relies on this
                throw err;
            }
        });
    }
    renderBodyContent() {
        const { superuser } = this.props;
        const { error } = this.state;
        const user = configStore_1.default.get('user');
        if (!user.hasPasswordAuth) {
            return (<React.Fragment>
          <textBlock_1.default>{(0, locale_1.t)('You will need to reauthenticate to continue.')}</textBlock_1.default>
          <button_1.default priority="primary" href={`/auth/login/?next=${encodeURIComponent(location.pathname)}`}>
            {(0, locale_1.t)('Continue')}
          </button_1.default>
        </React.Fragment>);
        }
        return (<React.Fragment>
        <StyledTextBlock>
          {superuser
                ? (0, locale_1.t)('You are attempting to access a resource that requires superuser access, please re-authenticate as a superuser.')
                : (0, locale_1.t)('Help us keep your account safe by confirming your identity.')}
        </StyledTextBlock>

        {error && (<StyledAlert type="error" icon={<icons_1.IconFlag size="md"/>}>
            {(0, locale_1.t)('Incorrect password')}
          </StyledAlert>)}

        <form_1.default apiMethod="PUT" apiEndpoint="/auth/" submitLabel={(0, locale_1.t)('Confirm Password')} onSubmitSuccess={this.handleSuccess} onSubmitError={this.handleError} hideFooter={!user.hasPasswordAuth} resetOnError>
          <StyledInputField type="password" inline={false} label={(0, locale_1.t)('Password')} name="password" autoFocus flexibleControlStateSize/>
          <u2fContainer_1.default displayMode="sudo" onTap={this.handleU2fTap}/>
        </form_1.default>
      </React.Fragment>);
    }
    render() {
        const { Header, Body } = this.props;
        return (<React.Fragment>
        <Header closeButton>{(0, locale_1.t)('Confirm Password to Continue')}</Header>
        <Body>{this.renderBodyContent()}</Body>
      </React.Fragment>);
    }
}
exports.SudoModal = SudoModal;
exports.default = (0, react_router_1.withRouter)((0, withApi_1.default)(SudoModal));
const StyledTextBlock = (0, styled_1.default)(textBlock_1.default) `
  margin-bottom: ${(0, space_1.default)(1)};
`;
const StyledInputField = (0, styled_1.default)(inputField_1.default) `
  padding-left: 0;
`;
const StyledAlert = (0, styled_1.default)(alert_1.default) `
  margin-bottom: 0;
`;
//# sourceMappingURL=sudoModal.jsx.map