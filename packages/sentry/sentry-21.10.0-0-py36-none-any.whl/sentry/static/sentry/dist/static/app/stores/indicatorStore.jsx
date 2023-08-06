Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reflux_1 = (0, tslib_1.__importDefault)(require("reflux"));
const indicatorActions_1 = (0, tslib_1.__importDefault)(require("app/actions/indicatorActions"));
const locale_1 = require("app/locale");
const storeConfig = {
    items: [],
    lastId: 0,
    init() {
        this.items = [];
        this.lastId = 0;
        this.listenTo(indicatorActions_1.default.append, this.append);
        this.listenTo(indicatorActions_1.default.replace, this.add);
        this.listenTo(indicatorActions_1.default.remove, this.remove);
        this.listenTo(indicatorActions_1.default.clear, this.clear);
    },
    addSuccess(message) {
        return this.add(message, 'success', { duration: 2000 });
    },
    addError(message = (0, locale_1.t)('An error occurred')) {
        return this.add(message, 'error', { duration: 2000 });
    },
    addMessage(message, type, _a = {}) {
        var { append } = _a, options = (0, tslib_1.__rest)(_a, ["append"]);
        const indicator = {
            id: this.lastId++,
            message,
            type,
            options,
            clearId: null,
        };
        if (options.duration) {
            indicator.clearId = window.setTimeout(() => {
                this.remove(indicator);
            }, options.duration);
        }
        const newItems = append ? [...this.items, indicator] : [indicator];
        this.items = newItems;
        this.trigger(this.items);
        return indicator;
    },
    append(message, type, options) {
        return this.addMessage(message, type, Object.assign(Object.assign({}, options), { append: true }));
    },
    add(message, type = 'loading', options = {}) {
        return this.addMessage(message, type, Object.assign(Object.assign({}, options), { append: false }));
    },
    clear() {
        this.items = [];
        this.trigger(this.items);
    },
    remove(indicator) {
        if (!indicator) {
            return;
        }
        this.items = this.items.filter(item => item !== indicator);
        if (indicator.clearId) {
            window.clearTimeout(indicator.clearId);
            indicator.clearId = null;
        }
        this.trigger(this.items);
    },
    getState() {
        return this.items;
    },
};
const IndicatorStore = reflux_1.default.createStore(storeConfig);
exports.default = IndicatorStore;
//# sourceMappingURL=indicatorStore.jsx.map