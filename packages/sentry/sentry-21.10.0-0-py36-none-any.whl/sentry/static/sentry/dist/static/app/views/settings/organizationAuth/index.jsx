Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const indicator_1 = require("app/actionCreators/indicator");
const locale_1 = require("app/locale");
const routeTitle_1 = (0, tslib_1.__importDefault)(require("app/utils/routeTitle"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const organizationAuthList_1 = (0, tslib_1.__importDefault)(require("./organizationAuthList"));
class OrganizationAuth extends asyncView_1.default {
    constructor() {
        super(...arguments);
        /**
         * TODO(epurkhiser): This does not work right now as we still fallback to the
         * old SSO auth configuration page
         */
        this.handleSendReminders = (_provider) => {
            this.setState({ sendRemindersBusy: true });
            this.api.request(`/organizations/${this.props.params.orgId}/auth-provider/send-reminders/`, {
                method: 'POST',
                data: {},
                success: () => (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Sent reminders to members')),
                error: () => (0, indicator_1.addErrorMessage)((0, locale_1.t)('Failed to send reminders')),
                complete: () => this.setState({ sendRemindersBusy: false }),
            });
        };
        /**
         * TODO(epurkhiser): This does not work right now as we still fallback to the
         * old SSO auth configuration page
         */
        this.handleConfigure = (provider) => {
            this.setState({ busy: true });
            this.api.request(`/organizations/${this.props.params.orgId}/auth-provider/`, {
                method: 'POST',
                data: { provider, init: true },
                success: data => {
                    // Redirect to auth provider URL
                    if (data && data.auth_url) {
                        window.location.href = data.auth_url;
                    }
                },
                error: () => {
                    this.setState({ busy: false });
                },
            });
        };
        /**
         * TODO(epurkhiser): This does not work right now as we still fallback to the
         * old SSO auth configuration page
         */
        this.handleDisableProvider = (provider) => {
            this.setState({ busy: true });
            this.api.request(`/organizations/${this.props.params.orgId}/auth-provider/`, {
                method: 'DELETE',
                data: { provider },
                success: () => {
                    this.setState({ provider: null, busy: false });
                },
                error: () => {
                    this.setState({ busy: false });
                },
            });
        };
    }
    UNSAFE_componentWillUpdate(_nextProps, nextState) {
        const access = this.props.organization.access;
        if (nextState.provider && access.includes('org:write')) {
            // If SSO provider is configured, keep showing loading while we redirect
            // to django configuration view
            window.location.assign(`/organizations/${this.props.params.orgId}/auth/configure/`);
        }
    }
    getEndpoints() {
        return [
            ['providerList', `/organizations/${this.props.params.orgId}/auth-providers/`],
            ['provider', `/organizations/${this.props.params.orgId}/auth-provider/`],
        ];
    }
    getTitle() {
        return (0, routeTitle_1.default)((0, locale_1.t)('Auth Settings'), this.props.organization.slug, false);
    }
    renderBody() {
        const { providerList, provider } = this.state;
        if (providerList === null) {
            return null;
        }
        if (this.props.organization.access.includes('org:write') && provider) {
            // If SSO provider is configured, keep showing loading while we redirect
            // to django configuration view
            return this.renderLoading();
        }
        const activeProvider = providerList === null || providerList === void 0 ? void 0 : providerList.find(p => p.key === (provider === null || provider === void 0 ? void 0 : provider.key));
        return (<organizationAuthList_1.default activeProvider={activeProvider} providerList={providerList}/>);
    }
}
exports.default = (0, withOrganization_1.default)(OrganizationAuth);
//# sourceMappingURL=index.jsx.map