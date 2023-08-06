Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const qrcode_react_1 = (0, tslib_1.__importDefault)(require("qrcode.react"));
const indicator_1 = require("app/actionCreators/indicator");
const modal_1 = require("app/actionCreators/modal");
const organizations_1 = require("app/actionCreators/organizations");
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const circleIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/circleIndicator"));
const panels_1 = require("app/components/panels");
const u2fsign_1 = (0, tslib_1.__importDefault)(require("app/components/u2f/u2fsign"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const getPendingInvite_1 = (0, tslib_1.__importDefault)(require("app/utils/getPendingInvite"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const removeConfirm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/account/accountSecurity/components/removeConfirm"));
const field_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field"));
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const jsonForm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/jsonForm"));
const model_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/model"));
const textCopyInput_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/textCopyInput"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const textBlock_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/text/textBlock"));
/**
 * Retrieve additional form fields (or modify ones) based on 2fa method
 */
const getFields = ({ authenticator, hasSentCode, sendingCode, onSmsReset, onU2fTap, }) => {
    const { form } = authenticator;
    if (!form) {
        return null;
    }
    if (authenticator.id === 'totp') {
        return [
            () => (<CodeContainer key="qrcode">
          <StyledQRCode value={authenticator.qrcode} size={228}/>
        </CodeContainer>),
            () => {
                var _a;
                return (<field_1.default key="secret" label={(0, locale_1.t)('Authenticator secret')}>
          <textCopyInput_1.default>{(_a = authenticator.secret) !== null && _a !== void 0 ? _a : ''}</textCopyInput_1.default>
        </field_1.default>);
            },
            ...form,
            () => (<Actions key="confirm">
          <button_1.default priority="primary" type="submit">
            {(0, locale_1.t)('Confirm')}
          </button_1.default>
        </Actions>),
        ];
    }
    // Sms Form needs a start over button + confirm button
    // Also inputs being disabled vary based on hasSentCode
    if (authenticator.id === 'sms') {
        // Ideally we would have greater flexibility when rendering footer
        return [
            Object.assign(Object.assign({}, form[0]), { disabled: sendingCode || hasSentCode }),
            ...(hasSentCode ? [Object.assign(Object.assign({}, form[1]), { required: true })] : []),
            () => (<Actions key="sms-footer">
          <buttonBar_1.default gap={1}>
            {hasSentCode && <button_1.default onClick={onSmsReset}>{(0, locale_1.t)('Start Over')}</button_1.default>}
            <button_1.default priority="primary" type="submit">
              {hasSentCode ? (0, locale_1.t)('Confirm') : (0, locale_1.t)('Send Code')}
            </button_1.default>
          </buttonBar_1.default>
        </Actions>),
        ];
    }
    // Need to render device name field + U2f component
    if (authenticator.id === 'u2f') {
        const deviceNameField = form.find(({ name }) => name === 'deviceName');
        return [
            deviceNameField,
            () => (<u2fsign_1.default key="u2f-enroll" style={{ marginBottom: 0 }} challengeData={authenticator.challenge} displayMode="enroll" onTap={onU2fTap}/>),
        ];
    }
    return null;
};
/**
 * Renders necessary forms in order to enroll user in 2fa
 */
class AccountSecurityEnroll extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.formModel = new model_1.default();
        this.pendingInvitation = null;
        // This resets state so that user can re-enter their phone number again
        this.handleSmsReset = () => this.setState({ hasSentCode: false }, this.remountComponent);
        // Handles SMS authenticators
        this.handleSmsSubmit = (dataModel) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { authenticator, hasSentCode } = this.state;
            const { phone, otp } = dataModel;
            // Don't submit if empty
            if (!phone || !authenticator) {
                return;
            }
            const data = {
                phone,
                // Make sure `otp` is undefined if we are submitting OTP verification
                // Otherwise API will think that we are on verification step (e.g. after submitting phone)
                otp: hasSentCode ? otp : undefined,
                secret: authenticator.secret,
            };
            // Only show loading when submitting OTP
            this.setState({ sendingCode: !hasSentCode });
            if (!hasSentCode) {
                (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Sending code to %s...', data.phone));
            }
            else {
                (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Verifying OTP...'));
            }
            try {
                yield this.api.requestPromise(this.enrollEndpoint, { data });
            }
            catch (error) {
                this.formModel.resetForm();
                (0, indicator_1.addErrorMessage)(this.state.hasSentCode ? (0, locale_1.t)('Incorrect OTP') : (0, locale_1.t)('Error sending SMS'));
                this.setState({
                    hasSentCode: false,
                    sendingCode: false,
                });
                // Re-mount because we want to fetch a fresh secret
                this.remountComponent();
                return;
            }
            if (!hasSentCode) {
                // Just successfully finished sending OTP to user
                this.setState({ hasSentCode: true, sendingCode: false });
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Sent code to %s', data.phone));
            }
            else {
                // OTP was accepted and SMS was added as a 2fa method
                this.handleEnrollSuccess();
            }
        });
        // Handle u2f device tap
        this.handleU2fTap = (tapData) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const data = Object.assign({ deviceName: this.formModel.getValue('deviceName') }, tapData);
            this.setState({ loading: true });
            try {
                yield this.api.requestPromise(this.enrollEndpoint, { data });
            }
            catch (err) {
                this.handleEnrollError();
                return;
            }
            this.handleEnrollSuccess();
        });
        // Currently only TOTP uses this
        this.handleTotpSubmit = (dataModel) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            if (!this.state.authenticator) {
                return;
            }
            const data = Object.assign(Object.assign({}, (dataModel !== null && dataModel !== void 0 ? dataModel : {})), { secret: this.state.authenticator.secret });
            this.setState({ loading: true });
            try {
                yield this.api.requestPromise(this.enrollEndpoint, { method: 'POST', data });
            }
            catch (err) {
                this.handleEnrollError();
                return;
            }
            this.handleEnrollSuccess();
        });
        this.handleSubmit = data => {
            var _a;
            const id = (_a = this.state.authenticator) === null || _a === void 0 ? void 0 : _a.id;
            if (id === 'totp') {
                this.handleTotpSubmit(data);
                return;
            }
            if (id === 'sms') {
                this.handleSmsSubmit(data);
                return;
            }
        };
        // Removes an authenticator
        this.handleRemove = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { authenticator } = this.state;
            if (!authenticator || !authenticator.authId) {
                return;
            }
            // `authenticator.authId` is NOT the same as `props.params.authId` This is
            // for backwards compatibility with API endpoint
            try {
                yield this.api.requestPromise(this.authenticatorEndpoint, { method: 'DELETE' });
            }
            catch (err) {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Error removing authenticator'));
                return;
            }
            this.props.router.push('/settings/account/security/');
            (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Authenticator has been removed'));
        });
    }
    getTitle() {
        return (0, locale_1.t)('Security');
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { hasSentCode: false });
    }
    get authenticatorEndpoint() {
        return `/users/me/authenticators/${this.props.params.authId}/`;
    }
    get enrollEndpoint() {
        return `${this.authenticatorEndpoint}enroll/`;
    }
    getEndpoints() {
        const errorHandler = (err) => {
            const alreadyEnrolled = err &&
                err.status === 400 &&
                err.responseJSON &&
                err.responseJSON.details === 'Already enrolled';
            if (alreadyEnrolled) {
                this.props.router.push('/settings/account/security/');
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Already enrolled'));
            }
            // Allow the endpoint to fail if the user is already enrolled
            return alreadyEnrolled;
        };
        return [['authenticator', this.enrollEndpoint, {}, { allowError: errorHandler }]];
    }
    componentDidMount() {
        this.pendingInvitation = (0, getPendingInvite_1.default)();
    }
    get authenticatorName() {
        var _a, _b;
        return (_b = (_a = this.state.authenticator) === null || _a === void 0 ? void 0 : _a.name) !== null && _b !== void 0 ? _b : 'Authenticator';
    }
    // Handler when we successfully add a 2fa device
    handleEnrollSuccess() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            // If we're pending approval of an invite, the user will have just joined
            // the organization when completing 2fa enrollment. We should reload the
            // organization context in that case to assign them to the org.
            if (this.pendingInvitation) {
                yield (0, organizations_1.fetchOrganizationByMember)(this.pendingInvitation.memberId.toString(), {
                    addOrg: true,
                    fetchOrgDetails: true,
                });
            }
            this.props.router.push('/settings/account/security/');
            (0, modal_1.openRecoveryOptions)({ authenticatorName: this.authenticatorName });
        });
    }
    // Handler when we failed to add a 2fa device
    handleEnrollError() {
        this.setState({ loading: false });
        (0, indicator_1.addErrorMessage)((0, locale_1.t)('Error adding %s authenticator', this.authenticatorName));
    }
    renderBody() {
        var _a;
        const { authenticator, hasSentCode, sendingCode } = this.state;
        if (!authenticator) {
            return null;
        }
        const fields = getFields({
            authenticator,
            hasSentCode,
            sendingCode,
            onSmsReset: this.handleSmsReset,
            onU2fTap: this.handleU2fTap,
        });
        // Attempt to extract `defaultValue` from server generated form fields
        const defaultValues = fields
            ? fields
                .filter(field => typeof field !== 'function' && typeof field.defaultValue !== 'undefined')
                .map(field => [
                field.name,
                typeof field !== 'function' ? field.defaultValue : '',
            ])
                .reduce((acc, [name, value]) => {
                acc[name] = value;
                return acc;
            }, {})
            : {};
        return (<react_1.Fragment>
        <settingsPageHeader_1.default title={<react_1.Fragment>
              <span>{authenticator.name}</span>
              <circleIndicator_1.default css={{ marginLeft: 6 }} enabled={authenticator.isEnrolled || authenticator.status === 'rotation'}/>
            </react_1.Fragment>} action={authenticator.isEnrolled &&
                authenticator.removeButton && (<removeConfirm_1.default onConfirm={this.handleRemove}>
                <button_1.default priority="danger">{authenticator.removeButton}</button_1.default>
              </removeConfirm_1.default>)}/>

        <textBlock_1.default>{authenticator.description}</textBlock_1.default>

        {authenticator.rotationWarning && authenticator.status === 'rotation' && (<alert_1.default type="warning" icon={<icons_1.IconWarning size="md"/>}>
            {authenticator.rotationWarning}
          </alert_1.default>)}

        {!!((_a = authenticator.form) === null || _a === void 0 ? void 0 : _a.length) && (<form_1.default model={this.formModel} apiMethod="POST" apiEndpoint={this.authenticatorEndpoint} onSubmit={this.handleSubmit} initialData={Object.assign(Object.assign({}, defaultValues), authenticator)} hideFooter>
            <jsonForm_1.default forms={[{ title: 'Configuration', fields: fields !== null && fields !== void 0 ? fields : [] }]}/>
          </form_1.default>)}
      </react_1.Fragment>);
    }
}
const CodeContainer = (0, styled_1.default)(panels_1.PanelItem) `
  justify-content: center;
`;
const Actions = (0, styled_1.default)(panels_1.PanelItem) `
  justify-content: flex-end;
`;
const StyledQRCode = (0, styled_1.default)(qrcode_react_1.default) `
  background: white;
  padding: ${(0, space_1.default)(2)};
`;
exports.default = (0, react_router_1.withRouter)(AccountSecurityEnroll);
//# sourceMappingURL=accountSecurityEnroll.jsx.map