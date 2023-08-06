Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const guideAnchor_1 = (0, tslib_1.__importDefault)(require("app/components/assistant/guideAnchor"));
const eventAnnotation_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventAnnotation"));
const inboxReason_1 = (0, tslib_1.__importDefault)(require("app/components/group/inboxBadges/inboxReason"));
const shortId_1 = (0, tslib_1.__importDefault)(require("app/components/group/inboxBadges/shortId"));
const timesTag_1 = (0, tslib_1.__importDefault)(require("app/components/group/inboxBadges/timesTag"));
const unhandledTag_1 = (0, tslib_1.__importDefault)(require("app/components/group/inboxBadges/unhandledTag"));
const projectBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge/projectBadge"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
function EventOrGroupExtraDetails({ data, showAssignee, params, hasGuideAnchor, showInboxTime, }) {
    const { id, lastSeen, firstSeen, subscriptionDetails, numComments, logger, assignedTo, annotations, shortId, project, lifetime, isUnhandled, inbox, } = data;
    const issuesPath = `/organizations/${params.orgId}/issues/`;
    const inboxReason = inbox && (<inboxReason_1.default inbox={inbox} showDateAdded={showInboxTime}/>);
    return (<GroupExtra>
      {inbox && (<guideAnchor_1.default target="inbox_guide_reason" disabled={!hasGuideAnchor}>
          {inboxReason}
        </guideAnchor_1.default>)}
      {shortId && (<shortId_1.default shortId={shortId} avatar={project && (<ShadowlessProjectBadge project={project} avatarSize={12} hideName/>)}/>)}
      {isUnhandled && <unhandledTag_1.default />}
      {!lifetime && !firstSeen && !lastSeen ? (<placeholder_1.default height="14px" width="100px"/>) : (<timesTag_1.default lastSeen={(lifetime === null || lifetime === void 0 ? void 0 : lifetime.lastSeen) || lastSeen} firstSeen={(lifetime === null || lifetime === void 0 ? void 0 : lifetime.firstSeen) || firstSeen}/>)}
      {/* Always display comment count on inbox */}
      {numComments > 0 && (<CommentsLink to={`${issuesPath}${id}/activity/`} className="comments">
          <icons_1.IconChat size="xs" color={(subscriptionDetails === null || subscriptionDetails === void 0 ? void 0 : subscriptionDetails.reason) === 'mentioned' ? 'green300' : undefined}/>
          <span>{numComments}</span>
        </CommentsLink>)}
      {logger && (<LoggerAnnotation>
          <link_1.default to={{
                pathname: issuesPath,
                query: {
                    query: `logger:${logger}`,
                },
            }}>
            {logger}
          </link_1.default>
        </LoggerAnnotation>)}
      {annotations === null || annotations === void 0 ? void 0 : annotations.map((annotation, key) => (<AnnotationNoMargin dangerouslySetInnerHTML={{
                __html: annotation,
            }} key={key}/>))}

      {showAssignee && assignedTo && (<div>{(0, locale_1.tct)('Assigned to [name]', { name: assignedTo.name })}</div>)}
    </GroupExtra>);
}
const GroupExtra = (0, styled_1.default)('div') `
  display: inline-grid;
  grid-auto-flow: column dense;
  grid-gap: ${(0, space_1.default)(1.5)};
  justify-content: start;
  align-items: center;
  color: ${p => p.theme.textColor};
  font-size: ${p => p.theme.fontSizeSmall};
  position: relative;
  min-width: 500px;
  white-space: nowrap;

  a {
    color: inherit;
  }
`;
const ShadowlessProjectBadge = (0, styled_1.default)(projectBadge_1.default) `
  * > img {
    box-shadow: none;
  }
`;
const CommentsLink = (0, styled_1.default)(link_1.default) `
  display: inline-grid;
  grid-gap: ${(0, space_1.default)(0.5)};
  align-items: center;
  grid-auto-flow: column;
  color: ${p => p.theme.textColor};
`;
const AnnotationNoMargin = (0, styled_1.default)(eventAnnotation_1.default) `
  margin-left: 0;
  padding-left: 0;
  border-left: none;
  & > a {
    color: ${p => p.theme.textColor};
  }
`;
const LoggerAnnotation = (0, styled_1.default)(AnnotationNoMargin) `
  color: ${p => p.theme.textColor};
`;
exports.default = (0, react_router_1.withRouter)(EventOrGroupExtraDetails);
//# sourceMappingURL=eventOrGroupExtraDetails.jsx.map