Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const textBlock_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/text/textBlock"));
class RecoveryOptionsModal extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.handleSkipSms = () => {
            this.setState({ skipSms: true });
        };
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { skipSms: false });
    }
    getEndpoints() {
        return [['authenticators', '/users/me/authenticators/']];
    }
    renderBody() {
        const { authenticatorName, closeModal, Body, Header, Footer } = this.props;
        const { authenticators, skipSms } = this.state;
        const { recovery, sms } = authenticators.reduce((obj, item) => {
            obj[item.id] = item;
            return obj;
        }, {});
        const recoveryEnrolled = recovery && recovery.isEnrolled;
        const displaySmsPrompt = sms && !sms.isEnrolled && !skipSms;
        return (<react_1.Fragment>
        <Header closeButton>{(0, locale_1.t)('Two-Factor Authentication Enabled')}</Header>

        <Body>
          <textBlock_1.default>
            {(0, locale_1.t)('Two-factor authentication via %s has been enabled.', authenticatorName)}
          </textBlock_1.default>
          <textBlock_1.default>
            {(0, locale_1.t)('You should now set up recovery options to secure your account.')}
          </textBlock_1.default>

          {displaySmsPrompt ? (
            // set up backup phone number
            <alert_1.default type="warning">
              {(0, locale_1.t)('We recommend adding a phone number as a backup 2FA method.')}
            </alert_1.default>) : (
            // get recovery codes
            <alert_1.default type="warning">
              {(0, locale_1.t)(`Recovery codes are the only way to access your account if you lose
                  your device and cannot receive two-factor authentication codes.`)}
            </alert_1.default>)}
        </Body>

        {displaySmsPrompt ? (
            // set up backup phone number
            <Footer>
            <button_1.default onClick={this.handleSkipSms} name="skipStep" autoFocus>
              {(0, locale_1.t)('Skip this step')}
            </button_1.default>
            <button_1.default priority="primary" onClick={closeModal} to={`/settings/account/security/mfa/${sms.id}/enroll/`} name="addPhone" css={{ marginLeft: (0, space_1.default)(1) }} autoFocus>
              {(0, locale_1.t)('Add a Phone Number')}
            </button_1.default>
          </Footer>) : (
            // get recovery codes
            <Footer>
            <button_1.default priority="primary" onClick={closeModal} to={recoveryEnrolled
                    ? `/settings/account/security/mfa/${recovery.authId}/`
                    : '/settings/account/security/'} name="getCodes" autoFocus>
              {(0, locale_1.t)('Get Recovery Codes')}
            </button_1.default>
          </Footer>)}
      </react_1.Fragment>);
    }
}
exports.default = RecoveryOptionsModal;
//# sourceMappingURL=recoveryOptionsModal.jsx.map