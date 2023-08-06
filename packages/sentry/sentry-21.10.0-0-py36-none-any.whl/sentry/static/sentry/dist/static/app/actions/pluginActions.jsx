Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reflux_1 = (0, tslib_1.__importDefault)(require("reflux"));
const PluginActions = reflux_1.default.createActions([
    'update',
    'updateError',
    'updateSuccess',
    'fetchAll',
    'fetchAllSuccess',
    'fetchAllError',
]);
exports.default = PluginActions;
//# sourceMappingURL=pluginActions.jsx.map