Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reflux_1 = (0, tslib_1.__importDefault)(require("reflux"));
const sdkUpdatesActions_1 = (0, tslib_1.__importDefault)(require("app/actions/sdkUpdatesActions"));
const storeConfig = {
    orgSdkUpdates: new Map(),
    init() {
        this.listenTo(sdkUpdatesActions_1.default.load, this.onLoadSuccess);
    },
    onLoadSuccess(orgSlug, data) {
        this.orgSdkUpdates.set(orgSlug, data);
        this.trigger(this.orgSdkUpdates);
    },
    getUpdates(orgSlug) {
        return this.orgSdkUpdates.get(orgSlug);
    },
    isSdkUpdatesLoaded(orgSlug) {
        return this.orgSdkUpdates.has(orgSlug);
    },
};
const SdkUpdatesStore = reflux_1.default.createStore(storeConfig);
exports.default = SdkUpdatesStore;
//# sourceMappingURL=sdkUpdatesStore.jsx.map