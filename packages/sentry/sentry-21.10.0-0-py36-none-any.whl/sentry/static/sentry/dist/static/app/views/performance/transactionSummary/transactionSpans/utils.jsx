Object.defineProperty(exports, "__esModule", { value: true });
exports.spansRouteWithQuery = exports.generateSpansRoute = void 0;
function generateSpansRoute({ orgSlug }) {
    return `/organizations/${orgSlug}/performance/summary/spans/`;
}
exports.generateSpansRoute = generateSpansRoute;
function spansRouteWithQuery({ orgSlug, transaction, projectID, query, }) {
    const pathname = generateSpansRoute({
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
        },
    };
}
exports.spansRouteWithQuery = spansRouteWithQuery;
//# sourceMappingURL=utils.jsx.map