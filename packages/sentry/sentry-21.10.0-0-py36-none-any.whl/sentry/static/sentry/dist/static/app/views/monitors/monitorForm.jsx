Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const mobx_react_1 = require("mobx-react");
const access_1 = (0, tslib_1.__importDefault)(require("app/components/acl/access"));
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const withGlobalSelection_1 = (0, tslib_1.__importDefault)(require("app/utils/withGlobalSelection"));
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
const field_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field"));
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const numberField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/numberField"));
const selectField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/selectField"));
const textCopyInput_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/textCopyInput"));
const textField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/textField"));
const monitorModel_1 = (0, tslib_1.__importDefault)(require("./monitorModel"));
const SCHEDULE_TYPES = [
    { value: 'crontab', label: 'Crontab' },
    { value: 'interval', label: 'Interval' },
];
const MONITOR_TYPES = [
    { value: 'cron_job', label: 'Cron Job' },
];
const INTERVALS = [
    { value: 'minute', label: 'minute(s)' },
    { value: 'hour', label: 'hour(s)' },
    { value: 'day', label: 'day(s)' },
    { value: 'week', label: 'week(s)' },
    { value: 'month', label: 'month(s)' },
    { value: 'year', label: 'year(s)' },
];
class MonitorForm extends react_1.Component {
    constructor() {
        super(...arguments);
        this.form = new monitorModel_1.default();
    }
    formDataFromConfig(type, config) {
        const rv = {};
        switch (type) {
            case 'cron_job':
                rv['config.schedule_type'] = config.schedule_type;
                rv['config.checkin_margin'] = config.checkin_margin;
                rv['config.max_runtime'] = config.max_runtime;
                switch (config.schedule_type) {
                    case 'interval':
                        rv['config.schedule.frequency'] = config.schedule[0];
                        rv['config.schedule.interval'] = config.schedule[1];
                        break;
                    case 'crontab':
                    default:
                        rv['config.schedule'] = config.schedule;
                }
                break;
            default:
        }
        return rv;
    }
    render() {
        const { monitor } = this.props;
        const selectedProjectId = this.props.selection.projects[0];
        const selectedProject = selectedProjectId
            ? this.props.projects.find(p => p.id === selectedProjectId + '')
            : null;
        return (<access_1.default access={['project:write']}>
        {({ hasAccess }) => (<form_1.default allowUndo requireChanges apiEndpoint={this.props.apiEndpoint} apiMethod={this.props.apiMethod} model={this.form} initialData={monitor
                    ? Object.assign({ name: monitor.name, type: monitor.type, project: monitor.project.slug }, this.formDataFromConfig(monitor.type, monitor.config)) : {
                    project: selectedProject ? selectedProject.slug : null,
                }} onSubmitSuccess={this.props.onSubmitSuccess}>
            <panels_1.Panel>
              <panels_1.PanelHeader>{(0, locale_1.t)('Details')}</panels_1.PanelHeader>

              <panels_1.PanelBody>
                {monitor && (<field_1.default label={(0, locale_1.t)('ID')}>
                    <div className="controls">
                      <textCopyInput_1.default>{monitor.id}</textCopyInput_1.default>
                    </div>
                  </field_1.default>)}
                <selectField_1.default name="project" label={(0, locale_1.t)('Project')} disabled={!hasAccess} options={this.props.projects
                    .filter(p => p.isMember)
                    .map(p => ({ value: p.slug, label: p.slug }))} required/>
                <textField_1.default name="name" placeholder={(0, locale_1.t)('My Cron Job')} label={(0, locale_1.t)('Name')} disabled={!hasAccess} required/>
              </panels_1.PanelBody>
            </panels_1.Panel>
            <panels_1.Panel>
              <panels_1.PanelHeader>{(0, locale_1.t)('Config')}</panels_1.PanelHeader>

              <panels_1.PanelBody>
                <selectField_1.default name="type" label={(0, locale_1.t)('Type')} disabled={!hasAccess} options={MONITOR_TYPES} required/>
                <mobx_react_1.Observer>
                  {() => {
                    switch (this.form.getValue('type')) {
                        case 'cron_job':
                            return (<react_1.Fragment>
                            <numberField_1.default name="config.max_runtime" label={(0, locale_1.t)('Max Runtime')} disabled={!hasAccess} help={(0, locale_1.t)("The maximum runtime (in minutes) a check-in is allowed before it's marked as a failure.")} placeholder="e.g. 30"/>
                            <selectField_1.default name="config.schedule_type" label={(0, locale_1.t)('Schedule Type')} disabled={!hasAccess} options={SCHEDULE_TYPES} required/>
                          </react_1.Fragment>);
                        default:
                            return null;
                    }
                }}
                </mobx_react_1.Observer>
                <mobx_react_1.Observer>
                  {() => {
                    switch (this.form.getValue('config.schedule_type')) {
                        case 'crontab':
                            return (<react_1.Fragment>
                            <textField_1.default name="config.schedule" label={(0, locale_1.t)('Schedule')} disabled={!hasAccess} placeholder="*/5 * * * *" required help={(0, locale_1.tct)('Changes to the schedule will apply on the next check-in. See [link:Wikipedia] for crontab syntax.', {
                                    link: <a href="https://en.wikipedia.org/wiki/Cron"/>,
                                })}/>
                            <numberField_1.default name="config.checkin_margin" label={(0, locale_1.t)('Check-in Margin')} disabled={!hasAccess} help={(0, locale_1.t)("The margin (in minutes) a check-in is allowed to exceed it's scheduled window before being treated as missed.")} placeholder="e.g. 30"/>
                          </react_1.Fragment>);
                        case 'interval':
                            return (<react_1.Fragment>
                            <numberField_1.default name="config.schedule.frequency" label={(0, locale_1.t)('Frequency')} disabled={!hasAccess} placeholder="e.g. 1" required/>
                            <selectField_1.default name="config.schedule.interval" label={(0, locale_1.t)('Interval')} disabled={!hasAccess} options={INTERVALS} required/>
                            <numberField_1.default name="config.checkin_margin" label={(0, locale_1.t)('Check-in Margin')} disabled={!hasAccess} help={(0, locale_1.t)("The margin (in minutes) a check-in is allowed to exceed it's scheduled window before being treated as missed.")} placeholder="e.g. 30"/>
                          </react_1.Fragment>);
                        default:
                            return null;
                    }
                }}
                </mobx_react_1.Observer>
              </panels_1.PanelBody>
            </panels_1.Panel>
          </form_1.default>)}
      </access_1.default>);
    }
}
exports.default = (0, withGlobalSelection_1.default)((0, withProjects_1.default)(MonitorForm));
//# sourceMappingURL=monitorForm.jsx.map