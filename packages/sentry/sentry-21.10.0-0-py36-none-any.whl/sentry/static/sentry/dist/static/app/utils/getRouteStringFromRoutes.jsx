Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const findLastIndex_1 = (0, tslib_1.__importDefault)(require("lodash/findLastIndex"));
/**
 * Creates a route string from an array of `routes` from react-router
 *
 * It will look for the last route path that begins with a `/` and
 * concatenate all of the following routes. Skips any routes without a path
 *
 * @param {Array<{}>} routes An array of route objects from react-router
 * @return String Returns a route path
 */
function getRouteStringFromRoutes(routes) {
    if (!Array.isArray(routes)) {
        return '';
    }
    const routesWithPaths = routes.filter((route) => !!route.path);
    const lastAbsolutePathIndex = (0, findLastIndex_1.default)(routesWithPaths, ({ path }) => path.startsWith('/'));
    return routesWithPaths
        .slice(lastAbsolutePathIndex)
        .filter(({ path }) => !!path)
        .map(({ path }) => path)
        .join('');
}
exports.default = getRouteStringFromRoutes;
//# sourceMappingURL=getRouteStringFromRoutes.jsx.map