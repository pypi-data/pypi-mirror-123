Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const commitLink_1 = (0, tslib_1.__importDefault)(require("app/components/commitLink"));
const duration_1 = (0, tslib_1.__importDefault)(require("app/components/duration"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const pullRequestLink_1 = (0, tslib_1.__importDefault)(require("app/components/pullRequestLink"));
const version_1 = (0, tslib_1.__importDefault)(require("app/components/version"));
const locale_1 = require("app/locale");
const memberListStore_1 = (0, tslib_1.__importDefault)(require("app/stores/memberListStore"));
const teamStore_1 = (0, tslib_1.__importDefault)(require("app/stores/teamStore"));
const types_1 = require("app/types");
function GroupActivityItem({ activity, orgSlug, projectId, author }) {
    const issuesLink = `/organizations/${orgSlug}/issues/`;
    function getIgnoredMessage(data) {
        if (data.ignoreDuration) {
            return (0, locale_1.tct)('[author] ignored this issue for [duration]', {
                author,
                duration: <duration_1.default seconds={data.ignoreDuration * 60}/>,
            });
        }
        if (data.ignoreCount && data.ignoreWindow) {
            return (0, locale_1.tct)('[author] ignored this issue until it happens [count] time(s) in [duration]', {
                author,
                count: data.ignoreCount,
                duration: <duration_1.default seconds={data.ignoreWindow * 60}/>,
            });
        }
        if (data.ignoreCount) {
            return (0, locale_1.tct)('[author] ignored this issue until it happens [count] time(s)', {
                author,
                count: data.ignoreCount,
            });
        }
        if (data.ignoreUserCount && data.ignoreUserWindow) {
            return (0, locale_1.tct)('[author] ignored this issue until it affects [count] user(s) in [duration]', {
                author,
                count: data.ignoreUserCount,
                duration: <duration_1.default seconds={data.ignoreUserWindow * 60}/>,
            });
        }
        if (data.ignoreUserCount) {
            return (0, locale_1.tct)('[author] ignored this issue until it affects [count] user(s)', {
                author,
                count: data.ignoreUserCount,
            });
        }
        return (0, locale_1.tct)('[author] ignored this issue', { author });
    }
    function getAssignedMessage(data) {
        let assignee = undefined;
        if (data.assigneeType === 'team') {
            const team = teamStore_1.default.getById(data.assignee);
            assignee = team ? team.slug : '<unknown-team>';
            return (0, locale_1.tct)('[author] assigned this issue to #[assignee]', {
                author,
                assignee,
            });
        }
        if (activity.user && activity.assignee === activity.user.id) {
            return (0, locale_1.tct)('[author] assigned this issue to themselves', { author });
        }
        assignee = memberListStore_1.default.getById(data.assignee);
        if (typeof assignee === 'object' && (assignee === null || assignee === void 0 ? void 0 : assignee.email)) {
            return (0, locale_1.tct)('[author] assigned this issue to [assignee]', {
                author,
                assignee: assignee.email,
            });
        }
        return (0, locale_1.tct)('[author] assigned this issue to an unknown user', { author });
    }
    function renderContent() {
        switch (activity.type) {
            case types_1.GroupActivityType.NOTE:
                return (0, locale_1.tct)('[author] left a comment', { author });
            case types_1.GroupActivityType.SET_RESOLVED:
                return (0, locale_1.tct)('[author] marked this issue as resolved', { author });
            case types_1.GroupActivityType.SET_RESOLVED_BY_AGE:
                return (0, locale_1.tct)('[author] marked this issue as resolved due to inactivity', {
                    author,
                });
            case types_1.GroupActivityType.SET_RESOLVED_IN_RELEASE:
                const { current_release_version, version } = activity.data;
                if (current_release_version) {
                    return (0, locale_1.tct)('[author] marked this issue as resolved in releases greater than [version]', {
                        author,
                        version: (<version_1.default version={current_release_version} projectId={projectId} tooltipRawVersion/>),
                    });
                }
                return version
                    ? (0, locale_1.tct)('[author] marked this issue as resolved in [version]', {
                        author,
                        version: (<version_1.default version={version} projectId={projectId} tooltipRawVersion/>),
                    })
                    : (0, locale_1.tct)('[author] marked this issue as resolved in the upcoming release', {
                        author,
                    });
            case types_1.GroupActivityType.SET_RESOLVED_IN_COMMIT:
                return (0, locale_1.tct)('[author] marked this issue as resolved in [version]', {
                    author,
                    version: (<commitLink_1.default inline commitId={activity.data.commit.id} repository={activity.data.commit.repository}/>),
                });
            case types_1.GroupActivityType.SET_RESOLVED_IN_PULL_REQUEST: {
                const { data } = activity;
                const { pullRequest } = data;
                return (0, locale_1.tct)('[author] marked this issue as resolved in [version]', {
                    author,
                    version: (<pullRequestLink_1.default inline pullRequest={pullRequest} repository={pullRequest.repository}/>),
                });
            }
            case types_1.GroupActivityType.SET_UNRESOLVED:
                return (0, locale_1.tct)('[author] marked this issue as unresolved', { author });
            case types_1.GroupActivityType.SET_IGNORED: {
                const { data } = activity;
                return getIgnoredMessage(data);
            }
            case types_1.GroupActivityType.SET_PUBLIC:
                return (0, locale_1.tct)('[author] made this issue public', { author });
            case types_1.GroupActivityType.SET_PRIVATE:
                return (0, locale_1.tct)('[author] made this issue private', { author });
            case types_1.GroupActivityType.SET_REGRESSION: {
                const { data } = activity;
                return data.version
                    ? (0, locale_1.tct)('[author] marked this issue as a regression in [version]', {
                        author,
                        version: (<version_1.default version={data.version} projectId={projectId} tooltipRawVersion/>),
                    })
                    : (0, locale_1.tct)('[author] marked this issue as a regression', { author });
            }
            case types_1.GroupActivityType.CREATE_ISSUE: {
                const { data } = activity;
                return (0, locale_1.tct)('[author] created an issue on [provider] titled [title]', {
                    author,
                    provider: data.provider,
                    title: <externalLink_1.default href={data.location}>{data.title}</externalLink_1.default>,
                });
            }
            case types_1.GroupActivityType.UNMERGE_SOURCE: {
                const { data } = activity;
                const { destination, fingerprints } = data;
                return (0, locale_1.tn)('%2$s migrated %1$s fingerprint to %3$s', '%2$s migrated %1$s fingerprints to %3$s', fingerprints.length, author, destination ? (<link_1.default to={`${issuesLink}${destination.id}`}>{destination.shortId}</link_1.default>) : ((0, locale_1.t)('a group')));
            }
            case types_1.GroupActivityType.UNMERGE_DESTINATION: {
                const { data } = activity;
                const { source, fingerprints } = data;
                return (0, locale_1.tn)('%2$s migrated %1$s fingerprint from %3$s', '%2$s migrated %1$s fingerprints from %3$s', fingerprints.length, author, source ? (<link_1.default to={`${issuesLink}${source.id}`}>{source.shortId}</link_1.default>) : ((0, locale_1.t)('a group')));
            }
            case types_1.GroupActivityType.FIRST_SEEN:
                return (0, locale_1.tct)('[author] first saw this issue', { author });
            case types_1.GroupActivityType.ASSIGNED: {
                const { data } = activity;
                return getAssignedMessage(data);
            }
            case types_1.GroupActivityType.UNASSIGNED:
                return (0, locale_1.tct)('[author] unassigned this issue', { author });
            case types_1.GroupActivityType.MERGE:
                return (0, locale_1.tn)('%2$s merged %1$s issue into this issue', '%2$s merged %1$s issues into this issue', activity.data.issues.length, author);
            case types_1.GroupActivityType.REPROCESS: {
                const { data } = activity;
                const { oldGroupId, eventCount } = data;
                return (0, locale_1.tct)('[author] reprocessed the events in this issue. [new-events]', {
                    author,
                    ['new-events']: (<link_1.default to={`/organizations/${orgSlug}/issues/?query=reprocessing.original_issue_id:${oldGroupId}`}>
              {(0, locale_1.tn)('See %s new event', 'See %s new events', eventCount)}
            </link_1.default>),
                });
            }
            case types_1.GroupActivityType.MARK_REVIEWED: {
                return (0, locale_1.tct)('[author] marked this issue as reviewed', {
                    author,
                });
            }
            default:
                return ''; // should never hit (?)
        }
    }
    return <React.Fragment>{renderContent()}</React.Fragment>;
}
exports.default = GroupActivityItem;
//# sourceMappingURL=groupActivityItem.jsx.map