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
    get(id) {
        return this.items.find((item) => item.id === id);
    },
    getAll() {
        return this.items;
    },
    add(issue) {
        if (!this.items.some(i => i.id === issue.id)) {
            this.items = this.items.concat([issue]);
            this.trigger(this.items);
        }
    },
};
const ExternalIssueStore = reflux_1.default.createStore(storeConfig);
exports.default = ExternalIssueStore;
//# sourceMappingURL=externalIssueStore.jsx.map