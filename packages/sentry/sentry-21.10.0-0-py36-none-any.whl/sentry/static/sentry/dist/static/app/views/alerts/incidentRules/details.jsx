Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const analytics_1 = require("app/utils/analytics");
const withTeams_1 = (0, tslib_1.__importDefault)(require("app/utils/withTeams"));
const ruleForm_1 = (0, tslib_1.__importDefault)(require("app/views/alerts/incidentRules/ruleForm"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
class IncidentRulesDetails extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.handleSubmitSuccess = () => {
            const { router } = this.props;
            const { orgId } = this.props.params;
            analytics_1.metric.endTransaction({ name: 'saveAlertRule' });
            router.push(`/organizations/${orgId}/alerts/rules/`);
        };
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { actions: new Map() });
    }
    getEndpoints() {
        const { orgId, ruleId } = this.props.params;
        return [['rule', `/organizations/${orgId}/alert-rules/${ruleId}/`]];
    }
    onRequestSuccess({ stateKey, data }) {
        if (stateKey === 'rule' && data.name) {
            this.props.onChangeTitle(data.name);
        }
    }
    renderBody() {
        const { teams } = this.props;
        const { ruleId } = this.props.params;
        const { rule } = this.state;
        const userTeamIds = teams.filter(({ isMember }) => isMember).map(({ id }) => id);
        return (<ruleForm_1.default {...this.props} ruleId={ruleId} rule={rule} onSubmitSuccess={this.handleSubmitSuccess} userTeamIds={userTeamIds}/>);
    }
}
exports.default = (0, withTeams_1.default)(IncidentRulesDetails);
//# sourceMappingURL=details.jsx.map