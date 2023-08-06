Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
/**
 * AccountSecurityDetails is only displayed when user is enrolled in the 2fa method.
 * It displays created + last used time of the 2fa method.
 *
 * Also displays 2fa method specific details.
 */
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const circleIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/circleIndicator"));
const dateTime_1 = (0, tslib_1.__importDefault)(require("app/components/dateTime"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const recoveryCodes_1 = (0, tslib_1.__importDefault)(require("app/views/settings/account/accountSecurity/components/recoveryCodes"));
const removeConfirm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/account/accountSecurity/components/removeConfirm"));
const u2fEnrolledDetails_1 = (0, tslib_1.__importDefault)(require("app/views/settings/account/accountSecurity/components/u2fEnrolledDetails"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const textBlock_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/text/textBlock"));
const ENDPOINT = '/users/me/authenticators/';
function AuthenticatorDate({ label, date }) {
    return (<react_1.Fragment>
      <DateLabel>{label}</DateLabel>
      <div>{date ? <dateTime_1.default date={date}/> : (0, locale_1.t)('never')}</div>
    </react_1.Fragment>);
}
class AccountSecurityDetails extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.handleRemove = (device) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { authenticator } = this.state;
            if (!authenticator || !authenticator.authId) {
                return;
            }
            // if the device is defined, it means that U2f is being removed
            const deviceId = device ? `${device.key_handle}/` : '';
            const deviceName = device ? device.name : (0, locale_1.t)('Authenticator');
            this.setState({ loading: true });
            try {
                yield this.api.requestPromise(`${ENDPOINT}${authenticator.authId}/${deviceId}`, {
                    method: 'DELETE',
                });
                this.props.router.push('/settings/account/security');
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)('%s has been removed', deviceName));
            }
            catch (_a) {
                // Error deleting authenticator
                this.setState({ loading: false });
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Error removing %s', deviceName));
            }
        });
    }
    getTitle() {
        return (0, locale_1.t)('Security');
    }
    getEndpoints() {
        const { params } = this.props;
        const { authId } = params;
        return [['authenticator', `${ENDPOINT}${authId}/`]];
    }
    renderBody() {
        const { authenticator } = this.state;
        if (!authenticator) {
            return null;
        }
        const { deleteDisabled, onRegenerateBackupCodes } = this.props;
        return (<react_1.Fragment>
        <settingsPageHeader_1.default title={<react_1.Fragment>
              <span>{authenticator.name}</span>
              <AuthenticatorStatus enabled={authenticator.isEnrolled}/>
            </react_1.Fragment>} action={<AuthenticatorActions>
              {authenticator.isEnrolled && authenticator.allowRotationInPlace && (<button_1.default to={`/settings/account/security/mfa/${authenticator.id}/enroll/`}>
                  {(0, locale_1.t)('Rotate Secret Key')}
                </button_1.default>)}
              {authenticator.isEnrolled && authenticator.removeButton && (<tooltip_1.default title={(0, locale_1.t)("Two-factor authentication is required for at least one organization you're a member of.")} disabled={!deleteDisabled}>
                  <removeConfirm_1.default onConfirm={this.handleRemove} disabled={deleteDisabled}>
                    <button_1.default priority="danger">{authenticator.removeButton}</button_1.default>
                  </removeConfirm_1.default>
                </tooltip_1.default>)}
            </AuthenticatorActions>}/>

        <textBlock_1.default>{authenticator.description}</textBlock_1.default>

        <AuthenticatorDates>
          <AuthenticatorDate label={(0, locale_1.t)('Created at')} date={authenticator.createdAt}/>
          <AuthenticatorDate label={(0, locale_1.t)('Last used')} date={authenticator.lastUsedAt}/>
        </AuthenticatorDates>

        <u2fEnrolledDetails_1.default isEnrolled={authenticator.isEnrolled} id={authenticator.id} devices={authenticator.devices} onRemoveU2fDevice={this.handleRemove}/>

        {authenticator.isEnrolled && authenticator.phone && (<PhoneWrapper>
            {(0, locale_1.t)('Confirmation codes are sent to the following phone number')}:
            <Phone>{authenticator.phone}</Phone>
          </PhoneWrapper>)}

        <recoveryCodes_1.default onRegenerateBackupCodes={onRegenerateBackupCodes} isEnrolled={authenticator.isEnrolled} codes={authenticator.codes}/>
      </react_1.Fragment>);
    }
}
exports.default = AccountSecurityDetails;
const AuthenticatorStatus = (0, styled_1.default)(circleIndicator_1.default) `
  margin-left: ${(0, space_1.default)(1)};
`;
const AuthenticatorActions = (0, styled_1.default)('div') `
  display: flex;
  justify-content: center;
  align-items: center;

  > * {
    margin-left: ${(0, space_1.default)(1)};
  }
`;
const AuthenticatorDates = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(2)};
  grid-template-columns: max-content auto;
`;
const DateLabel = (0, styled_1.default)('span') `
  font-weight: bold;
`;
const PhoneWrapper = (0, styled_1.default)('div') `
  margin-top: ${(0, space_1.default)(4)};
`;
const Phone = (0, styled_1.default)('span') `
  font-weight: bold;
  margin-left: ${(0, space_1.default)(1)};
`;
//# sourceMappingURL=accountSecurityDetails.jsx.map