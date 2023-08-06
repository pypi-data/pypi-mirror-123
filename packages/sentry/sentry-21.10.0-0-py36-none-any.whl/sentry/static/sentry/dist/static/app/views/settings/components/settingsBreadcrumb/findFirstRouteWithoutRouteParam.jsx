Object.defineProperty(exports, "__esModule", { value: true });
/**
 * For all routes with a `path`, find the first route without a route param (e.g. :apiKey)
 *
 * @param routes A list of react-router route objects
 * @param route If given, will only take into account routes between `route` and end of the routes list
 * @return Object Returns a react-router route object
 */
function findFirstRouteWithoutRouteParam(routes, route) {
    const routeIndex = route !== undefined ? routes.indexOf(route) : -1;
    const routesToSearch = route && routeIndex > -1 ? routes.slice(routeIndex) : routes;
    return (routesToSearch.filter(({ path }) => !!path).find(({ path }) => !(path === null || path === void 0 ? void 0 : path.includes(':'))) ||
        route);
}
exports.default = findFirstRouteWithoutRouteParam;
//# sourceMappingURL=findFirstRouteWithoutRouteParam.jsx.map