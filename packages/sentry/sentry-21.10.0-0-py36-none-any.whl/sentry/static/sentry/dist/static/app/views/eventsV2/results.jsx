Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const omit_1 = (0, tslib_1.__importDefault)(require("lodash/omit"));
const discoverSavedQueries_1 = require("app/actionCreators/discoverSavedQueries");
const events_1 = require("app/actionCreators/events");
const projects_1 = require("app/actionCreators/projects");
const tags_1 = require("app/actionCreators/tags");
const api_1 = require("app/api");
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const searchBar_1 = (0, tslib_1.__importDefault)(require("app/components/events/searchBar"));
const Layout = (0, tslib_1.__importStar)(require("app/components/layouts/thirds"));
const noProjectMessage_1 = (0, tslib_1.__importDefault)(require("app/components/noProjectMessage"));
const globalSelectionHeader_1 = (0, tslib_1.__importDefault)(require("app/components/organizations/globalSelectionHeader"));
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const sentryDocumentTitle_1 = (0, tslib_1.__importDefault)(require("app/components/sentryDocumentTitle"));
const constants_1 = require("app/constants");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const organization_1 = require("app/styles/organization");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const analytics_1 = require("app/utils/analytics");
const eventView_1 = (0, tslib_1.__importStar)(require("app/utils/discover/eventView"));
const fields_1 = require("app/utils/discover/fields");
const types_1 = require("app/utils/discover/types");
const localStorage_1 = (0, tslib_1.__importDefault)(require("app/utils/localStorage"));
const queryString_1 = require("app/utils/queryString");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withGlobalSelection_1 = (0, tslib_1.__importDefault)(require("app/utils/withGlobalSelection"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const utils_2 = require("../performance/utils");
const data_1 = require("./data");
const resultsChart_1 = (0, tslib_1.__importDefault)(require("./resultsChart"));
const resultsHeader_1 = (0, tslib_1.__importDefault)(require("./resultsHeader"));
const table_1 = (0, tslib_1.__importDefault)(require("./table"));
const tags_2 = (0, tslib_1.__importDefault)(require("./tags"));
const utils_3 = require("./utils");
const SHOW_TAGS_STORAGE_KEY = 'discover2:show-tags';
function readShowTagsState() {
    const value = localStorage_1.default.getItem(SHOW_TAGS_STORAGE_KEY);
    return value === '1';
}
function getYAxis(location, eventView, savedQuery) {
    return location.query.yAxis
        ? (0, queryString_1.decodeList)(location.query.yAxis)
        : (savedQuery === null || savedQuery === void 0 ? void 0 : savedQuery.yAxis) && savedQuery.yAxis.length > 0
            ? (0, queryString_1.decodeList)(savedQuery === null || savedQuery === void 0 ? void 0 : savedQuery.yAxis)
            : [eventView.getYAxis()];
}
class Results extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            eventView: eventView_1.default.fromSavedQueryOrLocation(this.props.savedQuery, this.props.location),
            error: '',
            errorCode: 200,
            totalValues: null,
            showTags: readShowTagsState(),
            needConfirmation: false,
            confirmedQuery: false,
            incompatibleAlertNotice: null,
        };
        this.tagsApi = new api_1.Client();
        this.canLoadEvents = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, location, organization } = this.props;
            const { eventView } = this.state;
            let needConfirmation = false;
            let confirmedQuery = true;
            const currentQuery = eventView.getEventsAPIPayload(location);
            const duration = eventView.getDays();
            if (duration > 30 && currentQuery.project) {
                let projectLength = currentQuery.project.length;
                if (projectLength === 0 ||
                    (projectLength === 1 && currentQuery.project[0] === '-1')) {
                    try {
                        const results = yield (0, projects_1.fetchProjectsCount)(api, organization.slug);
                        if (projectLength === 0)
                            projectLength = results.myProjects;
                        else
                            projectLength = results.allProjects;
                    }
                    catch (err) {
                        // do nothing, so the length is 0 or 1 and the query is assumed safe
                    }
                }
                if (projectLength > 10) {
                    needConfirmation = true;
                    confirmedQuery = false;
                }
            }
            // Once confirmed, a change of project or datetime will happen before this can set it to false,
            // this means a query will still happen even if the new conditions need confirmation
            // using a state callback to return this to false
            this.setState({ needConfirmation, confirmedQuery }, () => {
                this.setState({ confirmedQuery: false });
            });
            if (needConfirmation) {
                this.openConfirm();
            }
        });
        this.openConfirm = () => { };
        this.setOpenFunction = ({ open }) => {
            this.openConfirm = open;
            return null;
        };
        this.handleConfirmed = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            this.setState({ needConfirmation: false, confirmedQuery: true }, () => {
                this.setState({ confirmedQuery: false });
            });
        });
        this.handleCancelled = () => {
            this.setState({ needConfirmation: false, confirmedQuery: false });
        };
        this.handleChangeShowTags = () => {
            const { organization } = this.props;
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'discover_v2.results.toggle_tag_facets',
                eventName: 'Discoverv2: Toggle Tag Facets',
                organization_id: parseInt(organization.id, 10),
            });
            this.setState(state => {
                const newValue = !state.showTags;
                localStorage_1.default.setItem(SHOW_TAGS_STORAGE_KEY, newValue ? '1' : '0');
                return Object.assign(Object.assign({}, state), { showTags: newValue });
            });
        };
        this.handleSearch = (query) => {
            const { router, location } = this.props;
            const queryParams = (0, getParams_1.getParams)(Object.assign(Object.assign({}, (location.query || {})), { query }));
            // do not propagate pagination when making a new search
            const searchQueryParams = (0, omit_1.default)(queryParams, 'cursor');
            router.push({
                pathname: location.pathname,
                query: searchQueryParams,
            });
        };
        this.handleYAxisChange = (value) => {
            const { router, location } = this.props;
            const isDisplayMultiYAxisSupported = [
                types_1.DisplayModes.DEFAULT,
                types_1.DisplayModes.DAILY,
                types_1.DisplayModes.PREVIOUS,
            ].includes(location.query.display);
            const newQuery = Object.assign(Object.assign({}, location.query), { yAxis: value, 
                // If using Multi Y-axis and not in a supported display, change to the default display mode
                display: value.length > 1 && !isDisplayMultiYAxisSupported
                    ? location.query.display === types_1.DisplayModes.DAILYTOP5
                        ? types_1.DisplayModes.DAILY
                        : types_1.DisplayModes.DEFAULT
                    : location.query.display });
            router.push({
                pathname: location.pathname,
                query: newQuery,
            });
            // Treat axis changing like the user already confirmed the query
            if (!this.state.needConfirmation) {
                this.handleConfirmed();
            }
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'discover_v2.y_axis_change',
                eventName: "Discoverv2: Change chart's y axis",
                organization_id: parseInt(this.props.organization.id, 10),
                y_axis_value: value,
            });
        };
        this.handleDisplayChange = (value) => {
            const { router, location } = this.props;
            const newQuery = Object.assign(Object.assign({}, location.query), { display: value });
            router.push({
                pathname: location.pathname,
                query: newQuery,
            });
            // Treat display changing like the user already confirmed the query
            if (!this.state.needConfirmation) {
                this.handleConfirmed();
            }
        };
        this.handleTopEventsChange = (value) => {
            const { router, location } = this.props;
            const newQuery = Object.assign(Object.assign({}, location.query), { topEvents: value });
            router.push({
                pathname: location.pathname,
                query: newQuery,
            });
            // Treat display changing like the user already confirmed the query
            if (!this.state.needConfirmation) {
                this.handleConfirmed();
            }
        };
        this.generateTagUrl = (key, value) => {
            const { organization } = this.props;
            const { eventView } = this.state;
            const url = eventView.getResultsViewUrlTarget(organization.slug);
            url.query = (0, utils_1.generateQueryWithTag)(url.query, {
                key,
                value,
            });
            return url;
        };
        this.handleIncompatibleQuery = (incompatibleAlertNoticeFn, errors) => {
            const { organization } = this.props;
            const { eventView } = this.state;
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'discover_v2.create_alert_clicked',
                eventName: 'Discoverv2: Create alert clicked',
                status: 'error',
                query: eventView.query,
                errors,
                organization_id: organization.id,
                url: window.location.href,
            });
            const incompatibleAlertNotice = incompatibleAlertNoticeFn(() => this.setState({ incompatibleAlertNotice: null }));
            this.setState({ incompatibleAlertNotice });
        };
        this.setError = (error, errorCode) => {
            this.setState({ error, errorCode });
        };
    }
    static getDerivedStateFromProps(nextProps, prevState) {
        if (nextProps.savedQuery || !nextProps.loading) {
            const eventView = eventView_1.default.fromSavedQueryOrLocation(nextProps.savedQuery, nextProps.location);
            return Object.assign(Object.assign({}, prevState), { eventView, savedQuery: nextProps.savedQuery });
        }
        return prevState;
    }
    componentDidMount() {
        const { organization, selection, location } = this.props;
        (0, tags_1.loadOrganizationTags)(this.tagsApi, organization.slug, selection);
        (0, utils_2.addRoutePerformanceContext)(selection);
        this.checkEventView();
        this.canLoadEvents();
        if ((0, utils_1.defined)(location.query.id)) {
            (0, discoverSavedQueries_1.updateSavedQueryVisit)(organization.slug, location.query.id);
        }
    }
    componentDidUpdate(prevProps, prevState) {
        const { api, location, organization, selection } = this.props;
        const { eventView, confirmedQuery, savedQuery } = this.state;
        this.checkEventView();
        const currentQuery = eventView.getEventsAPIPayload(location);
        const prevQuery = prevState.eventView.getEventsAPIPayload(prevProps.location);
        const yAxisArray = getYAxis(location, eventView, savedQuery);
        const prevYAxisArray = getYAxis(prevProps.location, prevState.eventView, prevState.savedQuery);
        if (!(0, eventView_1.isAPIPayloadSimilar)(currentQuery, prevQuery) ||
            this.hasChartParametersChanged(prevState.eventView, eventView, prevYAxisArray, yAxisArray)) {
            api.clear();
            this.canLoadEvents();
        }
        if (!(0, isEqual_1.default)(prevProps.selection.datetime, selection.datetime) ||
            !(0, isEqual_1.default)(prevProps.selection.projects, selection.projects)) {
            (0, tags_1.loadOrganizationTags)(this.tagsApi, organization.slug, selection);
            (0, utils_2.addRoutePerformanceContext)(selection);
        }
        if (prevState.confirmedQuery !== confirmedQuery)
            this.fetchTotalCount();
    }
    hasChartParametersChanged(prevEventView, eventView, prevYAxisArray, yAxisArray) {
        if (!(0, isEqual_1.default)(prevYAxisArray, yAxisArray)) {
            return true;
        }
        const prevDisplay = prevEventView.getDisplayMode();
        const display = eventView.getDisplayMode();
        return prevDisplay !== display;
    }
    fetchTotalCount() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, organization, location } = this.props;
            const { eventView, confirmedQuery } = this.state;
            if (confirmedQuery === false || !eventView.isValid()) {
                return;
            }
            try {
                const totals = yield (0, events_1.fetchTotalCount)(api, organization.slug, eventView.getEventsAPIPayload(location));
                this.setState({ totalValues: totals });
            }
            catch (err) {
                Sentry.captureException(err);
            }
        });
    }
    checkEventView() {
        var _a;
        const { eventView } = this.state;
        const { loading } = this.props;
        if (eventView.isValid() || loading) {
            return;
        }
        // If the view is not valid, redirect to a known valid state.
        const { location, organization, selection } = this.props;
        const nextEventView = eventView_1.default.fromNewQueryWithLocation(data_1.DEFAULT_EVENT_VIEW, location);
        if (nextEventView.project.length === 0 && selection.projects) {
            nextEventView.project = selection.projects;
        }
        if ((_a = location.query) === null || _a === void 0 ? void 0 : _a.query) {
            nextEventView.query = (0, queryString_1.decodeScalar)(location.query.query, '');
        }
        react_router_1.browserHistory.replace(nextEventView.getResultsViewUrlTarget(organization.slug));
    }
    getDocumentTitle() {
        const { organization } = this.props;
        const { eventView } = this.state;
        if (!eventView) {
            return '';
        }
        return (0, utils_3.generateTitle)({ eventView, organization });
    }
    renderTagsTable() {
        const { organization, location } = this.props;
        const { eventView, totalValues, confirmedQuery } = this.state;
        return (<Layout.Side>
        <tags_2.default generateUrl={this.generateTagUrl} totalValues={totalValues} eventView={eventView} organization={organization} location={location} confirmedQuery={confirmedQuery}/>
      </Layout.Side>);
    }
    renderError(error) {
        if (!error) {
            return null;
        }
        return (<alert_1.default type="error" icon={<icons_1.IconFlag size="md"/>}>
        {error}
      </alert_1.default>);
    }
    render() {
        const { organization, location, router } = this.props;
        const { eventView, error, errorCode, totalValues, showTags, incompatibleAlertNotice, confirmedQuery, savedQuery, } = this.state;
        const fields = eventView.hasAggregateField()
            ? (0, fields_1.generateAggregateFields)(organization, eventView.fields)
            : eventView.fields;
        const query = eventView.query;
        const title = this.getDocumentTitle();
        const yAxisArray = getYAxis(location, eventView, savedQuery);
        return (<sentryDocumentTitle_1.default title={title} orgSlug={organization.slug}>
        <StyledPageContent>
          <noProjectMessage_1.default organization={organization}>
            <resultsHeader_1.default errorCode={errorCode} organization={organization} location={location} eventView={eventView} onIncompatibleAlertQuery={this.handleIncompatibleQuery} yAxis={yAxisArray}/>
            <Layout.Body>
              {incompatibleAlertNotice && <Top fullWidth>{incompatibleAlertNotice}</Top>}
              <Top fullWidth>
                {this.renderError(error)}
                <StyledSearchBar searchSource="eventsv2" organization={organization} projectIds={eventView.project} query={query} fields={fields} onSearch={this.handleSearch} maxQueryLength={constants_1.MAX_QUERY_LENGTH}/>
                <resultsChart_1.default router={router} organization={organization} eventView={eventView} location={location} onAxisChange={this.handleYAxisChange} onDisplayChange={this.handleDisplayChange} onTopEventsChange={this.handleTopEventsChange} total={totalValues} confirmedQuery={confirmedQuery} yAxis={yAxisArray}/>
              </Top>
              <Layout.Main fullWidth={!showTags}>
                <table_1.default organization={organization} eventView={eventView} location={location} title={title} setError={this.setError} onChangeShowTags={this.handleChangeShowTags} showTags={showTags} confirmedQuery={confirmedQuery}/>
              </Layout.Main>
              {showTags ? this.renderTagsTable() : null}
              <confirm_1.default priority="primary" header={<strong>{(0, locale_1.t)('May lead to thumb twiddling')}</strong>} confirmText={(0, locale_1.t)('Do it')} cancelText={(0, locale_1.t)('Nevermind')} onConfirm={this.handleConfirmed} onCancel={this.handleCancelled} message={<p>
                    {(0, locale_1.tct)(`You've created a query that will search for events made
                      [dayLimit:over more than 30 days] for [projectLimit:more than 10 projects].
                      A lot has happened during that time, so this might take awhile.
                      Are you sure you want to do this?`, {
                    dayLimit: <strong />,
                    projectLimit: <strong />,
                })}
                  </p>}>
                {this.setOpenFunction}
              </confirm_1.default>
            </Layout.Body>
          </noProjectMessage_1.default>
        </StyledPageContent>
      </sentryDocumentTitle_1.default>);
    }
}
const StyledPageContent = (0, styled_1.default)(organization_1.PageContent) `
  padding: 0;
`;
const StyledSearchBar = (0, styled_1.default)(searchBar_1.default) `
  margin-bottom: ${(0, space_1.default)(2)};
`;
const Top = (0, styled_1.default)(Layout.Main) `
  flex-grow: 0;
`;
class SavedQueryAPI extends asyncComponent_1.default {
    getEndpoints() {
        const { organization, location } = this.props;
        if (location.query.id) {
            return [
                [
                    'savedQuery',
                    `/organizations/${organization.slug}/discover/saved/${location.query.id}/`,
                ],
            ];
        }
        return [];
    }
    renderLoading() {
        return this.renderBody();
    }
    renderBody() {
        const { savedQuery, loading } = this.state;
        return (<Results {...this.props} savedQuery={savedQuery !== null && savedQuery !== void 0 ? savedQuery : undefined} loading={loading}/>);
    }
}
function ResultsContainer(props) {
    /**
     * Block `<Results>` from mounting until GSH is ready since there are API
     * requests being performed on mount.
     *
     * Also, we skip loading last used projects if you have multiple projects feature as
     * you no longer need to enforce a project if it is empty. We assume an empty project is
     * the desired behavior because saved queries can contain a project filter.
     */
    return (<globalSelectionHeader_1.default skipLoadLastUsed={props.organization.features.includes('global-views')}>
      <SavedQueryAPI {...props}/>
    </globalSelectionHeader_1.default>);
}
exports.default = (0, withApi_1.default)((0, withOrganization_1.default)((0, withGlobalSelection_1.default)(ResultsContainer)));
//# sourceMappingURL=results.jsx.map