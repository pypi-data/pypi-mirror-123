Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const moment_timezone_1 = (0, tslib_1.__importDefault)(require("moment-timezone"));
const reflux_1 = (0, tslib_1.__importDefault)(require("reflux"));
const storeConfig = {
    // When the app is booted we will _immediately_ hydrate the config store,
    // effecively ensureing this is not empty.
    config: {},
    init() {
        this.config = {};
    },
    get(key) {
        return this.config[key];
    },
    set(key, value) {
        this.config = Object.assign(Object.assign({}, this.config), { [key]: value });
        this.trigger({ [key]: value });
    },
    /**
     * This is only called by media query listener so that we can control
     * the auto switching of color schemes without affecting manual toggle
     */
    updateTheme(theme) {
        var _a;
        if (((_a = this.config.user) === null || _a === void 0 ? void 0 : _a.options.theme) !== 'system') {
            return;
        }
        this.set('theme', theme);
    },
    loadInitialData(config) {
        var _a;
        const shouldUseDarkMode = ((_a = config.user) === null || _a === void 0 ? void 0 : _a.options.theme) === 'dark';
        this.config = Object.assign(Object.assign({}, config), { features: new Set(config.features || []), theme: shouldUseDarkMode ? 'dark' : 'light' });
        // TODO(dcramer): abstract this out of ConfigStore
        if (config.user) {
            config.user.permissions = new Set(config.user.permissions);
            moment_timezone_1.default.tz.setDefault(config.user.options.timezone);
        }
        this.trigger(config);
    },
    getConfig() {
        return this.config;
    },
    getState() {
        return this.config;
    },
};
const ConfigStore = reflux_1.default.createStore(storeConfig);
exports.default = ConfigStore;
//# sourceMappingURL=configStore.jsx.map