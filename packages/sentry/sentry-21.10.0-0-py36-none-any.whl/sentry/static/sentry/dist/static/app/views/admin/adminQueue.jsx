Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const forms_1 = require("app/components/forms");
const internalStatChart_1 = (0, tslib_1.__importDefault)(require("app/components/internalStatChart"));
const panels_1 = require("app/components/panels");
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const TIME_WINDOWS = ['1h', '1d', '1w'];
class AdminQueue extends asyncView_1.default {
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { timeWindow: '1w', since: new Date().getTime() / 1000 - 3600 * 24 * 7, resolution: '1h', taskName: null });
    }
    getEndpoints() {
        return [['taskList', '/internal/queue/tasks/']];
    }
    changeWindow(timeWindow) {
        let seconds;
        if (timeWindow === '1h') {
            seconds = 3600;
        }
        else if (timeWindow === '1d') {
            seconds = 3600 * 24;
        }
        else if (timeWindow === '1w') {
            seconds = 3600 * 24 * 7;
        }
        else {
            throw new Error('Invalid time window');
        }
        this.setState({
            since: new Date().getTime() / 1000 - seconds,
            timeWindow,
        });
    }
    changeTask(value) {
        this.setState({ activeTask: value });
    }
    renderBody() {
        const { activeTask, taskList } = this.state;
        return (<div>
        <Header>
          <h3 className="no-border">Queue Overview</h3>

          <buttonBar_1.default merged active={this.state.timeWindow}>
            {TIME_WINDOWS.map(r => (<button_1.default size="small" barId={r} onClick={() => this.changeWindow(r)} key={r}>
                {r}
              </button_1.default>))}
          </buttonBar_1.default>
        </Header>

        <panels_1.Panel>
          <panels_1.PanelHeader>Global Throughput</panels_1.PanelHeader>
          <panels_1.PanelBody withPadding>
            <internalStatChart_1.default since={this.state.since} resolution={this.state.resolution} stat="jobs.all.started" label="jobs started"/>
          </panels_1.PanelBody>
        </panels_1.Panel>

        <h3 className="no-border">Task Details</h3>

        <div>
          <div className="m-b-1">
            <label>Show details for task:</label>
            <forms_1.SelectField name="task" onChange={value => this.changeTask(value)} value={activeTask} clearable options={taskList.map(t => ({
                value: t,
                label: t,
            }))}/>
          </div>
          {activeTask ? (<div>
              <panels_1.Panel key={`jobs.started.${activeTask}`}>
                <panels_1.PanelHeader>
                  Jobs Started <small>{activeTask}</small>
                </panels_1.PanelHeader>
                <panels_1.PanelBody withPadding>
                  <internalStatChart_1.default since={this.state.since} resolution={this.state.resolution} stat={`jobs.started.${activeTask}`} label="jobs" height={100}/>
                </panels_1.PanelBody>
              </panels_1.Panel>
              <panels_1.Panel key={`jobs.finished.${activeTask}`}>
                <panels_1.PanelHeader>
                  Jobs Finished <small>{activeTask}</small>
                </panels_1.PanelHeader>
                <panels_1.PanelBody withPadding>
                  <internalStatChart_1.default since={this.state.since} resolution={this.state.resolution} stat={`jobs.finished.${activeTask}`} label="jobs" height={100}/>
                </panels_1.PanelBody>
              </panels_1.Panel>
            </div>) : null}
        </div>
      </div>);
    }
}
exports.default = AdminQueue;
const Header = (0, styled_1.default)('div') `
  display: flex;
  justify-content: space-between;
  align-items: center;
`;
//# sourceMappingURL=adminQueue.jsx.map