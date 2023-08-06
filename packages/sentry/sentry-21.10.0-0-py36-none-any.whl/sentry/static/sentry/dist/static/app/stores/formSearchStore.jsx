Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reflux_1 = (0, tslib_1.__importDefault)(require("reflux"));
const formSearchActions_1 = (0, tslib_1.__importDefault)(require("app/actions/formSearchActions"));
/**
 * Store for "form" searches, but probably will include more
 */
const storeConfig = {
    searchMap: null,
    init() {
        this.reset();
        this.listenTo(formSearchActions_1.default.loadSearchMap, this.onLoadSearchMap);
    },
    get() {
        return this.searchMap;
    },
    reset() {
        // `null` means it hasn't been loaded yet
        this.searchMap = null;
    },
    /**
     * Adds to search map
     */
    onLoadSearchMap(searchMap) {
        // Only load once
        if (this.searchMap !== null) {
            return;
        }
        this.searchMap = searchMap;
        this.trigger(this.searchMap);
    },
};
const FormSearchStore = reflux_1.default.createStore(storeConfig);
exports.default = FormSearchStore;
//# sourceMappingURL=formSearchStore.jsx.map