Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const defaultIssuePlugin_1 = (0, tslib_1.__importDefault)(require("app/plugins/defaultIssuePlugin"));
const issueActions_1 = (0, tslib_1.__importDefault)(require("./components/issueActions"));
const settings_1 = (0, tslib_1.__importDefault)(require("./components/settings"));
class Jira extends defaultIssuePlugin_1.default {
    constructor() {
        super(...arguments);
        this.displayName = 'Jira';
    }
    renderSettings(props) {
        return <settings_1.default plugin={this.plugin} {...props}/>;
    }
    renderGroupActions(props) {
        return <issueActions_1.default {...props}/>;
    }
}
exports.default = Jira;
//# sourceMappingURL=index.jsx.map