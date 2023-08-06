Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const locale_1 = require("app/locale");
const analytics_1 = require("app/utils/analytics");
const eventView_1 = require("app/utils/discover/eventView");
const measurements_1 = (0, tslib_1.__importDefault)(require("app/utils/measurements/measurements"));
const parseLinkHeader_1 = (0, tslib_1.__importDefault)(require("app/utils/parseLinkHeader"));
const constants_1 = require("app/utils/performance/spanOperationBreakdowns/constants");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withTags_1 = (0, tslib_1.__importDefault)(require("app/utils/withTags"));
const tableView_1 = (0, tslib_1.__importDefault)(require("./tableView"));
/**
 * `Table` is a container element that handles 2 things
 * 1. Fetch data from source
 * 2. Handle pagination of data
 *
 * It will pass the data it fetched to `TableView`, where the state of the
 * Table is maintained and controlled
 */
class Table extends react_1.PureComponent {
    constructor() {
        super(...arguments);
        this.state = {
            isLoading: true,
            tableFetchID: undefined,
            error: null,
            pageLinks: null,
            tableData: null,
        };
        this.shouldRefetchData = (prevProps) => {
            const thisAPIPayload = this.props.eventView.getEventsAPIPayload(this.props.location);
            const otherAPIPayload = prevProps.eventView.getEventsAPIPayload(prevProps.location);
            return !(0, eventView_1.isAPIPayloadSimilar)(thisAPIPayload, otherAPIPayload);
        };
        this.fetchData = () => {
            const { eventView, organization, location, setError, confirmedQuery } = this.props;
            if (!eventView.isValid() || !confirmedQuery) {
                return;
            }
            // note: If the eventView has no aggregates, the endpoint will automatically add the event id in
            // the API payload response
            const url = `/organizations/${organization.slug}/eventsv2/`;
            const tableFetchID = Symbol('tableFetchID');
            const apiPayload = eventView.getEventsAPIPayload(location);
            apiPayload.referrer = 'api.discover.query-table';
            setError('', 200);
            this.setState({ isLoading: true, tableFetchID });
            analytics_1.metric.mark({ name: `discover-events-start-${apiPayload.query}` });
            this.props.api.clear();
            this.props.api
                .requestPromise(url, {
                method: 'GET',
                includeAllArgs: true,
                query: apiPayload,
            })
                .then(([data, _, resp]) => {
                // We want to measure this metric regardless of whether we use the result
                analytics_1.metric.measure({
                    name: 'app.api.discover-query',
                    start: `discover-events-start-${apiPayload.query}`,
                    data: {
                        status: resp && resp.status,
                    },
                });
                if (this.state.tableFetchID !== tableFetchID) {
                    // invariant: a different request was initiated after this request
                    return;
                }
                this.setState(prevState => ({
                    isLoading: false,
                    tableFetchID: undefined,
                    error: null,
                    pageLinks: resp ? resp.getResponseHeader('Link') : prevState.pageLinks,
                    tableData: data,
                }));
            })
                .catch(err => {
                var _a;
                analytics_1.metric.measure({
                    name: 'app.api.discover-query',
                    start: `discover-events-start-${apiPayload.query}`,
                    data: {
                        status: err.status,
                    },
                });
                const message = ((_a = err === null || err === void 0 ? void 0 : err.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) || (0, locale_1.t)('An unknown error occurred.');
                this.setState({
                    isLoading: false,
                    tableFetchID: undefined,
                    error: message,
                    pageLinks: null,
                    tableData: null,
                });
                (0, analytics_1.trackAnalyticsEvent)({
                    eventKey: 'discover_search.failed',
                    eventName: 'Discover Search: Failed',
                    organization_id: this.props.organization.id,
                    search_type: 'events',
                    search_source: 'discover_search',
                    error: message,
                });
                setError(message, err.status);
            });
        };
    }
    componentDidMount() {
        this.fetchData();
    }
    componentDidUpdate(prevProps) {
        // Reload data if we aren't already loading, or if we've moved
        // from an invalid view state to a valid one.
        if ((!this.state.isLoading && this.shouldRefetchData(prevProps)) ||
            (prevProps.eventView.isValid() === false && this.props.eventView.isValid()) ||
            prevProps.confirmedQuery !== this.props.confirmedQuery) {
            this.fetchData();
        }
    }
    render() {
        const { eventView, organization, tags } = this.props;
        const { pageLinks, tableData, isLoading, error } = this.state;
        const tagKeys = Object.values(tags).map(({ key }) => key);
        const isFirstPage = pageLinks
            ? (0, parseLinkHeader_1.default)(pageLinks).previous.results === false
            : false;
        return (<Container>
        <measurements_1.default organization={organization}>
          {({ measurements }) => {
                const measurementKeys = Object.values(measurements).map(({ key }) => key);
                return (<tableView_1.default {...this.props} isLoading={isLoading} isFirstPage={isFirstPage} error={error} eventView={eventView} tableData={tableData} tagKeys={tagKeys} measurementKeys={measurementKeys} spanOperationBreakdownKeys={constants_1.SPAN_OP_BREAKDOWN_FIELDS}/>);
            }}
        </measurements_1.default>
        <pagination_1.default pageLinks={pageLinks}/>
      </Container>);
    }
}
exports.default = (0, withApi_1.default)((0, withTags_1.default)(Table));
const Container = (0, styled_1.default)('div') `
  min-width: 0;
`;
//# sourceMappingURL=index.jsx.map