Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const basePlugin_1 = (0, tslib_1.__importDefault)(require("app/plugins/basePlugin"));
const settings_1 = (0, tslib_1.__importDefault)(require("./components/settings"));
class SessionStackPlugin extends basePlugin_1.default {
    constructor() {
        super(...arguments);
        this.displayName = 'SessionStack';
    }
    // should never be be called since this is a non-issue plugin
    renderGroupActions() {
        return null;
    }
    renderSettings(props) {
        return <settings_1.default plugin={this.plugin} {...props}/>;
    }
}
exports.default = SessionStackPlugin;
//# sourceMappingURL=index.jsx.map