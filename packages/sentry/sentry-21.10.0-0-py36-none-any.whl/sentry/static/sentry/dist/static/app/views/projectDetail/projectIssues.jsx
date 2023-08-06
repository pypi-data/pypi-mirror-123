Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const styles_1 = require("app/components/charts/styles");
const discoverButton_1 = (0, tslib_1.__importDefault)(require("app/components/discoverButton"));
const groupList_1 = (0, tslib_1.__importDefault)(require("app/components/issues/groupList"));
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const panels_1 = require("app/components/panels");
const constants_1 = require("app/constants");
const globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const queryString_1 = require("app/utils/queryString");
const noGroupsHandler_1 = (0, tslib_1.__importDefault)(require("../issueList/noGroupsHandler"));
function ProjectIssues({ organization, location, projectId, query, api }) {
    const [pageLinks, setPageLinks] = (0, react_1.useState)();
    const [onCursor, setOnCursor] = (0, react_1.useState)();
    function handleOpenInIssuesClick() {
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey: 'project_detail.open_issues',
            eventName: 'Project Detail: Open issues from project detail',
            organization_id: parseInt(organization.id, 10),
        });
    }
    function handleOpenInDiscoverClick() {
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey: 'project_detail.open_discover',
            eventName: 'Project Detail: Open discover from project detail',
            organization_id: parseInt(organization.id, 10),
        });
    }
    function handleFetchSuccess(groupListState, cursorHandler) {
        setPageLinks(groupListState.pageLinks);
        setOnCursor(() => cursorHandler);
    }
    function getDiscoverUrl() {
        return {
            pathname: `/organizations/${organization.slug}/discover/results/`,
            query: Object.assign({ name: (0, locale_1.t)('Frequent Unhandled Issues'), field: ['issue', 'title', 'count()', 'count_unique(user)', 'project'], sort: ['-count'], query: ['event.type:error error.unhandled:true', query].join(' ').trim(), display: 'top5' }, (0, getParams_1.getParams)((0, pick_1.default)(location.query, [...Object.values(globalSelectionHeader_1.URL_PARAM)]))),
        };
    }
    const endpointPath = `/organizations/${organization.slug}/issues/`;
    const issueQuery = ['is:unresolved error.unhandled:true ', query].join(' ').trim();
    const queryParams = Object.assign(Object.assign({ limit: 5 }, (0, getParams_1.getParams)((0, pick_1.default)(location.query, [...Object.values(globalSelectionHeader_1.URL_PARAM), 'cursor']))), { query: issueQuery, sort: 'freq' });
    const issueSearch = {
        pathname: endpointPath,
        query: queryParams,
    };
    function renderEmptyMessage() {
        const selectedTimePeriod = location.query.start
            ? null
            : constants_1.DEFAULT_RELATIVE_PERIODS[(0, queryString_1.decodeScalar)(location.query.statsPeriod, constants_1.DEFAULT_STATS_PERIOD)];
        const displayedPeriod = selectedTimePeriod
            ? selectedTimePeriod.toLowerCase()
            : (0, locale_1.t)('given timeframe');
        return (<panels_1.Panel>
        <panels_1.PanelBody>
          <noGroupsHandler_1.default api={api} organization={organization} query={issueQuery} selectedProjectIds={[projectId]} groupIds={[]} emptyMessage={(0, locale_1.tct)('No unhandled issues for the [timePeriod].', {
                timePeriod: displayedPeriod,
            })}/>
        </panels_1.PanelBody>
      </panels_1.Panel>);
    }
    return (<react_1.Fragment>
      <ControlsWrapper>
        <styles_1.SectionHeading>{(0, locale_1.t)('Frequent Unhandled Issues')}</styles_1.SectionHeading>
        <buttonBar_1.default gap={1}>
          <button_1.default data-test-id="issues-open" size="small" to={issueSearch} onClick={handleOpenInIssuesClick}>
            {(0, locale_1.t)('Open in Issues')}
          </button_1.default>
          <discoverButton_1.default onClick={handleOpenInDiscoverClick} to={getDiscoverUrl()} size="small">
            {(0, locale_1.t)('Open in Discover')}
          </discoverButton_1.default>
          <StyledPagination pageLinks={pageLinks} onCursor={onCursor}/>
        </buttonBar_1.default>
      </ControlsWrapper>

      <groupList_1.default orgId={organization.slug} endpointPath={endpointPath} queryParams={queryParams} query="" canSelectGroups={false} renderEmptyMessage={renderEmptyMessage} withChart={false} withPagination={false} onFetchSuccess={handleFetchSuccess}/>
    </react_1.Fragment>);
}
const ControlsWrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: ${(0, space_1.default)(1)};
  flex-wrap: wrap;
  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    display: block;
  }
`;
const StyledPagination = (0, styled_1.default)(pagination_1.default) `
  margin: 0;
`;
exports.default = ProjectIssues;
//# sourceMappingURL=projectIssues.jsx.map