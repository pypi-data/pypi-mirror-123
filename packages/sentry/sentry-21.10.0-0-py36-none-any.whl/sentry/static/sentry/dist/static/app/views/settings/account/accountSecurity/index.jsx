Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const modal_1 = require("app/actionCreators/modal");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const circleIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/circleIndicator"));
const listLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/listLink"));
const navTabs_1 = (0, tslib_1.__importDefault)(require("app/components/navTabs"));
const panels_1 = require("app/components/panels");
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const recreateRoute_1 = (0, tslib_1.__importDefault)(require("app/utils/recreateRoute"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const removeConfirm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/account/accountSecurity/components/removeConfirm"));
const twoFactorRequired_1 = (0, tslib_1.__importDefault)(require("app/views/settings/account/accountSecurity/components/twoFactorRequired"));
const passwordForm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/account/passwordForm"));
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const field_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const textBlock_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/text/textBlock"));
/**
 * Lists 2fa devices + password change form
 */
class AccountSecurity extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.handleSessionClose = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            try {
                yield this.api.requestPromise('/auth/', {
                    method: 'DELETE',
                    data: { all: true },
                });
                window.location.assign('/auth/login/');
            }
            catch (err) {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('There was a problem closing all sessions'));
                throw err;
            }
        });
        this.formatOrgSlugs = () => {
            const { orgsRequire2fa } = this.props;
            const slugs = orgsRequire2fa.map(({ slug }) => slug);
            return [slugs.slice(0, -1).join(', '), slugs.slice(-1)[0]].join(slugs.length > 1 ? ' and ' : '');
        };
        this.handleAdd2FAClicked = () => {
            const { handleRefresh } = this.props;
            (0, modal_1.openEmailVerification)({
                onClose: () => {
                    handleRefresh();
                },
                actionMessage: 'enrolling a 2FA device',
            });
        };
    }
    getTitle() {
        return (0, locale_1.t)('Security');
    }
    getEndpoints() {
        return [];
    }
    renderBody() {
        const { authenticators, countEnrolled, deleteDisabled, onDisable, hasVerifiedEmail } = this.props;
        const isEmpty = !(authenticators === null || authenticators === void 0 ? void 0 : authenticators.length);
        return (<div>
        <settingsPageHeader_1.default title={(0, locale_1.t)('Security')} tabs={<navTabs_1.default underlined>
              <listLink_1.default to={(0, recreateRoute_1.default)('', this.props)} index>
                {(0, locale_1.t)('Settings')}
              </listLink_1.default>
              <listLink_1.default to={(0, recreateRoute_1.default)('session-history/', this.props)}>
                {(0, locale_1.t)('Session History')}
              </listLink_1.default>
            </navTabs_1.default>}/>

        {!isEmpty && countEnrolled === 0 && <twoFactorRequired_1.default />}

        <passwordForm_1.default />

        <panels_1.Panel>
          <panels_1.PanelHeader>{(0, locale_1.t)('Sessions')}</panels_1.PanelHeader>
          <panels_1.PanelBody>
            <field_1.default alignRight flexibleControlStateSize label={(0, locale_1.t)('Sign out of all devices')} help={(0, locale_1.t)('Signing out of all devices will sign you out of this device as well.')}>
              <button_1.default data-test-id="signoutAll" onClick={this.handleSessionClose}>
                {(0, locale_1.t)('Sign out of all devices')}
              </button_1.default>
            </field_1.default>
          </panels_1.PanelBody>
        </panels_1.Panel>

        <panels_1.Panel>
          <panels_1.PanelHeader>{(0, locale_1.t)('Two-Factor Authentication')}</panels_1.PanelHeader>

          {isEmpty && (<emptyMessage_1.default>{(0, locale_1.t)('No available authenticators to add')}</emptyMessage_1.default>)}

          <panels_1.PanelBody>
            {!isEmpty &&
                (authenticators === null || authenticators === void 0 ? void 0 : authenticators.map(auth => {
                    const { id, authId, description, isBackupInterface, isEnrolled, configureButton, name, } = auth;
                    return (<AuthenticatorPanelItem key={id}>
                    <AuthenticatorHeader>
                      <AuthenticatorTitle>
                        <AuthenticatorStatus enabled={isEnrolled}/>
                        <AuthenticatorName>{name}</AuthenticatorName>
                      </AuthenticatorTitle>

                      <Actions>
                        {!isBackupInterface && !isEnrolled && hasVerifiedEmail && (<button_1.default to={`/settings/account/security/mfa/${id}/enroll/`} size="small" priority="primary" className="enroll-button">
                            {(0, locale_1.t)('Add')}
                          </button_1.default>)}
                        {!isBackupInterface && !isEnrolled && !hasVerifiedEmail && (<button_1.default onClick={this.handleAdd2FAClicked} size="small" priority="primary" className="enroll-button">
                            {(0, locale_1.t)('Add')}
                          </button_1.default>)}

                        {isEnrolled && authId && (<button_1.default to={`/settings/account/security/mfa/${authId}/`} size="small" className="details-button">
                            {configureButton}
                          </button_1.default>)}

                        {!isBackupInterface && isEnrolled && (<tooltip_1.default title={(0, locale_1.t)(`Two-factor authentication is required for organization(s): ${this.formatOrgSlugs()}.`)} disabled={!deleteDisabled}>
                            <removeConfirm_1.default onConfirm={() => onDisable(auth)} disabled={deleteDisabled}>
                              <button_1.default size="small" label={(0, locale_1.t)('delete')} icon={<icons_1.IconDelete />}/>
                            </removeConfirm_1.default>
                          </tooltip_1.default>)}
                      </Actions>

                      {isBackupInterface && !isEnrolled ? (0, locale_1.t)('requires 2FA') : null}
                    </AuthenticatorHeader>

                    <Description>{description}</Description>
                  </AuthenticatorPanelItem>);
                }))}
          </panels_1.PanelBody>
        </panels_1.Panel>
      </div>);
    }
}
const AuthenticatorName = (0, styled_1.default)('span') `
  font-size: 1.2em;
`;
const AuthenticatorPanelItem = (0, styled_1.default)(panels_1.PanelItem) `
  flex-direction: column;
`;
const AuthenticatorHeader = (0, styled_1.default)('div') `
  display: flex;
  flex: 1;
  align-items: center;
`;
const AuthenticatorTitle = (0, styled_1.default)('div') `
  flex: 1;
`;
const Actions = (0, styled_1.default)('div') `
  display: grid;
  grid-auto-flow: column;
  grid-gap: ${(0, space_1.default)(1)};
`;
const AuthenticatorStatus = (0, styled_1.default)(circleIndicator_1.default) `
  margin-right: ${(0, space_1.default)(1)};
`;
const Description = (0, styled_1.default)(textBlock_1.default) `
  margin-top: ${(0, space_1.default)(2)};
  margin-bottom: 0;
`;
exports.default = AccountSecurity;
//# sourceMappingURL=index.jsx.map