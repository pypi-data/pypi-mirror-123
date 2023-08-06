Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const utils_1 = require("@sentry/utils");
const account_1 = require("app/actionCreators/account");
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const narrowLayout_1 = (0, tslib_1.__importDefault)(require("app/components/narrowLayout"));
const locale_1 = require("app/locale");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
class AcceptOrganizationInvite extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.handleLogout = (e) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            e.preventDefault();
            yield (0, account_1.logout)(this.api);
            window.location.replace(this.makeNextUrl('/auth/login/'));
        });
        this.handleAcceptInvite = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { memberId, token } = this.props.params;
            this.setState({ accepting: true });
            try {
                yield this.api.requestPromise(`/accept-invite/${memberId}/${token}/`, {
                    method: 'POST',
                });
                react_router_1.browserHistory.replace(`/${this.state.inviteDetails.orgSlug}/`);
            }
            catch (_a) {
                this.setState({ acceptError: true });
            }
            this.setState({ accepting: false });
        });
    }
    getEndpoints() {
        const { memberId, token } = this.props.params;
        return [['inviteDetails', `/accept-invite/${memberId}/${token}/`]];
    }
    getTitle() {
        return (0, locale_1.t)('Accept Organization Invite');
    }
    makeNextUrl(path) {
        return `${path}?${(0, utils_1.urlEncode)({ next: window.location.pathname })}`;
    }
    get existingMemberAlert() {
        const user = configStore_1.default.get('user');
        return (<alert_1.default type="warning" data-test-id="existing-member">
        {(0, locale_1.tct)('Your account ([email]) is already a member of this organization. [switchLink:Switch accounts]?', {
                email: user.email,
                switchLink: (<link_1.default to="" data-test-id="existing-member-link" onClick={this.handleLogout}/>),
            })}
      </alert_1.default>);
    }
    get authenticationActions() {
        const { inviteDetails } = this.state;
        return (<react_1.Fragment>
        {!inviteDetails.requireSso && (<p data-test-id="action-info-general">
            {(0, locale_1.t)(`To continue, you must either create a new account, or login to an
              existing Sentry account.`)}
          </p>)}

        {inviteDetails.needsSso && (<p data-test-id="action-info-sso">
            {inviteDetails.requireSso
                    ? (0, locale_1.tct)(`Note that [orgSlug] has required Single Sign-On (SSO) using
               [authProvider]. You may create an account by authenticating with
               the organization's SSO provider.`, {
                        orgSlug: <strong>{inviteDetails.orgSlug}</strong>,
                        authProvider: inviteDetails.ssoProvider,
                    })
                    : (0, locale_1.tct)(`Note that [orgSlug] has enabled Single Sign-On (SSO) using
               [authProvider]. You may create an account by authenticating with
               the organization's SSO provider.`, {
                        orgSlug: <strong>{inviteDetails.orgSlug}</strong>,
                        authProvider: inviteDetails.ssoProvider,
                    })}
          </p>)}

        <Actions>
          <ActionsLeft>
            {inviteDetails.needsSso && (<button_1.default label="sso-login" priority="primary" href={this.makeNextUrl(`/auth/login/${inviteDetails.orgSlug}/`)}>
                {(0, locale_1.t)('Join with %s', inviteDetails.ssoProvider)}
              </button_1.default>)}
            {!inviteDetails.requireSso && (<button_1.default label="create-account" priority="primary" href={this.makeNextUrl('/auth/register/')}>
                {(0, locale_1.t)('Create a new account')}
              </button_1.default>)}
          </ActionsLeft>
          {!inviteDetails.requireSso && (<externalLink_1.default href={this.makeNextUrl('/auth/login/')} openInNewTab={false} data-test-id="link-with-existing">
              {(0, locale_1.t)('Login using an existing account')}
            </externalLink_1.default>)}
        </Actions>
      </react_1.Fragment>);
    }
    get warning2fa() {
        const { inviteDetails } = this.state;
        return (<react_1.Fragment>
        <p data-test-id="2fa-warning">
          {(0, locale_1.tct)('To continue, [orgSlug] requires all members to configure two-factor authentication.', { orgSlug: inviteDetails.orgSlug })}
        </p>
        <Actions>
          <button_1.default priority="primary" to="/settings/account/security/">
            {(0, locale_1.t)('Configure Two-Factor Auth')}
          </button_1.default>
        </Actions>
      </react_1.Fragment>);
    }
    get warningEmailVerification() {
        const { inviteDetails } = this.state;
        return (<react_1.Fragment>
        <p data-test-id="email-verification-warning">
          {(0, locale_1.tct)('To continue, [orgSlug] requires all members to verify their email address.', { orgSlug: inviteDetails.orgSlug })}
        </p>
        <Actions>
          <button_1.default priority="primary" to="/settings/account/emails/">
            {(0, locale_1.t)('Verify Email Address')}
          </button_1.default>
        </Actions>
      </react_1.Fragment>);
    }
    get acceptActions() {
        const { inviteDetails, accepting } = this.state;
        return (<Actions>
        <button_1.default label="join-organization" priority="primary" disabled={accepting} onClick={this.handleAcceptInvite}>
          {(0, locale_1.t)('Join the %s organization', inviteDetails.orgSlug)}
        </button_1.default>
      </Actions>);
    }
    renderError() {
        return (<narrowLayout_1.default>
        <alert_1.default type="warning">
          {(0, locale_1.t)('This organization invite link is no longer valid.')}
        </alert_1.default>
      </narrowLayout_1.default>);
    }
    renderBody() {
        const { inviteDetails, acceptError } = this.state;
        return (<narrowLayout_1.default>
        <settingsPageHeader_1.default title={(0, locale_1.t)('Accept organization invite')}/>
        {acceptError && (<alert_1.default type="error">
            {(0, locale_1.t)('Failed to join this organization. Please try again')}
          </alert_1.default>)}
        <InviteDescription data-test-id="accept-invite">
          {(0, locale_1.tct)('[orgSlug] is using Sentry to track and debug errors.', {
                orgSlug: <strong>{inviteDetails.orgSlug}</strong>,
            })}
        </InviteDescription>
        {inviteDetails.needsAuthentication
                ? this.authenticationActions
                : inviteDetails.existingMember
                    ? this.existingMemberAlert
                    : inviteDetails.needs2fa
                        ? this.warning2fa
                        : inviteDetails.needsEmailVerification
                            ? this.warningEmailVerification
                            : inviteDetails.needsSso
                                ? this.authenticationActions
                                : this.acceptActions}
      </narrowLayout_1.default>);
    }
}
const Actions = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: ${(0, space_1.default)(3)};
`;
const ActionsLeft = (0, styled_1.default)('span') `
  > a {
    margin-right: ${(0, space_1.default)(1)};
  }
`;
const InviteDescription = (0, styled_1.default)('p') `
  font-size: 1.2em;
`;
exports.default = AcceptOrganizationInvite;
//# sourceMappingURL=acceptOrganizationInvite.jsx.map