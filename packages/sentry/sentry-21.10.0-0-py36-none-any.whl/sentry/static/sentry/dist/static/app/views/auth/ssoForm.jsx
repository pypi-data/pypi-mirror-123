Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const form_1 = (0, tslib_1.__importDefault)(require("app/components/forms/form"));
const textField_1 = (0, tslib_1.__importDefault)(require("app/components/forms/textField"));
const locale_1 = require("app/locale");
class SsoForm extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            errorMessage: null,
        };
        this.handleSubmit = (data, onSuccess, onError) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api } = this.props;
            try {
                const response = yield api.requestPromise('/auth/sso-locate/', {
                    method: 'POST',
                    data,
                });
                onSuccess(data);
                react_router_1.browserHistory.push({ pathname: response.nextUri });
            }
            catch (e) {
                if (!e.responseJSON) {
                    onError(e);
                    return;
                }
                const message = e.responseJSON.detail;
                this.setState({ errorMessage: message });
                onError(e);
            }
        });
    }
    render() {
        const { serverHostname } = this.props.authConfig;
        const { errorMessage } = this.state;
        return (<form_1.default className="form-stacked" submitLabel={(0, locale_1.t)('Continue')} onSubmit={this.handleSubmit} footerClass="auth-footer" errorMessage={errorMessage}>
        <textField_1.default name="organization" placeholder="acme" label={(0, locale_1.t)('Organization ID')} required help={(0, locale_1.tct)('Your ID is the slug after the hostname. e.g. [example] is [slug].', {
                slug: <strong>acme</strong>,
                example: <SlugExample slug="acme" hostname={serverHostname}/>,
            })}/>
      </form_1.default>);
    }
}
const SlugExample = ({ hostname, slug }) => (<code>
    {hostname}/<strong>{slug}</strong>
  </code>);
exports.default = SsoForm;
//# sourceMappingURL=ssoForm.jsx.map