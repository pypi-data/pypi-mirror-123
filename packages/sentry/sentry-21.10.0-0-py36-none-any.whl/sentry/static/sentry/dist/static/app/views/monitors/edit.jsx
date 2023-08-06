Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const monitorForm_1 = (0, tslib_1.__importDefault)(require("./monitorForm"));
class EditMonitor extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.onUpdate = (data) => this.setState(state => ({ monitor: Object.assign(Object.assign({}, state.monitor), data) }));
        this.onSubmitSuccess = (data) => react_router_1.browserHistory.push(`/organizations/${this.props.params.orgId}/monitors/${data.id}/`);
    }
    getEndpoints() {
        const { params } = this.props;
        return [['monitor', `/monitors/${params.monitorId}/`]];
    }
    getTitle() {
        if (this.state.monitor) {
            return `${this.state.monitor.name} - Monitors - ${this.props.params.orgId}`;
        }
        return `Monitors - ${this.props.params.orgId}`;
    }
    renderBody() {
        const { monitor } = this.state;
        if (monitor === null) {
            return null;
        }
        return (<react_1.Fragment>
        <h1>Edit Monitor</h1>

        <monitorForm_1.default monitor={monitor} apiMethod="PUT" apiEndpoint={`/monitors/${monitor.id}/`} onSubmitSuccess={this.onSubmitSuccess}/>
      </react_1.Fragment>);
    }
}
exports.default = EditMonitor;
//# sourceMappingURL=edit.jsx.map