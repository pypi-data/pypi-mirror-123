Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const avatar_1 = (0, tslib_1.__importDefault)(require("app/components/activity/item/avatar"));
const commitLink_1 = (0, tslib_1.__importDefault)(require("app/components/commitLink"));
const duration_1 = (0, tslib_1.__importDefault)(require("app/components/duration"));
const issueLink_1 = (0, tslib_1.__importDefault)(require("app/components/issueLink"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const pullRequestLink_1 = (0, tslib_1.__importDefault)(require("app/components/pullRequestLink"));
const timeSince_1 = (0, tslib_1.__importDefault)(require("app/components/timeSince"));
const version_1 = (0, tslib_1.__importDefault)(require("app/components/version"));
const versionHoverCard_1 = (0, tslib_1.__importDefault)(require("app/components/versionHoverCard"));
const locale_1 = require("app/locale");
const memberListStore_1 = (0, tslib_1.__importDefault)(require("app/stores/memberListStore"));
const teamStore_1 = (0, tslib_1.__importDefault)(require("app/stores/teamStore"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const marked_1 = (0, tslib_1.__importDefault)(require("app/utils/marked"));
const defaultProps = {
    defaultClipped: false,
    clipHeight: 68,
};
class ActivityItem extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            clipped: this.props.defaultClipped,
        };
        this.activityBubbleRef = (0, react_1.createRef)();
        this.formatProjectActivity = (author, item) => {
            const data = item.data;
            const { organization } = this.props;
            const orgId = organization.slug;
            const issue = item.issue;
            const basePath = `/organizations/${orgId}/issues/`;
            const issueLink = issue ? (<issueLink_1.default orgId={orgId} issue={issue} to={`${basePath}${issue.id}/`} card>
        {issue.shortId}
      </issueLink_1.default>) : null;
            const versionLink = this.renderVersionLink(data.version, item);
            switch (item.type) {
                case 'note':
                    return (0, locale_1.tct)('[author] commented on [issue]', {
                        author,
                        issue: (<issueLink_1.default card orgId={orgId} issue={issue} to={`${basePath}${issue.id}/activity/#event_${item.id}`}>
              {issue.shortId}
            </issueLink_1.default>),
                    });
                case 'set_resolved':
                    return (0, locale_1.tct)('[author] marked [issue] as resolved', {
                        author,
                        issue: issueLink,
                    });
                case 'set_resolved_by_age':
                    return (0, locale_1.tct)('[author] marked [issue] as resolved due to age', {
                        author,
                        issue: issueLink,
                    });
                case 'set_resolved_in_release':
                    const { current_release_version, version } = item.data;
                    if (current_release_version) {
                        return (0, locale_1.tct)('[author] marked [issue] as resolved in releases greater than [version]', {
                            author,
                            version: this.renderVersionLink(current_release_version, item),
                            issue: issueLink,
                        });
                    }
                    if (version) {
                        return (0, locale_1.tct)('[author] marked [issue] as resolved in [version]', {
                            author,
                            version: versionLink,
                            issue: issueLink,
                        });
                    }
                    return (0, locale_1.tct)('[author] marked [issue] as resolved in the upcoming release', {
                        author,
                        issue: issueLink,
                    });
                case 'set_resolved_in_commit':
                    return (0, locale_1.tct)('[author] marked [issue] as resolved in [version]', {
                        author,
                        version: (<commitLink_1.default inline commitId={data.commit && data.commit.id} repository={data.commit && data.commit.repository}/>),
                        issue: issueLink,
                    });
                case 'set_resolved_in_pull_request':
                    return (0, locale_1.tct)('[author] marked [issue] as resolved in [version]', {
                        author,
                        version: (<pullRequestLink_1.default inline pullRequest={data.pullRequest} repository={data.pullRequest && data.pullRequest.repository}/>),
                        issue: issueLink,
                    });
                case 'set_unresolved':
                    return (0, locale_1.tct)('[author] marked [issue] as unresolved', {
                        author,
                        issue: issueLink,
                    });
                case 'set_ignored':
                    if (data.ignoreDuration) {
                        return (0, locale_1.tct)('[author] ignored [issue] for [duration]', {
                            author,
                            duration: <duration_1.default seconds={data.ignoreDuration * 60}/>,
                            issue: issueLink,
                        });
                    }
                    else if (data.ignoreCount && data.ignoreWindow) {
                        return (0, locale_1.tct)('[author] ignored [issue] until it happens [count] time(s) in [duration]', {
                            author,
                            count: data.ignoreCount,
                            duration: <duration_1.default seconds={data.ignoreWindow * 60}/>,
                            issue: issueLink,
                        });
                    }
                    else if (data.ignoreCount) {
                        return (0, locale_1.tct)('[author] ignored [issue] until it happens [count] time(s)', {
                            author,
                            count: data.ignoreCount,
                            issue: issueLink,
                        });
                    }
                    else if (data.ignoreUserCount && data.ignoreUserWindow) {
                        return (0, locale_1.tct)('[author] ignored [issue] until it affects [count] user(s) in [duration]', {
                            author,
                            count: data.ignoreUserCount,
                            duration: <duration_1.default seconds={data.ignoreUserWindow * 60}/>,
                            issue: issueLink,
                        });
                    }
                    else if (data.ignoreUserCount) {
                        return (0, locale_1.tct)('[author] ignored [issue] until it affects [count] user(s)', {
                            author,
                            count: data.ignoreUserCount,
                            issue: issueLink,
                        });
                    }
                    return (0, locale_1.tct)('[author] ignored [issue]', {
                        author,
                        issue: issueLink,
                    });
                case 'set_public':
                    return (0, locale_1.tct)('[author] made [issue] public', {
                        author,
                        issue: issueLink,
                    });
                case 'set_private':
                    return (0, locale_1.tct)('[author] made [issue] private', {
                        author,
                        issue: issueLink,
                    });
                case 'set_regression':
                    if (data.version) {
                        return (0, locale_1.tct)('[author] marked [issue] as a regression in [version]', {
                            author,
                            version: versionLink,
                            issue: issueLink,
                        });
                    }
                    return (0, locale_1.tct)('[author] marked [issue] as a regression', {
                        author,
                        issue: issueLink,
                    });
                case 'create_issue':
                    return (0, locale_1.tct)('[author] linked [issue] on [provider]', {
                        author,
                        provider: data.provider,
                        issue: issueLink,
                    });
                case 'unmerge_destination':
                    return (0, locale_1.tn)('%2$s migrated %1$s fingerprint from %3$s to %4$s', '%2$s migrated %1$s fingerprints from %3$s to %4$s', data.fingerprints.length, author, data.source ? (<a href={`${basePath}${data.source.id}`}>{data.source.shortId}</a>) : ((0, locale_1.t)('a group')), issueLink);
                case 'first_seen':
                    return (0, locale_1.tct)('[author] saw [link:issue]', {
                        author,
                        issue: issueLink,
                    });
                case 'assigned':
                    let assignee;
                    if (data.assigneeType === 'team') {
                        const team = teamStore_1.default.getById(data.assignee);
                        assignee = team ? team.slug : '<unknown-team>';
                        return (0, locale_1.tct)('[author] assigned [issue] to #[assignee]', {
                            author,
                            issue: issueLink,
                            assignee,
                        });
                    }
                    if (item.user && data.assignee === item.user.id) {
                        return (0, locale_1.tct)('[author] assigned [issue] to themselves', {
                            author,
                            issue: issueLink,
                        });
                    }
                    assignee = memberListStore_1.default.getById(data.assignee);
                    if (assignee && assignee.email) {
                        return (0, locale_1.tct)('[author] assigned [issue] to [assignee]', {
                            author,
                            assignee: <span title={assignee.email}>{assignee.name}</span>,
                            issue: issueLink,
                        });
                    }
                    else if (data.assigneeEmail) {
                        return (0, locale_1.tct)('[author] assigned [issue] to [assignee]', {
                            author,
                            assignee: data.assigneeEmail,
                            issue: issueLink,
                        });
                    }
                    return (0, locale_1.tct)('[author] assigned [issue] to an [help:unknown user]', {
                        author,
                        help: <span title={data.assignee}/>,
                        issue: issueLink,
                    });
                case 'unassigned':
                    return (0, locale_1.tct)('[author] unassigned [issue]', {
                        author,
                        issue: issueLink,
                    });
                case 'merge':
                    return (0, locale_1.tct)('[author] merged [count] [link:issues]', {
                        author,
                        count: data.issues.length + 1,
                        link: <link_1.default to={`${basePath}${issue.id}/`}/>,
                    });
                case 'release':
                    return (0, locale_1.tct)('[author] released version [version]', {
                        author,
                        version: versionLink,
                    });
                case 'deploy':
                    return (0, locale_1.tct)('[author] deployed version [version] to [environment].', {
                        author,
                        version: versionLink,
                        environment: data.environment || 'Default Environment',
                    });
                case 'mark_reviewed':
                    return (0, locale_1.tct)('[author] marked [issue] as reviewed', {
                        author,
                        issue: issueLink,
                    });
                default:
                    return ''; // should never hit (?)
            }
        };
    }
    componentDidMount() {
        if (this.activityBubbleRef.current) {
            const bubbleHeight = this.activityBubbleRef.current.offsetHeight;
            if (bubbleHeight > this.props.clipHeight) {
                // okay if this causes re-render; cannot determine until
                // rendered first anyways
                // eslint-disable-next-line react/no-did-mount-set-state
                this.setState({ clipped: true });
            }
        }
    }
    renderVersionLink(version, item) {
        const { organization } = this.props;
        const { project } = item;
        return version ? (<versionHoverCard_1.default organization={organization} projectSlug={project.slug} releaseVersion={version}>
        <version_1.default version={version} projectId={project.id}/>
      </versionHoverCard_1.default>) : null;
    }
    render() {
        var _a;
        const { className, item } = this.props;
        const avatar = (<avatar_1.default type={!item.user ? 'system' : 'user'} user={(_a = item.user) !== null && _a !== void 0 ? _a : undefined} size={36}/>);
        const author = {
            name: item.user ? item.user.name : 'Sentry',
            avatar,
        };
        const hasBubble = ['note', 'create_issue'].includes(item.type);
        const bubbleProps = Object.assign(Object.assign({}, (item.type === 'note'
            ? { dangerouslySetInnerHTML: { __html: (0, marked_1.default)(item.data.text) } }
            : {})), (item.type === 'create_issue'
            ? {
                children: (<externalLink_1.default href={item.data.location}>{item.data.title}</externalLink_1.default>),
            }
            : {}));
        return (<div className={className}>
        {author.avatar}
        <div>
          {this.formatProjectActivity(<span>
              <ActivityAuthor>{author.name}</ActivityAuthor>
            </span>, item)}
          {hasBubble && (<Bubble ref={this.activityBubbleRef} clipped={this.state.clipped} {...bubbleProps}/>)}
          <Meta>
            <Project>{item.project.slug}</Project>
            <StyledTimeSince date={item.dateCreated}/>
          </Meta>
        </div>
      </div>);
    }
}
ActivityItem.defaultProps = defaultProps;
exports.default = (0, styled_1.default)(ActivityItem) `
  display: grid;
  grid-gap: ${(0, space_1.default)(1)};
  grid-template-columns: max-content auto;
  position: relative;
  margin: 0;
  padding: ${(0, space_1.default)(1)};
  border-bottom: 1px solid ${p => p.theme.innerBorder};
  line-height: 1.4;
  font-size: ${p => p.theme.fontSizeMedium};
`;
const ActivityAuthor = (0, styled_1.default)('span') `
  font-weight: 600;
`;
const Meta = (0, styled_1.default)('div') `
  color: ${p => p.theme.textColor};
  font-size: ${p => p.theme.fontSizeRelativeSmall};
`;
const Project = (0, styled_1.default)('span') `
  font-weight: bold;
`;
const Bubble = (0, styled_1.default)('div') `
  background: ${p => p.theme.backgroundSecondary};
  margin: ${(0, space_1.default)(0.5)} 0;
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};
  border: 1px solid ${p => p.theme.border};
  border-radius: 3px;
  box-shadow: 0 1px 1px rgba(0, 0, 0, 0.04);
  position: relative;
  overflow: hidden;

  a {
    max-width: 100%;
    overflow-x: hidden;
    text-overflow: ellipsis;
  }

  p {
    &:last-child {
      margin-bottom: 0;
    }
  }

  ${p => p.clipped &&
    `
    max-height: 68px;

    &:after {
      position: absolute;
      content: '';
      display: block;
      bottom: 0;
      right: 0;
      left: 0;
      height: 36px;
      background-image: linear-gradient(180deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 1));
      border-bottom: 6px solid #fff;
      border-radius: 0 0 3px 3px;
      pointer-events: none;
    }
  `}
`;
const StyledTimeSince = (0, styled_1.default)(timeSince_1.default) `
  color: ${p => p.theme.gray300};
  padding-left: ${(0, space_1.default)(1)};
`;
//# sourceMappingURL=activityFeedItem.jsx.map