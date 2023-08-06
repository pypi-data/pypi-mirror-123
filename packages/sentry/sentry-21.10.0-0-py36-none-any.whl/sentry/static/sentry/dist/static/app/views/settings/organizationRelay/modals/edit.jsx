Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const locale_1 = require("app/locale");
const modalManager_1 = (0, tslib_1.__importDefault)(require("./modalManager"));
class Edit extends modalManager_1.default {
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { values: {
                name: this.props.relay.name,
                publicKey: this.props.relay.publicKey,
                description: this.props.relay.description || '',
            }, disables: { publicKey: true } });
    }
    getTitle() {
        return (0, locale_1.t)('Edit Key');
    }
    getData() {
        const { savedRelays } = this.props;
        const updatedRelay = this.state.values;
        const trustedRelays = savedRelays.map(relay => {
            if (relay.publicKey === updatedRelay.publicKey) {
                return updatedRelay;
            }
            return relay;
        });
        return { trustedRelays };
    }
}
exports.default = Edit;
//# sourceMappingURL=edit.jsx.map