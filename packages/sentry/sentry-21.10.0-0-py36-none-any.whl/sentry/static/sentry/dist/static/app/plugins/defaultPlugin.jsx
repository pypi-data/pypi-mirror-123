Object.defineProperty(exports, "__esModule", { value: true });
exports.DefaultPlugin = void 0;
const tslib_1 = require("tslib");
const basePlugin_1 = (0, tslib_1.__importDefault)(require("app/plugins/basePlugin"));
class DefaultPlugin extends basePlugin_1.default {
    // should never be be called since this is a non-issue plugin
    renderGroupActions() {
        return null;
    }
}
exports.DefaultPlugin = DefaultPlugin;
DefaultPlugin.displayName = 'DefaultPlugin';
//# sourceMappingURL=defaultPlugin.jsx.map