Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const analytics_1 = require("app/utils/analytics");
const withTeams_1 = (0, tslib_1.__importDefault)(require("app/utils/withTeams"));
const constants_1 = require("app/views/alerts/incidentRules/constants");
const ruleForm_1 = (0, tslib_1.__importDefault)(require("./ruleForm"));
/**
 * Show metric rules form with an empty rule. Redirects to alerts list after creation.
 */
function IncidentRulesCreate(props) {
    var _a;
    function handleSubmitSuccess() {
        const { router } = props;
        const { orgId } = props.params;
        analytics_1.metric.endTransaction({ name: 'saveAlertRule' });
        router.push(`/organizations/${orgId}/alerts/rules/`);
    }
    const { project, eventView, wizardTemplate, sessionId, teams } = props, otherProps = (0, tslib_1.__rest)(props, ["project", "eventView", "wizardTemplate", "sessionId", "teams"]);
    const defaultRule = eventView
        ? (0, constants_1.createRuleFromEventView)(eventView)
        : wizardTemplate
            ? (0, constants_1.createRuleFromWizardTemplate)(wizardTemplate)
            : (0, constants_1.createDefaultRule)();
    const userTeamIds = teams.filter(({ isMember }) => isMember).map(({ id }) => id);
    const projectTeamIds = new Set(project.teams.map(({ id }) => id));
    const defaultOwnerId = (_a = userTeamIds.find(id => projectTeamIds.has(id))) !== null && _a !== void 0 ? _a : null;
    defaultRule.owner = defaultOwnerId && `team:${defaultOwnerId}`;
    return (<ruleForm_1.default onSubmitSuccess={handleSubmitSuccess} rule={Object.assign(Object.assign({}, defaultRule), { projects: [project.slug] })} sessionId={sessionId} project={project} userTeamIds={userTeamIds} {...otherProps}/>);
}
exports.default = (0, withTeams_1.default)(IncidentRulesCreate);
//# sourceMappingURL=create.jsx.map