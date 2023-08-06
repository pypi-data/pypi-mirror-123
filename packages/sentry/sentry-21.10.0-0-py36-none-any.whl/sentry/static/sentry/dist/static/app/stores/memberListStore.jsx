Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reflux_1 = (0, tslib_1.__importDefault)(require("reflux"));
const storeConfig = {
    // listenables: MemberActions,
    loaded: false,
    state: [],
    init() {
        this.state = [];
        this.loaded = false;
    },
    // TODO(dcramer): this should actually come from an action of some sorts
    loadInitialData(items) {
        this.state = items;
        this.loaded = true;
        this.trigger(this.state, 'initial');
    },
    isLoaded() {
        return this.loaded;
    },
    getById(id) {
        if (!this.state) {
            return undefined;
        }
        id = '' + id;
        for (let i = 0; i < this.state.length; i++) {
            if (this.state[i].id === id) {
                return this.state[i];
            }
        }
        return undefined;
    },
    getByEmail(email) {
        if (!this.state) {
            return undefined;
        }
        email = email.toLowerCase();
        for (let i = 0; i < this.state.length; i++) {
            if (this.state[i].email.toLowerCase() === email) {
                return this.state[i];
            }
        }
        return undefined;
    },
    getAll() {
        return this.state;
    },
};
const MemberListStore = reflux_1.default.createStore(storeConfig);
exports.default = MemberListStore;
//# sourceMappingURL=memberListStore.jsx.map