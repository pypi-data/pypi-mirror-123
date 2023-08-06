Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const notFound_1 = (0, tslib_1.__importDefault)(require("app/components/errors/notFound"));
const eventEntries_1 = require("app/components/events/eventEntries");
const eventMetadata_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventMetadata"));
const eventVitals_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventVitals"));
const SpanEntryContext = (0, tslib_1.__importStar)(require("app/components/events/interfaces/spans/context"));
const rootSpanStatus_1 = (0, tslib_1.__importDefault)(require("app/components/events/rootSpanStatus"));
const fileSize_1 = (0, tslib_1.__importDefault)(require("app/components/fileSize"));
const Layout = (0, tslib_1.__importStar)(require("app/components/layouts/thirds"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const sentryDocumentTitle_1 = (0, tslib_1.__importDefault)(require("app/components/sentryDocumentTitle"));
const tagsTable_1 = (0, tslib_1.__importDefault)(require("app/components/tagsTable"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const analytics_1 = require("app/utils/analytics");
const QuickTraceContext = (0, tslib_1.__importStar)(require("app/utils/performance/quickTrace/quickTraceContext"));
const quickTraceQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/performance/quickTrace/quickTraceQuery"));
const traceMetaQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/performance/quickTrace/traceMetaQuery"));
const utils_1 = require("app/utils/performance/quickTrace/utils");
const projects_1 = (0, tslib_1.__importDefault)(require("app/utils/projects"));
const queryString_1 = require("app/utils/queryString");
const breadcrumb_1 = (0, tslib_1.__importDefault)(require("app/views/performance/breadcrumb"));
const utils_2 = require("../transactionSummary/utils");
const utils_3 = require("../utils");
const eventMetas_1 = (0, tslib_1.__importDefault)(require("./eventMetas"));
class EventDetailsContent extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.state = {
            // AsyncComponent state
            loading: true,
            reloading: false,
            error: false,
            errors: {},
            event: undefined,
            // local state
            isSidebarVisible: true,
        };
        this.toggleSidebar = () => {
            this.setState({ isSidebarVisible: !this.state.isSidebarVisible });
        };
        this.generateTagUrl = (tag) => {
            const { location, organization } = this.props;
            const { event } = this.state;
            if (!event) {
                return '';
            }
            const query = (0, queryString_1.decodeScalar)(location.query.query, '');
            const newQuery = Object.assign(Object.assign({}, location.query), { query: (0, queryString_1.appendTagCondition)(query, tag.key, tag.value) });
            return (0, utils_2.transactionSummaryRouteWithQuery)({
                orgSlug: organization.slug,
                transaction: event.title,
                projectID: event.projectID,
                query: newQuery,
            });
        };
    }
    getEndpoints() {
        const { organization, params } = this.props;
        const { eventSlug } = params;
        const url = `/organizations/${organization.slug}/events/${eventSlug}/`;
        return [['event', url]];
    }
    get projectId() {
        return this.props.eventSlug.split(':')[0];
    }
    renderBody() {
        const { event } = this.state;
        if (!event) {
            return <notFound_1.default />;
        }
        return this.renderContent(event);
    }
    renderContent(event) {
        var _a, _b, _c;
        const { organization, location, eventSlug, route, router } = this.props;
        // metrics
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey: 'performance.event_details',
            eventName: 'Performance: Opened Event Details',
            event_type: event.type,
            organization_id: parseInt(organization.id, 10),
        });
        const { isSidebarVisible } = this.state;
        const transactionName = event.title;
        const query = (0, queryString_1.decodeScalar)(location.query.query, '');
        const eventJsonUrl = `/api/0/projects/${organization.slug}/${this.projectId}/events/${event.eventID}/json/`;
        const traceId = (_c = (_b = (_a = event.contexts) === null || _a === void 0 ? void 0 : _a.trace) === null || _b === void 0 ? void 0 : _b.trace_id) !== null && _c !== void 0 ? _c : '';
        const { start, end } = (0, utils_1.getTraceTimeRangeFromEvent)(event);
        return (<traceMetaQuery_1.default location={location} orgSlug={organization.slug} traceId={traceId} start={start} end={end}>
        {metaResults => (<quickTraceQuery_1.default event={event} location={location} orgSlug={organization.slug}>
            {results => {
                    var _a;
                    return (<react_1.Fragment>
                <Layout.Header>
                  <Layout.HeaderContent>
                    <breadcrumb_1.default organization={organization} location={location} transaction={{
                            project: event.projectID,
                            name: transactionName,
                        }} eventSlug={eventSlug}/>
                    <Layout.Title data-test-id="event-header">{event.title}</Layout.Title>
                  </Layout.HeaderContent>
                  <Layout.HeaderActions>
                    <buttonBar_1.default gap={1}>
                      <button_1.default onClick={this.toggleSidebar}>
                        {isSidebarVisible ? 'Hide Details' : 'Show Details'}
                      </button_1.default>
                      {results && (<button_1.default icon={<icons_1.IconOpen />} href={eventJsonUrl} external>
                          {(0, locale_1.t)('JSON')} (<fileSize_1.default bytes={event.size}/>)
                        </button_1.default>)}
                    </buttonBar_1.default>
                  </Layout.HeaderActions>
                </Layout.Header>
                <Layout.Body>
                  {results && (<Layout.Main fullWidth>
                      <eventMetas_1.default quickTrace={results} meta={(_a = metaResults === null || metaResults === void 0 ? void 0 : metaResults.meta) !== null && _a !== void 0 ? _a : null} event={event} organization={organization} projectId={this.projectId} location={location} errorDest="issue" transactionDest="performance"/>
                    </Layout.Main>)}
                  <Layout.Main fullWidth={!isSidebarVisible}>
                    <projects_1.default orgId={organization.slug} slugs={[this.projectId]}>
                      {({ projects }) => (<SpanEntryContext.Provider value={{
                                getViewChildTransactionTarget: childTransactionProps => {
                                    return (0, utils_3.getTransactionDetailsUrl)(organization, childTransactionProps.eventSlug, childTransactionProps.transaction, location.query);
                                },
                            }}>
                          <QuickTraceContext.Provider value={results}>
                            <eventEntries_1.BorderlessEventEntries organization={organization} event={event} project={projects[0]} showExampleCommit={false} showTagSummary={false} location={location} api={this.api} router={router} route={route} isBorderless/>
                          </QuickTraceContext.Provider>
                        </SpanEntryContext.Provider>)}
                    </projects_1.default>
                  </Layout.Main>
                  {isSidebarVisible && (<Layout.Side>
                      {results === undefined && (<react_1.Fragment>
                          <eventMetadata_1.default event={event} organization={organization} projectId={this.projectId}/>
                          <rootSpanStatus_1.default event={event}/>
                        </react_1.Fragment>)}
                      <eventVitals_1.default event={event}/>
                      <tagsTable_1.default event={event} query={query} generateUrl={this.generateTagUrl}/>
                    </Layout.Side>)}
                </Layout.Body>
              </react_1.Fragment>);
                }}
          </quickTraceQuery_1.default>)}
      </traceMetaQuery_1.default>);
    }
    renderError(error) {
        const notFound = Object.values(this.state.errors).find(resp => resp && resp.status === 404);
        const permissionDenied = Object.values(this.state.errors).find(resp => resp && resp.status === 403);
        if (notFound) {
            return <notFound_1.default />;
        }
        if (permissionDenied) {
            return (<loadingError_1.default message={(0, locale_1.t)('You do not have permission to view that event.')}/>);
        }
        return super.renderError(error, true, true);
    }
    renderComponent() {
        const { organization } = this.props;
        return (<sentryDocumentTitle_1.default title={(0, locale_1.t)('Performance - Event Details')} orgSlug={organization.slug}>
        {super.renderComponent()}
      </sentryDocumentTitle_1.default>);
    }
}
exports.default = EventDetailsContent;
//# sourceMappingURL=content.jsx.map