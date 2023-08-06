Object.defineProperty(exports, "__esModule", { value: true });
exports.modalCss = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const hookOrDefault_1 = (0, tslib_1.__importDefault)(require("app/components/hookOrDefault"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const questionTooltip_1 = (0, tslib_1.__importDefault)(require("app/components/questionTooltip"));
const constants_1 = require("app/constants");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const guid_1 = require("app/utils/guid");
const withLatestContext_1 = (0, tslib_1.__importDefault)(require("app/utils/withLatestContext"));
const inviteRowControl_1 = (0, tslib_1.__importDefault)(require("./inviteRowControl"));
const DEFAULT_ROLE = 'member';
const InviteModalHook = (0, hookOrDefault_1.default)({
    hookName: 'member-invite-modal:customization',
    defaultComponent: ({ onSendInvites, children }) => children({ sendInvites: onSendInvites, canSend: true }),
});
class InviteMembersModal extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        /**
         * Used for analytics tracking of the modals usage.
         */
        this.sessionId = '';
        this.reset = () => {
            this.setState({
                pendingInvites: [this.inviteTemplate],
                inviteStatus: {},
                complete: false,
                sendingInvites: false,
            });
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'invite_modal.add_more',
                eventName: 'Invite Modal: Add More',
                organization_id: this.props.organization.id,
                modal_session: this.sessionId,
            });
        };
        this.sendInvite = (invite) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { slug } = this.props.organization;
            const data = {
                email: invite.email,
                teams: [...invite.teams],
                role: invite.role,
            };
            this.setState(state => ({
                inviteStatus: Object.assign(Object.assign({}, state.inviteStatus), { [invite.email]: { sent: false } }),
            }));
            const endpoint = this.willInvite
                ? `/organizations/${slug}/members/`
                : `/organizations/${slug}/invite-requests/`;
            try {
                yield this.api.requestPromise(endpoint, { method: 'POST', data });
            }
            catch (err) {
                const errorResponse = err.responseJSON;
                // Use the email error message if available. This inconsistently is
                // returned as either a list of errors for the field, or a single error.
                const emailError = !errorResponse || !errorResponse.email
                    ? false
                    : Array.isArray(errorResponse.email)
                        ? errorResponse.email[0]
                        : errorResponse.email;
                const error = emailError || (0, locale_1.t)('Could not invite user');
                this.setState(state => ({
                    inviteStatus: Object.assign(Object.assign({}, state.inviteStatus), { [invite.email]: { sent: false, error } }),
                }));
                return;
            }
            this.setState(state => ({
                inviteStatus: Object.assign(Object.assign({}, state.inviteStatus), { [invite.email]: { sent: true } }),
            }));
        });
        this.sendInvites = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            this.setState({ sendingInvites: true });
            yield Promise.all(this.invites.map(this.sendInvite));
            this.setState({ sendingInvites: false, complete: true });
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: this.willInvite
                    ? 'invite_modal.invites_sent'
                    : 'invite_modal.requests_sent',
                eventName: this.willInvite
                    ? 'Invite Modal: Invites Sent'
                    : 'Invite Modal: Requests Sent',
                organization_id: this.props.organization.id,
                modal_session: this.sessionId,
            });
        });
        this.addInviteRow = () => this.setState(state => ({
            pendingInvites: [...state.pendingInvites, this.inviteTemplate],
        }));
    }
    get inviteTemplate() {
        return {
            emails: new Set(),
            teams: new Set(),
            role: DEFAULT_ROLE,
        };
    }
    componentDidMount() {
        this.sessionId = (0, guid_1.uniqueId)();
        const { organization, source } = this.props;
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey: 'invite_modal.opened',
            eventName: 'Invite Modal: Opened',
            organization_id: organization.id,
            modal_session: this.sessionId,
            can_invite: this.willInvite,
            source,
        });
    }
    getEndpoints() {
        const orgId = this.props.organization.slug;
        return [['member', `/organizations/${orgId}/members/me/`]];
    }
    getDefaultState() {
        const state = super.getDefaultState();
        const { initialData } = this.props;
        const pendingInvites = initialData
            ? initialData.map(initial => (Object.assign(Object.assign({}, this.inviteTemplate), initial)))
            : [this.inviteTemplate];
        return Object.assign(Object.assign({}, state), { pendingInvites, inviteStatus: {}, complete: false, sendingInvites: false });
    }
    setEmails(emails, index) {
        this.setState(state => {
            const pendingInvites = [...state.pendingInvites];
            pendingInvites[index] = Object.assign(Object.assign({}, pendingInvites[index]), { emails: new Set(emails) });
            return { pendingInvites };
        });
    }
    setTeams(teams, index) {
        this.setState(state => {
            const pendingInvites = [...state.pendingInvites];
            pendingInvites[index] = Object.assign(Object.assign({}, pendingInvites[index]), { teams: new Set(teams) });
            return { pendingInvites };
        });
    }
    setRole(role, index) {
        this.setState(state => {
            const pendingInvites = [...state.pendingInvites];
            pendingInvites[index] = Object.assign(Object.assign({}, pendingInvites[index]), { role });
            return { pendingInvites };
        });
    }
    removeInviteRow(index) {
        this.setState(state => {
            const pendingInvites = [...state.pendingInvites];
            pendingInvites.splice(index, 1);
            return { pendingInvites };
        });
    }
    get invites() {
        return this.state.pendingInvites.reduce((acc, row) => [
            ...acc,
            ...[...row.emails].map(email => ({ email, teams: row.teams, role: row.role })),
        ], []);
    }
    get hasDuplicateEmails() {
        const emails = this.invites.map(inv => inv.email);
        return emails.length !== new Set(emails).size;
    }
    get isValidInvites() {
        return this.invites.length > 0 && !this.hasDuplicateEmails;
    }
    get statusMessage() {
        const { sendingInvites, complete, inviteStatus } = this.state;
        if (sendingInvites) {
            return (<StatusMessage>
          <loadingIndicator_1.default mini relative hideMessage size={16}/>
          {this.willInvite
                    ? (0, locale_1.t)('Sending organization invitations...')
                    : (0, locale_1.t)('Sending invite requests...')}
        </StatusMessage>);
        }
        if (complete) {
            const statuses = Object.values(inviteStatus);
            const sentCount = statuses.filter(i => i.sent).length;
            const errorCount = statuses.filter(i => i.error).length;
            if (this.willInvite) {
                const invites = <strong>{(0, locale_1.tn)('%s invite', '%s invites', sentCount)}</strong>;
                const tctComponents = {
                    invites,
                    failed: errorCount,
                };
                return (<StatusMessage status="success">
            <icons_1.IconCheckmark size="sm"/>
            {errorCount > 0
                        ? (0, locale_1.tct)('Sent [invites], [failed] failed to send.', tctComponents)
                        : (0, locale_1.tct)('Sent [invites]', tctComponents)}
          </StatusMessage>);
            }
            else {
                const inviteRequests = (<strong>{(0, locale_1.tn)('%s invite request', '%s invite requests', sentCount)}</strong>);
                const tctComponents = {
                    inviteRequests,
                    failed: errorCount,
                };
                return (<StatusMessage status="success">
            <icons_1.IconCheckmark size="sm"/>
            {errorCount > 0
                        ? (0, locale_1.tct)('[inviteRequests] pending approval, [failed] failed to send.', tctComponents)
                        : (0, locale_1.tct)('[inviteRequests] pending approval', tctComponents)}
          </StatusMessage>);
            }
        }
        if (this.hasDuplicateEmails) {
            return (<StatusMessage status="error">
          <icons_1.IconWarning size="sm"/>
          {(0, locale_1.t)('Duplicate emails between invite rows.')}
        </StatusMessage>);
        }
        return null;
    }
    get willInvite() {
        var _a;
        return (_a = this.props.organization.access) === null || _a === void 0 ? void 0 : _a.includes('member:write');
    }
    get inviteButtonLabel() {
        if (this.invites.length > 0) {
            const numberInvites = this.invites.length;
            // Note we use `t()` here because `tn()` expects the same # of string formatters
            const inviteText = numberInvites === 1 ? (0, locale_1.t)('Send invite') : (0, locale_1.t)('Send invites (%s)', numberInvites);
            const requestText = numberInvites === 1
                ? (0, locale_1.t)('Send invite request')
                : (0, locale_1.t)('Send invite requests (%s)', numberInvites);
            return this.willInvite ? inviteText : requestText;
        }
        return this.willInvite ? (0, locale_1.t)('Send invite') : (0, locale_1.t)('Send invite request');
    }
    render() {
        const { Footer, closeModal, organization } = this.props;
        const { pendingInvites, sendingInvites, complete, inviteStatus, member } = this.state;
        const disableInputs = sendingInvites || complete;
        // eslint-disable-next-line react/prop-types
        const hookRenderer = ({ sendInvites, canSend, headerInfo }) => (<React.Fragment>
        <Heading>
          {(0, locale_1.t)('Invite New Members')}
          {!this.willInvite && (<questionTooltip_1.default title={(0, locale_1.t)(`You do not have permission to directly invite members. Email
                 addresses entered here will be forwarded to organization
                 managers and owners; they will be prompted to approve the
                 invitation.`)} size="sm" position="bottom"/>)}
        </Heading>
        <Subtext>
          {this.willInvite
                ? (0, locale_1.t)('Invite new members by email to join your organization.')
                : (0, locale_1.t)(`You don’t have permission to directly invite users, but we'll send a request to your organization owner and manager for review.`)}
        </Subtext>

        {headerInfo}

        <InviteeHeadings>
          <div>{(0, locale_1.t)('Email addresses')}</div>
          <div>{(0, locale_1.t)('Role')}</div>
          <div>{(0, locale_1.t)('Add to team')}</div>
        </InviteeHeadings>

        {pendingInvites.map(({ emails, role, teams }, i) => (<StyledInviteRow key={i} disabled={disableInputs} emails={[...emails]} role={role} teams={[...teams]} roleOptions={member ? member.roles : constants_1.MEMBER_ROLES} roleDisabledUnallowed={this.willInvite} inviteStatus={inviteStatus} onRemove={() => this.removeInviteRow(i)} onChangeEmails={opts => { var _a; return this.setEmails((_a = opts === null || opts === void 0 ? void 0 : opts.map(v => v.value)) !== null && _a !== void 0 ? _a : [], i); }} onChangeRole={value => this.setRole(value === null || value === void 0 ? void 0 : value.value, i)} onChangeTeams={opts => this.setTeams(opts ? opts.map(v => v.value) : [], i)} disableRemove={disableInputs || pendingInvites.length === 1}/>))}

        <AddButton disabled={disableInputs} priority="link" onClick={this.addInviteRow} icon={<icons_1.IconAdd size="xs" isCircled/>}>
          {(0, locale_1.t)('Add another')}
        </AddButton>

        <Footer>
          <FooterContent>
            <div>{this.statusMessage}</div>

            {complete ? (<React.Fragment>
                <button_1.default data-test-id="send-more" size="small" onClick={this.reset}>
                  {(0, locale_1.t)('Send more invites')}
                </button_1.default>
                <button_1.default data-test-id="close" priority="primary" size="small" onClick={() => {
                    (0, analytics_1.trackAnalyticsEvent)({
                        eventKey: 'invite_modal.closed',
                        eventName: 'Invite Modal: Closed',
                        organization_id: this.props.organization.id,
                        modal_session: this.sessionId,
                    });
                    closeModal();
                }}>
                  {(0, locale_1.t)('Close')}
                </button_1.default>
              </React.Fragment>) : (<React.Fragment>
                <button_1.default data-test-id="cancel" size="small" onClick={closeModal} disabled={disableInputs}>
                  {(0, locale_1.t)('Cancel')}
                </button_1.default>
                <button_1.default size="small" data-test-id="send-invites" priority="primary" disabled={!canSend || !this.isValidInvites || disableInputs} onClick={sendInvites}>
                  {this.inviteButtonLabel}
                </button_1.default>
              </React.Fragment>)}
          </FooterContent>
        </Footer>
      </React.Fragment>);
        return (<InviteModalHook organization={organization} willInvite={this.willInvite} onSendInvites={this.sendInvites}>
        {hookRenderer}
      </InviteModalHook>);
    }
}
const Heading = (0, styled_1.default)('h1') `
  display: inline-grid;
  grid-gap: ${(0, space_1.default)(1.5)};
  grid-auto-flow: column;
  align-items: center;
  font-weight: 400;
  font-size: ${p => p.theme.headerFontSize};
  margin-top: 0;
  margin-bottom: ${(0, space_1.default)(0.75)};
`;
const Subtext = (0, styled_1.default)('p') `
  color: ${p => p.theme.subText};
  margin-bottom: ${(0, space_1.default)(3)};
`;
const inviteRowGrid = (0, react_1.css) `
  display: grid;
  grid-gap: ${(0, space_1.default)(1.5)};
  grid-template-columns: 3fr 180px 2fr max-content;
`;
const InviteeHeadings = (0, styled_1.default)('div') `
  ${inviteRowGrid};

  margin-bottom: ${(0, space_1.default)(1)};
  font-weight: 600;
  text-transform: uppercase;
  font-size: ${p => p.theme.fontSizeSmall};
`;
const StyledInviteRow = (0, styled_1.default)(inviteRowControl_1.default) `
  ${inviteRowGrid};
  margin-bottom: ${(0, space_1.default)(1.5)};
`;
const AddButton = (0, styled_1.default)(button_1.default) `
  margin-top: ${(0, space_1.default)(3)};
`;
const FooterContent = (0, styled_1.default)('div') `
  width: 100%;
  display: grid;
  grid-template-columns: 1fr max-content max-content;
  grid-gap: ${(0, space_1.default)(1)};
`;
const StatusMessage = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: max-content max-content;
  grid-gap: ${(0, space_1.default)(1)};
  align-items: center;
  font-size: ${p => p.theme.fontSizeMedium};
  color: ${p => (p.status === 'error' ? p.theme.red300 : p.theme.gray400)};

  > :first-child {
    ${p => p.status === 'success' && `color: ${p.theme.green300}`};
  }
`;
exports.modalCss = (0, react_1.css) `
  width: 100%;
  max-width: 800px;
  margin: 50px auto;
`;
exports.default = (0, withLatestContext_1.default)(InviteMembersModal);
//# sourceMappingURL=index.jsx.map