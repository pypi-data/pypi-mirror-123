Object.defineProperty(exports, "__esModule", { value: true });
class StreamManager {
    // TODO(dcramer): this should listen to changes on GroupStore and remove
    // items that are removed there
    // TODO(ts) Add better typing for store. Generally this is GroupStore, but it could be other things.
    constructor(store, options = {}) {
        this.idList = [];
        this.store = store;
        this.limit = options.limit || 100;
    }
    reset() {
        this.idList = [];
    }
    trim() {
        if (this.limit > this.idList.length) {
            return;
        }
        const excess = this.idList.splice(this.limit, this.idList.length - this.limit);
        this.store.remove(excess);
    }
    push(items = []) {
        items = Array.isArray(items) ? items : [items];
        if (items.length === 0) {
            return;
        }
        items = items.filter(item => item.hasOwnProperty('id'));
        const ids = items.map(item => item.id);
        this.idList = this.idList.filter(id => !ids.includes(id));
        this.idList = [...this.idList, ...ids];
        this.trim();
        this.store.add(items);
    }
    getAllItems() {
        return this.store
            .getAllItems()
            .slice()
            .sort((a, b) => this.idList.indexOf(a.id) - this.idList.indexOf(b.id));
    }
    unshift(items = []) {
        items = Array.isArray(items) ? items : [items];
        if (items.length === 0) {
            return;
        }
        const ids = items.map(item => item.id);
        this.idList = this.idList.filter(id => !ids.includes(id));
        this.idList = [...ids, ...this.idList];
        this.trim();
        this.store.add(items);
    }
}
exports.default = StreamManager;
//# sourceMappingURL=streamManager.jsx.map