Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reflux_1 = (0, tslib_1.__importDefault)(require("reflux"));
const groupStore_1 = (0, tslib_1.__importDefault)(require("app/stores/groupStore"));
const storeConfig = {
    records: {},
    init() {
        this.records = {};
        this.listenTo(groupStore_1.default, this.onGroupChange, this.onGroupChange);
    },
    onGroupChange(itemIds) {
        this.prune();
        this.add(itemIds);
        this.trigger();
    },
    add(ids) {
        const allSelected = this.allSelected();
        ids.forEach(id => {
            if (!this.records.hasOwnProperty(id)) {
                this.records[id] = allSelected;
            }
        });
    },
    prune() {
        const existingIds = new Set(groupStore_1.default.getAllItemIds());
        // Remove ids that no longer exist
        for (const itemId in this.records) {
            if (!existingIds.has(itemId)) {
                delete this.records[itemId];
            }
        }
    },
    allSelected() {
        const itemIds = this.getSelectedIds();
        const numRecords = this.numSelected();
        return itemIds.size > 0 && itemIds.size === numRecords;
    },
    numSelected() {
        return Object.keys(this.records).length;
    },
    anySelected() {
        const itemIds = this.getSelectedIds();
        return itemIds.size > 0;
    },
    multiSelected() {
        const itemIds = this.getSelectedIds();
        return itemIds.size > 1;
    },
    getSelectedIds() {
        const selected = new Set();
        for (const itemId in this.records) {
            if (this.records[itemId]) {
                selected.add(itemId);
            }
        }
        return selected;
    },
    isSelected(itemId) {
        return this.records[itemId] === true;
    },
    deselectAll() {
        for (const itemId in this.records) {
            this.records[itemId] = false;
        }
        this.trigger();
    },
    toggleSelect(itemId) {
        if (!this.records.hasOwnProperty(itemId)) {
            return;
        }
        this.records[itemId] = !this.records[itemId];
        this.trigger();
    },
    toggleSelectAll() {
        const allSelected = !this.allSelected();
        for (const itemId in this.records) {
            this.records[itemId] = allSelected;
        }
        this.trigger();
    },
};
const SelectedGroupStore = reflux_1.default.createStore(storeConfig);
exports.default = SelectedGroupStore;
//# sourceMappingURL=selectedGroupStore.jsx.map