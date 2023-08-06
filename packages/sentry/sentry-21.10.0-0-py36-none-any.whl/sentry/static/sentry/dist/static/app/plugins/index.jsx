Object.defineProperty(exports, "__esModule", { value: true });
exports.registry = exports.DefaultIssuePlugin = exports.BasePlugin = void 0;
const tslib_1 = require("tslib");
const basePlugin_1 = (0, tslib_1.__importDefault)(require("app/plugins/basePlugin"));
exports.BasePlugin = basePlugin_1.default;
const defaultIssuePlugin_1 = (0, tslib_1.__importDefault)(require("app/plugins/defaultIssuePlugin"));
exports.DefaultIssuePlugin = defaultIssuePlugin_1.default;
const registry_1 = (0, tslib_1.__importDefault)(require("app/plugins/registry"));
const sessionstack_1 = (0, tslib_1.__importDefault)(require("./sessionstack/contexts/sessionstack"));
const jira_1 = (0, tslib_1.__importDefault)(require("./jira"));
const sessionstack_2 = (0, tslib_1.__importDefault)(require("./sessionstack"));
const contexts = {};
const registry = new registry_1.default();
exports.registry = registry;
// Register legacy plugins
// Sessionstack
registry.add('sessionstack', sessionstack_2.default);
contexts.sessionstack = sessionstack_1.default;
// Jira
registry.add('jira', jira_1.default);
const add = registry.add.bind(registry);
const get = registry.get.bind(registry);
const isLoaded = registry.isLoaded.bind(registry);
const load = registry.load.bind(registry);
exports.default = {
    BasePlugin: basePlugin_1.default,
    DefaultIssuePlugin: defaultIssuePlugin_1.default,
    add,
    addContext: function (id, component) {
        contexts[id] = component;
    },
    contexts,
    get,
    isLoaded,
    load,
};
//# sourceMappingURL=index.jsx.map