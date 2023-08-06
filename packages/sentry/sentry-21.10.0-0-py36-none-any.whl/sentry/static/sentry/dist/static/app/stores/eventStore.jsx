Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const extend_1 = (0, tslib_1.__importDefault)(require("lodash/extend"));
const isArray_1 = (0, tslib_1.__importDefault)(require("lodash/isArray"));
const reflux_1 = (0, tslib_1.__importDefault)(require("reflux"));
const storeConfig = {
    items: [],
    itemsById: {},
    init() {
        this.reset();
    },
    reset() {
        this.items = [];
    },
    loadInitialData(items) {
        this.reset();
        const itemIds = new Set();
        items.forEach(item => {
            itemIds.add(item.id);
            this.items.push(item);
        });
        this.trigger(itemIds);
    },
    add(items) {
        if (!(0, isArray_1.default)(items)) {
            items = [items];
        }
        const itemsById = {};
        const itemIds = new Set();
        items.forEach(item => {
            itemsById[item.id] = item;
            itemIds.add(item.id);
        });
        items.forEach((item, idx) => {
            if (itemsById[item.id]) {
                this.items[idx] = (0, extend_1.default)(true, {}, item, itemsById[item.id]);
                delete itemsById[item.id];
            }
        });
        for (const itemId in itemsById) {
            this.items.push(itemsById[itemId]);
        }
        this.trigger(itemIds);
    },
    remove(itemId) {
        this.items.forEach((item, idx) => {
            if (item.id === itemId) {
                this.items.splice(idx, idx + 1);
            }
        });
        this.trigger(new Set([itemId]));
    },
    get(id) {
        for (let i = 0; i < this.items.length; i++) {
            if (this.items[i].id === id) {
                return this.items[i];
            }
        }
        return undefined;
    },
    getAllItemIds() {
        return this.items.map(item => item.id);
    },
    getAllItems() {
        return this.items;
    },
};
const EventStore = reflux_1.default.createStore(storeConfig);
exports.default = EventStore;
//# sourceMappingURL=eventStore.jsx.map