Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const notFound_1 = (0, tslib_1.__importDefault)(require("app/components/errors/notFound"));
const eventOrGroupTitle_1 = (0, tslib_1.__importDefault)(require("app/components/eventOrGroupTitle"));
const eventEntries_1 = require("app/components/events/eventEntries");
const eventMessage_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventMessage"));
const eventVitals_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventVitals"));
const SpanEntryContext = (0, tslib_1.__importStar)(require("app/components/events/interfaces/spans/context"));
const fileSize_1 = (0, tslib_1.__importDefault)(require("app/components/fileSize"));
const Layout = (0, tslib_1.__importStar)(require("app/components/layouts/thirds"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const sentryDocumentTitle_1 = (0, tslib_1.__importDefault)(require("app/components/sentryDocumentTitle"));
const tagsTable_1 = (0, tslib_1.__importDefault)(require("app/components/tagsTable"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const fields_1 = require("app/utils/discover/fields");
const urls_1 = require("app/utils/discover/urls");
const events_1 = require("app/utils/events");
const QuickTraceContext = (0, tslib_1.__importStar)(require("app/utils/performance/quickTrace/quickTraceContext"));
const quickTraceQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/performance/quickTrace/quickTraceQuery"));
const traceMetaQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/performance/quickTrace/traceMetaQuery"));
const utils_1 = require("app/utils/performance/quickTrace/utils");
const projects_1 = (0, tslib_1.__importDefault)(require("app/utils/projects"));
const eventMetas_1 = (0, tslib_1.__importDefault)(require("app/views/performance/transactionDetails/eventMetas"));
const utils_2 = require("app/views/performance/transactionSummary/utils");
const breadcrumb_1 = (0, tslib_1.__importDefault)(require("../breadcrumb"));
const utils_3 = require("../utils");
const linkedIssue_1 = (0, tslib_1.__importDefault)(require("./linkedIssue"));
/**
 * Some tag keys should never be formatted as `tag[...]`
 * when used as a filter because they are predefined.
 */
const EXCLUDED_TAG_KEYS = new Set(['release']);
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
        this.generateTagKey = (tag) => {
            // Some tags may be normalized from context, but not all of them are.
            // This supports a user making a custom tag with the same name as one
            // that comes from context as all of these are also tags.
            if (tag.key in fields_1.FIELD_TAGS && !EXCLUDED_TAG_KEYS.has(tag.key)) {
                return `tags[${tag.key}]`;
            }
            return tag.key;
        };
        this.generateTagUrl = (tag) => {
            const { eventView, organization } = this.props;
            const { event } = this.state;
            if (!event) {
                return '';
            }
            const eventReference = Object.assign({}, event);
            if (eventReference.id) {
                delete eventReference.id;
            }
            const tagKey = this.generateTagKey(tag);
            const nextView = (0, utils_3.getExpandedResults)(eventView, { [tagKey]: tag.value }, eventReference);
            return nextView.getResultsViewUrlTarget(organization.slug);
        };
        this.getEventSlug = () => {
            const { eventSlug } = this.props.params;
            if (typeof eventSlug === 'string') {
                return eventSlug.trim();
            }
            return '';
        };
    }
    getEndpoints() {
        const { organization, params, location, eventView } = this.props;
        const { eventSlug } = params;
        const query = eventView.getEventsAPIPayload(location);
        // Fields aren't used, reduce complexity by omitting from query entirely
        query.field = [];
        const url = `/organizations/${organization.slug}/events/${eventSlug}/`;
        // Get a specific event. This could be coming from
        // a paginated group or standalone event.
        return [['event', url, { query }]];
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
        var _a, _b, _c, _d;
        const { organization, location, eventView, route, router } = this.props;
        const { isSidebarVisible } = this.state;
        // metrics
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey: 'discover_v2.event_details',
            eventName: 'Discoverv2: Opened Event Details',
            event_type: event.type,
            organization_id: parseInt(organization.id, 10),
        });
        const transactionName = (_a = event.tags.find(tag => tag.key === 'transaction')) === null || _a === void 0 ? void 0 : _a.value;
        const transactionSummaryTarget = event.type === 'transaction' && transactionName
            ? (0, utils_2.transactionSummaryRouteWithQuery)({
                orgSlug: organization.slug,
                transaction: transactionName,
                projectID: event.projectID,
                query: location.query,
            })
            : null;
        const eventJsonUrl = `/api/0/projects/${organization.slug}/${this.projectId}/events/${event.eventID}/json/`;
        const renderContent = (results, metaResults) => {
            var _a;
            return (<react_1.Fragment>
        <Layout.Header>
          <Layout.HeaderContent>
            <breadcrumb_1.default eventView={eventView} event={event} organization={organization} location={location}/>
            <EventHeader event={event}/>
          </Layout.HeaderContent>
          <Layout.HeaderActions>
            <buttonBar_1.default gap={1}>
              <button_1.default onClick={this.toggleSidebar}>
                {isSidebarVisible ? 'Hide Details' : 'Show Details'}
              </button_1.default>
              <button_1.default icon={<icons_1.IconOpen />} href={eventJsonUrl} external>
                {(0, locale_1.t)('JSON')} (<fileSize_1.default bytes={event.size}/>)
              </button_1.default>
              {transactionSummaryTarget && (<feature_1.default organization={organization} features={['performance-view']}>
                  {({ hasFeature }) => (<button_1.default disabled={!hasFeature} priority="primary" to={transactionSummaryTarget}>
                      {(0, locale_1.t)('Go to Summary')}
                    </button_1.default>)}
                </feature_1.default>)}
            </buttonBar_1.default>
          </Layout.HeaderActions>
        </Layout.Header>
        <Layout.Body>
          <Layout.Main fullWidth>
            <eventMetas_1.default quickTrace={results !== null && results !== void 0 ? results : null} meta={(_a = metaResults === null || metaResults === void 0 ? void 0 : metaResults.meta) !== null && _a !== void 0 ? _a : null} event={event} organization={organization} projectId={this.projectId} location={location} errorDest="discover" transactionDest="discover"/>
          </Layout.Main>
          <Layout.Main fullWidth={!isSidebarVisible}>
            <projects_1.default orgId={organization.slug} slugs={[this.projectId]}>
              {({ projects, initiallyLoaded }) => initiallyLoaded ? (<SpanEntryContext.Provider value={{
                        getViewChildTransactionTarget: childTransactionProps => {
                            const childTransactionLink = (0, urls_1.eventDetailsRoute)({
                                eventSlug: childTransactionProps.eventSlug,
                                orgSlug: organization.slug,
                            });
                            return {
                                pathname: childTransactionLink,
                                query: eventView.generateQueryStringObject(),
                            };
                        },
                    }}>
                    <QuickTraceContext.Provider value={results}>
                      <eventEntries_1.BorderlessEventEntries organization={organization} event={event} project={projects[0]} location={location} showExampleCommit={false} showTagSummary={false} api={this.api} router={router} route={route} isBorderless/>
                    </QuickTraceContext.Provider>
                  </SpanEntryContext.Provider>) : (<loadingIndicator_1.default />)}
            </projects_1.default>
          </Layout.Main>
          {isSidebarVisible && (<Layout.Side>
              <eventVitals_1.default event={event}/>
              {event.groupID && (<linkedIssue_1.default groupId={event.groupID} eventId={event.eventID}/>)}
              <tagsTable_1.default generateUrl={this.generateTagUrl} event={event} query={eventView.query}/>
            </Layout.Side>)}
        </Layout.Body>
      </react_1.Fragment>);
        };
        const hasQuickTraceView = organization.features.includes('performance-view');
        if (hasQuickTraceView) {
            const traceId = (_d = (_c = (_b = event.contexts) === null || _b === void 0 ? void 0 : _b.trace) === null || _c === void 0 ? void 0 : _c.trace_id) !== null && _d !== void 0 ? _d : '';
            const { start, end } = (0, utils_1.getTraceTimeRangeFromEvent)(event);
            return (<traceMetaQuery_1.default location={location} orgSlug={organization.slug} traceId={traceId} start={start} end={end}>
          {metaResults => (<quickTraceQuery_1.default event={event} location={location} orgSlug={organization.slug}>
              {results => renderContent(results, metaResults)}
            </quickTraceQuery_1.default>)}
        </traceMetaQuery_1.default>);
        }
        return renderContent();
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
        const { eventView, organization } = this.props;
        const { event } = this.state;
        const eventSlug = this.getEventSlug();
        const projectSlug = eventSlug.split(':')[0];
        const title = (0, utils_3.generateTitle)({ eventView, event, organization });
        return (<sentryDocumentTitle_1.default title={title} orgSlug={organization.slug} projectSlug={projectSlug}>
        {super.renderComponent()}
      </sentryDocumentTitle_1.default>);
    }
}
const EventHeader = ({ event }) => {
    const message = (0, events_1.getMessage)(event);
    return (<EventHeaderContainer data-test-id="event-header">
      <TitleWrapper>
        <eventOrGroupTitle_1.default data={event}/>
      </TitleWrapper>
      {message && (<MessageWrapper>
          <eventMessage_1.default message={message}/>
        </MessageWrapper>)}
    </EventHeaderContainer>);
};
const EventHeaderContainer = (0, styled_1.default)('div') `
  max-width: ${p => p.theme.breakpoints[0]};
`;
const TitleWrapper = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.headerFontSize};
  margin-top: 20px;
`;
const MessageWrapper = (0, styled_1.default)('div') `
  margin-top: ${(0, space_1.default)(1)};
`;
exports.default = EventDetailsContent;
//# sourceMappingURL=content.jsx.map