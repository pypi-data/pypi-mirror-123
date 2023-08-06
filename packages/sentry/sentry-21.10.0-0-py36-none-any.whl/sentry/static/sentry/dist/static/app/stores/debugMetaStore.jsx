Object.defineProperty(exports, "__esModule", { value: true });
exports.DebugMetaStore = exports.DebugMetaActions = void 0;
const tslib_1 = require("tslib");
const reflux_1 = (0, tslib_1.__importDefault)(require("reflux"));
const DebugMetaActions = reflux_1.default.createActions(['updateFilter']);
exports.DebugMetaActions = DebugMetaActions;
const storeConfig = {
    filter: null,
    init() {
        this.reset();
        this.listenTo(DebugMetaActions.updateFilter, this.updateFilter);
    },
    reset() {
        this.filter = null;
        this.trigger(this.get());
    },
    updateFilter(word) {
        this.filter = word;
        this.trigger(this.get());
    },
    get() {
        return {
            filter: this.filter,
        };
    },
};
const DebugMetaStore = reflux_1.default.createStore(storeConfig);
exports.DebugMetaStore = DebugMetaStore;
exports.default = DebugMetaStore;
//# sourceMappingURL=debugMetaStore.jsx.map