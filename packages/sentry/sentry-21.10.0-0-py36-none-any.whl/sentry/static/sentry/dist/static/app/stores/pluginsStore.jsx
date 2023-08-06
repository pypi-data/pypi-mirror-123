Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reflux_1 = (0, tslib_1.__importDefault)(require("reflux"));
const pluginActions_1 = (0, tslib_1.__importDefault)(require("app/actions/pluginActions"));
const defaultState = {
    loading: true,
    plugins: [],
    error: null,
    pageLinks: null,
};
const storeConfig = {
    plugins: null,
    state: Object.assign({}, defaultState),
    updating: new Map(),
    reset() {
        // reset our state
        this.plugins = null;
        this.state = Object.assign({}, defaultState);
        this.updating = new Map();
        return this.state;
    },
    getInitialState() {
        return this.getState();
    },
    getState() {
        const _a = this.state, { plugins: _plugins } = _a, state = (0, tslib_1.__rest)(_a, ["plugins"]);
        return Object.assign(Object.assign({}, state), { plugins: this.plugins ? Array.from(this.plugins.values()) : [] });
    },
    init() {
        this.reset();
        this.listenTo(pluginActions_1.default.fetchAll, this.onFetchAll);
        this.listenTo(pluginActions_1.default.fetchAllSuccess, this.onFetchAllSuccess);
        this.listenTo(pluginActions_1.default.fetchAllError, this.onFetchAllError);
        this.listenTo(pluginActions_1.default.update, this.onUpdate);
        this.listenTo(pluginActions_1.default.updateSuccess, this.onUpdateSuccess);
        this.listenTo(pluginActions_1.default.updateError, this.onUpdateError);
    },
    triggerState() {
        this.trigger(this.getState());
    },
    onFetchAll({ resetLoading } = {}) {
        if (resetLoading) {
            this.state.loading = true;
            this.state.error = null;
            this.plugins = null;
        }
        this.triggerState();
    },
    onFetchAllSuccess(data, { pageLinks }) {
        this.plugins = new Map(data.map(plugin => [plugin.id, plugin]));
        this.state.pageLinks = pageLinks || null;
        this.state.loading = false;
        this.triggerState();
    },
    onFetchAllError(err) {
        this.plugins = null;
        this.state.loading = false;
        this.state.error = err;
        this.triggerState();
    },
    onUpdate(id, updateObj) {
        if (!this.plugins) {
            return;
        }
        const plugin = this.plugins.get(id);
        if (!plugin) {
            return;
        }
        const newPlugin = Object.assign(Object.assign({}, plugin), updateObj);
        this.plugins.set(id, newPlugin);
        this.updating.set(id, plugin);
        this.triggerState();
    },
    onUpdateSuccess(id, _updateObj) {
        this.updating.delete(id);
    },
    onUpdateError(id, _updateObj, err) {
        const origPlugin = this.updating.get(id);
        if (!origPlugin || !this.plugins) {
            return;
        }
        this.plugins.set(id, origPlugin);
        this.updating.delete(id);
        this.state.error = err;
        this.triggerState();
    },
};
const PluginStore = reflux_1.default.createStore(storeConfig);
exports.default = PluginStore;
//# sourceMappingURL=pluginsStore.jsx.map