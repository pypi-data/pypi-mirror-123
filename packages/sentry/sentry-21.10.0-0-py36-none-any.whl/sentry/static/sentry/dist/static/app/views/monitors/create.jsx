Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const monitorForm_1 = (0, tslib_1.__importDefault)(require("./monitorForm"));
class CreateMonitor extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.onSubmitSuccess = (data) => {
            react_router_1.browserHistory.push(`/organizations/${this.props.params.orgId}/monitors/${data.id}/`);
        };
    }
    getTitle() {
        return `Monitors - ${this.props.params.orgId}`;
    }
    renderBody() {
        return (<react_1.Fragment>
        <h1>New Monitor</h1>
        <monitorForm_1.default apiMethod="POST" apiEndpoint={`/organizations/${this.props.params.orgId}/monitors/`} onSubmitSuccess={this.onSubmitSuccess}/>
      </react_1.Fragment>);
    }
}
exports.default = CreateMonitor;
//# sourceMappingURL=create.jsx.map