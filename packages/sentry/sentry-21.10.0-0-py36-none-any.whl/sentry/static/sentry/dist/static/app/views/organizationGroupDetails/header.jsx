Object.defineProperty(exports, "__esModule", { value: true });
exports.GroupHeader = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const omit_1 = (0, tslib_1.__importDefault)(require("lodash/omit"));
const members_1 = require("app/actionCreators/members");
const assigneeSelector_1 = (0, tslib_1.__importDefault)(require("app/components/assigneeSelector"));
const guideAnchor_1 = (0, tslib_1.__importDefault)(require("app/components/assistant/guideAnchor"));
const badge_1 = (0, tslib_1.__importDefault)(require("app/components/badge"));
const count_1 = (0, tslib_1.__importDefault)(require("app/components/count"));
const eventOrGroupTitle_1 = (0, tslib_1.__importDefault)(require("app/components/eventOrGroupTitle"));
const errorLevel_1 = (0, tslib_1.__importDefault)(require("app/components/events/errorLevel"));
const eventAnnotation_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventAnnotation"));
const eventMessage_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventMessage"));
const inboxReason_1 = (0, tslib_1.__importDefault)(require("app/components/group/inboxBadges/inboxReason"));
const unhandledTag_1 = (0, tslib_1.__importDefault)(require("app/components/group/inboxBadges/unhandledTag"));
const projectBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge/projectBadge"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const listLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/listLink"));
const navTabs_1 = (0, tslib_1.__importDefault)(require("app/components/navTabs"));
const seenByList_1 = (0, tslib_1.__importDefault)(require("app/components/seenByList"));
const shortId_1 = (0, tslib_1.__importDefault)(require("app/components/shortId"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const events_1 = require("app/utils/events");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const actions_1 = (0, tslib_1.__importDefault)(require("./actions"));
const types_1 = require("./types");
const unhandledTag_2 = require("./unhandledTag");
const utils_1 = require("./utils");
class GroupHeader extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {};
    }
    componentDidMount() {
        const { group, api, organization } = this.props;
        const { project } = group;
        (0, members_1.fetchOrgMembers)(api, organization.slug, [project.id]).then(memberList => {
            const users = memberList.map(member => member.user);
            this.setState({ memberList: users });
        });
    }
    getDisabledTabs() {
        const { organization } = this.props;
        const hasReprocessingV2Feature = organization.features.includes('reprocessing-v2');
        if (!hasReprocessingV2Feature) {
            return [];
        }
        const { groupReprocessingStatus } = this.props;
        if (groupReprocessingStatus === utils_1.ReprocessingStatus.REPROCESSING) {
            return [
                types_1.Tab.ACTIVITY,
                types_1.Tab.USER_FEEDBACK,
                types_1.Tab.ATTACHMENTS,
                types_1.Tab.EVENTS,
                types_1.Tab.MERGED,
                types_1.Tab.GROUPING,
                types_1.Tab.SIMILAR_ISSUES,
                types_1.Tab.TAGS,
            ];
        }
        if (groupReprocessingStatus === utils_1.ReprocessingStatus.REPROCESSED_AND_HASNT_EVENT) {
            return [
                types_1.Tab.DETAILS,
                types_1.Tab.ATTACHMENTS,
                types_1.Tab.EVENTS,
                types_1.Tab.MERGED,
                types_1.Tab.GROUPING,
                types_1.Tab.SIMILAR_ISSUES,
                types_1.Tab.TAGS,
                types_1.Tab.USER_FEEDBACK,
            ];
        }
        return [];
    }
    render() {
        const { project, group, currentTab, baseUrl, event, organization, location } = this.props;
        const projectFeatures = new Set(project ? project.features : []);
        const organizationFeatures = new Set(organization ? organization.features : []);
        const userCount = group.userCount;
        const hasGroupingTreeUI = organizationFeatures.has('grouping-tree-ui');
        const hasSimilarView = projectFeatures.has('similarity-view');
        const hasEventAttachments = organizationFeatures.has('event-attachments');
        let className = 'group-detail';
        if (group.hasSeen) {
            className += ' hasSeen';
        }
        if (group.status === 'resolved') {
            className += ' isResolved';
        }
        const { memberList } = this.state;
        const orgId = organization.slug;
        const message = (0, events_1.getMessage)(group);
        const searchTermWithoutQuery = (0, omit_1.default)(location.query, 'query');
        const eventRouteToObject = {
            pathname: `${baseUrl}events/`,
            query: searchTermWithoutQuery,
        };
        const disabledTabs = this.getDisabledTabs();
        const disableActions = !!disabledTabs.length;
        return (<div className={className}>
        <div className="row">
          <div className="col-sm-7">
            <TitleWrapper>
              <h3>
                <eventOrGroupTitle_1.default hasGuideAnchor data={group}/>
              </h3>
              {group.inbox && (<InboxReasonWrapper>
                  <inboxReason_1.default inbox={group.inbox} fontSize="md"/>
                </InboxReasonWrapper>)}
            </TitleWrapper>
            <StyledTagAndMessageWrapper>
              {group.level && <errorLevel_1.default level={group.level} size="11px"/>}
              {group.isUnhandled && <unhandledTag_1.default />}
              <eventMessage_1.default message={message} annotations={<React.Fragment>
                    {group.logger && (<EventAnnotationWithSpace>
                        <link_1.default to={{
                        pathname: `/organizations/${orgId}/issues/`,
                        query: { query: 'logger:' + group.logger },
                    }}>
                          {group.logger}
                        </link_1.default>
                      </EventAnnotationWithSpace>)}
                    {group.annotations.map((annotation, i) => (<EventAnnotationWithSpace key={i} dangerouslySetInnerHTML={{ __html: annotation }}/>))}
                  </React.Fragment>}/>
            </StyledTagAndMessageWrapper>
          </div>

          <div className="col-sm-5 stats">
            <div className="flex flex-justify-right">
              {group.shortId && (<guideAnchor_1.default target="issue_number" position="bottom">
                  <div className="short-id-box count align-right">
                    <h6 className="nav-header">
                      <tooltip_1.default className="help-link" title={(0, locale_1.t)('This identifier is unique across your organization, and can be used to reference an issue in various places, like commit messages.')} position="bottom">
                        <externalLink_1.default href="https://docs.sentry.io/product/integrations/source-code-mgmt/github/#resolve-via-commit-or-pull-request">
                          {(0, locale_1.t)('Issue #')}
                        </externalLink_1.default>
                      </tooltip_1.default>
                    </h6>
                    <shortId_1.default shortId={group.shortId} avatar={<StyledProjectBadge project={project} avatarSize={20} hideName/>}/>
                  </div>
                </guideAnchor_1.default>)}
              <div className="count align-right m-l-1">
                <h6 className="nav-header">{(0, locale_1.t)('Events')}</h6>
                {disableActions ? (<count_1.default className="count" value={group.count}/>) : (<link_1.default to={eventRouteToObject}>
                    <count_1.default className="count" value={group.count}/>
                  </link_1.default>)}
              </div>
              <div className="count align-right m-l-1">
                <h6 className="nav-header">{(0, locale_1.t)('Users')}</h6>
                {userCount !== 0 ? (disableActions ? (<count_1.default className="count" value={userCount}/>) : (<link_1.default to={`${baseUrl}tags/user/${location.search}`}>
                      <count_1.default className="count" value={userCount}/>
                    </link_1.default>)) : (<span>0</span>)}
              </div>
              <div className="assigned-to m-l-1">
                <h6 className="nav-header">{(0, locale_1.t)('Assignee')}</h6>
                <assigneeSelector_1.default id={group.id} memberList={memberList} disabled={disableActions}/>
              </div>
            </div>
          </div>
        </div>
        <seenByList_1.default seenBy={group.seenBy} iconTooltip={(0, locale_1.t)('People who have viewed this issue')}/>
        <actions_1.default group={group} project={project} disabled={disableActions} event={event}/>
        <navTabs_1.default>
          <listLink_1.default to={`${baseUrl}${location.search}`} isActive={() => currentTab === types_1.Tab.DETAILS} disabled={disabledTabs.includes(types_1.Tab.DETAILS)}>
            {(0, locale_1.t)('Details')}
          </listLink_1.default>
          <StyledListLink to={`${baseUrl}activity/${location.search}`} isActive={() => currentTab === types_1.Tab.ACTIVITY} disabled={disabledTabs.includes(types_1.Tab.ACTIVITY)}>
            {(0, locale_1.t)('Activity')}
            <badge_1.default>
              {group.numComments}
              <icons_1.IconChat size="xs"/>
            </badge_1.default>
          </StyledListLink>
          <StyledListLink to={`${baseUrl}feedback/${location.search}`} isActive={() => currentTab === types_1.Tab.USER_FEEDBACK} disabled={disabledTabs.includes(types_1.Tab.USER_FEEDBACK)}>
            {(0, locale_1.t)('User Feedback')} <badge_1.default text={group.userReportCount}/>
          </StyledListLink>
          {hasEventAttachments && (<listLink_1.default to={`${baseUrl}attachments/${location.search}`} isActive={() => currentTab === types_1.Tab.ATTACHMENTS} disabled={disabledTabs.includes(types_1.Tab.ATTACHMENTS)}>
              {(0, locale_1.t)('Attachments')}
            </listLink_1.default>)}
          <listLink_1.default to={`${baseUrl}tags/${location.search}`} isActive={() => currentTab === types_1.Tab.TAGS} disabled={disabledTabs.includes(types_1.Tab.TAGS)}>
            {(0, locale_1.t)('Tags')}
          </listLink_1.default>
          <listLink_1.default to={eventRouteToObject} isActive={() => currentTab === types_1.Tab.EVENTS} disabled={disabledTabs.includes(types_1.Tab.EVENTS)}>
            {(0, locale_1.t)('Events')}
          </listLink_1.default>
          <listLink_1.default to={`${baseUrl}merged/${location.search}`} isActive={() => currentTab === types_1.Tab.MERGED} disabled={disabledTabs.includes(types_1.Tab.MERGED)}>
            {(0, locale_1.t)('Merged Issues')}
          </listLink_1.default>
          {hasGroupingTreeUI && (<listLink_1.default to={`${baseUrl}grouping/${location.search}`} isActive={() => currentTab === types_1.Tab.GROUPING} disabled={disabledTabs.includes(types_1.Tab.GROUPING)}>
              {(0, locale_1.t)('Grouping')}
            </listLink_1.default>)}
          {hasSimilarView && (<listLink_1.default to={`${baseUrl}similar/${location.search}`} isActive={() => currentTab === types_1.Tab.SIMILAR_ISSUES} disabled={disabledTabs.includes(types_1.Tab.SIMILAR_ISSUES)}>
              {(0, locale_1.t)('Similar Issues')}
            </listLink_1.default>)}
        </navTabs_1.default>
      </div>);
    }
}
exports.GroupHeader = GroupHeader;
exports.default = (0, withApi_1.default)((0, react_router_1.withRouter)((0, withOrganization_1.default)(GroupHeader)));
const TitleWrapper = (0, styled_1.default)('div') `
  display: flex;
  line-height: 24px;
`;
const InboxReasonWrapper = (0, styled_1.default)('div') `
  margin-left: ${(0, space_1.default)(1)};
`;
const StyledTagAndMessageWrapper = (0, styled_1.default)(unhandledTag_2.TagAndMessageWrapper) `
  display: grid;
  grid-auto-flow: column;
  gap: ${(0, space_1.default)(1)};
  justify-content: flex-start;
  line-height: 1.2;

  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    margin-bottom: ${(0, space_1.default)(2)};
  }
`;
const StyledListLink = (0, styled_1.default)(listLink_1.default) `
  svg {
    margin-left: ${(0, space_1.default)(0.5)};
    margin-bottom: ${(0, space_1.default)(0.25)};
    vertical-align: middle;
  }
`;
const StyledProjectBadge = (0, styled_1.default)(projectBadge_1.default) `
  flex-shrink: 0;
`;
const EventAnnotationWithSpace = (0, styled_1.default)(eventAnnotation_1.default) `
  margin-left: ${(0, space_1.default)(1)};
`;
//# sourceMappingURL=header.jsx.map