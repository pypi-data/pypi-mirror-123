Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const account_1 = require("app/actionCreators/account");
const indicator_1 = require("app/actionCreators/indicator");
const members_1 = require("app/actionCreators/members");
const autoSelectText_1 = (0, tslib_1.__importDefault)(require("app/components/autoSelectText"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const dateTime_1 = (0, tslib_1.__importDefault)(require("app/components/dateTime"));
const notFound_1 = (0, tslib_1.__importDefault)(require("app/components/errors/notFound"));
const hookOrDefault_1 = (0, tslib_1.__importDefault)(require("app/components/hookOrDefault"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const panels_1 = require("app/components/panels");
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const locale_1 = require("app/locale");
const input_1 = require("app/styles/input");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const isMemberDisabledFromLimit_1 = (0, tslib_1.__importDefault)(require("app/utils/isMemberDisabledFromLimit"));
const recreateRoute_1 = (0, tslib_1.__importDefault)(require("app/utils/recreateRoute"));
const teams_1 = (0, tslib_1.__importDefault)(require("app/utils/teams"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const field_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const teamSelect_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/teamSelect"));
const roleSelect_1 = (0, tslib_1.__importDefault)(require("./inviteMember/roleSelect"));
const MULTIPLE_ORGS = (0, locale_1.t)('Cannot be reset since user is in more than one organization');
const NOT_ENROLLED = (0, locale_1.t)('Not enrolled in two-factor authentication');
const NO_PERMISSION = (0, locale_1.t)('You do not have permission to perform this action');
const TWO_FACTOR_REQUIRED = (0, locale_1.t)('Cannot be reset since two-factor is required for this organization');
const DisabledMemberTooltip = (0, hookOrDefault_1.default)({
    hookName: 'component:disabled-member-tooltip',
    defaultComponent: ({ children }) => <react_1.Fragment>{children}</react_1.Fragment>,
});
class OrganizationMemberDetail extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.handleSave = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { organization, params } = this.props;
            (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Saving...'));
            this.setState({ busy: true });
            try {
                yield (0, members_1.updateMember)(this.api, {
                    orgId: organization.slug,
                    memberId: params.memberId,
                    data: this.state.member,
                });
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Saved'));
                this.redirectToMemberPage();
            }
            catch (resp) {
                const errorMessage = (resp && resp.responseJSON && resp.responseJSON.detail) || (0, locale_1.t)('Could not save...');
                (0, indicator_1.addErrorMessage)(errorMessage);
            }
            this.setState({ busy: false });
        });
        this.handleInvite = (regenerate) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { organization, params } = this.props;
            (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Sending invite...'));
            this.setState({ busy: true });
            try {
                const data = yield (0, members_1.resendMemberInvite)(this.api, {
                    orgId: organization.slug,
                    memberId: params.memberId,
                    regenerate,
                });
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Sent invite!'));
                if (regenerate) {
                    this.setState(state => ({ member: Object.assign(Object.assign({}, state.member), data) }));
                }
            }
            catch (_err) {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Could not send invite'));
            }
            this.setState({ busy: false });
        });
        this.handleAddTeam = (team) => {
            const { member } = this.state;
            if (!member.teams.includes(team.slug)) {
                member.teams.push(team.slug);
            }
            this.setState({ member });
        };
        this.handleRemoveTeam = (removedTeam) => {
            const { member } = this.state;
            this.setState({
                member: Object.assign(Object.assign({}, member), { teams: member.teams.filter(slug => slug !== removedTeam) }),
            });
        };
        this.handle2faReset = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { organization, router } = this.props;
            const { user } = this.state.member;
            const requests = user.authenticators.map(auth => (0, account_1.removeAuthenticator)(this.api, user.id, auth.id));
            try {
                yield Promise.all(requests);
                router.push(`/settings/${organization.slug}/members/`);
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)('All authenticators have been removed'));
            }
            catch (err) {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Error removing authenticators'));
                Sentry.captureException(err);
            }
        });
        this.showResetButton = () => {
            const { organization } = this.props;
            const { member } = this.state;
            const { user } = member;
            if (!user || !user.authenticators || organization.require2FA) {
                return false;
            }
            const hasAuth = user.authenticators.length >= 1;
            return hasAuth && user.canReset2fa;
        };
        this.getTooltip = () => {
            const { organization } = this.props;
            const { member } = this.state;
            const { user } = member;
            if (!user) {
                return '';
            }
            if (!user.authenticators) {
                return NO_PERMISSION;
            }
            if (!user.authenticators.length) {
                return NOT_ENROLLED;
            }
            if (!user.canReset2fa) {
                return MULTIPLE_ORGS;
            }
            if (organization.require2FA) {
                return TWO_FACTOR_REQUIRED;
            }
            return '';
        };
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { roleList: [], selectedRole: '', member: null });
    }
    getEndpoints() {
        const { organization, params } = this.props;
        return [
            ['member', `/organizations/${organization.slug}/members/${params.memberId}/`],
        ];
    }
    redirectToMemberPage() {
        const { location, params, routes } = this.props;
        const members = (0, recreateRoute_1.default)('members/', {
            location,
            routes,
            params,
            stepBack: -2,
        });
        react_router_1.browserHistory.push(members);
    }
    get memberDeactivated() {
        return (0, isMemberDisabledFromLimit_1.default)(this.state.member);
    }
    renderMemberStatus(member) {
        if (this.memberDeactivated) {
            return (<em>
          <DisabledMemberTooltip>{(0, locale_1.t)('Deactivated')}</DisabledMemberTooltip>
        </em>);
        }
        if (member.expired) {
            return <em>{(0, locale_1.t)('Invitation Expired')}</em>;
        }
        if (member.pending) {
            return <em>{(0, locale_1.t)('Invitation Pending')}</em>;
        }
        return (0, locale_1.t)('Active');
    }
    renderBody() {
        const { organization } = this.props;
        const { member } = this.state;
        if (!member) {
            return <notFound_1.default />;
        }
        const { access } = organization;
        const inviteLink = member.invite_link;
        const canEdit = access.includes('org:write') && !this.memberDeactivated;
        const { email, expired, pending } = member;
        const canResend = !expired;
        const showAuth = !pending;
        return (<react_1.Fragment>
        <settingsPageHeader_1.default title={<react_1.Fragment>
              <div>{member.name}</div>
              <ExtraHeaderText>{(0, locale_1.t)('Member Settings')}</ExtraHeaderText>
            </react_1.Fragment>}/>

        <panels_1.Panel>
          <panels_1.PanelHeader>{(0, locale_1.t)('Basics')}</panels_1.PanelHeader>

          <panels_1.PanelBody>
            <panels_1.PanelItem>
              <OverflowWrapper>
                <Details>
                  <div>
                    <DetailLabel>{(0, locale_1.t)('Email')}</DetailLabel>
                    <div>
                      <externalLink_1.default href={`mailto:${email}`}>{email}</externalLink_1.default>
                    </div>
                  </div>
                  <div>
                    <DetailLabel>{(0, locale_1.t)('Status')}</DetailLabel>
                    <div data-test-id="member-status">
                      {this.renderMemberStatus(member)}
                    </div>
                  </div>
                  <div>
                    <DetailLabel>{(0, locale_1.t)('Added')}</DetailLabel>
                    <div>
                      <dateTime_1.default dateOnly date={member.dateCreated}/>
                    </div>
                  </div>
                </Details>

                {inviteLink && (<InviteSection>
                    <div>
                      <DetailLabel>{(0, locale_1.t)('Invite Link')}</DetailLabel>
                      <autoSelectText_1.default>
                        <CodeInput>{inviteLink}</CodeInput>
                      </autoSelectText_1.default>
                      <p className="help-block">
                        {(0, locale_1.t)('This unique invite link may only be used by this member.')}
                      </p>
                    </div>
                    <InviteActions>
                      <button_1.default onClick={() => this.handleInvite(true)}>
                        {(0, locale_1.t)('Generate New Invite')}
                      </button_1.default>
                      {canResend && (<button_1.default data-test-id="resend-invite" onClick={() => this.handleInvite(false)}>
                          {(0, locale_1.t)('Resend Invite')}
                        </button_1.default>)}
                    </InviteActions>
                  </InviteSection>)}
              </OverflowWrapper>
            </panels_1.PanelItem>
          </panels_1.PanelBody>
        </panels_1.Panel>

        {showAuth && (<panels_1.Panel>
            <panels_1.PanelHeader>{(0, locale_1.t)('Authentication')}</panels_1.PanelHeader>
            <panels_1.PanelBody>
              <field_1.default alignRight flexibleControlStateSize label={(0, locale_1.t)('Reset two-factor authentication')} help={(0, locale_1.t)('Resetting two-factor authentication will remove all two-factor authentication methods for this member.')}>
                <tooltip_1.default data-test-id="reset-2fa-tooltip" disabled={this.showResetButton()} title={this.getTooltip()}>
                  <confirm_1.default disabled={!this.showResetButton()} message={(0, locale_1.tct)('Are you sure you want to disable all two-factor authentication methods for [name]?', { name: member.name ? member.name : 'this member' })} onConfirm={this.handle2faReset} data-test-id="reset-2fa-confirm">
                    <button_1.default data-test-id="reset-2fa" priority="danger">
                      {(0, locale_1.t)('Reset two-factor authentication')}
                    </button_1.default>
                  </confirm_1.default>
                </tooltip_1.default>
              </field_1.default>
            </panels_1.PanelBody>
          </panels_1.Panel>)}

        <roleSelect_1.default enforceAllowed={false} disabled={!canEdit} roleList={member.roles} selectedRole={member.role} setRole={slug => this.setState({ member: Object.assign(Object.assign({}, member), { role: slug }) })}/>

        <teams_1.default slugs={member.teams}>
          {({ teams, initiallyLoaded }) => (<teamSelect_1.default organization={organization} selectedTeams={teams} disabled={!canEdit} onAddTeam={this.handleAddTeam} onRemoveTeam={this.handleRemoveTeam} loadingTeams={!initiallyLoaded}/>)}
        </teams_1.default>

        <Footer>
          <button_1.default priority="primary" busy={this.state.busy} onClick={this.handleSave} disabled={!canEdit}>
            {(0, locale_1.t)('Save Member')}
          </button_1.default>
        </Footer>
      </react_1.Fragment>);
    }
}
exports.default = (0, withOrganization_1.default)(OrganizationMemberDetail);
const ExtraHeaderText = (0, styled_1.default)('div') `
  color: ${p => p.theme.gray300};
  font-weight: normal;
  font-size: ${p => p.theme.fontSizeLarge};
`;
const Details = (0, styled_1.default)('div') `
  display: grid;
  grid-auto-flow: column;
  grid-template-columns: 2fr 1fr 1fr;
  grid-gap: ${(0, space_1.default)(2)};
  width: 100%;

  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    grid-auto-flow: row;
    grid-template-columns: auto;
  }
`;
const DetailLabel = (0, styled_1.default)('div') `
  font-weight: bold;
  margin-bottom: ${(0, space_1.default)(0.5)};
  color: ${p => p.theme.textColor};
`;
const OverflowWrapper = (0, styled_1.default)('div') `
  overflow: hidden;
  flex: 1;
`;
const InviteSection = (0, styled_1.default)('div') `
  border-top: 1px solid ${p => p.theme.border};
  margin-top: ${(0, space_1.default)(2)};
  padding-top: ${(0, space_1.default)(2)};
`;
const CodeInput = (0, styled_1.default)('code') `
  ${p => (0, input_1.inputStyles)(p)}; /* Have to do this for typescript :( */
`;
const InviteActions = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(1)};
  grid-auto-flow: column;
  justify-content: flex-end;
  margin-top: ${(0, space_1.default)(2)};
`;
const Footer = (0, styled_1.default)('div') `
  display: flex;
  justify-content: flex-end;
`;
//# sourceMappingURL=organizationMemberDetail.jsx.map