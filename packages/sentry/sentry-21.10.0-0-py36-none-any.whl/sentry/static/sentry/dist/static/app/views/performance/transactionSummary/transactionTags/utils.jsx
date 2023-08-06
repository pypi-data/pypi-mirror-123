Object.defineProperty(exports, "__esModule", { value: true });
exports.parseHistogramBucketInfo = exports.getTagSortForTagsPage = exports.tagsRouteWithQuery = exports.trackTagPageInteraction = exports.decodeSelectedTagKey = exports.generateTagsRoute = void 0;
const analytics_1 = require("app/utils/analytics");
const queryString_1 = require("app/utils/queryString");
function generateTagsRoute({ orgSlug }) {
    return `/organizations/${orgSlug}/performance/summary/tags/`;
}
exports.generateTagsRoute = generateTagsRoute;
function decodeSelectedTagKey(location) {
    return (0, queryString_1.decodeScalar)(location.query.tagKey);
}
exports.decodeSelectedTagKey = decodeSelectedTagKey;
function trackTagPageInteraction(organization) {
    (0, analytics_1.trackAnalyticsEvent)({
        eventKey: 'performance_views.tags.interaction',
        eventName: 'Performance Views: Tag Page - Interaction',
        organization_id: parseInt(organization.id, 10),
    });
}
exports.trackTagPageInteraction = trackTagPageInteraction;
function tagsRouteWithQuery({ orgSlug, transaction, projectID, query, }) {
    const pathname = generateTagsRoute({
        orgSlug,
    });
    return {
        pathname,
        query: {
            transaction,
            project: projectID,
            environment: query.environment,
            statsPeriod: query.statsPeriod,
            start: query.start,
            end: query.end,
            query: query.query,
            tagKey: query.tagKey,
        },
    };
}
exports.tagsRouteWithQuery = tagsRouteWithQuery;
function getTagSortForTagsPage(location) {
    var _a, _b;
    // Retrieves the tag from the same query param segment explorer uses, but removes columns that aren't supported.
    let tagSort = (_b = (0, queryString_1.decodeScalar)((_a = location.query) === null || _a === void 0 ? void 0 : _a.tagSort)) !== null && _b !== void 0 ? _b : '-frequency';
    if (['sumdelta'].find(denied => tagSort === null || tagSort === void 0 ? void 0 : tagSort.includes(denied))) {
        tagSort = '-frequency';
    }
    return tagSort;
}
exports.getTagSortForTagsPage = getTagSortForTagsPage;
// TODO(k-fish): Improve meta of backend response to return these directly
function parseHistogramBucketInfo(row) {
    const field = Object.keys(row).find(f => f.includes('histogram'));
    if (!field) {
        return undefined;
    }
    const parts = field.split('_');
    return {
        histogramField: field,
        bucketSize: parseInt(parts[parts.length - 3], 10),
        offset: parseInt(parts[parts.length - 2], 10),
        multiplier: parseInt(parts[parts.length - 1], 10),
    };
}
exports.parseHistogramBucketInfo = parseHistogramBucketInfo;
//# sourceMappingURL=utils.jsx.map