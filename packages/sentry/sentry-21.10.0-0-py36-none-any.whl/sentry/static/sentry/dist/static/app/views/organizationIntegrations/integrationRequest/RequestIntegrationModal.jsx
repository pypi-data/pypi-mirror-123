Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const indicator_1 = require("app/actionCreators/indicator");
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const locale_1 = require("app/locale");
const integrationUtil_1 = require("app/utils/integrationUtil");
const textareaField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/textareaField"));
const textBlock_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/text/textBlock"));
/**
 * This modal serves as a non-owner's confirmation step before sending
 * organization owners an email requesting a new organization integration. It
 * lets the user attach an optional message to be included in the email.
 */
class RequestIntegrationModal extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.state = Object.assign(Object.assign({}, this.getDefaultState()), { isSending: false, message: '' });
        this.sendRequest = () => {
            const { organization, slug, type } = this.props;
            const { message } = this.state;
            (0, integrationUtil_1.trackIntegrationAnalytics)('integrations.request_install', {
                integration_type: type,
                integration: slug,
                organization,
            });
            const endpoint = `/organizations/${organization.slug}/integration-requests/`;
            this.api.request(endpoint, {
                method: 'POST',
                data: {
                    providerSlug: slug,
                    providerType: type,
                    message,
                },
                success: this.handleSubmitSuccess,
                error: this.handleSubmitError,
            });
        };
        this.handleSubmitSuccess = () => {
            const { closeModal, onSuccess } = this.props;
            (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Request successfully sent.'));
            this.setState({ isSending: false });
            onSuccess();
            closeModal();
        };
        this.handleSubmitError = () => {
            (0, indicator_1.addErrorMessage)('Error sending the request');
            this.setState({ isSending: false });
        };
    }
    render() {
        const { Header, Body, Footer, name } = this.props;
        const buttonText = this.state.isSending ? (0, locale_1.t)('Sending Request') : (0, locale_1.t)('Send Request');
        return (<react_1.Fragment>
        <Header>
          <h4>{(0, locale_1.t)('Request %s Installation', name)}</h4>
        </Header>
        <Body>
          <textBlock_1.default>
            {(0, locale_1.t)('Looks like your organization owner, manager, or admin needs to install %s. Want to send them a request?', name)}
          </textBlock_1.default>
          <textBlock_1.default>
            {(0, locale_1.t)('(Optional) You’ve got good reasons for installing the %s Integration. Share them with your organization owner.', name)}
          </textBlock_1.default>
          <textareaField_1.default inline={false} flexibleControlStateSize stacked name="message" type="string" onChange={value => this.setState({ message: value })} placeholder={(0, locale_1.t)('Optional message…')}/>
          <textBlock_1.default>
            {(0, locale_1.t)('When you click “Send Request”, we’ll email your request to your organization’s owners. So just keep that in mind.')}
          </textBlock_1.default>
        </Body>
        <Footer>
          <button_1.default onClick={this.sendRequest}>{buttonText}</button_1.default>
        </Footer>
      </react_1.Fragment>);
    }
}
exports.default = RequestIntegrationModal;
//# sourceMappingURL=RequestIntegrationModal.jsx.map