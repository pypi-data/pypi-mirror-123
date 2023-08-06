Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const members_1 = require("app/actionCreators/members");
const organizations_1 = require("app/actionCreators/organizations");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const dropdownMenu_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownMenu"));
const hookOrDefault_1 = (0, tslib_1.__importDefault)(require("app/components/hookOrDefault"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const panels_1 = require("app/components/panels");
const constants_1 = require("app/constants");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const trackAdvancedAnalyticsEvent_1 = (0, tslib_1.__importDefault)(require("app/utils/analytics/trackAdvancedAnalyticsEvent"));
const routeTitle_1 = (0, tslib_1.__importDefault)(require("app/utils/routeTitle"));
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const withTeams_1 = (0, tslib_1.__importDefault)(require("app/utils/withTeams"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const defaultSearchBar_1 = require("app/views/settings/components/defaultSearchBar");
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const membersFilter_1 = (0, tslib_1.__importDefault)(require("./components/membersFilter"));
const inviteRequestRow_1 = (0, tslib_1.__importDefault)(require("./inviteRequestRow"));
const organizationMemberRow_1 = (0, tslib_1.__importDefault)(require("./organizationMemberRow"));
const MemberListHeader = (0, hookOrDefault_1.default)({
    hookName: 'component:member-list-header',
    defaultComponent: () => <panels_1.PanelHeader>{(0, locale_1.t)('Active Members')}</panels_1.PanelHeader>,
});
class OrganizationMembersList extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.removeMember = (id) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { orgId } = this.props.params;
            yield this.api.requestPromise(`/organizations/${orgId}/members/${id}/`, {
                method: 'DELETE',
                data: {},
            });
            this.setState(state => ({
                members: state.members.filter(({ id: existingId }) => existingId !== id),
            }));
        });
        this.handleRemove = ({ id, name }) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { organization } = this.props;
            const { slug: orgName } = organization;
            try {
                yield this.removeMember(id);
            }
            catch (_a) {
                (0, indicator_1.addErrorMessage)((0, locale_1.tct)('Error removing [name] from [orgName]', { name, orgName }));
                return;
            }
            (0, indicator_1.addSuccessMessage)((0, locale_1.tct)('Removed [name] from [orgName]', { name, orgName }));
        });
        this.handleLeave = ({ id }) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { organization } = this.props;
            const { slug: orgName } = organization;
            try {
                yield this.removeMember(id);
            }
            catch (_b) {
                (0, indicator_1.addErrorMessage)((0, locale_1.tct)('Error leaving [orgName]', { orgName }));
                return;
            }
            (0, organizations_1.redirectToRemainingOrganization)({ orgId: orgName, removeOrg: true });
            (0, indicator_1.addSuccessMessage)((0, locale_1.tct)('You left [orgName]', { orgName }));
        });
        this.handleSendInvite = ({ id, expired }) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            this.setState(state => ({
                invited: Object.assign(Object.assign({}, state.invited), { [id]: 'loading' }),
            }));
            try {
                yield (0, members_1.resendMemberInvite)(this.api, {
                    orgId: this.props.params.orgId,
                    memberId: id,
                    regenerate: expired,
                });
            }
            catch (_c) {
                this.setState(state => ({ invited: Object.assign(Object.assign({}, state.invited), { [id]: null }) }));
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Error sending invite'));
                return;
            }
            this.setState(state => ({ invited: Object.assign(Object.assign({}, state.invited), { [id]: 'success' }) }));
        });
        this.updateInviteRequest = (id, data) => this.setState(state => {
            const inviteRequests = [...state.inviteRequests];
            const inviteIndex = inviteRequests.findIndex(request => request.id === id);
            inviteRequests[inviteIndex] = Object.assign(Object.assign({}, inviteRequests[inviteIndex]), data);
            return { inviteRequests };
        });
        this.removeInviteRequest = (id) => this.setState(state => ({
            inviteRequests: state.inviteRequests.filter(request => request.id !== id),
        }));
        this.handleInviteRequestAction = ({ inviteRequest, method, data, successMessage, errorMessage, eventKey, }) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { params, organization } = this.props;
            this.setState(state => ({
                inviteRequestBusy: Object.assign(Object.assign({}, state.inviteRequestBusy), { [inviteRequest.id]: true }),
            }));
            try {
                yield this.api.requestPromise(`/organizations/${params.orgId}/invite-requests/${inviteRequest.id}/`, {
                    method,
                    data,
                });
                this.removeInviteRequest(inviteRequest.id);
                (0, indicator_1.addSuccessMessage)(successMessage);
                (0, trackAdvancedAnalyticsEvent_1.default)(eventKey, {
                    member_id: parseInt(inviteRequest.id, 10),
                    invite_status: inviteRequest.inviteStatus,
                    organization,
                });
            }
            catch (_d) {
                (0, indicator_1.addErrorMessage)(errorMessage);
            }
            this.setState(state => ({
                inviteRequestBusy: Object.assign(Object.assign({}, state.inviteRequestBusy), { [inviteRequest.id]: false }),
            }));
        });
        this.handleInviteRequestApprove = (inviteRequest) => {
            this.handleInviteRequestAction({
                inviteRequest,
                method: 'PUT',
                data: {
                    role: inviteRequest.role,
                    teams: inviteRequest.teams,
                    approve: 1,
                },
                successMessage: (0, locale_1.tct)('[email] has been invited', { email: inviteRequest.email }),
                errorMessage: (0, locale_1.tct)('Error inviting [email]', { email: inviteRequest.email }),
                eventKey: 'invite_request.approved',
            });
        };
        this.handleInviteRequestDeny = (inviteRequest) => {
            this.handleInviteRequestAction({
                inviteRequest,
                method: 'DELETE',
                data: {},
                successMessage: (0, locale_1.tct)('Invite request for [email] denied', {
                    email: inviteRequest.email,
                }),
                errorMessage: (0, locale_1.tct)('Error denying invite request for [email]', {
                    email: inviteRequest.email,
                }),
                eventKey: 'invite_request.denied',
            });
        };
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { members: [], invited: {} });
    }
    getEndpoints() {
        const { orgId } = this.props.params;
        return [
            ['members', `/organizations/${orgId}/members/`, {}, { paginate: true }],
            [
                'member',
                `/organizations/${orgId}/members/me/`,
                {},
                { allowError: error => error.status === 404 },
            ],
            [
                'authProvider',
                `/organizations/${orgId}/auth-provider/`,
                {},
                { allowError: error => error.status === 403 },
            ],
            ['inviteRequests', `/organizations/${orgId}/invite-requests/`],
        ];
    }
    getTitle() {
        const orgId = this.props.organization.slug;
        return (0, routeTitle_1.default)((0, locale_1.t)('Members'), orgId, false);
    }
    renderBody() {
        const { params, organization, routes, teams } = this.props;
        const { membersPageLinks, members, member: currentMember, inviteRequests } = this.state;
        const { name: orgName, access } = organization;
        const canAddMembers = access.includes('member:write');
        const canRemove = access.includes('member:admin');
        const currentUser = configStore_1.default.get('user');
        // Find out if current user is the only owner
        const isOnlyOwner = !members.find(({ role, email, pending }) => role === 'owner' && email !== currentUser.email && !pending);
        // Only admins/owners can remove members
        const requireLink = !!this.state.authProvider && this.state.authProvider.require_link;
        // eslint-disable-next-line react/prop-types
        const renderSearch = ({ defaultSearchBar, value, handleChange }) => (<SearchWrapperWithFilter>
        <dropdownMenu_1.default closeOnEscape>
          {({ getActorProps, isOpen }) => {
                var _a;
                return (<FilterWrapper>
              <button_1.default icon={<icons_1.IconSliders size="xs"/>} {...getActorProps({})}>
                {(0, locale_1.t)('Filter')}
              </button_1.default>
              {isOpen && (<StyledMembersFilter roles={(_a = currentMember === null || currentMember === void 0 ? void 0 : currentMember.roles) !== null && _a !== void 0 ? _a : constants_1.MEMBER_ROLES} query={value} onChange={(query) => handleChange(query)}/>)}
            </FilterWrapper>);
            }}
        </dropdownMenu_1.default>
        {defaultSearchBar}
      </SearchWrapperWithFilter>);
        return (<React.Fragment>
        <react_1.ClassNames>
          {({ css }) => this.renderSearchInput({
                updateRoute: true,
                placeholder: (0, locale_1.t)('Search Members'),
                children: renderSearch,
                className: css `
                font-size: ${theme_1.default.fontSizeMedium};
              `,
            })}
        </react_1.ClassNames>
        {inviteRequests && inviteRequests.length > 0 && (<panels_1.Panel>
            <panels_1.PanelHeader>
              <StyledPanelItem>
                <div>{(0, locale_1.t)('Pending Members')}</div>
                <div>{(0, locale_1.t)('Role')}</div>
                <div>{(0, locale_1.t)('Teams')}</div>
              </StyledPanelItem>
            </panels_1.PanelHeader>
            <panels_1.PanelBody>
              {inviteRequests.map(inviteRequest => {
                    var _a;
                    return (<inviteRequestRow_1.default key={inviteRequest.id} organization={organization} inviteRequest={inviteRequest} inviteRequestBusy={{}} allTeams={teams} allRoles={(_a = currentMember === null || currentMember === void 0 ? void 0 : currentMember.roles) !== null && _a !== void 0 ? _a : constants_1.MEMBER_ROLES} onApprove={this.handleInviteRequestApprove} onDeny={this.handleInviteRequestDeny} onUpdate={data => this.updateInviteRequest(inviteRequest.id, data)}/>);
                })}
            </panels_1.PanelBody>
          </panels_1.Panel>)}
        <panels_1.Panel data-test-id="org-member-list">
          <MemberListHeader members={members} organization={organization}/>
          <panels_1.PanelBody>
            {members.map(member => (<organizationMemberRow_1.default routes={routes} params={params} key={member.id} member={member} status={this.state.invited[member.id]} orgName={orgName} memberCanLeave={!isOnlyOwner} currentUser={currentUser} canRemoveMembers={canRemove} canAddMembers={canAddMembers} requireLink={requireLink} onSendInvite={this.handleSendInvite} onRemove={this.handleRemove} onLeave={this.handleLeave}/>))}
            {members.length === 0 && (<emptyMessage_1.default>{(0, locale_1.t)('No members found.')}</emptyMessage_1.default>)}
          </panels_1.PanelBody>
        </panels_1.Panel>

        <pagination_1.default pageLinks={membersPageLinks}/>
      </React.Fragment>);
    }
}
const SearchWrapperWithFilter = (0, styled_1.default)(defaultSearchBar_1.SearchWrapper) `
  display: grid;
  grid-template-columns: max-content 1fr;
  margin-top: 0;
`;
const FilterWrapper = (0, styled_1.default)('div') `
  position: relative;
`;
const StyledMembersFilter = (0, styled_1.default)(membersFilter_1.default) `
  position: absolute;
  right: 0;
  top: 42px;
  z-index: ${p => p.theme.zIndex.dropdown};

  &:before,
  &:after {
    position: absolute;
    top: -16px;
    right: 32px;
    content: '';
    height: 16px;
    width: 16px;
    border: 8px solid transparent;
    border-bottom-color: ${p => p.theme.backgroundSecondary};
  }

  &:before {
    margin-top: -1px;
    border-bottom-color: ${p => p.theme.border};
  }
`;
const StyledPanelItem = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: minmax(150px, auto) minmax(100px, 140px) 420px;
  grid-gap: ${(0, space_1.default)(2)};
  align-items: center;
  width: 100%;
`;
exports.default = (0, withTeams_1.default)((0, withOrganization_1.default)(OrganizationMembersList));
//# sourceMappingURL=organizationMembersList.jsx.map