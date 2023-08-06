Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const isUndefined_1 = (0, tslib_1.__importDefault)(require("lodash/isUndefined"));
const reflux_1 = (0, tslib_1.__importDefault)(require("reflux"));
const storeConfig = {
    hooks: {},
    init() {
        this.hooks = {};
    },
    add(hookName, callback) {
        if ((0, isUndefined_1.default)(this.hooks[hookName])) {
            this.hooks[hookName] = [];
        }
        this.hooks[hookName].push(callback);
        this.trigger(hookName, this.hooks[hookName]);
    },
    remove(hookName, callback) {
        if ((0, isUndefined_1.default)(this.hooks[hookName])) {
            return;
        }
        this.hooks[hookName] = this.hooks[hookName].filter(cb => cb !== callback);
        this.trigger(hookName, this.hooks[hookName]);
    },
    get(hookName) {
        return this.hooks[hookName] || [];
    },
};
/**
 * HookStore is used to allow extensibility into Sentry's frontend via
 * registration of 'hook functions'.
 *
 * This functionality is primarily used by the SASS sentry.io product.
 */
const HookStore = reflux_1.default.createStore(storeConfig);
exports.default = HookStore;
//# sourceMappingURL=hookStore.jsx.map