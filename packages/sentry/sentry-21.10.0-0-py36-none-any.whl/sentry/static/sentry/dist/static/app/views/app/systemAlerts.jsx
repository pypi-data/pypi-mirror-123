Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const alertStore_1 = (0, tslib_1.__importDefault)(require("app/stores/alertStore"));
const useLegacyStore_1 = require("app/stores/useLegacyStore");
const alertMessage_1 = (0, tslib_1.__importDefault)(require("./alertMessage"));
function SystemAlerts(props) {
    const alerts = (0, useLegacyStore_1.useLegacyStore)(alertStore_1.default);
    return (<div {...props}>
      {alerts.map((alert, index) => (<alertMessage_1.default alert={alert} key={`${alert.id}-${index}`} system/>))}
    </div>);
}
exports.default = SystemAlerts;
//# sourceMappingURL=systemAlerts.jsx.map