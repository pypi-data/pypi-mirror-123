Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const monitorCheckIns_1 = (0, tslib_1.__importDefault)(require("./monitorCheckIns"));
const monitorHeader_1 = (0, tslib_1.__importDefault)(require("./monitorHeader"));
const monitorIssues_1 = (0, tslib_1.__importDefault)(require("./monitorIssues"));
const monitorStats_1 = (0, tslib_1.__importDefault)(require("./monitorStats"));
class MonitorDetails extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.onUpdate = (data) => this.setState(state => ({ monitor: Object.assign(Object.assign({}, state.monitor), data) }));
    }
    getEndpoints() {
        const { params, location } = this.props;
        return [['monitor', `/monitors/${params.monitorId}/`, { query: location.query }]];
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
        <monitorHeader_1.default monitor={monitor} orgId={this.props.params.orgId} onUpdate={this.onUpdate}/>

        <monitorStats_1.default monitor={monitor}/>

        <panels_1.Panel style={{ paddingBottom: 0 }}>
          <panels_1.PanelHeader>{(0, locale_1.t)('Related Issues')}</panels_1.PanelHeader>

          <monitorIssues_1.default monitor={monitor} orgId={this.props.params.orgId}/>
        </panels_1.Panel>

        <panels_1.Panel>
          <panels_1.PanelHeader>{(0, locale_1.t)('Recent Check-ins')}</panels_1.PanelHeader>

          <monitorCheckIns_1.default monitor={monitor}/>
        </panels_1.Panel>
      </react_1.Fragment>);
    }
}
exports.default = MonitorDetails;
//# sourceMappingURL=details.jsx.map