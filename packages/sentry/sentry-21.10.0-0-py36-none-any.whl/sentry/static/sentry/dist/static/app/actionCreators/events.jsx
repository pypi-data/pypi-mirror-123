Object.defineProperty(exports, "__esModule", { value: true });
exports.fetchTotalCount = exports.fetchTagFacets = exports.doEventsRequest = void 0;
const tslib_1 = require("tslib");
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const utils_1 = require("app/components/charts/utils");
const getPeriod_1 = require("app/utils/getPeriod");
const constants_1 = require("app/utils/performance/constants");
/**
 * Make requests to `events-stats` endpoint
 *
 * @param {Object} api API client instance
 * @param {Object} options Request parameters
 * @param {Object} options.organization Organization object
 * @param {Number[]} options.project List of project ids
 * @param {String[]} options.environment List of environments to query for
 * @param {String[]} options.team List of teams to query for
 * @param {String} options.period Time period to query for, in the format: <integer><units> where units are "d" or "h"
 * @param {String} options.interval Time interval to group results in, in the format: <integer><units> where units are "d", "h", "m", "s"
 * @param {Number} options.comparisonDelta Comparison delta for change alert event stats to include comparison stats
 * @param {Boolean} options.includePrevious Should request also return reqsults for previous period?
 * @param {Number} options.limit The number of rows to return
 * @param {String} options.query Search query
 */
const doEventsRequest = (api, { organization, project, environment, team, period, start, end, interval, comparisonDelta, includePrevious, query, yAxis, field, topEvents, orderby, partial, withoutZerofill, referrer, }) => {
    const shouldDoublePeriod = (0, utils_1.canIncludePreviousPeriod)(includePrevious, period);
    const urlQuery = Object.fromEntries(Object.entries({
        interval,
        comparisonDelta,
        project,
        environment,
        team,
        query,
        yAxis,
        field,
        topEvents,
        orderby,
        partial: partial ? '1' : undefined,
        withoutZerofill: withoutZerofill ? '1' : undefined,
        referrer: referrer ? referrer : 'api.organization-event-stats',
    }).filter(([, value]) => typeof value !== 'undefined'));
    // Doubling period for absolute dates is not accurate unless starting and
    // ending times are the same (at least for daily intervals). This is
    // the tradeoff for now.
    const periodObj = (0, getPeriod_1.getPeriod)({ period, start, end }, { shouldDoublePeriod });
    return api.requestPromise(`/organizations/${organization.slug}/events-stats/`, {
        query: Object.assign(Object.assign({}, urlQuery), periodObj),
    });
};
exports.doEventsRequest = doEventsRequest;
/**
 * Fetches tag facets for a query
 */
function fetchTagFacets(api, orgSlug, query) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const urlParams = (0, pick_1.default)(query, Object.values(constants_1.PERFORMANCE_URL_PARAM));
        const queryOption = Object.assign(Object.assign({}, urlParams), { query: query.query });
        return api.requestPromise(`/organizations/${orgSlug}/events-facets/`, {
            query: queryOption,
        });
    });
}
exports.fetchTagFacets = fetchTagFacets;
/**
 * Fetches total count of events for a given query
 */
function fetchTotalCount(api, orgSlug, query) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const urlParams = (0, pick_1.default)(query, Object.values(constants_1.PERFORMANCE_URL_PARAM));
        const queryOption = Object.assign(Object.assign({}, urlParams), { query: query.query });
        return api
            .requestPromise(`/organizations/${orgSlug}/events-meta/`, {
            query: queryOption,
        })
            .then((res) => res.count);
    });
}
exports.fetchTotalCount = fetchTotalCount;
//# sourceMappingURL=events.jsx.map