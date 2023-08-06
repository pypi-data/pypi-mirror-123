Object.defineProperty(exports, "__esModule", { value: true });
exports.IssueListOverview = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const react_1 = require("@sentry/react");
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const js_cookie_1 = (0, tslib_1.__importDefault)(require("js-cookie"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const mapValues_1 = (0, tslib_1.__importDefault)(require("lodash/mapValues"));
const omit_1 = (0, tslib_1.__importDefault)(require("lodash/omit"));
const pickBy_1 = (0, tslib_1.__importDefault)(require("lodash/pickBy"));
const qs = (0, tslib_1.__importStar)(require("query-string"));
const members_1 = require("app/actionCreators/members");
const savedSearches_1 = require("app/actionCreators/savedSearches");
const tags_1 = require("app/actionCreators/tags");
const groupActions_1 = (0, tslib_1.__importDefault)(require("app/actions/groupActions"));
const guideAnchor_1 = (0, tslib_1.__importDefault)(require("app/components/assistant/guideAnchor"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const utils_1 = require("app/components/organizations/globalSelectionHeader/utils");
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const panels_1 = require("app/components/panels");
const queryCount_1 = (0, tslib_1.__importDefault)(require("app/components/queryCount"));
const group_1 = (0, tslib_1.__importDefault)(require("app/components/stream/group"));
const processingIssueList_1 = (0, tslib_1.__importDefault)(require("app/components/stream/processingIssueList"));
const constants_1 = require("app/constants");
const locale_1 = require("app/locale");
const groupStore_1 = (0, tslib_1.__importDefault)(require("app/stores/groupStore"));
const organization_1 = require("app/styles/organization");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_2 = require("app/utils");
const analytics_1 = require("app/utils/analytics");
const callIfFunction_1 = require("app/utils/callIfFunction");
const cursorPoller_1 = (0, tslib_1.__importDefault)(require("app/utils/cursorPoller"));
const dates_1 = require("app/utils/dates");
const getCurrentSentryReactTransaction_1 = (0, tslib_1.__importDefault)(require("app/utils/getCurrentSentryReactTransaction"));
const parseApiError_1 = (0, tslib_1.__importDefault)(require("app/utils/parseApiError"));
const parseLinkHeader_1 = (0, tslib_1.__importDefault)(require("app/utils/parseLinkHeader"));
const streamManager_1 = (0, tslib_1.__importDefault)(require("app/utils/streamManager"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withGlobalSelection_1 = (0, tslib_1.__importDefault)(require("app/utils/withGlobalSelection"));
const withIssueTags_1 = (0, tslib_1.__importDefault)(require("app/utils/withIssueTags"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const withSavedSearches_1 = (0, tslib_1.__importDefault)(require("app/utils/withSavedSearches"));
const actions_1 = (0, tslib_1.__importDefault)(require("./actions"));
const filters_1 = (0, tslib_1.__importDefault)(require("./filters"));
const header_1 = (0, tslib_1.__importDefault)(require("./header"));
const noGroupsHandler_1 = (0, tslib_1.__importDefault)(require("./noGroupsHandler"));
const sidebar_1 = (0, tslib_1.__importDefault)(require("./sidebar"));
const utils_3 = require("./utils");
const MAX_ITEMS = 25;
const DEFAULT_SORT = utils_3.IssueSortOptions.DATE;
const DEFAULT_DISPLAY = utils_3.IssueDisplayOptions.EVENTS;
// the default period for the graph in each issue row
const DEFAULT_GRAPH_STATS_PERIOD = '24h';
// the allowed period choices for graph in each issue row
const DYNAMIC_COUNTS_STATS_PERIODS = new Set(['14d', '24h', 'auto']);
class IssueListOverview extends React.Component {
    constructor() {
        super(...arguments);
        this.state = this.getInitialState();
        this._streamManager = new streamManager_1.default(groupStore_1.default);
        this.getEndpointParams = () => {
            const { selection } = this.props;
            const params = Object.assign({ project: selection.projects, environment: selection.environments, query: this.getQuery() }, selection.datetime);
            if (selection.datetime.period) {
                delete params.period;
                params.statsPeriod = selection.datetime.period;
            }
            if (params.end) {
                params.end = (0, dates_1.getUtcDateString)(params.end);
            }
            if (params.start) {
                params.start = (0, dates_1.getUtcDateString)(params.start);
            }
            const sort = this.getSort();
            if (sort !== DEFAULT_SORT) {
                params.sort = sort;
            }
            const display = this.getDisplay();
            if (display !== DEFAULT_DISPLAY) {
                params.display = display;
            }
            const groupStatsPeriod = this.getGroupStatsPeriod();
            if (groupStatsPeriod !== DEFAULT_GRAPH_STATS_PERIOD) {
                params.groupStatsPeriod = groupStatsPeriod;
            }
            // only include defined values.
            return (0, pickBy_1.default)(params, v => (0, utils_2.defined)(v));
        };
        this.getGlobalSearchProjectIds = () => {
            return this.props.selection.projects;
        };
        this.fetchStats = (groups) => {
            // If we have no groups to fetch, just skip stats
            if (!groups.length) {
                this.setState({ hasSessions: false });
                return;
            }
            const requestParams = Object.assign(Object.assign({}, this.getEndpointParams()), { groups });
            // If no stats period values are set, use default
            if (!requestParams.statsPeriod && !requestParams.start) {
                requestParams.statsPeriod = constants_1.DEFAULT_STATS_PERIOD;
            }
            if (this.props.organization.features.includes('issue-percent-display')) {
                requestParams.expand = 'sessions';
            }
            this._lastStatsRequest = this.props.api.request(this.getGroupStatsEndpoint(), {
                method: 'GET',
                data: qs.stringify(requestParams),
                success: data => {
                    if (!data) {
                        return;
                    }
                    groupActions_1.default.populateStats(groups, data);
                    const hasSessions = data.filter(groupStats => !groupStats.sessionCount).length === 0;
                    if (hasSessions !== this.state.hasSessions) {
                        this.setState({
                            hasSessions,
                        });
                    }
                },
                error: err => {
                    this.setState({
                        error: (0, parseApiError_1.default)(err),
                    });
                },
                complete: () => {
                    var _a;
                    this._lastStatsRequest = null;
                    // End navigation transaction to prevent additional page requests from impacting page metrics.
                    // Other transactions include stacktrace preview request
                    const currentTransaction = (_a = Sentry.getCurrentHub().getScope()) === null || _a === void 0 ? void 0 : _a.getTransaction();
                    if ((currentTransaction === null || currentTransaction === void 0 ? void 0 : currentTransaction.op) === 'navigation') {
                        currentTransaction.finish();
                    }
                },
            });
        };
        this.fetchCounts = (currentQueryCount, fetchAllCounts) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            var _a;
            const { organization } = this.props;
            const { queryCounts: _queryCounts } = this.state;
            let queryCounts = Object.assign({}, _queryCounts);
            const endpointParams = this.getEndpointParams();
            const tabQueriesWithCounts = (0, utils_3.getTabsWithCounts)(organization);
            const currentTabQuery = tabQueriesWithCounts.includes(endpointParams.query)
                ? endpointParams.query
                : null;
            // If all tabs' counts are fetched, skip and only set
            if (fetchAllCounts ||
                !tabQueriesWithCounts.every(tabQuery => queryCounts[tabQuery] !== undefined)) {
                const requestParams = Object.assign(Object.assign({}, (0, omit_1.default)(endpointParams, 'query')), { 
                    // fetch the counts for the tabs whose counts haven't been fetched yet
                    query: tabQueriesWithCounts.filter(_query => _query !== currentTabQuery) });
                // If no stats period values are set, use default
                if (!requestParams.statsPeriod && !requestParams.start) {
                    requestParams.statsPeriod = constants_1.DEFAULT_STATS_PERIOD;
                }
                try {
                    const response = yield this.props.api.requestPromise(this.getGroupCountsEndpoint(), {
                        method: 'GET',
                        data: qs.stringify(requestParams),
                    });
                    // Counts coming from the counts endpoint is limited to 100, for >= 100 we display 99+
                    queryCounts = Object.assign(Object.assign({}, queryCounts), (0, mapValues_1.default)(response, (count) => ({
                        count,
                        hasMore: count > utils_3.TAB_MAX_COUNT,
                    })));
                }
                catch (e) {
                    this.setState({
                        error: (0, parseApiError_1.default)(e),
                    });
                    return;
                }
            }
            // Update the count based on the exact number of issues, these shown as is
            if (currentTabQuery) {
                queryCounts[currentTabQuery] = {
                    count: currentQueryCount,
                    hasMore: false,
                };
                const tab = (_a = (0, utils_3.getTabs)(organization).find(([tabQuery]) => currentTabQuery === tabQuery)) === null || _a === void 0 ? void 0 : _a[1];
                if (tab && !endpointParams.cursor) {
                    (0, analytics_1.trackAnalyticsEvent)({
                        eventKey: 'issues_tab.viewed',
                        eventName: 'Viewed Issues Tab',
                        organization_id: organization.id,
                        tab: tab.analyticsName,
                        num_issues: queryCounts[currentTabQuery].count,
                    });
                }
            }
            this.setState({ queryCounts });
        });
        this.fetchData = (fetchAllCounts = false) => {
            groupStore_1.default.loadInitialData([]);
            this._streamManager.reset();
            const transaction = (0, getCurrentSentryReactTransaction_1.default)();
            transaction === null || transaction === void 0 ? void 0 : transaction.setTag('query.sort', this.getSort());
            this.setState({
                issuesLoading: true,
                queryCount: 0,
                itemsRemoved: 0,
                error: null,
            });
            const requestParams = Object.assign(Object.assign({}, this.getEndpointParams()), { limit: MAX_ITEMS, shortIdLookup: 1 });
            const currentQuery = this.props.location.query || {};
            if ('cursor' in currentQuery) {
                requestParams.cursor = currentQuery.cursor;
            }
            // If no stats period values are set, use default
            if (!requestParams.statsPeriod && !requestParams.start) {
                requestParams.statsPeriod = constants_1.DEFAULT_STATS_PERIOD;
            }
            requestParams.expand = ['owners', 'inbox'];
            requestParams.collapse = 'stats';
            if (this._lastRequest) {
                this._lastRequest.cancel();
            }
            if (this._lastStatsRequest) {
                this._lastStatsRequest.cancel();
            }
            this._poller.disable();
            this._lastRequest = this.props.api.request(this.getGroupListEndpoint(), {
                method: 'GET',
                data: qs.stringify(requestParams),
                success: (data, _, resp) => {
                    if (!resp) {
                        return;
                    }
                    const { orgId } = this.props.params;
                    // If this is a direct hit, we redirect to the intended result directly.
                    if (resp.getResponseHeader('X-Sentry-Direct-Hit') === '1') {
                        let redirect;
                        if (data[0] && data[0].matchingEventId) {
                            const { id, matchingEventId } = data[0];
                            redirect = `/organizations/${orgId}/issues/${id}/events/${matchingEventId}/`;
                        }
                        else {
                            const { id } = data[0];
                            redirect = `/organizations/${orgId}/issues/${id}/`;
                        }
                        react_router_1.browserHistory.replace({
                            pathname: redirect,
                            query: (0, utils_1.extractSelectionParameters)(this.props.location.query),
                        });
                        return;
                    }
                    this._streamManager.push(data);
                    this.fetchStats(data.map((group) => group.id));
                    const hits = resp.getResponseHeader('X-Hits');
                    const queryCount = typeof hits !== 'undefined' && hits ? parseInt(hits, 10) || 0 : 0;
                    const maxHits = resp.getResponseHeader('X-Max-Hits');
                    const queryMaxCount = typeof maxHits !== 'undefined' && maxHits ? parseInt(maxHits, 10) || 0 : 0;
                    const pageLinks = resp.getResponseHeader('Link');
                    this.fetchCounts(queryCount, fetchAllCounts);
                    this.setState({
                        error: null,
                        issuesLoading: false,
                        queryCount,
                        queryMaxCount,
                        pageLinks: pageLinks !== null ? pageLinks : '',
                    });
                },
                error: err => {
                    (0, analytics_1.trackAnalyticsEvent)({
                        eventKey: 'issue_search.failed',
                        eventName: 'Issue Search: Failed',
                        organization_id: this.props.organization.id,
                        search_type: 'issues',
                        search_source: 'main_search',
                        error: (0, parseApiError_1.default)(err),
                    });
                    this.setState({
                        error: (0, parseApiError_1.default)(err),
                        issuesLoading: false,
                    });
                },
                complete: () => {
                    this._lastRequest = null;
                    this.resumePolling();
                },
            });
        };
        this.resumePolling = () => {
            if (!this.state.pageLinks) {
                return;
            }
            // Only resume polling if we're on the first page of results
            const links = (0, parseLinkHeader_1.default)(this.state.pageLinks);
            if (links && !links.previous.results && this.state.realtimeActive) {
                // Remove collapse stats from endpoint before supplying to poller
                const issueEndpoint = new URL(links.previous.href, window.location.origin);
                issueEndpoint.searchParams.delete('collapse');
                this._poller.setEndpoint(decodeURIComponent(issueEndpoint.href));
                this._poller.enable();
            }
        };
        this.onRealtimeChange = (realtime) => {
            js_cookie_1.default.set('realtimeActive', realtime.toString());
            this.setState({ realtimeActive: realtime });
        };
        this.onSelectStatsPeriod = (period) => {
            if (period !== this.getGroupStatsPeriod()) {
                this.transitionTo({ groupStatsPeriod: period });
            }
        };
        this.onRealtimePoll = (data, _links) => {
            // Note: We do not update state with cursors from polling,
            // `CursorPoller` updates itself with new cursors
            this._streamManager.unshift(data);
        };
        this.listener = groupStore_1.default.listen(() => this.onGroupChange(), undefined);
        this.onIssueListSidebarSearch = (query) => {
            (0, analytics_1.analytics)('search.searched', {
                org_id: this.props.organization.id,
                query,
                search_type: 'issues',
                search_source: 'search_builder',
            });
            this.onSearch(query);
        };
        this.onSearch = (query) => {
            if (query === this.state.query) {
                // if query is the same, just re-fetch data
                this.fetchData();
            }
            else {
                // Clear the saved search as the user wants something else.
                this.transitionTo({ query }, null);
            }
        };
        this.onSortChange = (sort) => {
            this.transitionTo({ sort });
        };
        this.onDisplayChange = (display) => {
            this.transitionTo({ display });
        };
        this.onCursorChange = (nextCursor, _path, _query, delta) => {
            const queryPageInt = parseInt(this.props.location.query.page, 10);
            let nextPage = isNaN(queryPageInt) ? delta : queryPageInt + delta;
            let cursor = nextCursor;
            // unset cursor and page when we navigate back to the first page
            // also reset cursor if somehow the previous button is enabled on
            // first page and user attempts to go backwards
            if (nextPage <= 0) {
                cursor = undefined;
                nextPage = undefined;
            }
            this.transitionTo({ cursor, page: nextPage });
        };
        this.onSidebarToggle = () => {
            const { organization } = this.props;
            this.setState({
                isSidebarVisible: !this.state.isSidebarVisible,
                renderSidebar: true,
            });
            (0, analytics_1.analytics)('issue.search_sidebar_clicked', {
                org_id: parseInt(organization.id, 10),
            });
        };
        this.transitionTo = (newParams = {}, savedSearch = this.props.savedSearch) => {
            const query = Object.assign(Object.assign({}, this.getEndpointParams()), newParams);
            const { organization } = this.props;
            let path;
            if (savedSearch && savedSearch.id) {
                path = `/organizations/${organization.slug}/issues/searches/${savedSearch.id}/`;
                // Remove the query as saved searches bring their own query string.
                delete query.query;
                // If we aren't going to another page in the same search
                // drop the query and replace the current project, with the saved search search project
                // if available.
                if (!query.cursor && savedSearch.projectId) {
                    query.project = [savedSearch.projectId];
                }
                if (!query.cursor && !newParams.sort && savedSearch.sort) {
                    query.sort = savedSearch.sort;
                }
            }
            else {
                path = `/organizations/${organization.slug}/issues/`;
            }
            // Remove inbox tab specific sort
            if (query.sort === utils_3.IssueSortOptions.INBOX && query.query !== utils_3.Query.FOR_REVIEW) {
                delete query.sort;
            }
            if (path !== this.props.location.pathname ||
                !(0, isEqual_1.default)(query, this.props.location.query)) {
                react_router_1.browserHistory.push({
                    pathname: path,
                    query,
                });
                this.setState({ issuesLoading: true });
            }
        };
        this.renderGroupNodes = (ids, groupStatsPeriod) => {
            const topIssue = ids[0];
            const { memberList } = this.state;
            const query = this.getQuery();
            const showInboxTime = this.getSort() === utils_3.IssueSortOptions.INBOX;
            return ids.map((id, index) => {
                const hasGuideAnchor = id === topIssue;
                const group = groupStore_1.default.get(id);
                let members;
                if (group === null || group === void 0 ? void 0 : group.project) {
                    members = memberList[group.project.slug];
                }
                const showReprocessingTab = this.displayReprocessingTab();
                const displayReprocessingLayout = this.displayReprocessingLayout(showReprocessingTab, query);
                return (<group_1.default index={index} key={id} id={id} statsPeriod={groupStatsPeriod} query={query} hasGuideAnchor={hasGuideAnchor} memberList={members} displayReprocessingLayout={displayReprocessingLayout} useFilteredStats showInboxTime={showInboxTime} display={this.getDisplay()}/>);
            });
        };
        this.fetchSavedSearches = () => {
            const { organization, api } = this.props;
            (0, savedSearches_1.fetchSavedSearches)(api, organization.slug);
        };
        this.onSavedSearchSelect = (savedSearch) => {
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'organization_saved_search.selected',
                eventName: 'Organization Saved Search: Selected saved search',
                organization_id: this.props.organization.id,
                search_type: 'issues',
                id: savedSearch.id ? parseInt(savedSearch.id, 10) : -1,
            });
            this.setState({ issuesLoading: true }, () => this.transitionTo(undefined, savedSearch));
        };
        this.onSavedSearchDelete = (search) => {
            const { orgId } = this.props.params;
            (0, savedSearches_1.deleteSavedSearch)(this.props.api, orgId, search).then(() => {
                this.setState({
                    issuesLoading: true,
                }, () => this.transitionTo({}, null));
            });
        };
        this.onDelete = () => {
            this.fetchData(true);
        };
        this.onMarkReviewed = (itemIds) => {
            const query = this.getQuery();
            if (!(0, utils_3.isForReviewQuery)(query)) {
                return;
            }
            const { queryCounts, itemsRemoved } = this.state;
            const currentQueryCount = queryCounts[query];
            if (itemIds.length && currentQueryCount) {
                const inInboxCount = itemIds.filter(id => { var _a; return (_a = groupStore_1.default.get(id)) === null || _a === void 0 ? void 0 : _a.inbox; }).length;
                currentQueryCount.count -= inInboxCount;
                this.setState({
                    queryCounts: Object.assign(Object.assign({}, queryCounts), { [query]: currentQueryCount }),
                    itemsRemoved: itemsRemoved + inInboxCount,
                });
            }
        };
        this.tagValueLoader = (key, search) => {
            const { orgId } = this.props.params;
            const projectIds = this.getGlobalSearchProjectIds().map(id => id.toString());
            const endpointParams = this.getEndpointParams();
            return (0, tags_1.fetchTagValues)(this.props.api, orgId, key, search, projectIds, endpointParams);
        };
    }
    getInitialState() {
        const realtimeActiveCookie = js_cookie_1.default.get('realtimeActive');
        const realtimeActive = typeof realtimeActiveCookie === 'undefined'
            ? false
            : realtimeActiveCookie === 'true';
        return {
            groupIds: [],
            selectAllActive: false,
            realtimeActive,
            pageLinks: '',
            itemsRemoved: 0,
            queryCount: 0,
            queryCounts: {},
            queryMaxCount: 0,
            error: null,
            isSidebarVisible: false,
            renderSidebar: false,
            issuesLoading: true,
            tagsLoading: true,
            memberList: {},
            hasSessions: false,
        };
    }
    componentDidMount() {
        var _a;
        const links = (0, parseLinkHeader_1.default)(this.state.pageLinks);
        this._poller = new cursorPoller_1.default({
            endpoint: ((_a = links.previous) === null || _a === void 0 ? void 0 : _a.href) || '',
            success: this.onRealtimePoll,
        });
        // Start by getting searches first so if the user is on a saved search
        // or they have a pinned search we load the correct data the first time.
        this.fetchSavedSearches();
        this.fetchTags();
        this.fetchMemberList();
    }
    componentDidUpdate(prevProps, prevState) {
        var _a;
        if (prevState.realtimeActive !== this.state.realtimeActive) {
            // User toggled realtime button
            if (this.state.realtimeActive) {
                this.resumePolling();
            }
            else {
                this._poller.disable();
            }
        }
        // If the project selection has changed reload the member list and tag keys
        // allowing autocomplete and tag sidebar to be more accurate.
        if (!(0, isEqual_1.default)(prevProps.selection.projects, this.props.selection.projects)) {
            this.fetchMemberList();
            this.fetchTags();
            // Reset display when selecting multiple projects
            const projects = (_a = this.props.selection.projects) !== null && _a !== void 0 ? _a : [];
            const hasMultipleProjects = projects.length !== 1 || projects[0] === -1;
            if (hasMultipleProjects && this.getDisplay() !== DEFAULT_DISPLAY) {
                this.transitionTo({ display: undefined });
            }
        }
        // Wait for saved searches to load before we attempt to fetch stream data
        if (this.props.savedSearchLoading) {
            return;
        }
        else if (prevProps.savedSearchLoading) {
            this.fetchData();
            return;
        }
        const prevQuery = prevProps.location.query;
        const newQuery = this.props.location.query;
        const selectionChanged = !(0, isEqual_1.default)(prevProps.selection, this.props.selection);
        // If any important url parameter changed or saved search changed
        // reload data.
        if (selectionChanged ||
            prevQuery.cursor !== newQuery.cursor ||
            prevQuery.sort !== newQuery.sort ||
            prevQuery.query !== newQuery.query ||
            prevQuery.statsPeriod !== newQuery.statsPeriod ||
            prevQuery.groupStatsPeriod !== newQuery.groupStatsPeriod ||
            prevProps.savedSearch !== this.props.savedSearch) {
            this.fetchData(selectionChanged);
        }
        else if (!this._lastRequest &&
            prevState.issuesLoading === false &&
            this.state.issuesLoading) {
            // Reload if we issues are loading or their loading state changed.
            // This can happen when transitionTo is called
            this.fetchData();
        }
    }
    componentWillUnmount() {
        this._poller.disable();
        groupStore_1.default.reset();
        this.props.api.clear();
        (0, callIfFunction_1.callIfFunction)(this.listener);
        // Reset store when unmounting because we always fetch on mount
        // This means if you navigate away from stream and then back to stream,
        // this component will go from:
        // "ready" ->
        // "loading" (because fetching saved searches) ->
        // "ready"
        //
        // We don't render anything until saved searches is ready, so this can
        // cause weird side effects (e.g. ProcessingIssueList mounting and making
        // a request, but immediately unmounting when fetching saved searches)
        (0, savedSearches_1.resetSavedSearches)();
    }
    getQuery() {
        const { savedSearch, location } = this.props;
        if (savedSearch) {
            return savedSearch.query;
        }
        const { query } = location.query;
        if (query !== undefined) {
            return query;
        }
        return constants_1.DEFAULT_QUERY;
    }
    getSort() {
        const { location, savedSearch } = this.props;
        if (!location.query.sort && (savedSearch === null || savedSearch === void 0 ? void 0 : savedSearch.id)) {
            return savedSearch.sort;
        }
        if (location.query.sort) {
            return location.query.sort;
        }
        return DEFAULT_SORT;
    }
    getDisplay() {
        const { organization, location } = this.props;
        if (organization.features.includes('issue-percent-display')) {
            if (location.query.display &&
                Object.values(utils_3.IssueDisplayOptions).includes(location.query.display)) {
                return location.query.display;
            }
        }
        return DEFAULT_DISPLAY;
    }
    getGroupStatsPeriod() {
        var _a;
        let currentPeriod;
        if (typeof ((_a = this.props.location.query) === null || _a === void 0 ? void 0 : _a.groupStatsPeriod) === 'string') {
            currentPeriod = this.props.location.query.groupStatsPeriod;
        }
        else if (this.getSort() === utils_3.IssueSortOptions.TREND) {
            // Default to the larger graph when sorting by relative change
            currentPeriod = 'auto';
        }
        else {
            currentPeriod = DEFAULT_GRAPH_STATS_PERIOD;
        }
        return DYNAMIC_COUNTS_STATS_PERIODS.has(currentPeriod)
            ? currentPeriod
            : DEFAULT_GRAPH_STATS_PERIOD;
    }
    fetchMemberList() {
        var _a;
        const projectIds = (_a = this.getGlobalSearchProjectIds()) === null || _a === void 0 ? void 0 : _a.map(projectId => String(projectId));
        (0, members_1.fetchOrgMembers)(this.props.api, this.props.organization.slug, projectIds).then(members => {
            this.setState({ memberList: (0, members_1.indexMembersByProject)(members) });
        });
    }
    fetchTags() {
        const { organization, selection } = this.props;
        this.setState({ tagsLoading: true });
        (0, tags_1.loadOrganizationTags)(this.props.api, organization.slug, selection).then(() => this.setState({ tagsLoading: false }));
    }
    getGroupListEndpoint() {
        const { orgId } = this.props.params;
        return `/organizations/${orgId}/issues/`;
    }
    getGroupCountsEndpoint() {
        const { orgId } = this.props.params;
        return `/organizations/${orgId}/issues-count/`;
    }
    getGroupStatsEndpoint() {
        const { orgId } = this.props.params;
        return `/organizations/${orgId}/issues-stats/`;
    }
    onGroupChange() {
        var _a;
        const groupIds = (_a = this._streamManager.getAllItems().map(item => item.id)) !== null && _a !== void 0 ? _a : [];
        if (!(0, isEqual_1.default)(groupIds, this.state.groupIds)) {
            this.setState({ groupIds });
        }
    }
    /**
     * Returns true if all results in the current query are visible/on this page
     */
    allResultsVisible() {
        if (!this.state.pageLinks) {
            return false;
        }
        const links = (0, parseLinkHeader_1.default)(this.state.pageLinks);
        return links && !links.previous.results && !links.next.results;
    }
    displayReprocessingTab() {
        var _a;
        const { organization } = this.props;
        const { queryCounts } = this.state;
        return (organization.features.includes('reprocessing-v2') &&
            !!((_a = queryCounts === null || queryCounts === void 0 ? void 0 : queryCounts[utils_3.Query.REPROCESSING]) === null || _a === void 0 ? void 0 : _a.count));
    }
    displayReprocessingLayout(showReprocessingTab, query) {
        return showReprocessingTab && query === utils_3.Query.REPROCESSING;
    }
    renderLoading() {
        return (<StyledPageContent>
        <loadingIndicator_1.default />
      </StyledPageContent>);
    }
    renderStreamBody() {
        const { issuesLoading, error, groupIds } = this.state;
        if (issuesLoading) {
            return <loadingIndicator_1.default hideMessage/>;
        }
        if (error) {
            return <loadingError_1.default message={error} onRetry={this.fetchData}/>;
        }
        if (groupIds.length > 0) {
            return (<panels_1.PanelBody>
          {this.renderGroupNodes(groupIds, this.getGroupStatsPeriod())}
        </panels_1.PanelBody>);
        }
        const { api, organization, selection } = this.props;
        return (<noGroupsHandler_1.default api={api} organization={organization} query={this.getQuery()} selectedProjectIds={selection.projects} groupIds={groupIds}/>);
    }
    render() {
        var _a, _b, _c;
        if (this.props.savedSearchLoading) {
            return this.renderLoading();
        }
        const { renderSidebar, isSidebarVisible, tagsLoading, pageLinks, queryCount, queryCounts, realtimeActive, groupIds, queryMaxCount, itemsRemoved, hasSessions, } = this.state;
        const { organization, savedSearch, savedSearches, tags, selection, location, router } = this.props;
        const links = (0, parseLinkHeader_1.default)(pageLinks);
        const query = this.getQuery();
        const queryPageInt = parseInt(location.query.page, 10);
        // Cursor must be present for the page number to be used
        const page = isNaN(queryPageInt) || !location.query.cursor ? 0 : queryPageInt;
        const pageBasedCount = page * MAX_ITEMS + groupIds.length;
        let pageCount = pageBasedCount > queryCount ? queryCount : pageBasedCount;
        if (!((_a = links === null || links === void 0 ? void 0 : links.next) === null || _a === void 0 ? void 0 : _a.results) || this.allResultsVisible()) {
            // On last available page
            pageCount = queryCount;
        }
        else if (!((_b = links === null || links === void 0 ? void 0 : links.previous) === null || _b === void 0 ? void 0 : _b.results)) {
            // On first available page
            pageCount = groupIds.length;
        }
        // Subtract # items that have been marked reviewed
        pageCount = Math.max(pageCount - itemsRemoved, 0);
        const modifiedQueryCount = Math.max(queryCount - itemsRemoved, 0);
        const displayCount = (0, locale_1.tct)('[count] of [total]', {
            count: pageCount,
            total: (<StyledQueryCount hideParens hideIfEmpty={false} count={modifiedQueryCount} max={queryMaxCount || 100}/>),
        });
        // TODO(workflow): When organization:semver flag is removed add semver tags to tagStore
        if (organization.features.includes('semver') && !tags['release.version']) {
            tags['release.version'] = {
                key: 'release.version',
                name: 'release.version',
            };
            tags['release.build'] = {
                key: 'release.build',
                name: 'release.build',
            };
            tags['release.package'] = {
                key: 'release.package',
                name: 'release.package',
            };
            tags['release.stage'] = {
                key: 'release.stage',
                name: 'release.stage',
                predefined: true,
                values: constants_1.RELEASE_ADOPTION_STAGES,
            };
        }
        const projectIds = (_c = selection === null || selection === void 0 ? void 0 : selection.projects) === null || _c === void 0 ? void 0 : _c.map(p => p.toString());
        const showReprocessingTab = this.displayReprocessingTab();
        const displayReprocessingActions = this.displayReprocessingLayout(showReprocessingTab, query);
        return (<React.Fragment>
        <header_1.default organization={organization} query={query} sort={this.getSort()} queryCount={queryCount} queryCounts={queryCounts} realtimeActive={realtimeActive} onRealtimeChange={this.onRealtimeChange} router={router} savedSearchList={savedSearches} onSavedSearchSelect={this.onSavedSearchSelect} onSavedSearchDelete={this.onSavedSearchDelete} displayReprocessingTab={showReprocessingTab} selectedProjectIds={selection.projects}/>

        <StyledPageContent>
          <StreamContent showSidebar={isSidebarVisible}>
            <filters_1.default organization={organization} query={query} savedSearch={savedSearch} sort={this.getSort()} display={this.getDisplay()} onDisplayChange={this.onDisplayChange} onSortChange={this.onSortChange} onSearch={this.onSearch} onSidebarToggle={this.onSidebarToggle} isSearchDisabled={isSidebarVisible} tagValueLoader={this.tagValueLoader} tags={tags} hasSessions={hasSessions} selectedProjects={selection.projects}/>

            <panels_1.Panel>
              <actions_1.default organization={organization} selection={selection} query={query} queryCount={modifiedQueryCount} displayCount={displayCount} onSelectStatsPeriod={this.onSelectStatsPeriod} onMarkReviewed={this.onMarkReviewed} onDelete={this.onDelete} statsPeriod={this.getGroupStatsPeriod()} groupIds={groupIds} allResultsVisible={this.allResultsVisible()} displayReprocessingActions={displayReprocessingActions}/>
              <panels_1.PanelBody>
                <processingIssueList_1.default organization={organization} projectIds={projectIds} showProject/>
                {this.renderStreamBody()}
              </panels_1.PanelBody>
            </panels_1.Panel>
            <StyledPagination caption={(0, locale_1.tct)('Showing [displayCount] issues', {
                displayCount,
            })} pageLinks={pageLinks} onCursor={this.onCursorChange}/>
          </StreamContent>

          <SidebarContainer showSidebar={isSidebarVisible}>
            {/* Avoid rendering sidebar until first accessed */}
            {renderSidebar && (<sidebar_1.default loading={tagsLoading} tags={tags} query={query} onQueryChange={this.onIssueListSidebarSearch} tagValueLoader={this.tagValueLoader}/>)}
          </SidebarContainer>
        </StyledPageContent>

        {query === utils_3.Query.FOR_REVIEW && <guideAnchor_1.default target="is_inbox_tab"/>}
      </React.Fragment>);
    }
}
exports.IssueListOverview = IssueListOverview;
exports.default = (0, withApi_1.default)((0, withGlobalSelection_1.default)((0, withSavedSearches_1.default)((0, withOrganization_1.default)((0, withIssueTags_1.default)((0, react_1.withProfiler)(IssueListOverview))))));
// TODO(workflow): Replace PageContent with thirds body
const StyledPageContent = (0, styled_1.default)(organization_1.PageContent) `
  display: flex;
  flex-direction: row;
  background-color: ${p => p.theme.background};

  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    /* Matches thirds layout */
    padding: ${(0, space_1.default)(2)} ${(0, space_1.default)(2)} 0 ${(0, space_1.default)(2)};
  }
`;
const StreamContent = (0, styled_1.default)('div') `
  width: ${p => (p.showSidebar ? '75%' : '100%')};
  transition: width 0.2s ease-in-out;

  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    width: 100%;
  }
`;
const SidebarContainer = (0, styled_1.default)('div') `
  display: ${p => (p.showSidebar ? 'block' : 'none')};
  overflow: ${p => (p.showSidebar ? 'visible' : 'hidden')};
  height: ${p => (p.showSidebar ? 'auto' : 0)};
  width: ${p => (p.showSidebar ? '25%' : 0)};
  transition: width 0.2s ease-in-out;
  margin-left: 20px;

  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    display: none;
  }
`;
const StyledPagination = (0, styled_1.default)(pagination_1.default) `
  margin-top: 0;
`;
const StyledQueryCount = (0, styled_1.default)(queryCount_1.default) `
  margin-left: 0;
`;
//# sourceMappingURL=overview.jsx.map