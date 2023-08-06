Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reflux_1 = (0, tslib_1.__importDefault)(require("reflux"));
const preferencesActions_1 = (0, tslib_1.__importDefault)(require("app/actions/preferencesActions"));
const storeConfig = {
    prefs: {},
    init() {
        this.reset();
        this.listenTo(preferencesActions_1.default.hideSidebar, this.onHideSidebar);
        this.listenTo(preferencesActions_1.default.showSidebar, this.onShowSidebar);
        this.listenTo(preferencesActions_1.default.loadInitialState, this.loadInitialState);
    },
    getInitialState() {
        return this.prefs;
    },
    reset() {
        this.prefs = { collapsed: false };
    },
    loadInitialState(prefs) {
        this.prefs = Object.assign({}, prefs);
        this.trigger(this.prefs);
    },
    onHideSidebar() {
        this.prefs = Object.assign(Object.assign({}, this.prefs), { collapsed: true });
        this.trigger(this.prefs);
    },
    onShowSidebar() {
        this.prefs = Object.assign(Object.assign({}, this.prefs), { collapsed: false });
        this.trigger(this.prefs);
    },
    getState() {
        return this.prefs;
    },
};
/**
 * This store is used to hold local user preferences
 * Side-effects (like reading/writing to cookies) are done in associated actionCreators
 */
const PreferenceStore = reflux_1.default.createStore(storeConfig);
exports.default = PreferenceStore;
//# sourceMappingURL=preferencesStore.jsx.map