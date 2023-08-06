Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const userAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/userAvatar"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const hookOrDefault_1 = (0, tslib_1.__importDefault)(require("app/components/hookOrDefault"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const panels_1 = require("app/components/panels");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const isMemberDisabledFromLimit_1 = (0, tslib_1.__importDefault)(require("app/utils/isMemberDisabledFromLimit"));
const recreateRoute_1 = (0, tslib_1.__importDefault)(require("app/utils/recreateRoute"));
const DisabledMemberTooltip = (0, hookOrDefault_1.default)({
    hookName: 'component:disabled-member-tooltip',
    defaultComponent: ({ children }) => <react_1.Fragment>{children}</react_1.Fragment>,
});
class OrganizationMemberRow extends react_1.PureComponent {
    constructor() {
        super(...arguments);
        this.state = {
            busy: false,
        };
        this.handleRemove = () => {
            const { onRemove } = this.props;
            if (typeof onRemove !== 'function') {
                return;
            }
            this.setState({ busy: true });
            onRemove(this.props.member);
        };
        this.handleLeave = () => {
            const { onLeave } = this.props;
            if (typeof onLeave !== 'function') {
                return;
            }
            this.setState({ busy: true });
            onLeave(this.props.member);
        };
        this.handleSendInvite = () => {
            const { onSendInvite, member } = this.props;
            if (typeof onSendInvite !== 'function') {
                return;
            }
            onSendInvite(member);
        };
    }
    renderMemberRole() {
        const { member } = this.props;
        const { roleName, pending, expired } = member;
        if ((0, isMemberDisabledFromLimit_1.default)(member)) {
            return <DisabledMemberTooltip>{(0, locale_1.t)('Deactivated')}</DisabledMemberTooltip>;
        }
        if (pending) {
            return (<InvitedRole>
          <icons_1.IconMail size="md"/>
          {expired ? (0, locale_1.t)('Expired Invite') : (0, locale_1.tct)('Invited [roleName]', { roleName })}
        </InvitedRole>);
        }
        return roleName;
    }
    render() {
        const { params, routes, member, orgName, status, requireLink, memberCanLeave, currentUser, canRemoveMembers, canAddMembers, } = this.props;
        const { id, flags, email, name, pending, user } = member;
        // if member is not the only owner, they can leave
        const needsSso = !flags['sso:linked'] && requireLink;
        const isCurrentUser = currentUser.email === email;
        const showRemoveButton = !isCurrentUser;
        const showLeaveButton = isCurrentUser;
        const canRemoveMember = canRemoveMembers && !isCurrentUser;
        // member has a `user` property if they are registered with sentry
        // i.e. has accepted an invite to join org
        const has2fa = user && user.has2fa;
        const detailsUrl = (0, recreateRoute_1.default)(id, { routes, params });
        const isInviteSuccessful = status === 'success';
        const isInviting = status === 'loading';
        const showResendButton = pending || needsSso;
        return (<StyledPanelItem data-test-id={email}>
        <MemberHeading>
          <userAvatar_1.default size={32} user={user !== null && user !== void 0 ? user : { id: email, email }}/>
          <MemberDescription to={detailsUrl}>
            <h5 style={{ margin: '0 0 3px' }}>
              <UserName>{name}</UserName>
            </h5>
            <Email>{email}</Email>
          </MemberDescription>
        </MemberHeading>

        <div data-test-id="member-role">{this.renderMemberRole()}</div>

        <div data-test-id="member-status">
          {showResendButton ? (<react_1.Fragment>
              {isInviting && (<LoadingContainer>
                  <loadingIndicator_1.default mini/>
                </LoadingContainer>)}
              {isInviteSuccessful && <span>{(0, locale_1.t)('Sent!')}</span>}
              {!isInviting && !isInviteSuccessful && (<button_1.default disabled={!canAddMembers} priority="primary" size="small" onClick={this.handleSendInvite}>
                  {pending ? (0, locale_1.t)('Resend invite') : (0, locale_1.t)('Resend SSO link')}
                </button_1.default>)}
            </react_1.Fragment>) : (<AuthStatus>
              {has2fa ? (<icons_1.IconCheckmark isCircled color="success"/>) : (<icons_1.IconFlag color="error"/>)}
              {has2fa ? (0, locale_1.t)('2FA Enabled') : (0, locale_1.t)('2FA Not Enabled')}
            </AuthStatus>)}
        </div>

        {showRemoveButton || showLeaveButton ? (<div>
            {showRemoveButton && canRemoveMember && (<confirm_1.default message={(0, locale_1.tct)('Are you sure you want to remove [name] from [orgName]?', {
                        name,
                        orgName,
                    })} onConfirm={this.handleRemove}>
                <button_1.default data-test-id="remove" icon={<icons_1.IconSubtract isCircled size="xs"/>} size="small" busy={this.state.busy}>
                  {(0, locale_1.t)('Remove')}
                </button_1.default>
              </confirm_1.default>)}

            {showRemoveButton && !canRemoveMember && (<button_1.default disabled size="small" title={(0, locale_1.t)('You do not have access to remove members')} icon={<icons_1.IconSubtract isCircled size="xs"/>}>
                {(0, locale_1.t)('Remove')}
              </button_1.default>)}

            {showLeaveButton && memberCanLeave && (<confirm_1.default message={(0, locale_1.tct)('Are you sure you want to leave [orgName]?', {
                        orgName,
                    })} onConfirm={this.handleLeave}>
                <button_1.default priority="danger" size="small" icon={<icons_1.IconClose size="xs"/>}>
                  {(0, locale_1.t)('Leave')}
                </button_1.default>
              </confirm_1.default>)}

            {showLeaveButton && !memberCanLeave && (<button_1.default size="small" icon={<icons_1.IconClose size="xs"/>} disabled title={(0, locale_1.t)('You cannot leave this organization as you are the only organization owner.')}>
                {(0, locale_1.t)('Leave')}
              </button_1.default>)}
          </div>) : null}
      </StyledPanelItem>);
    }
}
exports.default = OrganizationMemberRow;
const StyledPanelItem = (0, styled_1.default)(panels_1.PanelItem) `
  display: grid;
  grid-template-columns: minmax(150px, 2fr) minmax(90px, 1fr) minmax(120px, 1fr) 90px;
  grid-gap: ${(0, space_1.default)(2)};
  align-items: center;
`;
const Section = (0, styled_1.default)('div') `
  display: inline-grid;
  grid-template-columns: max-content auto;
  grid-gap: ${(0, space_1.default)(1)};
  align-items: center;
`;
const MemberHeading = (0, styled_1.default)(Section) ``;
const MemberDescription = (0, styled_1.default)(link_1.default) `
  overflow: hidden;
`;
const UserName = (0, styled_1.default)('div') `
  display: block;
  font-size: ${p => p.theme.fontSizeLarge};
  overflow: hidden;
  text-overflow: ellipsis;
`;
const Email = (0, styled_1.default)('div') `
  color: ${p => p.theme.textColor};
  font-size: ${p => p.theme.fontSizeMedium};
  overflow: hidden;
  text-overflow: ellipsis;
`;
const InvitedRole = (0, styled_1.default)(Section) ``;
const LoadingContainer = (0, styled_1.default)('div') `
  margin-top: 0;
  margin-bottom: ${(0, space_1.default)(1.5)};
`;
const AuthStatus = (0, styled_1.default)(Section) ``;
//# sourceMappingURL=organizationMemberRow.jsx.map