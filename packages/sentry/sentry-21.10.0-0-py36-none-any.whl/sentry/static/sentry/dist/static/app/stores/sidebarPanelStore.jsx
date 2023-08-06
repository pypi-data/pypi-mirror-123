Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reflux_1 = (0, tslib_1.__importDefault)(require("reflux"));
const sidebarPanelActions_1 = (0, tslib_1.__importDefault)(require("app/actions/sidebarPanelActions"));
const storeConfig = {
    activePanel: '',
    init() {
        this.listenTo(sidebarPanelActions_1.default.activatePanel, this.onActivatePanel);
        this.listenTo(sidebarPanelActions_1.default.hidePanel, this.onHidePanel);
        this.listenTo(sidebarPanelActions_1.default.togglePanel, this.onTogglePanel);
    },
    onActivatePanel(panel) {
        this.activePanel = panel;
        this.trigger(this.activePanel);
    },
    onTogglePanel(panel) {
        if (this.activePanel === panel) {
            this.onHidePanel();
        }
        else {
            this.onActivatePanel(panel);
        }
    },
    onHidePanel() {
        this.activePanel = '';
        this.trigger(this.activePanel);
    },
    getState() {
        return this.activePanel;
    },
};
/**
 * This store is used to hold local user preferences
 * Side-effects (like reading/writing to cookies) are done in associated actionCreators
 */
const SidebarPanelStore = reflux_1.default.createStore(storeConfig);
exports.default = SidebarPanelStore;
//# sourceMappingURL=sidebarPanelStore.jsx.map