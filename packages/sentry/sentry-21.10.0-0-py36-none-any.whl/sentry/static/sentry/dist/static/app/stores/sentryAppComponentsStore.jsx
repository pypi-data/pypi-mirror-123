Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reflux_1 = (0, tslib_1.__importDefault)(require("reflux"));
const sentryAppComponentActions_1 = (0, tslib_1.__importDefault)(require("app/actions/sentryAppComponentActions"));
const storeConfig = {
    init() {
        this.items = [];
        this.listenTo(sentryAppComponentActions_1.default.loadComponents, this.onLoadComponents);
    },
    getInitialState() {
        return this.items;
    },
    onLoadComponents(items) {
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
    getComponentByType(type) {
        if (!type) {
            return this.getAll();
        }
        const items = this.items;
        return items.filter(item => item.type === type);
    },
};
const SentryAppComponentsStore = reflux_1.default.createStore(storeConfig);
exports.default = SentryAppComponentsStore;
//# sourceMappingURL=sentryAppComponentsStore.jsx.map