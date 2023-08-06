Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reflux_1 = (0, tslib_1.__importDefault)(require("reflux"));
const organizationsActions_1 = (0, tslib_1.__importDefault)(require("app/actions/organizationsActions"));
const storeConfig = {
    listenables: [organizationsActions_1.default],
    state: [],
    loaded: false,
    // So we can use Reflux.connect in a component mixin
    getInitialState() {
        return this.state;
    },
    init() {
        this.state = [];
        this.loaded = false;
    },
    onUpdate(org) {
        this.add(org);
    },
    onChangeSlug(prev, next) {
        if (prev.slug === next.slug) {
            return;
        }
        this.remove(prev.slug);
        this.add(next);
    },
    onRemoveSuccess(slug) {
        this.remove(slug);
    },
    get(slug) {
        return this.state.find((item) => item.slug === slug);
    },
    getAll() {
        return this.state;
    },
    remove(slug) {
        this.state = this.state.filter(item => slug !== item.slug);
        this.trigger(this.state);
    },
    add(item) {
        let match = false;
        this.state.forEach((existing, idx) => {
            if (existing.id === item.id) {
                item = Object.assign(Object.assign({}, existing), item);
                this.state[idx] = item;
                match = true;
            }
        });
        if (!match) {
            this.state = [...this.state, item];
        }
        this.trigger(this.state);
    },
    load(items) {
        this.state = items;
        this.loaded = true;
        this.trigger(items);
    },
};
const OrganizationsStore = reflux_1.default.createStore(storeConfig);
exports.default = OrganizationsStore;
//# sourceMappingURL=organizationsStore.jsx.map