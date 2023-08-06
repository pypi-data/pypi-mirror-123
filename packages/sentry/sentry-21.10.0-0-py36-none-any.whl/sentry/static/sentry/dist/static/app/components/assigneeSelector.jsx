Object.defineProperty(exports, "__esModule", { value: true });
exports.putSessionUserFirst = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const group_1 = require("app/actionCreators/group");
const modal_1 = require("app/actionCreators/modal");
const actorAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/actorAvatar"));
const suggestedAvatarStack_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/suggestedAvatarStack"));
const teamAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/teamAvatar"));
const userAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/userAvatar"));
const dropdownAutoComplete_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownAutoComplete"));
const dropdownBubble_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownBubble"));
const highlight_1 = (0, tslib_1.__importDefault)(require("app/components/highlight"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const textOverflow_1 = (0, tslib_1.__importDefault)(require("app/components/textOverflow"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const groupStore_1 = (0, tslib_1.__importDefault)(require("app/stores/groupStore"));
const memberListStore_1 = (0, tslib_1.__importDefault)(require("app/stores/memberListStore"));
const projectsStore_1 = (0, tslib_1.__importDefault)(require("app/stores/projectsStore"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
class AssigneeSelector extends React.Component {
    constructor() {
        super(...arguments);
        this.state = this.getInitialState();
        this.unlisteners = [
            groupStore_1.default.listen(itemIds => this.onGroupChange(itemIds), undefined),
            memberListStore_1.default.listen((users) => {
                this.handleMemberListUpdate(users);
            }, undefined),
        ];
        this.handleMemberListUpdate = (members) => {
            if (members === this.state.memberList) {
                return;
            }
            this.setState({ memberList: members });
        };
        this.handleAssign = ({ value: { type, assignee } }, _state, e) => {
            if (type === 'member') {
                this.assignToUser(assignee);
            }
            if (type === 'team') {
                this.assignToTeam(assignee);
            }
            e === null || e === void 0 ? void 0 : e.stopPropagation();
            const { onAssign } = this.props;
            if (onAssign) {
                const suggestionType = type === 'member' ? 'user' : type;
                const suggestion = this.getSuggestedAssignees().find(actor => actor.type === suggestionType && actor.id === assignee.id);
                onAssign === null || onAssign === void 0 ? void 0 : onAssign(type, assignee, suggestion);
            }
        };
        this.clearAssignTo = (e) => {
            // clears assignment
            (0, group_1.clearAssignment)(this.props.id, 'assignee_selector');
            this.setState({ loading: true });
            e.stopPropagation();
        };
    }
    getInitialState() {
        const group = groupStore_1.default.get(this.props.id);
        const memberList = memberListStore_1.default.loaded ? memberListStore_1.default.getAll() : undefined;
        const loading = groupStore_1.default.hasStatus(this.props.id, 'assignTo');
        const suggestedOwners = group === null || group === void 0 ? void 0 : group.owners;
        return {
            assignedTo: group === null || group === void 0 ? void 0 : group.assignedTo,
            memberList,
            loading,
            suggestedOwners,
        };
    }
    componentWillReceiveProps(nextProps) {
        const loading = groupStore_1.default.hasStatus(nextProps.id, 'assignTo');
        if (nextProps.id !== this.props.id || loading !== this.state.loading) {
            const group = groupStore_1.default.get(this.props.id);
            this.setState({
                loading,
                assignedTo: group === null || group === void 0 ? void 0 : group.assignedTo,
                suggestedOwners: group === null || group === void 0 ? void 0 : group.owners,
            });
        }
    }
    shouldComponentUpdate(nextProps, nextState) {
        if (nextState.loading !== this.state.loading) {
            return true;
        }
        // If the memberList in props has changed, re-render as
        // props have updated, and we won't use internal state anyways.
        if (nextProps.memberList &&
            !(0, utils_1.valueIsEqual)(this.props.memberList, nextProps.memberList)) {
            return true;
        }
        const currentMembers = this.memberList();
        // XXX(billyvg): this means that once `memberList` is not-null, this component will never update due to `memberList` changes
        // Note: this allows us to show a "loading" state for memberList, but only before `MemberListStore.loadInitialData`
        // is called
        if (currentMembers === undefined && nextState.memberList !== currentMembers) {
            return true;
        }
        return !(0, utils_1.valueIsEqual)(nextState.assignedTo, this.state.assignedTo, true);
    }
    componentWillUnmount() {
        this.unlisteners.forEach(unlistener => unlistener === null || unlistener === void 0 ? void 0 : unlistener());
    }
    memberList() {
        return this.props.memberList ? this.props.memberList : this.state.memberList;
    }
    onGroupChange(itemIds) {
        if (!itemIds.has(this.props.id)) {
            return;
        }
        const group = groupStore_1.default.get(this.props.id);
        this.setState({
            assignedTo: group === null || group === void 0 ? void 0 : group.assignedTo,
            suggestedOwners: group === null || group === void 0 ? void 0 : group.owners,
            loading: groupStore_1.default.hasStatus(this.props.id, 'assignTo'),
        });
    }
    assignableTeams() {
        var _a, _b;
        const group = groupStore_1.default.get(this.props.id);
        if (!group) {
            return [];
        }
        const teams = (_b = (_a = projectsStore_1.default.getBySlug(group.project.slug)) === null || _a === void 0 ? void 0 : _a.teams) !== null && _b !== void 0 ? _b : [];
        return teams
            .sort((a, b) => a.slug.localeCompare(b.slug))
            .map(team => ({
            id: (0, utils_1.buildTeamId)(team.id),
            display: `#${team.slug}`,
            email: team.id,
            team,
        }));
    }
    assignToUser(user) {
        (0, group_1.assignToUser)({ id: this.props.id, user, assignedBy: 'assignee_selector' });
        this.setState({ loading: true });
    }
    assignToTeam(team) {
        (0, group_1.assignToActor)({
            actor: { id: team.id, type: 'team' },
            id: this.props.id,
            assignedBy: 'assignee_selector',
        });
        this.setState({ loading: true });
    }
    renderMemberNode(member, suggestedReason) {
        const { size } = this.props;
        return {
            value: { type: 'member', assignee: member },
            searchKey: `${member.email} ${member.name}`,
            label: ({ inputValue }) => (<MenuItemWrapper data-test-id="assignee-option" key={(0, utils_1.buildUserId)(member.id)} onSelect={this.assignToUser.bind(this, member)}>
          <IconContainer>
            <userAvatar_1.default user={member} size={size}/>
          </IconContainer>
          <Label>
            <highlight_1.default text={inputValue}>{member.name || member.email}</highlight_1.default>
            {suggestedReason && <SuggestedReason>{suggestedReason}</SuggestedReason>}
          </Label>
        </MenuItemWrapper>),
        };
    }
    renderNewMemberNodes() {
        const members = putSessionUserFirst(this.memberList());
        return members.map(member => this.renderMemberNode(member));
    }
    renderTeamNode(assignableTeam, suggestedReason) {
        const { size } = this.props;
        const { id, display, team } = assignableTeam;
        return {
            value: { type: 'team', assignee: team },
            searchKey: team.slug,
            label: ({ inputValue }) => (<MenuItemWrapper data-test-id="assignee-option" key={id} onSelect={this.assignToTeam.bind(this, team)}>
          <IconContainer>
            <teamAvatar_1.default team={team} size={size}/>
          </IconContainer>
          <Label>
            <highlight_1.default text={inputValue}>{display}</highlight_1.default>
            {suggestedReason && <SuggestedReason>{suggestedReason}</SuggestedReason>}
          </Label>
        </MenuItemWrapper>),
        };
    }
    renderNewTeamNodes() {
        return this.assignableTeams().map(team => this.renderTeamNode(team));
    }
    renderSuggestedAssigneeNodes() {
        const { assignedTo } = this.state;
        // filter out suggested assignees if a suggestion is already selected
        return this.getSuggestedAssignees()
            .filter(({ type, id }) => !(type === (assignedTo === null || assignedTo === void 0 ? void 0 : assignedTo.type) && id === (assignedTo === null || assignedTo === void 0 ? void 0 : assignedTo.id)))
            .filter(({ type }) => type === 'user' || type === 'team')
            .map(({ type, suggestedReason, assignee }) => {
            const reason = suggestedReason === 'suspectCommit'
                ? (0, locale_1.t)('(Suspect Commit)')
                : (0, locale_1.t)('(Issue Owner)');
            if (type === 'user') {
                return this.renderMemberNode(assignee, reason);
            }
            return this.renderTeamNode(assignee, reason);
        });
    }
    renderDropdownGroupLabel(label) {
        return <GroupHeader>{label}</GroupHeader>;
    }
    renderNewDropdownItems() {
        var _a;
        const teams = this.renderNewTeamNodes();
        const members = this.renderNewMemberNodes();
        const suggestedAssignees = (_a = this.renderSuggestedAssigneeNodes()) !== null && _a !== void 0 ? _a : [];
        const assigneeIds = new Set(suggestedAssignees.map(assignee => `${assignee.value.type}:${assignee.value.assignee.id}`));
        // filter out duplicates of Team/Member if also a Suggested Assignee
        const filteredTeams = teams.filter(team => {
            return !assigneeIds.has(`${team.value.type}:${team.value.assignee.id}`);
        });
        const filteredMembers = members.filter(member => {
            return !assigneeIds.has(`${member.value.type}:${member.value.assignee.id}`);
        });
        const dropdownItems = [
            {
                label: this.renderDropdownGroupLabel((0, locale_1.t)('Teams')),
                id: 'team-header',
                items: filteredTeams,
            },
            {
                label: this.renderDropdownGroupLabel((0, locale_1.t)('People')),
                id: 'members-header',
                items: filteredMembers,
            },
        ];
        if (suggestedAssignees.length) {
            dropdownItems.unshift({
                label: this.renderDropdownGroupLabel((0, locale_1.t)('Suggested')),
                id: 'suggested-header',
                items: suggestedAssignees,
            });
        }
        return dropdownItems;
    }
    getSuggestedAssignees() {
        var _a;
        const { suggestedOwners } = this.state;
        if (!suggestedOwners) {
            return [];
        }
        const assignableTeams = this.assignableTeams();
        const memberList = (_a = this.memberList()) !== null && _a !== void 0 ? _a : [];
        const suggestedAssignees = suggestedOwners.map(owner => {
            // converts a backend suggested owner to a suggested assignee
            const [ownerType, id] = owner.owner.split(':');
            if (ownerType === 'user') {
                const member = memberList.find(user => user.id === id);
                if (member) {
                    return {
                        type: 'user',
                        id,
                        name: member.name,
                        suggestedReason: owner.type,
                        assignee: member,
                    };
                }
            }
            else if (ownerType === 'team') {
                const matchingTeam = assignableTeams.find(assignableTeam => assignableTeam.id === owner.owner);
                if (matchingTeam) {
                    return {
                        type: 'team',
                        id,
                        name: matchingTeam.team.name,
                        suggestedReason: owner.type,
                        assignee: matchingTeam,
                    };
                }
            }
            return null;
        });
        return suggestedAssignees.filter(owner => !!owner);
    }
    render() {
        const { disabled } = this.props;
        const { loading, assignedTo } = this.state;
        const memberList = this.memberList();
        const suggestedActors = this.getSuggestedAssignees();
        const suggestedReasons = {
            suspectCommit: (0, locale_1.tct)('Based on [commit:commit data]', {
                commit: (<TooltipSubExternalLink href="https://docs.sentry.io/product/sentry-basics/guides/integrate-frontend/configure-scms/"/>),
            }),
            ownershipRule: (0, locale_1.t)('Matching Issue Owners Rule'),
        };
        const assignedToSuggestion = suggestedActors.find(actor => actor.id === (assignedTo === null || assignedTo === void 0 ? void 0 : assignedTo.id));
        return (<AssigneeWrapper>
        {loading && (<loadingIndicator_1.default mini style={{ height: '24px', margin: 0, marginRight: 11 }}/>)}
        {!loading && (<dropdownAutoComplete_1.default disabled={disabled} maxHeight={400} onOpen={e => {
                    // This can be called multiple times and does not always have `event`
                    e === null || e === void 0 ? void 0 : e.stopPropagation();
                }} busy={memberList === undefined} items={memberList !== undefined ? this.renderNewDropdownItems() : null} alignMenu="right" onSelect={this.handleAssign} itemSize="small" searchPlaceholder={(0, locale_1.t)('Filter teams and people')} menuHeader={assignedTo && (<MenuItemWrapper data-test-id="clear-assignee" onClick={this.clearAssignTo} py={0}>
                  <IconContainer>
                    <ClearAssigneeIcon isCircled size="14px"/>
                  </IconContainer>
                  <Label>{(0, locale_1.t)('Clear Assignee')}</Label>
                </MenuItemWrapper>)} menuFooter={<InviteMemberLink to="" data-test-id="invite-member" disabled={loading} onClick={() => (0, modal_1.openInviteMembersModal)({ source: 'assignee_selector' })}>
                <MenuItemWrapper>
                  <IconContainer>
                    <InviteMemberIcon isCircled size="14px"/>
                  </IconContainer>
                  <Label>{(0, locale_1.t)('Invite Member')}</Label>
                </MenuItemWrapper>
              </InviteMemberLink>} menuWithArrow emptyHidesInput>
            {({ getActorProps, isOpen }) => (<DropdownButton {...getActorProps({})}>
                {assignedTo ? (<actorAvatar_1.default actor={assignedTo} className="avatar" size={24} tooltip={<TooltipWrapper>
                        {(0, locale_1.tct)('Assigned to [name]', {
                                name: assignedTo.type === 'team'
                                    ? `#${assignedTo.name}`
                                    : assignedTo.name,
                            })}
                        {assignedToSuggestion && (<TooltipSubtext>
                            {suggestedReasons[assignedToSuggestion.suggestedReason]}
                          </TooltipSubtext>)}
                      </TooltipWrapper>}/>) : suggestedActors && suggestedActors.length > 0 ? (<suggestedAvatarStack_1.default size={24} owners={suggestedActors} tooltipOptions={{ isHoverable: true }} tooltip={<TooltipWrapper>
                        <div>
                          {(0, locale_1.tct)('Suggestion: [name]', {
                                name: suggestedActors[0].type === 'team'
                                    ? `#${suggestedActors[0].name}`
                                    : suggestedActors[0].name,
                            })}
                          {suggestedActors.length > 1 &&
                                (0, locale_1.tn)(' + %s other', ' + %s others', suggestedActors.length - 1)}
                        </div>
                        <TooltipSubtext>
                          {suggestedReasons[suggestedActors[0].suggestedReason]}
                        </TooltipSubtext>
                      </TooltipWrapper>}/>) : (<tooltip_1.default isHoverable skipWrapper title={<TooltipWrapper>
                        <div>{(0, locale_1.t)('Unassigned')}</div>
                        <TooltipSubtext>
                          {(0, locale_1.tct)('You can auto-assign issues by adding [issueOwners:Issue Owner rules].', {
                                issueOwners: (<TooltipSubExternalLink href="https://docs.sentry.io/product/error-monitoring/issue-owners/"/>),
                            })}
                        </TooltipSubtext>
                      </TooltipWrapper>}>
                    <StyledIconUser size="20px" color="gray400"/>
                  </tooltip_1.default>)}
                <StyledChevron direction={isOpen ? 'up' : 'down'} size="xs"/>
              </DropdownButton>)}
          </dropdownAutoComplete_1.default>)}
      </AssigneeWrapper>);
    }
}
AssigneeSelector.defaultProps = {
    size: 20,
};
function putSessionUserFirst(members) {
    // If session user is in the filtered list of members, put them at the top
    if (!members) {
        return [];
    }
    const sessionUser = configStore_1.default.get('user');
    const sessionUserIndex = members.findIndex(member => member.id === (sessionUser === null || sessionUser === void 0 ? void 0 : sessionUser.id));
    if (sessionUserIndex === -1) {
        return members;
    }
    const arrangedMembers = [members[sessionUserIndex]];
    arrangedMembers.push(...members.slice(0, sessionUserIndex));
    arrangedMembers.push(...members.slice(sessionUserIndex + 1));
    return arrangedMembers;
}
exports.putSessionUserFirst = putSessionUserFirst;
exports.default = AssigneeSelector;
const AssigneeWrapper = (0, styled_1.default)('div') `
  display: flex;
  justify-content: flex-end;

  /* manually align menu underneath dropdown caret */
  ${dropdownBubble_1.default} {
    right: -14px;
  }
`;
const StyledIconUser = (0, styled_1.default)(icons_1.IconUser) `
  /* We need this to center with Avatar */
  margin-right: 2px;
`;
const IconContainer = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  flex-shrink: 0;
`;
const MenuItemWrapper = (0, styled_1.default)('div') `
  cursor: ${p => (p.disabled ? 'not-allowed' : 'pointer')};
  display: flex;
  align-items: center;
  font-size: 13px;
  ${p => typeof p.py !== 'undefined' &&
    `
      padding-top: ${p.py};
      padding-bottom: ${p.py};
    `};
`;
const InviteMemberLink = (0, styled_1.default)(link_1.default) `
  color: ${p => (p.disabled ? p.theme.disabled : p.theme.textColor)};
`;
const Label = (0, styled_1.default)(textOverflow_1.default) `
  margin-left: 6px;
`;
const ClearAssigneeIcon = (0, styled_1.default)(icons_1.IconClose) `
  opacity: 0.3;
`;
const InviteMemberIcon = (0, styled_1.default)(icons_1.IconAdd) `
  opacity: 0.3;
`;
const StyledChevron = (0, styled_1.default)(icons_1.IconChevron) `
  margin-left: ${(0, space_1.default)(1)};
`;
const DropdownButton = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  font-size: 20px;
`;
const GroupHeader = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeSmall};
  font-weight: 600;
  margin: ${(0, space_1.default)(1)} 0;
  color: ${p => p.theme.subText};
  line-height: ${p => p.theme.fontSizeSmall};
  text-align: left;
`;
const SuggestedReason = (0, styled_1.default)('span') `
  margin-left: ${(0, space_1.default)(0.5)};
  color: ${p => p.theme.textColor};
`;
const TooltipWrapper = (0, styled_1.default)('div') `
  text-align: left;
`;
const TooltipSubtext = (0, styled_1.default)('div') `
  color: ${p => p.theme.subText};
`;
const TooltipSubExternalLink = (0, styled_1.default)(externalLink_1.default) `
  color: ${p => p.theme.subText};
  text-decoration: underline;

  :hover {
    color: ${p => p.theme.subText};
  }
`;
//# sourceMappingURL=assigneeSelector.jsx.map