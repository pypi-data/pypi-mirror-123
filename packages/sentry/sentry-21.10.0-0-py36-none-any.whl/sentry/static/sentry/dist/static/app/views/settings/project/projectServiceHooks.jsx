Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const indicator_1 = require("app/actionCreators/indicator");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const panels_1 = require("app/components/panels");
const switchButton_1 = (0, tslib_1.__importDefault)(require("app/components/switchButton"));
const truncate_1 = (0, tslib_1.__importDefault)(require("app/components/truncate"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const field_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
function ServiceHookRow({ orgId, projectId, hook, onToggleActive }) {
    return (<field_1.default label={<link_1.default data-test-id="project-service-hook" to={`/settings/${orgId}/projects/${projectId}/hooks/${hook.id}/`}>
          <truncate_1.default value={hook.url}/>
        </link_1.default>} help={<small>
          {hook.events && hook.events.length !== 0 ? (hook.events.join(', ')) : (<em>{(0, locale_1.t)('no events configured')}</em>)}
        </small>}>
      <switchButton_1.default isActive={hook.status === 'active'} size="lg" toggle={onToggleActive}/>
    </field_1.default>);
}
class ProjectServiceHooks extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.onToggleActive = (hook) => {
            const { orgId, projectId } = this.props.params;
            const { hookList } = this.state;
            if (!hookList) {
                return;
            }
            (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Saving changes\u2026'));
            this.api.request(`/projects/${orgId}/${projectId}/hooks/${hook.id}/`, {
                method: 'PUT',
                data: {
                    isActive: hook.status !== 'active',
                },
                success: data => {
                    (0, indicator_1.clearIndicators)();
                    this.setState({
                        hookList: hookList.map(h => {
                            if (h.id === data.id) {
                                return Object.assign(Object.assign({}, h), data);
                            }
                            return h;
                        }),
                    });
                },
                error: () => {
                    (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to remove application. Please try again.'));
                },
            });
        };
    }
    getEndpoints() {
        const { orgId, projectId } = this.props.params;
        return [['hookList', `/projects/${orgId}/${projectId}/hooks/`]];
    }
    renderEmpty() {
        return (<emptyMessage_1.default>
        {(0, locale_1.t)('There are no service hooks associated with this project.')}
      </emptyMessage_1.default>);
    }
    renderResults() {
        var _a;
        const { orgId, projectId } = this.props.params;
        return (<react_1.Fragment>
        <panels_1.PanelHeader key="header">{(0, locale_1.t)('Service Hook')}</panels_1.PanelHeader>
        <panels_1.PanelBody key="body">
          <panels_1.PanelAlert type="info" icon={<icons_1.IconFlag size="md"/>}>
            {(0, locale_1.t)('Service Hooks are an early adopter preview feature and will change in the future.')}
          </panels_1.PanelAlert>
          {(_a = this.state.hookList) === null || _a === void 0 ? void 0 : _a.map(hook => (<ServiceHookRow key={hook.id} orgId={orgId} projectId={projectId} hook={hook} onToggleActive={this.onToggleActive.bind(this, hook)}/>))}
        </panels_1.PanelBody>
      </react_1.Fragment>);
    }
    renderBody() {
        const { hookList } = this.state;
        const body = hookList && hookList.length > 0 ? this.renderResults() : this.renderEmpty();
        const { orgId, projectId } = this.props.params;
        const access = new Set(this.props.organization.access);
        return (<react_1.Fragment>
        <settingsPageHeader_1.default title={(0, locale_1.t)('Service Hooks')} action={access.has('project:write') ? (<button_1.default data-test-id="new-service-hook" to={`/settings/${orgId}/projects/${projectId}/hooks/new/`} size="small" priority="primary" icon={<icons_1.IconAdd size="xs" isCircled/>}>
                {(0, locale_1.t)('Create New Hook')}
              </button_1.default>) : null}/>
        <panels_1.Panel>{body}</panels_1.Panel>
      </react_1.Fragment>);
    }
}
exports.default = (0, withOrganization_1.default)(ProjectServiceHooks);
//# sourceMappingURL=projectServiceHooks.jsx.map