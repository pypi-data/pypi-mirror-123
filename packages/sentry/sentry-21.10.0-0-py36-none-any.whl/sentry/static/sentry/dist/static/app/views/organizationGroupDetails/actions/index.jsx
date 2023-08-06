Object.defineProperty(exports, "__esModule", { value: true });
exports.Actions = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const group_1 = require("app/actionCreators/group");
const indicator_1 = require("app/actionCreators/indicator");
const modal_1 = require("app/actionCreators/modal");
const groupActions_1 = (0, tslib_1.__importDefault)(require("app/actions/groupActions"));
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/actions/button"));
const ignore_1 = (0, tslib_1.__importDefault)(require("app/components/actions/ignore"));
const resolve_1 = (0, tslib_1.__importDefault)(require("app/components/actions/resolve"));
const guideAnchor_1 = (0, tslib_1.__importDefault)(require("app/components/assistant/guideAnchor"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const iconRefresh_1 = require("app/icons/iconRefresh");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const trackAdvancedAnalyticsEvent_1 = (0, tslib_1.__importDefault)(require("app/utils/analytics/trackAdvancedAnalyticsEvent"));
const eventView_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/eventView"));
const displayReprocessEventAction_1 = require("app/utils/displayReprocessEventAction");
const guid_1 = require("app/utils/guid");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const reviewAction_1 = (0, tslib_1.__importDefault)(require("app/views/issueList/actions/reviewAction"));
const shareIssue_1 = (0, tslib_1.__importDefault)(require("app/views/organizationGroupDetails/actions/shareIssue"));
const deleteAction_1 = (0, tslib_1.__importDefault)(require("./deleteAction"));
const subscribeAction_1 = (0, tslib_1.__importDefault)(require("./subscribeAction"));
class Actions extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            shareBusy: false,
        };
        this.onDelete = () => {
            const { group, project, organization, api } = this.props;
            (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Delete event\u2026'));
            (0, group_1.bulkDelete)(api, {
                orgId: organization.slug,
                projectId: project.slug,
                itemIds: [group.id],
            }, {
                complete: () => {
                    (0, indicator_1.clearIndicators)();
                    react_router_1.browserHistory.push(`/${organization.slug}/${project.slug}/`);
                },
            });
        };
        this.onUpdate = (data) => {
            const { group, project, organization, api } = this.props;
            (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Saving changes\u2026'));
            (0, group_1.bulkUpdate)(api, {
                orgId: organization.slug,
                projectId: project.slug,
                itemIds: [group.id],
                data,
            }, {
                complete: indicator_1.clearIndicators,
            });
        };
        this.onReprocessEvent = () => {
            const { group, organization } = this.props;
            (0, modal_1.openReprocessEventModal)({ organization, groupId: group.id });
        };
        this.onToggleShare = () => {
            this.onShare(!this.props.group.isPublic);
        };
        this.onToggleBookmark = () => {
            this.onUpdate({ isBookmarked: !this.props.group.isBookmarked });
        };
        this.onToggleSubscribe = () => {
            this.onUpdate({ isSubscribed: !this.props.group.isSubscribed });
        };
        this.onDiscard = () => {
            const { group, project, organization, api } = this.props;
            const id = (0, guid_1.uniqueId)();
            (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Discarding event\u2026'));
            groupActions_1.default.discard(id, group.id);
            api.request(`/issues/${group.id}/`, {
                method: 'PUT',
                data: { discard: true },
                success: response => {
                    groupActions_1.default.discardSuccess(id, group.id, response);
                    react_router_1.browserHistory.push(`/${organization.slug}/${project.slug}/`);
                },
                error: error => {
                    groupActions_1.default.discardError(id, group.id, error);
                },
                complete: indicator_1.clearIndicators,
            });
        };
    }
    componentWillReceiveProps(nextProps) {
        if (this.state.shareBusy && nextProps.group.shareId !== this.props.group.shareId) {
            this.setState({ shareBusy: false });
        }
    }
    getShareUrl(shareId) {
        if (!shareId) {
            return '';
        }
        const path = `/share/issue/${shareId}/`;
        const { host, protocol } = window.location;
        return `${protocol}//${host}${path}`;
    }
    getDiscoverUrl() {
        const { group, project, organization } = this.props;
        const { title, id, type } = group;
        const discoverQuery = {
            id: undefined,
            name: title || type,
            fields: ['title', 'release', 'environment', 'user.display', 'timestamp'],
            orderby: '-timestamp',
            query: `issue.id:${id}`,
            projects: [Number(project.id)],
            version: 2,
            range: '90d',
        };
        const discoverView = eventView_1.default.fromSavedQuery(discoverQuery);
        return discoverView.getResultsViewUrlTarget(organization.slug);
    }
    onShare(shared) {
        const { group, project, organization, api } = this.props;
        this.setState({ shareBusy: true });
        // not sure why this is a bulkUpdate
        (0, group_1.bulkUpdate)(api, {
            orgId: organization.slug,
            projectId: project.slug,
            itemIds: [group.id],
            data: {
                isPublic: shared,
            },
        }, {
            error: () => {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Error sharing'));
            },
            complete: () => {
                // shareBusy marked false in componentWillReceiveProps to sync
                // busy state update with shareId update
            },
        });
    }
    handleClick(disabled, onClick) {
        return function (event) {
            if (disabled) {
                event.preventDefault();
                event.stopPropagation();
                return;
            }
            onClick(event);
        };
    }
    render() {
        var _a;
        const { group, project, organization, disabled, event } = this.props;
        const { status, isBookmarked } = group;
        const orgFeatures = new Set(organization.features);
        const bookmarkTitle = isBookmarked ? (0, locale_1.t)('Remove bookmark') : (0, locale_1.t)('Bookmark');
        const hasRelease = !!((_a = project.features) === null || _a === void 0 ? void 0 : _a.includes('releases'));
        const isResolved = status === 'resolved';
        const isIgnored = status === 'ignored';
        return (<Wrapper>
        <guideAnchor_1.default target="resolve" position="bottom" offset={(0, space_1.default)(3)}>
          <resolve_1.default disabled={disabled} disableDropdown={disabled} hasRelease={hasRelease} latestRelease={project.latestRelease} onUpdate={this.onUpdate} orgSlug={organization.slug} projectSlug={project.slug} isResolved={isResolved} isAutoResolved={group.status === 'resolved' ? group.statusDetails.autoResolved : undefined}/>
        </guideAnchor_1.default>
        <guideAnchor_1.default target="ignore_delete_discard" position="bottom" offset={(0, space_1.default)(3)}>
          <ignore_1.default isIgnored={isIgnored} onUpdate={this.onUpdate} disabled={disabled}/>
        </guideAnchor_1.default>
        <tooltip_1.default disabled={!!group.inbox || disabled} title={(0, locale_1.t)('Issue has been reviewed')}>
          <reviewAction_1.default onUpdate={this.onUpdate} disabled={!group.inbox || disabled}/>
        </tooltip_1.default>
        <deleteAction_1.default disabled={disabled} organization={organization} project={project} onDelete={this.onDelete} onDiscard={this.onDiscard}/>
        {orgFeatures.has('shared-issues') && (<shareIssue_1.default disabled={disabled} loading={this.state.shareBusy} isShared={group.isPublic} shareUrl={this.getShareUrl(group.shareId)} onToggle={this.onToggleShare} onReshare={() => this.onShare(true)}/>)}

        <feature_1.default hookName="feature-disabled:open-in-discover" features={['discover-basic']} organization={organization}>
          <button_1.default disabled={disabled} to={disabled ? '' : this.getDiscoverUrl()} onClick={() => {
                (0, trackAdvancedAnalyticsEvent_1.default)('growth.issue_open_in_discover_btn_clicked', {
                    organization,
                });
            }}>
            <guideAnchor_1.default target="open_in_discover">{(0, locale_1.t)('Open in Discover')}</guideAnchor_1.default>
          </button_1.default>
        </feature_1.default>

        <BookmarkButton disabled={disabled} isActive={group.isBookmarked} title={bookmarkTitle} label={bookmarkTitle} onClick={this.handleClick(disabled, this.onToggleBookmark)} icon={<icons_1.IconStar isSolid size="xs"/>}/>

        <subscribeAction_1.default disabled={disabled} group={group} onClick={this.handleClick(disabled, this.onToggleSubscribe)}/>

        {(0, displayReprocessEventAction_1.displayReprocessEventAction)(organization.features, event) && (<ReprocessAction disabled={disabled} icon={<iconRefresh_1.IconRefresh size="xs"/>} title={(0, locale_1.t)('Reprocess this issue')} label={(0, locale_1.t)('Reprocess this issue')} onClick={this.handleClick(disabled, this.onReprocessEvent)}/>)}
      </Wrapper>);
    }
}
exports.Actions = Actions;
const ReprocessAction = (0, styled_1.default)(button_1.default) ``;
const BookmarkButton = (0, styled_1.default)(button_1.default) `
  ${p => p.isActive &&
    `
   && {
 background: ${p.theme.yellow100};
 color: ${p.theme.yellow300};
 border-color: ${p.theme.yellow300};
 text-shadow: 0 1px 0 rgba(0, 0, 0, 0.15);
}
  `}
`;
const Wrapper = (0, styled_1.default)('div') `
  display: grid;
  justify-content: flex-start;
  align-items: center;
  grid-auto-flow: column;
  gap: ${(0, space_1.default)(0.5)};
  margin-top: ${(0, space_1.default)(2)};
  white-space: nowrap;
`;
exports.default = (0, withApi_1.default)((0, withOrganization_1.default)(Actions));
//# sourceMappingURL=index.jsx.map