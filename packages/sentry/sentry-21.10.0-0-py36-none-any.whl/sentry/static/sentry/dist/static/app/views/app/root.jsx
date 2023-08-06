Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const constants_1 = require("app/constants");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const useLegacyStore_1 = require("app/stores/useLegacyStore");
const replaceRouterParams_1 = (0, tslib_1.__importDefault)(require("app/utils/replaceRouterParams"));
/**
 * This view is used when a user lands on the route `/` which historically
 * is a server-rendered route which redirects the user to their last selected organization
 *
 * However, this does not work when in the experimental SPA mode (e.g. developing against a remote API,
 * or a deploy preview), so we must replicate the functionality and redirect
 * the user to the proper organization.
 *
 * TODO: There might be an edge case where user does not have `lastOrganization` set,
 * in which case we should load their list of organizations and make a decision
 */
function AppRoot() {
    const config = (0, useLegacyStore_1.useLegacyStore)(configStore_1.default);
    (0, react_1.useEffect)(() => {
        if (!config.lastOrganization) {
            return;
        }
        const orgSlug = config.lastOrganization;
        const url = (0, replaceRouterParams_1.default)(constants_1.DEFAULT_APP_ROUTE, { orgSlug });
        react_router_1.browserHistory.replace(url);
    }, [config]);
    return null;
}
exports.default = AppRoot;
//# sourceMappingURL=root.jsx.map