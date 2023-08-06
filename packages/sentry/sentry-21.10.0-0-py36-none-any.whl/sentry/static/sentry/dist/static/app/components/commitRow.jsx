Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const modal_1 = require("app/actionCreators/modal");
const userAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/userAvatar"));
const commitLink_1 = (0, tslib_1.__importDefault)(require("app/components/commitLink"));
const hovercard_1 = (0, tslib_1.__importDefault)(require("app/components/hovercard"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const panels_1 = require("app/components/panels");
const textOverflow_1 = (0, tslib_1.__importDefault)(require("app/components/textOverflow"));
const timeSince_1 = (0, tslib_1.__importDefault)(require("app/components/timeSince"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
class CommitRow extends React.Component {
    renderMessage(message) {
        if (!message) {
            return (0, locale_1.t)('No message provided');
        }
        const firstLine = message.split(/\n/)[0];
        return firstLine;
    }
    renderHovercardBody(author) {
        return (<EmailWarning>
        {(0, locale_1.tct)('The email [actorEmail] is not a member of your organization. [inviteUser:Invite] them or link additional emails in [accountSettings:account settings].', {
                actorEmail: <strong>{author.email}</strong>,
                accountSettings: <StyledLink to="/settings/account/emails/"/>,
                inviteUser: (<StyledLink to="" onClick={() => (0, modal_1.openInviteMembersModal)({
                        initialData: [
                            {
                                emails: new Set([author.email]),
                            },
                        ],
                        source: 'suspect_commit',
                    })}/>),
            })}
      </EmailWarning>);
    }
    render() {
        const _a = this.props, { commit, customAvatar } = _a, props = (0, tslib_1.__rest)(_a, ["commit", "customAvatar"]);
        const { id, dateCreated, message, author, repository } = commit;
        const nonMemberEmail = author && author.id === undefined;
        return (<panels_1.PanelItem key={id} {...props}>
        {customAvatar ? (customAvatar) : nonMemberEmail ? (<AvatarWrapper>
            <hovercard_1.default body={this.renderHovercardBody(author)}>
              <userAvatar_1.default size={36} user={author}/>
              <EmailWarningIcon>
                <icons_1.IconWarning size="xs"/>
              </EmailWarningIcon>
            </hovercard_1.default>
          </AvatarWrapper>) : (<AvatarWrapper>
            <userAvatar_1.default size={36} user={author}/>
          </AvatarWrapper>)}

        <CommitMessage>
          <Message>{this.renderMessage(message)}</Message>
          <Meta>
            {(0, locale_1.tct)('[author] committed [timeago]', {
                author: <strong>{(author && author.name) || (0, locale_1.t)('Unknown author')}</strong>,
                timeago: <timeSince_1.default date={dateCreated}/>,
            })}
          </Meta>
        </CommitMessage>

        <div>
          <commitLink_1.default commitId={id} repository={repository}/>
        </div>
      </panels_1.PanelItem>);
    }
}
const AvatarWrapper = (0, styled_1.default)('div') `
  position: relative;
  align-self: flex-start;
  margin-right: ${(0, space_1.default)(2)};
`;
const EmailWarning = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeSmall};
  line-height: 1.4;
  margin: -4px;
`;
const StyledLink = (0, styled_1.default)(link_1.default) `
  color: ${p => p.theme.textColor};
  border-bottom: 1px dotted ${p => p.theme.textColor};

  &:hover {
    color: ${p => p.theme.textColor};
  }
`;
const EmailWarningIcon = (0, styled_1.default)('span') `
  position: absolute;
  bottom: -6px;
  right: -7px;
  line-height: 12px;
  border-radius: 50%;
  border: 1px solid ${p => p.theme.white};
  background: ${p => p.theme.yellow200};
  padding: 1px 2px 3px 2px;
`;
const CommitMessage = (0, styled_1.default)('div') `
  flex: 1;
  flex-direction: column;
  min-width: 0;
  margin-right: ${(0, space_1.default)(2)};
`;
const Message = (0, styled_1.default)(textOverflow_1.default) `
  font-size: 15px;
  line-height: 1.1;
  font-weight: bold;
`;
const Meta = (0, styled_1.default)(textOverflow_1.default) `
  font-size: 13px;
  line-height: 1.5;
  margin: 0;
  color: ${p => p.theme.subText};
`;
exports.default = (0, styled_1.default)(CommitRow) `
  align-items: center;
`;
//# sourceMappingURL=commitRow.jsx.map