Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const react_2 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const capitalize_1 = (0, tslib_1.__importDefault)(require("lodash/capitalize"));
const errorBoundary_1 = (0, tslib_1.__importDefault)(require("app/components/errorBoundary"));
const eventOrGroupTitle_1 = (0, tslib_1.__importDefault)(require("app/components/eventOrGroupTitle"));
const globalSelectionLink_1 = (0, tslib_1.__importDefault)(require("app/components/globalSelectionLink"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const events_1 = require("app/utils/events");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const unhandledTag_1 = require("app/views/organizationGroupDetails/unhandledTag");
const eventTitleError_1 = (0, tslib_1.__importDefault)(require("./eventTitleError"));
/**
 * Displays an event or group/issue title (i.e. in Stream)
 */
function EventOrGroupHeader(_a) {
    var _b;
    var { data, index, organization, params, query, onClick, className, hideIcons, hideLevel, includeLink = true, size = 'normal', grouping = false } = _a, props = (0, tslib_1.__rest)(_a, ["data", "index", "organization", "params", "query", "onClick", "className", "hideIcons", "hideLevel", "includeLink", "size", "grouping"]);
    const hasGroupingTreeUI = !!((_b = organization.features) === null || _b === void 0 ? void 0 : _b.includes('grouping-tree-ui'));
    function getTitleChildren() {
        const { level, status, isBookmarked, hasSeen } = data;
        return (<react_1.Fragment>
        {!hideLevel && level && (<GroupLevel level={level}>
            <tooltip_1.default title={(0, locale_1.tct)('Error level: [level]', { level: (0, capitalize_1.default)(level) })}>
              <span />
            </tooltip_1.default>
          </GroupLevel>)}
        {!hideIcons && status === 'ignored' && (<IconWrapper>
            <icons_1.IconMute color="red300"/>
          </IconWrapper>)}
        {!hideIcons && isBookmarked && (<IconWrapper>
            <icons_1.IconStar isSolid color="yellow300"/>
          </IconWrapper>)}
        <errorBoundary_1.default customComponent={<eventTitleError_1.default />} mini>
          <StyledEventOrGroupTitle data={data} organization={organization} hasSeen={hasGroupingTreeUI && hasSeen === undefined ? true : hasSeen} withStackTracePreview hasGuideAnchor={index === 0} guideAnchorName="issue_stream_title" grouping={grouping}/>
        </errorBoundary_1.default>
      </react_1.Fragment>);
    }
    function getTitle() {
        const orgId = params === null || params === void 0 ? void 0 : params.orgId;
        const { id, status } = data;
        const { eventID, groupID } = data;
        const { location } = props;
        const commonEleProps = {
            'data-test-id': status === 'resolved' ? 'resolved-issue' : null,
            style: status === 'resolved' ? { textDecoration: 'line-through' } : undefined,
        };
        if (includeLink) {
            return (<globalSelectionLink_1.default {...commonEleProps} to={{
                    pathname: `/organizations/${orgId}/issues/${eventID ? groupID : id}/${eventID ? `events/${eventID}/` : ''}`,
                    query: Object.assign(Object.assign({ query }, (location.query.sort !== undefined ? { sort: location.query.sort } : {})), (location.query.project !== undefined ? {} : { _allp: 1 })),
                }} onClick={onClick}>
          {getTitleChildren()}
        </globalSelectionLink_1.default>);
        }
        return <span {...commonEleProps}>{getTitleChildren()}</span>;
    }
    const location = (0, events_1.getLocation)(data);
    const message = (0, events_1.getMessage)(data);
    return (<div className={className} data-test-id="event-issue-header">
      <Title size={size} hasGroupingTreeUI={hasGroupingTreeUI}>
        {getTitle()}
      </Title>
      {location && <Location size={size}>{location}</Location>}
      {message && (<StyledTagAndMessageWrapper size={size}>
          {message && <Message>{message}</Message>}
        </StyledTagAndMessageWrapper>)}
    </div>);
}
const truncateStyles = (0, react_2.css) `
  overflow: hidden;
  max-width: 100%;
  text-overflow: ellipsis;
  white-space: nowrap;
`;
const getMargin = ({ size }) => {
    if (size === 'small') {
        return 'margin: 0;';
    }
    return 'margin: 0 0 5px';
};
const Title = (0, styled_1.default)('div') `
  line-height: 1;
  ${getMargin};
  & em {
    font-size: ${p => p.theme.fontSizeMedium};
    font-style: normal;
    font-weight: 300;
    color: ${p => p.theme.subText};
  }
  ${p => !p.hasGroupingTreeUI
    ? (0, react_2.css) `
          ${truncateStyles}
        `
    : (0, react_2.css) `
          > a:first-child {
            display: flex;
          }
        `}
`;
const LocationWrapper = (0, styled_1.default)('div') `
  ${truncateStyles};
  ${getMargin};
  direction: rtl;
  text-align: left;
  font-size: ${p => p.theme.fontSizeMedium};
  color: ${p => p.theme.subText};
  span {
    direction: ltr;
  }
`;
function Location(props) {
    const { children } = props, rest = (0, tslib_1.__rest)(props, ["children"]);
    return (<LocationWrapper {...rest}>
      {(0, locale_1.tct)('in [location]', {
            location: <span>{children}</span>,
        })}
    </LocationWrapper>);
}
const StyledTagAndMessageWrapper = (0, styled_1.default)(unhandledTag_1.TagAndMessageWrapper) `
  ${getMargin};
`;
const Message = (0, styled_1.default)('div') `
  ${truncateStyles};
  font-size: ${p => p.theme.fontSizeMedium};
`;
const IconWrapper = (0, styled_1.default)('span') `
  position: relative;
  top: 2px;

  margin-right: 5px;
`;
const GroupLevel = (0, styled_1.default)('div') `
  position: absolute;
  left: -1px;
  width: 9px;
  height: 15px;
  border-radius: 0 3px 3px 0;

  background-color: ${p => { var _a; return (_a = p.theme.level[p.level]) !== null && _a !== void 0 ? _a : p.theme.level.default; }};

  & span {
    display: block;
    width: 9px;
    height: 15px;
  }
`;
exports.default = (0, react_router_1.withRouter)((0, withOrganization_1.default)(EventOrGroupHeader));
const StyledEventOrGroupTitle = (0, styled_1.default)(eventOrGroupTitle_1.default) `
  font-weight: ${p => (p.hasSeen ? 400 : 600)};
`;
//# sourceMappingURL=eventOrGroupHeader.jsx.map