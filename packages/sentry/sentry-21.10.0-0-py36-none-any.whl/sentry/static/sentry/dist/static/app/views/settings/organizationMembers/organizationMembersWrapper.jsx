Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const modal_1 = require("app/actionCreators/modal");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const routeTitle_1 = (0, tslib_1.__importDefault)(require("app/utils/routeTitle"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
class OrganizationMembersWrapper extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.removeAccessRequest = (id) => this.setState(state => ({
            requestList: state.requestList.filter(request => request.id !== id),
        }));
        this.removeInviteRequest = (id) => this.setState(state => ({
            inviteRequests: state.inviteRequests.filter(request => request.id !== id),
        }));
        this.updateInviteRequest = (id, data) => this.setState(state => {
            const inviteRequests = [...state.inviteRequests];
            const inviteIndex = inviteRequests.findIndex(request => request.id === id);
            inviteRequests[inviteIndex] = Object.assign(Object.assign({}, inviteRequests[inviteIndex]), data);
            return { inviteRequests };
        });
    }
    getEndpoints() {
        const { orgId } = this.props.params;
        return [
            ['inviteRequests', `/organizations/${orgId}/invite-requests/`],
            ['requestList', `/organizations/${orgId}/access-requests/`],
        ];
    }
    getTitle() {
        const { orgId } = this.props.params;
        return (0, routeTitle_1.default)((0, locale_1.t)('Members'), orgId, false);
    }
    get onRequestsTab() {
        return location.pathname.includes('/requests/');
    }
    get hasWriteAccess() {
        const { organization } = this.props;
        if (!organization || !organization.access) {
            return false;
        }
        return organization.access.includes('member:write');
    }
    get showInviteRequests() {
        return this.hasWriteAccess;
    }
    get showNavTabs() {
        const { requestList } = this.state;
        // show the requests tab if there are pending team requests,
        // or if the user has access to approve or deny invite requests
        return (requestList && requestList.length > 0) || this.showInviteRequests;
    }
    get requestCount() {
        const { requestList, inviteRequests } = this.state;
        let count = requestList.length;
        // if the user can't see the invite requests panel,
        // exclude those requests from the total count
        if (this.showInviteRequests) {
            count += inviteRequests.length;
        }
        return count ? count.toString() : null;
    }
    renderBody() {
        const { children } = this.props;
        const { requestList, inviteRequests } = this.state;
        const action = (<button_1.default priority="primary" size="small" onClick={() => (0, modal_1.openInviteMembersModal)({
                onClose: () => {
                    this.fetchData();
                },
                source: 'members_settings',
            })} data-test-id="email-invite" icon={<icons_1.IconMail />}>
        {(0, locale_1.t)('Invite Members')}
      </button_1.default>);
        return (<react_1.Fragment>
        <settingsPageHeader_1.default title="Members" action={action}/>
        {children &&
                (0, react_1.cloneElement)(children, {
                    requestList,
                    inviteRequests,
                    onRemoveInviteRequest: this.removeInviteRequest,
                    onUpdateInviteRequest: this.updateInviteRequest,
                    onRemoveAccessRequest: this.removeAccessRequest,
                    showInviteRequests: this.showInviteRequests,
                })}
      </react_1.Fragment>);
    }
}
exports.default = (0, withOrganization_1.default)(OrganizationMembersWrapper);
//# sourceMappingURL=organizationMembersWrapper.jsx.map