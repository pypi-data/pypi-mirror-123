Object.defineProperty(exports, "__esModule", { value: true });
exports.getDisplayName = exports.getUrlRoutingName = void 0;
const DEFAULT_EMPTY_ROUTING_NAME = 'none';
const DEFAULT_EMPTY_ENV_NAME = '(No Environment)';
function getUrlRoutingName(env) {
    if (env.name) {
        return encodeURIComponent(env.name);
    }
    if (env.displayName) {
        return encodeURIComponent(env.displayName);
    }
    return DEFAULT_EMPTY_ROUTING_NAME;
}
exports.getUrlRoutingName = getUrlRoutingName;
function getDisplayName(env) {
    return env.name || env.displayName || DEFAULT_EMPTY_ENV_NAME;
}
exports.getDisplayName = getDisplayName;
//# sourceMappingURL=environment.jsx.map