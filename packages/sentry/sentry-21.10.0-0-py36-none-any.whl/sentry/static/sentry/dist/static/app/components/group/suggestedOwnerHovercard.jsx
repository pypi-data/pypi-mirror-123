Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const modal_1 = require("app/actionCreators/modal");
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const actorAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/actorAvatar"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const hovercard_1 = (0, tslib_1.__importDefault)(require("app/components/hovercard"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
class SuggestedOwnerHovercard extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            commitsExpanded: false,
            rulesExpanded: false,
        };
    }
    render() {
        const _a = this.props, { actor, commits, rules } = _a, props = (0, tslib_1.__rest)(_a, ["actor", "commits", "rules"]);
        const { commitsExpanded, rulesExpanded } = this.state;
        const modalData = {
            initialData: [
                {
                    emails: actor.email ? new Set([actor.email]) : new Set([]),
                },
            ],
            source: 'suggested_assignees',
        };
        return (<hovercard_1.default header={<React.Fragment>
            <HovercardHeader>
              <HovercardActorAvatar actor={actor}/>
              {actor.name || actor.email}
            </HovercardHeader>
            {actor.id === undefined && (<EmailAlert icon={<icons_1.IconWarning size="xs"/>} type="warning">
                {(0, locale_1.tct)('The email [actorEmail] is not a member of your organization. [inviteUser:Invite] them or link additional emails in [accountSettings:account settings].', {
                        actorEmail: <strong>{actor.email}</strong>,
                        accountSettings: <link_1.default to="/settings/account/emails/"/>,
                        inviteUser: <a onClick={() => (0, modal_1.openInviteMembersModal)(modalData)}/>,
                    })}
              </EmailAlert>)}
          </React.Fragment>} body={<HovercardBody>
            {commits !== undefined && (<React.Fragment>
                <div className="divider">
                  <h6>{(0, locale_1.t)('Commits')}</h6>
                </div>
                <div>
                  {commits
                        .slice(0, commitsExpanded ? commits.length : 3)
                        .map(({ message, dateCreated }, i) => (<CommitReasonItem key={i}>
                        <CommitIcon />
                        <CommitMessage message={message !== null && message !== void 0 ? message : undefined} date={dateCreated}/>
                      </CommitReasonItem>))}
                </div>
                {commits.length > 3 && !commitsExpanded ? (<ViewMoreButton onClick={() => this.setState({ commitsExpanded: true })}/>) : null}
              </React.Fragment>)}
            {(0, utils_1.defined)(rules) && (<React.Fragment>
                <div className="divider">
                  <h6>{(0, locale_1.t)('Matching Ownership Rules')}</h6>
                </div>
                <div>
                  {rules
                        .slice(0, rulesExpanded ? rules.length : 3)
                        .map(([type, matched], i) => (<RuleReasonItem key={i}>
                        <OwnershipTag tagType={type}/>
                        <OwnershipValue>{matched}</OwnershipValue>
                      </RuleReasonItem>))}
                </div>
                {rules.length > 3 && !rulesExpanded ? (<ViewMoreButton onClick={() => this.setState({ rulesExpanded: true })}/>) : null}
              </React.Fragment>)}
          </HovercardBody>} {...props}/>);
    }
}
const tagColors = {
    url: theme_1.default.green200,
    path: theme_1.default.purple300,
    tag: theme_1.default.blue300,
    codeowners: theme_1.default.orange300,
};
const CommitIcon = (0, styled_1.default)(icons_1.IconCommit) `
  margin-right: ${(0, space_1.default)(0.5)};
  flex-shrink: 0;
`;
const CommitMessage = (0, styled_1.default)((_a) => {
    var { message = '', date } = _a, props = (0, tslib_1.__rest)(_a, ["message", "date"]);
    return (<div {...props}>
    {message.split('\n')[0]}
    <CommitDate date={date}/>
  </div>);
}) `
  color: ${p => p.theme.textColor};
  font-size: ${p => p.theme.fontSizeExtraSmall};
  margin-top: ${(0, space_1.default)(0.25)};
  hyphens: auto;
`;
const CommitDate = (0, styled_1.default)((_a) => {
    var { date } = _a, props = (0, tslib_1.__rest)(_a, ["date"]);
    return (<div {...props}>{(0, moment_1.default)(date).fromNow()}</div>);
}) `
  margin-top: ${(0, space_1.default)(0.5)};
  color: ${p => p.theme.gray300};
`;
const CommitReasonItem = (0, styled_1.default)('div') `
  display: flex;
  align-items: flex-start;

  &:not(:last-child) {
    margin-bottom: ${(0, space_1.default)(1)};
  }
`;
const RuleReasonItem = (0, styled_1.default)('code') `
  display: flex;
  align-items: flex-start;

  &:not(:last-child) {
    margin-bottom: ${(0, space_1.default)(1)};
  }
`;
const OwnershipTag = (0, styled_1.default)((_a) => {
    var { tagType } = _a, props = (0, tslib_1.__rest)(_a, ["tagType"]);
    return <div {...props}>{tagType}</div>;
}) `
  background: ${p => tagColors[p.tagType.indexOf('tags') === -1 ? p.tagType : 'tag']};
  color: ${p => p.theme.white};
  font-size: ${p => p.theme.fontSizeExtraSmall};
  padding: ${(0, space_1.default)(0.25)} ${(0, space_1.default)(0.5)};
  margin: ${(0, space_1.default)(0.25)} ${(0, space_1.default)(0.5)} ${(0, space_1.default)(0.25)} 0;
  border-radius: 2px;
  font-weight: bold;
  text-align: center;
`;
const ViewMoreButton = (0, styled_1.default)((p) => (<button_1.default {...p} priority="link" size="zero">
    {(0, locale_1.t)('View more')}
  </button_1.default>)) `
  border: none;
  color: ${p => p.theme.gray300};
  font-size: ${p => p.theme.fontSizeExtraSmall};
  padding: ${(0, space_1.default)(0.25)} ${(0, space_1.default)(0.5)};
  margin: ${(0, space_1.default)(1)} ${(0, space_1.default)(0.25)} ${(0, space_1.default)(0.25)} 0;
  width: 100%;
  min-width: 34px;
`;
const OwnershipValue = (0, styled_1.default)('code') `
  word-break: break-all;
  line-height: 1.2;
`;
const EmailAlert = (0, styled_1.default)(alert_1.default) `
  margin: 10px -13px -13px;
  border-radius: 0;
  border-color: #ece0b0;
  padding: 10px;
  font-size: ${p => p.theme.fontSizeSmall};
  font-weight: normal;
  box-shadow: none;
`;
const HovercardHeader = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
`;
const HovercardActorAvatar = (0, styled_1.default)(p => (<actorAvatar_1.default size={20} hasTooltip={false} {...p}/>)) `
  margin-right: ${(0, space_1.default)(1)};
`;
const HovercardBody = (0, styled_1.default)('div') `
  margin-top: -${(0, space_1.default)(2)};
`;
exports.default = SuggestedOwnerHovercard;
//# sourceMappingURL=suggestedOwnerHovercard.jsx.map