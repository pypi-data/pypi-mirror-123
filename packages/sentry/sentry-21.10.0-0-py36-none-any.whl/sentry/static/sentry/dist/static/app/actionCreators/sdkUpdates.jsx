Object.defineProperty(exports, "__esModule", { value: true });
exports.loadSdkUpdates = void 0;
const tslib_1 = require("tslib");
const sdkUpdatesActions_1 = (0, tslib_1.__importDefault)(require("app/actions/sdkUpdatesActions"));
/**
 * Load SDK Updates for a specific organization
 */
function loadSdkUpdates(api, orgSlug) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const updates = yield api.requestPromise(`/organizations/${orgSlug}/sdk-updates/`);
        sdkUpdatesActions_1.default.load(orgSlug, updates);
    });
}
exports.loadSdkUpdates = loadSdkUpdates;
//# sourceMappingURL=sdkUpdates.jsx.map