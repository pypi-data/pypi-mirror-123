Object.defineProperty(exports, "__esModule", { value: true });
exports.CompactIssue = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const group_1 = require("app/actionCreators/group");
const indicator_1 = require("app/actionCreators/indicator");
const eventOrGroupTitle_1 = (0, tslib_1.__importDefault)(require("app/components/eventOrGroupTitle"));
const errorLevel_1 = (0, tslib_1.__importDefault)(require("app/components/events/errorLevel"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const panels_1 = require("app/components/panels");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const groupStore_1 = (0, tslib_1.__importDefault)(require("app/stores/groupStore"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const events_1 = require("app/utils/events");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
class CompactIssueHeader extends react_1.Component {
    render() {
        const { data, organization, projectId, eventId } = this.props;
        const basePath = `/organizations/${organization.slug}/issues/`;
        const issueLink = eventId
            ? `/organizations/${organization.slug}/projects/${projectId}/events/${eventId}/`
            : `${basePath}${data.id}/`;
        const commentColor = data.subscriptionDetails && data.subscriptionDetails.reason === 'mentioned'
            ? 'success'
            : 'textColor';
        return (<react_1.Fragment>
        <IssueHeaderMetaWrapper>
          <StyledErrorLevel size="12px" level={data.level} title={data.level}/>
          <h3 className="truncate">
            <IconLink to={issueLink || ''}>
              {data.status === 'ignored' && <icons_1.IconMute size="xs"/>}
              {data.isBookmarked && <icons_1.IconStar isSolid size="xs"/>}
              <eventOrGroupTitle_1.default data={data}/>
            </IconLink>
          </h3>
        </IssueHeaderMetaWrapper>
        <div className="event-extra">
          <span className="project-name">
            <strong>{data.project.slug}</strong>
          </span>
          {data.numComments !== 0 && (<span>
              <IconLink to={`${basePath}${data.id}/activity/`} className="comments">
                <icons_1.IconChat size="xs" color={commentColor}/>
                <span className="tag-count">{data.numComments}</span>
              </IconLink>
            </span>)}
          <span className="culprit">{(0, events_1.getMessage)(data)}</span>
        </div>
      </react_1.Fragment>);
    }
}
/**
 * Type assertion to disambiguate GroupTypes
 *
 * The GroupCollapseRelease type isn't compatible with BaseGroup
 */
function isGroup(maybe) {
    return maybe.status !== undefined;
}
class CompactIssue extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            issue: this.props.data || groupStore_1.default.get(this.props.id),
        };
        this.listener = groupStore_1.default.listen((itemIds) => this.onGroupChange(itemIds), undefined);
    }
    componentWillReceiveProps(nextProps) {
        if (nextProps.id !== this.props.id) {
            this.setState({
                issue: groupStore_1.default.get(this.props.id),
            });
        }
    }
    componentWillUnmount() {
        this.listener();
    }
    onGroupChange(itemIds) {
        if (!itemIds.has(this.props.id)) {
            return;
        }
        const id = this.props.id;
        const issue = groupStore_1.default.get(id);
        this.setState({
            issue,
        });
    }
    onUpdate(data) {
        const issue = this.state.issue;
        if (!issue) {
            return;
        }
        (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Saving changes\u2026'));
        (0, group_1.bulkUpdate)(this.props.api, {
            orgId: this.props.organization.slug,
            projectId: issue.project.slug,
            itemIds: [issue.id],
            data,
        }, {
            complete: () => {
                (0, indicator_1.clearIndicators)();
            },
        });
    }
    render() {
        const issue = this.state.issue;
        const { organization } = this.props;
        if (!isGroup(issue)) {
            return null;
        }
        let className = 'issue';
        if (issue.isBookmarked) {
            className += ' isBookmarked';
        }
        if (issue.hasSeen) {
            className += ' hasSeen';
        }
        if (issue.status === 'resolved') {
            className += ' isResolved';
        }
        if (issue.status === 'ignored') {
            className += ' isIgnored';
        }
        return (<IssueRow className={className}>
        <CompactIssueHeader data={issue} organization={organization} projectId={issue.project.slug} eventId={this.props.eventId}/>
        {this.props.children}
      </IssueRow>);
    }
}
exports.CompactIssue = CompactIssue;
exports.default = (0, withApi_1.default)((0, withOrganization_1.default)(CompactIssue));
const IssueHeaderMetaWrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
`;
const StyledErrorLevel = (0, styled_1.default)(errorLevel_1.default) `
  display: block;
  margin-right: ${(0, space_1.default)(1)};
`;
const IconLink = (0, styled_1.default)(link_1.default) `
  & > svg {
    margin-right: ${(0, space_1.default)(0.5)};
  }
`;
const IssueRow = (0, styled_1.default)(panels_1.PanelItem) `
  padding-top: ${(0, space_1.default)(1.5)};
  padding-bottom: ${(0, space_1.default)(0.75)};
  flex-direction: column;
`;
//# sourceMappingURL=compactIssue.jsx.map