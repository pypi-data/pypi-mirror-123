Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const alertLink_1 = (0, tslib_1.__importDefault)(require("app/components/alertLink"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const panels_1 = require("app/components/panels");
const pluginList_1 = (0, tslib_1.__importDefault)(require("app/components/pluginList"));
const projectAlerts_1 = require("app/data/forms/projectAlerts");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const routeTitle_1 = (0, tslib_1.__importDefault)(require("app/utils/routeTitle"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const jsonForm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/jsonForm"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const permissionAlert_1 = (0, tslib_1.__importDefault)(require("app/views/settings/project/permissionAlert"));
class Settings extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.handleEnablePlugin = (plugin) => {
            this.setState(prevState => {
                var _a;
                return ({
                    pluginList: ((_a = prevState.pluginList) !== null && _a !== void 0 ? _a : []).map(p => {
                        if (p.id !== plugin.id) {
                            return p;
                        }
                        return Object.assign(Object.assign({}, plugin), { enabled: true });
                    }),
                });
            });
        };
        this.handleDisablePlugin = (plugin) => {
            this.setState(prevState => {
                var _a;
                return ({
                    pluginList: ((_a = prevState.pluginList) !== null && _a !== void 0 ? _a : []).map(p => {
                        if (p.id !== plugin.id) {
                            return p;
                        }
                        return Object.assign(Object.assign({}, plugin), { enabled: false });
                    }),
                });
            });
        };
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { project: null, pluginList: [] });
    }
    getProjectEndpoint({ orgId, projectId }) {
        return `/projects/${orgId}/${projectId}/`;
    }
    getEndpoints() {
        const { params } = this.props;
        const { orgId, projectId } = params;
        const projectEndpoint = this.getProjectEndpoint(params);
        return [
            ['project', projectEndpoint],
            ['pluginList', `/projects/${orgId}/${projectId}/plugins/`],
        ];
    }
    getTitle() {
        const { projectId } = this.props.params;
        return (0, routeTitle_1.default)((0, locale_1.t)('Alerts Settings'), projectId, false);
    }
    renderBody() {
        const { canEditRule, organization, params } = this.props;
        const { orgId } = params;
        const { project, pluginList } = this.state;
        if (!project) {
            return null;
        }
        const projectEndpoint = this.getProjectEndpoint(params);
        return (<react_1.Fragment>
        <settingsPageHeader_1.default title={(0, locale_1.t)('Alerts Settings')} action={<button_1.default to={{
                    pathname: `/organizations/${orgId}/alerts/rules/`,
                    query: { project: project.id },
                }} size="small">
              {(0, locale_1.t)('View Alert Rules')}
            </button_1.default>}/>
        <permissionAlert_1.default />
        <alertLink_1.default to="/settings/account/notifications/" icon={<icons_1.IconMail />}>
          {(0, locale_1.t)('Looking to fine-tune your personal notification preferences? Visit your Account Settings')}
        </alertLink_1.default>

        <form_1.default saveOnBlur allowUndo initialData={{
                subjectTemplate: project.subjectTemplate,
                digestsMinDelay: project.digestsMinDelay,
                digestsMaxDelay: project.digestsMaxDelay,
            }} apiMethod="PUT" apiEndpoint={projectEndpoint}>
          <jsonForm_1.default disabled={!canEditRule} title={(0, locale_1.t)('Email Settings')} fields={[projectAlerts_1.fields.subjectTemplate]}/>

          <jsonForm_1.default title={(0, locale_1.t)('Digests')} disabled={!canEditRule} fields={[projectAlerts_1.fields.digestsMinDelay, projectAlerts_1.fields.digestsMaxDelay]} renderHeader={() => (<panels_1.PanelAlert type="info">
                {(0, locale_1.t)('Sentry will automatically digest alerts sent by some services to avoid flooding your inbox with individual issue notifications. To control how frequently notifications are delivered, use the sliders below.')}
              </panels_1.PanelAlert>)}/>
        </form_1.default>

        {canEditRule && (<pluginList_1.default organization={organization} project={project} pluginList={(pluginList !== null && pluginList !== void 0 ? pluginList : []).filter(p => p.type === 'notification' && p.hasConfiguration)} onEnablePlugin={this.handleEnablePlugin} onDisablePlugin={this.handleDisablePlugin}/>)}
      </react_1.Fragment>);
    }
}
exports.default = Settings;
//# sourceMappingURL=settings.jsx.map