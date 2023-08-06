Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const settings_1 = (0, tslib_1.__importDefault)(require("app/plugins/components/settings"));
class BasePlugin {
    constructor(data) {
        this.plugin = data;
    }
    renderSettings(props) {
        return <settings_1.default plugin={this.plugin} {...props}/>;
    }
}
exports.default = BasePlugin;
//# sourceMappingURL=basePlugin.jsx.map