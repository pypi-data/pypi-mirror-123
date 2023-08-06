Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reflux_1 = (0, tslib_1.__importDefault)(require("reflux"));
const storeConfig = {
    init() {
        this.items = [];
    },
    getInitialState() {
        return this.items;
    },
    load(items) {
        this.items = items;
        this.trigger(items);
    },
    get(uuid) {
        const items = this.items;
        return items.find(item => item.uuid === uuid);
    },
    getAll() {
        return this.items;
    },
};
const SentryAppInstallationStore = reflux_1.default.createStore(storeConfig);
exports.default = SentryAppInstallationStore;
//# sourceMappingURL=sentryAppInstallationsStore.jsx.map