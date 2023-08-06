Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const indicator_1 = require("app/actionCreators/indicator");
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const locale_1 = require("app/locale");
const utils_1 = require("app/utils");
const ENDPOINT = '/users/me/authenticators/';
class AccountSecurityWrapper extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.handleDisable = (auth) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            if (!auth || !auth.authId) {
                return;
            }
            this.setState({ loading: true });
            try {
                yield this.api.requestPromise(`${ENDPOINT}${auth.authId}/`, { method: 'DELETE' });
                this.remountComponent();
            }
            catch (_err) {
                this.setState({ loading: false });
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Error disabling %s', auth.name));
            }
        });
        this.handleRegenerateBackupCodes = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            this.setState({ loading: true });
            try {
                yield this.api.requestPromise(`${ENDPOINT}${this.props.params.authId}/`, {
                    method: 'PUT',
                });
                this.remountComponent();
            }
            catch (_err) {
                this.setState({ loading: false });
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Error regenerating backup codes'));
            }
        });
        this.handleRefresh = () => {
            this.fetchData();
        };
    }
    getEndpoints() {
        return [
            ['authenticators', ENDPOINT],
            ['organizations', '/organizations/'],
            ['emails', '/users/me/emails/'],
        ];
    }
    renderBody() {
        const { children } = this.props;
        const { authenticators, organizations, emails } = this.state;
        const enrolled = (authenticators === null || authenticators === void 0 ? void 0 : authenticators.filter(auth => auth.isEnrolled && !auth.isBackupInterface)) || [];
        const countEnrolled = enrolled.length;
        const orgsRequire2fa = (organizations === null || organizations === void 0 ? void 0 : organizations.filter(org => org.require2FA)) || [];
        const deleteDisabled = orgsRequire2fa.length > 0 && countEnrolled === 1;
        const hasVerifiedEmail = !!(emails === null || emails === void 0 ? void 0 : emails.find(({ isVerified }) => isVerified));
        // This happens when you switch between children views and the next child
        // view is lazy loaded, it can potentially be `null` while the code split
        // package is being fetched
        if (!(0, utils_1.defined)(children)) {
            return null;
        }
        return React.cloneElement(this.props.children, {
            onDisable: this.handleDisable,
            onRegenerateBackupCodes: this.handleRegenerateBackupCodes,
            authenticators,
            deleteDisabled,
            orgsRequire2fa,
            countEnrolled,
            hasVerifiedEmail,
            handleRefresh: this.handleRefresh,
        });
    }
}
exports.default = AccountSecurityWrapper;
//# sourceMappingURL=accountSecurityWrapper.jsx.map