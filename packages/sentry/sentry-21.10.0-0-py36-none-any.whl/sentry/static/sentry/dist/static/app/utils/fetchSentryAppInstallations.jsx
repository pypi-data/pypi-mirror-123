Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const sentryAppInstallationsStore_1 = (0, tslib_1.__importDefault)(require("app/stores/sentryAppInstallationsStore"));
const fetchSentryAppInstallations = (api, orgSlug) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
    const installsUri = `/organizations/${orgSlug}/sentry-app-installations/`;
    const installs = yield api.requestPromise(installsUri);
    sentryAppInstallationsStore_1.default.load(installs);
});
exports.default = fetchSentryAppInstallations;
//# sourceMappingURL=fetchSentryAppInstallations.jsx.map