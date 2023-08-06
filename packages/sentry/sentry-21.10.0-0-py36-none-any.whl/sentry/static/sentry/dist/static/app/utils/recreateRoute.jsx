Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const findLastIndex_1 = (0, tslib_1.__importDefault)(require("lodash/findLastIndex"));
const replaceRouterParams_1 = (0, tslib_1.__importDefault)(require("app/utils/replaceRouterParams"));
/**
 * Given a route object or a string and a list of routes + params from router, this will attempt to recreate a location string while replacing url params.
 * Can additionally specify the number of routes to move back
 *
 * See tests for examples
 */
function recreateRoute(to, options) {
    var _a, _b;
    const { routes, params, location, stepBack } = options;
    const paths = routes.map(({ path }) => path || '');
    let lastRootIndex;
    let routeIndex;
    // TODO(ts): typescript things
    if (typeof to !== 'string') {
        routeIndex = routes.indexOf(to) + 1;
        lastRootIndex = (0, findLastIndex_1.default)(paths.slice(0, routeIndex), path => path[0] === '/');
    }
    else {
        lastRootIndex = (0, findLastIndex_1.default)(paths, path => path[0] === '/');
    }
    let baseRoute = paths.slice(lastRootIndex, routeIndex);
    if (typeof stepBack !== 'undefined') {
        baseRoute = baseRoute.slice(0, stepBack);
    }
    const search = (_a = location === null || location === void 0 ? void 0 : location.search) !== null && _a !== void 0 ? _a : '';
    const hash = (_b = location === null || location === void 0 ? void 0 : location.hash) !== null && _b !== void 0 ? _b : '';
    const fullRoute = `${baseRoute.join('')}${typeof to !== 'string' ? '' : to}${search}${hash}`;
    return (0, replaceRouterParams_1.default)(fullRoute, params);
}
exports.default = recreateRoute;
//# sourceMappingURL=recreateRoute.jsx.map