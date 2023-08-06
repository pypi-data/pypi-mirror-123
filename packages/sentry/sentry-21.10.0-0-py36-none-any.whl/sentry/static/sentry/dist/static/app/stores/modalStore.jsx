Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reflux_1 = (0, tslib_1.__importDefault)(require("reflux"));
const modalActions_1 = (0, tslib_1.__importDefault)(require("app/actions/modalActions"));
const storeConfig = {
    init() {
        this.reset();
        this.listenTo(modalActions_1.default.closeModal, this.onCloseModal);
        this.listenTo(modalActions_1.default.openModal, this.onOpenModal);
    },
    get() {
        return this.state;
    },
    reset() {
        this.state = {
            renderer: null,
            options: {},
        };
    },
    onCloseModal() {
        this.reset();
        this.trigger(this.state);
    },
    onOpenModal(renderer, options) {
        this.state = { renderer, options };
        this.trigger(this.state);
    },
};
const ModalStore = reflux_1.default.createStore(storeConfig);
exports.default = ModalStore;
//# sourceMappingURL=modalStore.jsx.map