Object.defineProperty(exports, "__esModule", { value: true });
exports.DEFAULT_STREAM_GROUP_STATS_PERIOD = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const classnames_1 = (0, tslib_1.__importDefault)(require("classnames"));
const assigneeSelector_1 = (0, tslib_1.__importDefault)(require("app/components/assigneeSelector"));
const guideAnchor_1 = (0, tslib_1.__importDefault)(require("app/components/assistant/guideAnchor"));
const count_1 = (0, tslib_1.__importDefault)(require("app/components/count"));
const dropdownMenu_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownMenu"));
const eventOrGroupExtraDetails_1 = (0, tslib_1.__importDefault)(require("app/components/eventOrGroupExtraDetails"));
const eventOrGroupHeader_1 = (0, tslib_1.__importDefault)(require("app/components/eventOrGroupHeader"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const menuItem_1 = (0, tslib_1.__importDefault)(require("app/components/menuItem"));
const utils_1 = require("app/components/organizations/timeRangeSelector/utils");
const panels_1 = require("app/components/panels");
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const progressBar_1 = (0, tslib_1.__importDefault)(require("app/components/progressBar"));
const groupChart_1 = (0, tslib_1.__importDefault)(require("app/components/stream/groupChart"));
const groupCheckBox_1 = (0, tslib_1.__importDefault)(require("app/components/stream/groupCheckBox"));
const timeSince_1 = (0, tslib_1.__importDefault)(require("app/components/timeSince"));
const constants_1 = require("app/constants");
const locale_1 = require("app/locale");
const groupStore_1 = (0, tslib_1.__importDefault)(require("app/stores/groupStore"));
const selectedGroupStore_1 = (0, tslib_1.__importDefault)(require("app/stores/selectedGroupStore"));
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_2 = require("app/utils");
const analytics_1 = require("app/utils/analytics");
const callIfFunction_1 = require("app/utils/callIfFunction");
const eventView_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/eventView"));
const formatters_1 = require("app/utils/formatters");
const stream_1 = require("app/utils/stream");
const withGlobalSelection_1 = (0, tslib_1.__importDefault)(require("app/utils/withGlobalSelection"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const utils_3 = require("app/views/issueList/utils");
const DiscoveryExclusionFields = [
    'query',
    'status',
    'bookmarked_by',
    'assigned',
    'assigned_to',
    'unassigned',
    'subscribed_by',
    'active_at',
    'first_release',
    'first_seen',
    'is',
    '__text',
];
exports.DEFAULT_STREAM_GROUP_STATS_PERIOD = '24h';
const DEFAULT_DISPLAY = utils_3.IssueDisplayOptions.EVENTS;
const defaultProps = {
    statsPeriod: exports.DEFAULT_STREAM_GROUP_STATS_PERIOD,
    canSelect: true,
    withChart: true,
    useFilteredStats: false,
    useTintRow: true,
    display: DEFAULT_DISPLAY,
    narrowGroups: false,
};
class StreamGroup extends React.Component {
    constructor() {
        super(...arguments);
        this.state = this.getInitialState();
        this.listener = groupStore_1.default.listen(itemIds => this.onGroupChange(itemIds), undefined);
        this.trackClick = () => {
            const { query, organization } = this.props;
            const { data } = this.state;
            if (query === utils_3.Query.FOR_REVIEW) {
                (0, analytics_1.trackAnalyticsEvent)({
                    eventKey: 'inbox_tab.issue_clicked',
                    eventName: 'Clicked Issue from Inbox Tab',
                    organization_id: organization.id,
                    group_id: data.id,
                });
            }
            if (query !== undefined) {
                (0, analytics_1.trackAnalyticsEvent)(Object.assign({ eventKey: 'issues_stream.issue_clicked', eventName: 'Clicked Issue from Issues Stream' }, this.sharedAnalytics()));
            }
        };
        this.trackAssign = (type, _assignee, suggestedAssignee) => {
            const { query } = this.props;
            if (query !== undefined) {
                (0, analytics_1.trackAnalyticsEvent)(Object.assign(Object.assign({ eventKey: 'issues_stream.issue_assigned', eventName: 'Assigned Issue from Issues Stream' }, this.sharedAnalytics()), { did_assign_suggestion: !!suggestedAssignee, assigned_suggestion_reason: suggestedAssignee === null || suggestedAssignee === void 0 ? void 0 : suggestedAssignee.suggestedReason, assigned_type: type }));
            }
        };
        this.toggleSelect = (evt) => {
            var _a, _b, _c;
            const targetElement = evt.target;
            if (((_a = targetElement === null || targetElement === void 0 ? void 0 : targetElement.tagName) === null || _a === void 0 ? void 0 : _a.toLowerCase()) === 'a') {
                return;
            }
            if (((_b = targetElement === null || targetElement === void 0 ? void 0 : targetElement.tagName) === null || _b === void 0 ? void 0 : _b.toLowerCase()) === 'input') {
                return;
            }
            let e = targetElement;
            while (e.parentElement) {
                if (((_c = e === null || e === void 0 ? void 0 : e.tagName) === null || _c === void 0 ? void 0 : _c.toLowerCase()) === 'a') {
                    return;
                }
                e = e.parentElement;
            }
            selectedGroupStore_1.default.toggleSelect(this.state.data.id);
        };
    }
    getInitialState() {
        const { id, useFilteredStats } = this.props;
        const data = groupStore_1.default.get(id);
        return {
            data: Object.assign(Object.assign({}, data), { filtered: useFilteredStats ? data.filtered : null }),
            reviewed: false,
            actionTaken: false,
        };
    }
    componentWillReceiveProps(nextProps) {
        if (nextProps.id !== this.props.id ||
            nextProps.useFilteredStats !== this.props.useFilteredStats) {
            const data = groupStore_1.default.get(this.props.id);
            this.setState({
                data: Object.assign(Object.assign({}, data), { filtered: nextProps.useFilteredStats ? data.filtered : null }),
            });
        }
    }
    shouldComponentUpdate(nextProps, nextState) {
        if (nextProps.statsPeriod !== this.props.statsPeriod) {
            return true;
        }
        if (!(0, utils_2.valueIsEqual)(this.state.data, nextState.data)) {
            return true;
        }
        return false;
    }
    componentWillUnmount() {
        (0, callIfFunction_1.callIfFunction)(this.listener);
    }
    onGroupChange(itemIds) {
        const { id, query } = this.props;
        if (!itemIds.has(id)) {
            return;
        }
        const actionTaken = this.state.data.status !== 'unresolved';
        const data = groupStore_1.default.get(id);
        this.setState(state => {
            var _a;
            // When searching is:for_review and the inbox reason is removed
            const reviewed = state.reviewed ||
                ((0, utils_3.isForReviewQuery)(query) &&
                    ((_a = state.data.inbox) === null || _a === void 0 ? void 0 : _a.reason) !== undefined &&
                    data.inbox === false);
            return { data, reviewed, actionTaken };
        });
    }
    /** Shared between two events */
    sharedAnalytics() {
        var _a;
        const { query, organization } = this.props;
        const { data } = this.state;
        const tab = (_a = (0, utils_3.getTabs)(organization).find(([tabQuery]) => tabQuery === query)) === null || _a === void 0 ? void 0 : _a[1];
        const owners = (data === null || data === void 0 ? void 0 : data.owners) || [];
        return {
            organization_id: organization.id,
            group_id: data.id,
            tab: (tab === null || tab === void 0 ? void 0 : tab.analyticsName) || 'other',
            was_shown_suggestion: owners.length > 0,
        };
    }
    getDiscoverUrl(isFiltered) {
        const { organization, query, selection, customStatsPeriod } = this.props;
        const { data } = this.state;
        // when there is no discover feature open events page
        const hasDiscoverQuery = organization.features.includes('discover-basic');
        const queryTerms = [];
        if (isFiltered && typeof query === 'string') {
            const queryObj = (0, stream_1.queryToObj)(query);
            for (const queryTag in queryObj)
                if (!DiscoveryExclusionFields.includes(queryTag)) {
                    const queryVal = queryObj[queryTag].includes(' ')
                        ? `"${queryObj[queryTag]}"`
                        : queryObj[queryTag];
                    queryTerms.push(`${queryTag}:${queryVal}`);
                }
            if (queryObj.__text) {
                queryTerms.push(queryObj.__text);
            }
        }
        const commonQuery = { projects: [Number(data.project.id)] };
        const searchQuery = (queryTerms.length ? ' ' : '') + queryTerms.join(' ');
        if (hasDiscoverQuery) {
            const { period, start, end } = customStatsPeriod !== null && customStatsPeriod !== void 0 ? customStatsPeriod : (selection.datetime || {});
            const discoverQuery = Object.assign(Object.assign({}, commonQuery), { id: undefined, name: data.title || data.type, fields: ['title', 'release', 'environment', 'user', 'timestamp'], orderby: '-timestamp', query: `issue.id:${data.id}${searchQuery}`, version: 2 });
            if (!!start && !!end) {
                discoverQuery.start = String(start);
                discoverQuery.end = String(end);
            }
            else {
                discoverQuery.range = period || constants_1.DEFAULT_STATS_PERIOD;
            }
            const discoverView = eventView_1.default.fromSavedQuery(discoverQuery);
            return discoverView.getResultsViewUrlTarget(organization.slug);
        }
        return {
            pathname: `/organizations/${organization.slug}/issues/${data.id}/events/`,
            query: Object.assign(Object.assign({}, commonQuery), { query: searchQuery }),
        };
    }
    renderReprocessingColumns() {
        const { data } = this.state;
        const { statusDetails, count } = data;
        const { info, pendingEvents } = statusDetails;
        if (!info) {
            return null;
        }
        const { totalEvents, dateCreated } = info;
        const remainingEventsToReprocess = totalEvents - pendingEvents;
        const remainingEventsToReprocessPercent = (0, utils_2.percent)(remainingEventsToReprocess, totalEvents);
        return (<React.Fragment>
        <StartedColumn>
          <timeSince_1.default date={dateCreated}/>
        </StartedColumn>
        <EventsReprocessedColumn>
          {!(0, utils_2.defined)(count) ? (<placeholder_1.default height="17px"/>) : (<React.Fragment>
              <count_1.default value={remainingEventsToReprocess}/>
              {'/'}
              <count_1.default value={totalEvents}/>
            </React.Fragment>)}
        </EventsReprocessedColumn>
        <ProgressColumn>
          <progressBar_1.default value={remainingEventsToReprocessPercent}/>
        </ProgressColumn>
      </React.Fragment>);
    }
    render() {
        var _a, _b;
        const { data, reviewed, actionTaken } = this.state;
        const { index, query, hasGuideAnchor, canSelect, memberList, withChart, statsPeriod, selection, organization, displayReprocessingLayout, showInboxTime, useFilteredStats, useTintRow, customStatsPeriod, display, queryFilterDescription, narrowGroups, } = this.props;
        const { period, start, end } = selection.datetime || {};
        const summary = (_a = customStatsPeriod === null || customStatsPeriod === void 0 ? void 0 : customStatsPeriod.label.toLowerCase()) !== null && _a !== void 0 ? _a : (!!start && !!end
            ? 'time range'
            : (0, utils_1.getRelativeSummary)(period || constants_1.DEFAULT_STATS_PERIOD).toLowerCase());
        // Use data.filtered to decide on which value to use
        // In case of the query has filters but we avoid showing both sets of filtered/unfiltered stats
        // we use useFilteredStats param passed to Group for deciding
        const primaryCount = data.filtered ? data.filtered.count : data.count;
        const secondaryCount = data.filtered ? data.count : undefined;
        const primaryUserCount = data.filtered ? data.filtered.userCount : data.userCount;
        const secondaryUserCount = data.filtered ? data.userCount : undefined;
        const showSecondaryPoints = Boolean(withChart && data && data.filtered && statsPeriod && useFilteredStats);
        const showSessions = display === utils_3.IssueDisplayOptions.SESSIONS;
        // calculate a percentage count based on session data if the user has selected sessions display
        const primaryPercent = showSessions &&
            data.sessionCount &&
            (0, formatters_1.formatPercentage)(Number(primaryCount) / Number(data.sessionCount));
        const secondaryPercent = showSessions &&
            data.sessionCount &&
            secondaryCount &&
            (0, formatters_1.formatPercentage)(Number(secondaryCount) / Number(data.sessionCount));
        return (<Wrapper data-test-id="group" onClick={displayReprocessingLayout ? undefined : this.toggleSelect} reviewed={reviewed} unresolved={data.status === 'unresolved'} actionTaken={actionTaken} useTintRow={useTintRow !== null && useTintRow !== void 0 ? useTintRow : true}>
        {canSelect && (<GroupCheckBoxWrapper>
            <groupCheckBox_1.default id={data.id} disabled={!!displayReprocessingLayout}/>
          </GroupCheckBoxWrapper>)}
        <GroupSummary canSelect={!!canSelect}>
          <eventOrGroupHeader_1.default index={index} organization={organization} includeLink data={data} query={query} size="normal" onClick={this.trackClick}/>
          <eventOrGroupExtraDetails_1.default hasGuideAnchor={hasGuideAnchor} data={data} showInboxTime={showInboxTime}/>
        </GroupSummary>
        {hasGuideAnchor && <guideAnchor_1.default target="issue_stream"/>}
        {withChart && !displayReprocessingLayout && (<ChartWrapper className={`hidden-xs hidden-sm ${narrowGroups ? 'hidden-md' : ''}`}>
            {!((_b = data.filtered) === null || _b === void 0 ? void 0 : _b.stats) && !data.stats ? (<placeholder_1.default height="24px"/>) : (<groupChart_1.default statsPeriod={statsPeriod} data={data} showSecondaryPoints={showSecondaryPoints}/>)}
          </ChartWrapper>)}
        {displayReprocessingLayout ? (this.renderReprocessingColumns()) : (<React.Fragment>
            <EventUserWrapper>
              {!(0, utils_2.defined)(primaryCount) ? (<placeholder_1.default height="18px"/>) : (<dropdownMenu_1.default isNestedDropdown>
                  {({ isOpen, getRootProps, getActorProps, getMenuProps }) => {
                        const topLevelCx = (0, classnames_1.default)('dropdown', {
                            'anchor-middle': true,
                            open: isOpen,
                        });
                        return (<guideAnchor_1.default target="dynamic_counts" disabled={!hasGuideAnchor}>
                        <span {...getRootProps({
                            className: topLevelCx,
                        })}>
                          <span {...getActorProps({})}>
                            <div className="dropdown-actor-title">
                              {primaryPercent ? (<PrimaryPercent>{primaryPercent}</PrimaryPercent>) : (<PrimaryCount value={primaryCount}/>)}
                              {secondaryCount !== undefined &&
                                useFilteredStats &&
                                (secondaryPercent ? (<SecondaryPercent>{secondaryPercent}</SecondaryPercent>) : (<SecondaryCount value={secondaryCount}/>))}
                            </div>
                          </span>
                          {useFilteredStats && (<StyledDropdownList {...getMenuProps({ className: 'dropdown-menu inverted' })}>
                              {data.filtered && (<React.Fragment>
                                  <StyledMenuItem to={this.getDiscoverUrl(true)}>
                                    <MenuItemText>
                                      {queryFilterDescription !== null && queryFilterDescription !== void 0 ? queryFilterDescription : (0, locale_1.t)('Matching search filters')}
                                    </MenuItemText>
                                    {primaryPercent ? (<MenuItemPercent>{primaryPercent}</MenuItemPercent>) : (<MenuItemCount value={data.filtered.count}/>)}
                                  </StyledMenuItem>
                                  <menuItem_1.default divider/>
                                </React.Fragment>)}

                              <StyledMenuItem to={this.getDiscoverUrl()}>
                                <MenuItemText>{(0, locale_1.t)(`Total in ${summary}`)}</MenuItemText>
                                {secondaryPercent ? (<MenuItemPercent>{secondaryPercent}</MenuItemPercent>) : (<MenuItemCount value={secondaryPercent || data.count}/>)}
                              </StyledMenuItem>

                              {data.lifetime && (<React.Fragment>
                                  <menuItem_1.default divider/>
                                  <StyledMenuItem>
                                    <MenuItemText>{(0, locale_1.t)('Since issue began')}</MenuItemText>
                                    <MenuItemCount value={data.lifetime.count}/>
                                  </StyledMenuItem>
                                </React.Fragment>)}
                            </StyledDropdownList>)}
                        </span>
                      </guideAnchor_1.default>);
                    }}
                </dropdownMenu_1.default>)}
            </EventUserWrapper>
            <EventUserWrapper>
              {!(0, utils_2.defined)(primaryUserCount) ? (<placeholder_1.default height="18px"/>) : (<dropdownMenu_1.default isNestedDropdown>
                  {({ isOpen, getRootProps, getActorProps, getMenuProps }) => {
                        const topLevelCx = (0, classnames_1.default)('dropdown', {
                            'anchor-middle': true,
                            open: isOpen,
                        });
                        return (<span {...getRootProps({
                            className: topLevelCx,
                        })}>
                        <span {...getActorProps({})}>
                          <div className="dropdown-actor-title">
                            <PrimaryCount value={primaryUserCount}/>
                            {secondaryUserCount !== undefined && useFilteredStats && (<SecondaryCount dark value={secondaryUserCount}/>)}
                          </div>
                        </span>
                        {useFilteredStats && (<StyledDropdownList {...getMenuProps({ className: 'dropdown-menu inverted' })}>
                            {data.filtered && (<React.Fragment>
                                <StyledMenuItem to={this.getDiscoverUrl(true)}>
                                  <MenuItemText>
                                    {queryFilterDescription !== null && queryFilterDescription !== void 0 ? queryFilterDescription : (0, locale_1.t)('Matching search filters')}
                                  </MenuItemText>
                                  <MenuItemCount value={data.filtered.userCount}/>
                                </StyledMenuItem>
                                <menuItem_1.default divider/>
                              </React.Fragment>)}

                            <StyledMenuItem to={this.getDiscoverUrl()}>
                              <MenuItemText>{(0, locale_1.t)(`Total in ${summary}`)}</MenuItemText>
                              <MenuItemCount value={data.userCount}/>
                            </StyledMenuItem>

                            {data.lifetime && (<React.Fragment>
                                <menuItem_1.default divider/>
                                <StyledMenuItem>
                                  <MenuItemText>{(0, locale_1.t)('Since issue began')}</MenuItemText>
                                  <MenuItemCount value={data.lifetime.userCount}/>
                                </StyledMenuItem>
                              </React.Fragment>)}
                          </StyledDropdownList>)}
                      </span>);
                    }}
                </dropdownMenu_1.default>)}
            </EventUserWrapper>
            <AssigneeWrapper className="hidden-xs hidden-sm">
              <assigneeSelector_1.default id={data.id} memberList={memberList} onAssign={this.trackAssign}/>
            </AssigneeWrapper>
          </React.Fragment>)}
      </Wrapper>);
    }
}
StreamGroup.defaultProps = defaultProps;
exports.default = (0, withGlobalSelection_1.default)((0, withOrganization_1.default)(StreamGroup));
// Position for wrapper is relative for overlay actions
const Wrapper = (0, styled_1.default)(panels_1.PanelItem) `
  position: relative;
  padding: ${(0, space_1.default)(1.5)} 0;
  line-height: 1.1;

  ${p => p.useTintRow &&
    (p.reviewed || !p.unresolved) &&
    !p.actionTaken &&
    (0, react_1.css) `
      animation: tintRow 0.2s linear forwards;
      position: relative;

      /*
       * A mask that fills the entire row and makes the text opaque. Doing this because
       * opacity adds a stacking context in CSS so we need to apply it to another element.
       */
      &:after {
        content: '';
        pointer-events: none;
        position: absolute;
        left: 0;
        right: 0;
        top: 0;
        bottom: 0;
        width: 100%;
        height: 100%;
        background-color: ${p.theme.bodyBackground};
        opacity: 0.4;
        z-index: 1;
      }

      @keyframes tintRow {
        0% {
          background-color: ${p.theme.bodyBackground};
        }
        100% {
          background-color: ${p.theme.backgroundSecondary};
        }
      }
    `};
`;
const GroupSummary = (0, styled_1.default)('div') `
  overflow: hidden;
  margin-left: ${p => (0, space_1.default)(p.canSelect ? 1 : 2)};
  margin-right: ${(0, space_1.default)(1)};
  flex: 1;
  width: 66.66%;

  @media (min-width: ${p => p.theme.breakpoints[1]}) {
    width: 50%;
  }
`;
const GroupCheckBoxWrapper = (0, styled_1.default)('div') `
  margin-left: ${(0, space_1.default)(2)};
  align-self: flex-start;

  & input[type='checkbox'] {
    margin: 0;
    display: block;
  }
`;
const primaryStatStyle = (theme) => (0, react_1.css) `
  font-size: ${theme.fontSizeLarge};
  font-variant-numeric: tabular-nums;
`;
const PrimaryCount = (0, styled_1.default)(count_1.default) `
  ${p => primaryStatStyle(p.theme)};
`;
const PrimaryPercent = (0, styled_1.default)('div') `
  ${p => primaryStatStyle(p.theme)};
`;
const secondaryStatStyle = (theme) => (0, react_1.css) `
  font-size: ${theme.fontSizeLarge};
  font-variant-numeric: tabular-nums;

  :before {
    content: '/';
    padding-left: ${(0, space_1.default)(0.25)};
    padding-right: 2px;
    color: ${theme.gray300};
  }
`;
const SecondaryCount = (0, styled_1.default)((_a) => {
    var { value } = _a, p = (0, tslib_1.__rest)(_a, ["value"]);
    return <count_1.default {...p} value={value}/>;
}) `
  ${p => secondaryStatStyle(p.theme)}
`;
const SecondaryPercent = (0, styled_1.default)('div') `
  ${p => secondaryStatStyle(p.theme)}
`;
const StyledDropdownList = (0, styled_1.default)('ul') `
  z-index: ${p => p.theme.zIndex.hovercard};
`;
const StyledMenuItem = (0, styled_1.default)((_a) => {
    var { to, children } = _a, p = (0, tslib_1.__rest)(_a, ["to", "children"]);
    return (<menuItem_1.default noAnchor>
    {to ? (
        // @ts-expect-error allow target _blank for this link to open in new window
        <link_1.default to={to} target="_blank">
        <div {...p}>{children}</div>
      </link_1.default>) : (<div className="dropdown-toggle">
        <div {...p}>{children}</div>
      </div>)}
  </menuItem_1.default>);
}) `
  margin: 0;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
`;
const menuItemStatStyles = (0, react_1.css) `
  text-align: right;
  font-weight: bold;
  font-variant-numeric: tabular-nums;
  padding-left: ${(0, space_1.default)(1)};
`;
const MenuItemCount = (0, styled_1.default)((_a) => {
    var { value } = _a, p = (0, tslib_1.__rest)(_a, ["value"]);
    return (<div {...p}>
    <count_1.default value={value}/>
  </div>);
}) `
  ${menuItemStatStyles};
  color: ${p => p.theme.subText};
`;
const MenuItemPercent = (0, styled_1.default)('div') `
  ${menuItemStatStyles};
`;
const MenuItemText = (0, styled_1.default)('div') `
  white-space: nowrap;
  font-weight: normal;
  text-align: left;
  padding-right: ${(0, space_1.default)(1)};
  color: ${p => p.theme.textColor};
`;
const ChartWrapper = (0, styled_1.default)('div') `
  width: 160px;
  margin: 0 ${(0, space_1.default)(2)};
  align-self: center;
`;
const EventUserWrapper = (0, styled_1.default)('div') `
  display: flex;
  justify-content: flex-end;
  align-self: center;
  width: 60px;
  margin: 0 ${(0, space_1.default)(2)};

  @media (min-width: ${p => p.theme.breakpoints[3]}) {
    width: 80px;
  }
`;
const AssigneeWrapper = (0, styled_1.default)('div') `
  width: 80px;
  margin: 0 ${(0, space_1.default)(2)};
  align-self: center;
`;
// Reprocessing
const StartedColumn = (0, styled_1.default)('div') `
  align-self: center;
  margin: 0 ${(0, space_1.default)(2)};
  color: ${p => p.theme.gray500};
  ${overflowEllipsis_1.default};
  width: 85px;

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    display: block;
    width: 140px;
  }
`;
const EventsReprocessedColumn = (0, styled_1.default)('div') `
  align-self: center;
  margin: 0 ${(0, space_1.default)(2)};
  color: ${p => p.theme.gray500};
  ${overflowEllipsis_1.default};
  width: 75px;

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    width: 140px;
  }
`;
const ProgressColumn = (0, styled_1.default)('div') `
  margin: 0 ${(0, space_1.default)(2)};
  align-self: center;
  display: none;

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    display: block;
    width: 160px;
  }
`;
//# sourceMappingURL=group.jsx.map