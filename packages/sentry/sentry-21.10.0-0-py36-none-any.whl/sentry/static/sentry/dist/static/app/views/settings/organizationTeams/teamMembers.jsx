Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const debounce_1 = (0, tslib_1.__importDefault)(require("lodash/debounce"));
const indicator_1 = require("app/actionCreators/indicator");
const modal_1 = require("app/actionCreators/modal");
const teams_1 = require("app/actionCreators/teams");
const userAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/userAvatar"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const dropdownAutoComplete_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownAutoComplete"));
const dropdownButton_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownButton"));
const idBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const panels_1 = require("app/components/panels");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withConfig_1 = (0, tslib_1.__importDefault)(require("app/utils/withConfig"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
class TeamMembers extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            loading: true,
            error: false,
            dropdownBusy: false,
            teamMemberList: [],
            orgMemberList: [],
        };
        this.debouncedFetchMembersRequest = (0, debounce_1.default)((query) => this.setState({ dropdownBusy: true }, () => this.fetchMembersRequest(query)), 200);
        this.fetchMembersRequest = (query) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { params, api } = this.props;
            const { orgId } = params;
            try {
                const data = yield api.requestPromise(`/organizations/${orgId}/members/`, {
                    query: { query },
                });
                this.setState({
                    orgMemberList: data,
                    dropdownBusy: false,
                });
            }
            catch (_err) {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to load organization members.'), {
                    duration: 2000,
                });
                this.setState({
                    dropdownBusy: false,
                });
            }
        });
        this.fetchData = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, params } = this.props;
            try {
                const data = yield api.requestPromise(`/teams/${params.orgId}/${params.teamId}/members/`);
                this.setState({
                    teamMemberList: data,
                    loading: false,
                    error: false,
                });
            }
            catch (err) {
                this.setState({
                    loading: false,
                    error: true,
                });
            }
            this.fetchMembersRequest('');
        });
        this.addTeamMember = (selection) => {
            const { params } = this.props;
            this.setState({ loading: true });
            // Reset members list after adding member to team
            this.debouncedFetchMembersRequest('');
            (0, teams_1.joinTeam)(this.props.api, {
                orgId: params.orgId,
                teamId: params.teamId,
                memberId: selection.value,
            }, {
                success: () => {
                    const orgMember = this.state.orgMemberList.find(member => member.id === selection.value);
                    if (orgMember === undefined) {
                        return;
                    }
                    this.setState({
                        loading: false,
                        error: false,
                        teamMemberList: this.state.teamMemberList.concat([orgMember]),
                    });
                    (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Successfully added member to team.'));
                },
                error: () => {
                    this.setState({
                        loading: false,
                    });
                    (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to add team member.'));
                },
            });
        };
        /**
         * We perform an API request to support orgs with > 100 members (since that's the max API returns)
         *
         * @param {Event} e React Event when member filter input changes
         */
        this.handleMemberFilterChange = (e) => {
            this.setState({ dropdownBusy: true });
            this.debouncedFetchMembersRequest(e.target.value);
        };
    }
    componentDidMount() {
        this.fetchData();
    }
    UNSAFE_componentWillReceiveProps(nextProps) {
        const params = this.props.params;
        if (nextProps.params.teamId !== params.teamId ||
            nextProps.params.orgId !== params.orgId) {
            this.setState({
                loading: true,
                error: false,
            }, this.fetchData);
        }
    }
    removeMember(member) {
        const { params } = this.props;
        (0, teams_1.leaveTeam)(this.props.api, {
            orgId: params.orgId,
            teamId: params.teamId,
            memberId: member.id,
        }, {
            success: () => {
                this.setState({
                    teamMemberList: this.state.teamMemberList.filter(m => m.id !== member.id),
                });
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Successfully removed member from team.'));
            },
            error: () => (0, indicator_1.addErrorMessage)((0, locale_1.t)('There was an error while trying to remove a member from the team.')),
        });
    }
    renderDropdown(hasWriteAccess) {
        const { organization, params } = this.props;
        const existingMembers = new Set(this.state.teamMemberList.map(member => member.id));
        // members can add other members to a team if the `Open Membership` setting is enabled
        // otherwise, `org:write` or `team:admin` permissions are required
        const hasOpenMembership = !!(organization === null || organization === void 0 ? void 0 : organization.openMembership);
        const canAddMembers = hasOpenMembership || hasWriteAccess;
        const items = (this.state.orgMemberList || [])
            .filter(m => !existingMembers.has(m.id))
            .map(m => ({
            searchKey: `${m.name} ${m.email}`,
            value: m.id,
            label: (<StyledUserListElement>
            <StyledAvatar user={m} size={24} className="avatar"/>
            <StyledNameOrEmail>{m.name || m.email}</StyledNameOrEmail>
          </StyledUserListElement>),
        }));
        const menuHeader = (<StyledMembersLabel>
        {(0, locale_1.t)('Members')}
        <StyledCreateMemberLink to="" onClick={() => (0, modal_1.openInviteMembersModal)({ source: 'teams' })} data-test-id="invite-member">
          {(0, locale_1.t)('Invite Member')}
        </StyledCreateMemberLink>
      </StyledMembersLabel>);
        return (<dropdownAutoComplete_1.default items={items} alignMenu="right" onSelect={canAddMembers
                ? this.addTeamMember
                : selection => (0, modal_1.openTeamAccessRequestModal)({
                    teamId: params.teamId,
                    orgId: params.orgId,
                    memberId: selection.value,
                })} menuHeader={menuHeader} emptyMessage={(0, locale_1.t)('No members')} onChange={this.handleMemberFilterChange} busy={this.state.dropdownBusy} onClose={() => this.debouncedFetchMembersRequest('')}>
        {({ isOpen }) => (<dropdownButton_1.default isOpen={isOpen} size="xsmall" data-test-id="add-member">
            {(0, locale_1.t)('Add Member')}
          </dropdownButton_1.default>)}
      </dropdownAutoComplete_1.default>);
    }
    removeButton(member) {
        return (<button_1.default size="small" icon={<icons_1.IconSubtract size="xs" isCircled/>} onClick={() => this.removeMember(member)} label={(0, locale_1.t)('Remove')}>
        {(0, locale_1.t)('Remove')}
      </button_1.default>);
    }
    render() {
        if (this.state.loading) {
            return <loadingIndicator_1.default />;
        }
        if (this.state.error) {
            return <loadingError_1.default onRetry={this.fetchData}/>;
        }
        const { params, organization, config } = this.props;
        const { access } = organization;
        const hasWriteAccess = access.includes('org:write') || access.includes('team:admin');
        return (<panels_1.Panel>
        <panels_1.PanelHeader hasButtons>
          <div>{(0, locale_1.t)('Members')}</div>
          <div style={{ textTransform: 'none' }}>{this.renderDropdown(hasWriteAccess)}</div>
        </panels_1.PanelHeader>
        {this.state.teamMemberList.length ? (this.state.teamMemberList.map(member => {
                const isSelf = member.email === config.user.email;
                const canRemoveMember = hasWriteAccess || isSelf;
                return (<StyledMemberContainer key={member.id}>
                <idBadge_1.default avatarSize={36} member={member} useLink orgId={params.orgId}/>
                {canRemoveMember && this.removeButton(member)}
              </StyledMemberContainer>);
            })) : (<emptyMessage_1.default icon={<icons_1.IconUser size="xl"/>} size="large">
            {(0, locale_1.t)('This team has no members')}
          </emptyMessage_1.default>)}
      </panels_1.Panel>);
    }
}
const StyledMemberContainer = (0, styled_1.default)(panels_1.PanelItem) `
  justify-content: space-between;
  align-items: center;
`;
const StyledUserListElement = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: max-content 1fr;
  grid-gap: ${(0, space_1.default)(0.5)};
  align-items: center;
`;
const StyledNameOrEmail = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeSmall};
  ${overflowEllipsis_1.default};
`;
const StyledAvatar = (0, styled_1.default)(props => <userAvatar_1.default {...props}/>) `
  min-width: 1.75em;
  min-height: 1.75em;
  width: 1.5em;
  height: 1.5em;
`;
const StyledMembersLabel = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: 1fr max-content;
  padding: ${(0, space_1.default)(1)} 0;
  font-size: ${p => p.theme.fontSizeExtraSmall};
  text-transform: uppercase;
`;
const StyledCreateMemberLink = (0, styled_1.default)(link_1.default) `
  text-transform: none;
`;
exports.default = (0, withConfig_1.default)((0, withApi_1.default)((0, withOrganization_1.default)(TeamMembers)));
//# sourceMappingURL=teamMembers.jsx.map