Object.defineProperty(exports, "__esModule", { value: true });
exports.EmailAddresses = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const alertLink_1 = (0, tslib_1.__importDefault)(require("app/components/alertLink"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const panels_1 = require("app/components/panels");
const tag_1 = (0, tslib_1.__importDefault)(require("app/components/tag"));
const accountEmails_1 = (0, tslib_1.__importDefault)(require("app/data/forms/accountEmails"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const jsonForm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/jsonForm"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const ENDPOINT = '/users/me/emails/';
class AccountEmails extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.handleSubmitSuccess = (_change, model, id) => {
            if (id === undefined) {
                return;
            }
            model.setValue(id, '');
            this.remountComponent();
        };
    }
    getTitle() {
        return (0, locale_1.t)('Emails');
    }
    getEndpoints() {
        return [];
    }
    renderBody() {
        return (<React.Fragment>
        <settingsPageHeader_1.default title={(0, locale_1.t)('Email Addresses')}/>
        <EmailAddresses />
        <form_1.default apiMethod="POST" apiEndpoint={ENDPOINT} saveOnBlur allowUndo={false} onSubmitSuccess={this.handleSubmitSuccess}>
          <jsonForm_1.default forms={accountEmails_1.default}/>
        </form_1.default>

        <alertLink_1.default to="/settings/account/notifications" icon={<icons_1.IconStack />}>
          {(0, locale_1.t)('Want to change how many emails you get? Use the notifications panel.')}
        </alertLink_1.default>
      </React.Fragment>);
    }
}
exports.default = AccountEmails;
class EmailAddresses extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.handleSetPrimary = (email) => this.doApiCall(ENDPOINT, {
            method: 'PUT',
            data: { email },
        });
        this.handleRemove = (email) => this.doApiCall(ENDPOINT, {
            method: 'DELETE',
            data: { email },
        });
        this.handleVerify = (email) => this.doApiCall(`${ENDPOINT}confirm/`, {
            method: 'POST',
            data: { email },
        });
    }
    getEndpoints() {
        return [['emails', ENDPOINT]];
    }
    doApiCall(endpoint, requestParams) {
        this.setState({ loading: true, emails: [] }, () => this.api
            .requestPromise(endpoint, requestParams)
            .then(() => this.remountComponent())
            .catch(err => {
            var _a;
            this.remountComponent();
            if ((_a = err === null || err === void 0 ? void 0 : err.responseJSON) === null || _a === void 0 ? void 0 : _a.email) {
                (0, indicator_1.addErrorMessage)(err.responseJSON.email);
            }
        }));
    }
    render() {
        const { emails, loading } = this.state;
        const primary = emails === null || emails === void 0 ? void 0 : emails.find(({ isPrimary }) => isPrimary);
        const secondary = emails === null || emails === void 0 ? void 0 : emails.filter(({ isPrimary }) => !isPrimary);
        if (loading) {
            return (<panels_1.Panel>
          <panels_1.PanelHeader>{(0, locale_1.t)('Email Addresses')}</panels_1.PanelHeader>
          <panels_1.PanelBody>
            <loadingIndicator_1.default />
          </panels_1.PanelBody>
        </panels_1.Panel>);
        }
        return (<panels_1.Panel>
        <panels_1.PanelHeader>{(0, locale_1.t)('Email Addresses')}</panels_1.PanelHeader>
        <panels_1.PanelBody>
          {primary && (<EmailRow onRemove={this.handleRemove} onVerify={this.handleVerify} {...primary}/>)}

          {secondary === null || secondary === void 0 ? void 0 : secondary.map(emailObj => (<EmailRow key={emailObj.email} onSetPrimary={this.handleSetPrimary} onRemove={this.handleRemove} onVerify={this.handleVerify} {...emailObj}/>))}
        </panels_1.PanelBody>
      </panels_1.Panel>);
    }
}
exports.EmailAddresses = EmailAddresses;
const EmailRow = ({ email, onRemove, onVerify, onSetPrimary, isVerified, isPrimary, hideRemove, }) => (<EmailItem>
    <EmailTags>
      {email}
      {!isVerified && <tag_1.default type="warning">{(0, locale_1.t)('Unverified')}</tag_1.default>}
      {isPrimary && <tag_1.default type="success">{(0, locale_1.t)('Primary')}</tag_1.default>}
    </EmailTags>
    <buttonBar_1.default gap={1}>
      {!isPrimary && isVerified && (<button_1.default size="small" onClick={e => onSetPrimary === null || onSetPrimary === void 0 ? void 0 : onSetPrimary(email, e)}>
          {(0, locale_1.t)('Set as primary')}
        </button_1.default>)}
      {!isVerified && (<button_1.default size="small" onClick={e => onVerify(email, e)}>
          {(0, locale_1.t)('Resend verification')}
        </button_1.default>)}
      {!hideRemove && !isPrimary && (<button_1.default label={(0, locale_1.t)('Remove email')} data-test-id="remove" priority="danger" size="small" icon={<icons_1.IconDelete />} onClick={e => onRemove(email, e)}/>)}
    </buttonBar_1.default>
  </EmailItem>);
const EmailTags = (0, styled_1.default)('div') `
  display: grid;
  grid-auto-flow: column;
  grid-gap: ${(0, space_1.default)(1)};
  align-items: center;
`;
const EmailItem = (0, styled_1.default)(panels_1.PanelItem) `
  justify-content: space-between;
`;
//# sourceMappingURL=accountEmails.jsx.map