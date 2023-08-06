Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const guideAnchor_1 = (0, tslib_1.__importDefault)(require("app/components/assistant/guideAnchor"));
const badge_1 = (0, tslib_1.__importDefault)(require("app/components/badge"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const globalEventProcessingAlert_1 = (0, tslib_1.__importDefault)(require("app/components/globalEventProcessingAlert"));
const Layout = (0, tslib_1.__importStar)(require("app/components/layouts/thirds"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const queryCount_1 = (0, tslib_1.__importDefault)(require("app/components/queryCount"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
const savedSearchTab_1 = (0, tslib_1.__importDefault)(require("./savedSearchTab"));
const utils_1 = require("./utils");
function WrapGuideTabs({ children, tabQuery, query, to }) {
    if (tabQuery === utils_1.Query.FOR_REVIEW) {
        return (<guideAnchor_1.default target="inbox_guide_tab" disabled={query === utils_1.Query.FOR_REVIEW} to={to}>
        <guideAnchor_1.default target="for_review_guide_tab">{children}</guideAnchor_1.default>
      </guideAnchor_1.default>);
    }
    return children;
}
function IssueListHeader({ organization, query, sort, queryCount, queryCounts, realtimeActive, onRealtimeChange, onSavedSearchSelect, onSavedSearchDelete, savedSearchList, router, displayReprocessingTab, selectedProjectIds, projects, }) {
    var _a, _b;
    const tabs = (0, utils_1.getTabs)(organization);
    const visibleTabs = displayReprocessingTab
        ? tabs
        : tabs.filter(([tab]) => tab !== utils_1.Query.REPROCESSING);
    const savedSearchTabActive = !visibleTabs.some(([tabQuery]) => tabQuery === query);
    // Remove cursor and page when switching tabs
    const _c = (_b = (_a = router === null || router === void 0 ? void 0 : router.location) === null || _a === void 0 ? void 0 : _a.query) !== null && _b !== void 0 ? _b : {}, { cursor: _, page: __ } = _c, queryParms = (0, tslib_1.__rest)(_c, ["cursor", "page"]);
    const sortParam = queryParms.sort === utils_1.IssueSortOptions.INBOX ? undefined : queryParms.sort;
    function trackTabClick(tabQuery) {
        // Clicking on inbox tab and currently another tab is active
        if (tabQuery === utils_1.Query.FOR_REVIEW && query !== utils_1.Query.FOR_REVIEW) {
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'inbox_tab.clicked',
                eventName: 'Clicked Inbox Tab',
                organization_id: organization.id,
            });
        }
    }
    const selectedProjects = projects.filter(({ id }) => selectedProjectIds.includes(Number(id)));
    return (<React.Fragment>
      <BorderlessHeader>
        <StyledHeaderContent>
          <StyledLayoutTitle>{(0, locale_1.t)('Issues')}</StyledLayoutTitle>
        </StyledHeaderContent>
        <Layout.HeaderActions>
          <buttonBar_1.default gap={1}>
            <button_1.default size="small" data-test-id="real-time" title={(0, locale_1.t)('%s real-time updates', realtimeActive ? (0, locale_1.t)('Pause') : (0, locale_1.t)('Enable'))} onClick={() => onRealtimeChange(!realtimeActive)}>
              {realtimeActive ? <icons_1.IconPause size="xs"/> : <icons_1.IconPlay size="xs"/>}
            </button_1.default>
          </buttonBar_1.default>
        </Layout.HeaderActions>
        <StyledGlobalEventProcessingAlert projects={selectedProjects}/>
      </BorderlessHeader>
      <TabLayoutHeader>
        <Layout.HeaderNavTabs underlined>
          {visibleTabs.map(([tabQuery, { name: queryName, tooltipTitle, tooltipHoverable }]) => {
            var _a;
            const to = {
                query: Object.assign(Object.assign({}, queryParms), { query: tabQuery, sort: tabQuery === utils_1.Query.FOR_REVIEW ? utils_1.IssueSortOptions.INBOX : sortParam }),
                pathname: `/organizations/${organization.slug}/issues/`,
            };
            return (<li key={tabQuery} className={query === tabQuery ? 'active' : ''}>
                  <link_1.default to={to} onClick={() => trackTabClick(tabQuery)}>
                    <WrapGuideTabs query={query} tabQuery={tabQuery} to={to}>
                      <tooltip_1.default title={tooltipTitle} position="bottom" isHoverable={tooltipHoverable} delay={1000}>
                        {queryName}{' '}
                        {((_a = queryCounts[tabQuery]) === null || _a === void 0 ? void 0 : _a.count) > 0 && (<badge_1.default type={tabQuery === utils_1.Query.FOR_REVIEW &&
                        queryCounts[tabQuery].count > 0
                        ? 'review'
                        : 'default'}>
                            <queryCount_1.default hideParens count={queryCounts[tabQuery].count} max={queryCounts[tabQuery].hasMore ? utils_1.TAB_MAX_COUNT : 1000}/>
                          </badge_1.default>)}
                      </tooltip_1.default>
                    </WrapGuideTabs>
                  </link_1.default>
                </li>);
        })}
          <savedSearchTab_1.default organization={organization} query={query} sort={sort} savedSearchList={savedSearchList} onSavedSearchSelect={onSavedSearchSelect} onSavedSearchDelete={onSavedSearchDelete} isActive={savedSearchTabActive} queryCount={queryCount}/>
        </Layout.HeaderNavTabs>
      </TabLayoutHeader>
    </React.Fragment>);
}
exports.default = (0, withProjects_1.default)(IssueListHeader);
const StyledLayoutTitle = (0, styled_1.default)(Layout.Title) `
  margin-top: ${(0, space_1.default)(0.5)};
`;
const BorderlessHeader = (0, styled_1.default)(Layout.Header) `
  border-bottom: 0;
  /* Not enough buttons to change direction for mobile view */
  grid-template-columns: 1fr auto;
`;
const TabLayoutHeader = (0, styled_1.default)(Layout.Header) `
  padding-top: 0;

  @media (max-width: ${p => p.theme.breakpoints[1]}) {
    padding-top: 0;
  }
`;
const StyledHeaderContent = (0, styled_1.default)(Layout.HeaderContent) `
  margin-bottom: 0;
  margin-right: ${(0, space_1.default)(2)};
`;
const StyledGlobalEventProcessingAlert = (0, styled_1.default)(globalEventProcessingAlert_1.default) `
  grid-column: 1/-1;
  margin-top: ${(0, space_1.default)(1)};
  margin-bottom: ${(0, space_1.default)(1)};

  @media (min-width: ${p => p.theme.breakpoints[1]}) {
    margin-top: ${(0, space_1.default)(2)};
    margin-bottom: 0;
  }
`;
//# sourceMappingURL=header.jsx.map