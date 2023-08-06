Object.defineProperty(exports, "__esModule", { value: true });
exports.fetchSentryAppComponents = void 0;
const tslib_1 = require("tslib");
const sentryAppComponentActions_1 = (0, tslib_1.__importDefault)(require("app/actions/sentryAppComponentActions"));
function fetchSentryAppComponents(api, orgSlug, projectId) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const componentsUri = `/organizations/${orgSlug}/sentry-app-components/?projectId=${projectId}`;
        const res = yield api.requestPromise(componentsUri);
        sentryAppComponentActions_1.default.loadComponents(res);
        return res;
    });
}
exports.fetchSentryAppComponents = fetchSentryAppComponents;
//# sourceMappingURL=sentryAppComponents.jsx.map