Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const multiSelectControl_1 = (0, tslib_1.__importDefault)(require("app/components/forms/multiSelectControl"));
const hookOrDefault_1 = (0, tslib_1.__importDefault)(require("app/components/hookOrDefault"));
const panels_1 = require("app/components/panels");
const roleSelectControl_1 = (0, tslib_1.__importDefault)(require("app/components/roleSelectControl"));
const tag_1 = (0, tslib_1.__importDefault)(require("app/components/tag"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const InviteModalHook = (0, hookOrDefault_1.default)({
    hookName: 'member-invite-modal:customization',
    defaultComponent: ({ onSendInvites, children }) => children({ sendInvites: onSendInvites, canSend: true }),
});
const InviteRequestRow = ({ inviteRequest, inviteRequestBusy, organization, onApprove, onDeny, onUpdate, allTeams, allRoles, }) => {
    const role = allRoles.find(r => r.id === inviteRequest.role);
    const roleDisallowed = !(role && role.allowed);
    const { access } = organization;
    const canApprove = access.includes('member:admin');
    // eslint-disable-next-line react/prop-types
    const hookRenderer = ({ sendInvites, canSend, headerInfo }) => (<StyledPanelItem>
      <div>
        <h5 style={{ marginBottom: (0, space_1.default)(0.5) }}>
          <UserName>{inviteRequest.email}</UserName>
        </h5>
        {inviteRequest.inviteStatus === 'requested_to_be_invited' ? (inviteRequest.inviterName && (<Description>
              <tooltip_1.default title={(0, locale_1.t)('An existing member has asked to invite this user to your organization')}>
                {(0, locale_1.tct)('Requested by [inviterName]', {
                inviterName: inviteRequest.inviterName,
            })}
              </tooltip_1.default>
            </Description>)) : (<JoinRequestIndicator tooltipText={(0, locale_1.t)('This user has asked to join your organization.')}>
            {(0, locale_1.t)('Join request')}
          </JoinRequestIndicator>)}
      </div>

      {canApprove ? (<StyledRoleSelectControl name="role" disableUnallowed onChange={r => onUpdate({ role: r.value })} value={inviteRequest.role} roles={allRoles}/>) : (<div>{inviteRequest.roleName}</div>)}
      {canApprove ? (<TeamSelectControl name="teams" placeholder={(0, locale_1.t)('Add to teams\u2026')} onChange={(teams) => onUpdate({ teams: (teams || []).map(team => team.value) })} value={inviteRequest.teams} options={allTeams.map(({ slug }) => ({
                value: slug,
                label: `#${slug}`,
            }))} clearable/>) : (<div>{inviteRequest.teams.join(', ')}</div>)}

      <ButtonGroup>
        <button_1.default size="small" busy={inviteRequestBusy[inviteRequest.id]} onClick={() => onDeny(inviteRequest)} icon={<icons_1.IconClose />} disabled={!canApprove} title={canApprove
            ? undefined
            : (0, locale_1.t)('This request needs to be reviewed by a privileged user')}>
          {(0, locale_1.t)('Deny')}
        </button_1.default>
        <confirm_1.default onConfirm={sendInvites} disableConfirmButton={!canSend} disabled={!canApprove || roleDisallowed} message={<React.Fragment>
              {(0, locale_1.tct)('Are you sure you want to invite [email] to your organization?', {
                email: inviteRequest.email,
            })}
              {headerInfo}
            </React.Fragment>}>
          <button_1.default priority="primary" size="small" busy={inviteRequestBusy[inviteRequest.id]} title={canApprove
            ? roleDisallowed
                ? (0, locale_1.t)(`You do not have permission to approve a user of this role.
                      Select a different role to approve this user.`)
                : undefined
            : (0, locale_1.t)('This request needs to be reviewed by a privileged user')} icon={<icons_1.IconCheckmark />}>
            {(0, locale_1.t)('Approve')}
          </button_1.default>
        </confirm_1.default>
      </ButtonGroup>
    </StyledPanelItem>);
    return (<InviteModalHook willInvite organization={organization} onSendInvites={() => onApprove(inviteRequest)}>
      {hookRenderer}
    </InviteModalHook>);
};
const JoinRequestIndicator = (0, styled_1.default)(tag_1.default) `
  text-transform: uppercase;
`;
const StyledPanelItem = (0, styled_1.default)(panels_1.PanelItem) `
  display: grid;
  grid-template-columns: minmax(150px, auto) minmax(100px, 140px) 220px max-content;
  grid-gap: ${(0, space_1.default)(2)};
  align-items: center;
`;
const UserName = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeLarge};
  overflow: hidden;
  text-overflow: ellipsis;
`;
const Description = (0, styled_1.default)('div') `
  display: block;
  color: ${p => p.theme.subText};
  font-size: 14px;
  overflow: hidden;
  text-overflow: ellipsis;
`;
const StyledRoleSelectControl = (0, styled_1.default)(roleSelectControl_1.default) `
  max-width: 140px;
`;
const TeamSelectControl = (0, styled_1.default)(multiSelectControl_1.default) `
  max-width: 220px;
  .Select-value-label {
    max-width: 150px;
    word-break: break-all;
  }
`;
const ButtonGroup = (0, styled_1.default)('div') `
  display: inline-grid;
  grid-template-columns: repeat(2, max-content);
  grid-gap: ${(0, space_1.default)(1)};
`;
exports.default = InviteRequestRow;
//# sourceMappingURL=inviteRequestRow.jsx.map