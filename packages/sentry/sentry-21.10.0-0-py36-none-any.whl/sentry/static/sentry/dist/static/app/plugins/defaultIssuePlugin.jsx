Object.defineProperty(exports, "__esModule", { value: true });
exports.DefaultIssuePlugin = void 0;
const tslib_1 = require("tslib");
const basePlugin_1 = (0, tslib_1.__importDefault)(require("app/plugins/basePlugin"));
const issueActions_1 = (0, tslib_1.__importDefault)(require("app/plugins/components/issueActions"));
class DefaultIssuePlugin extends basePlugin_1.default {
    renderGroupActions(props) {
        return <issueActions_1.default {...props}/>;
    }
}
exports.DefaultIssuePlugin = DefaultIssuePlugin;
exports.default = DefaultIssuePlugin;
//# sourceMappingURL=defaultIssuePlugin.jsx.map