Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const indicator_1 = require("app/actionCreators/indicator");
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const miniBarChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/miniBarChart"));
const errorBoundary_1 = (0, tslib_1.__importDefault)(require("app/components/errorBoundary"));
const panels_1 = require("app/components/panels");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const field_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field"));
const textCopyInput_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/textCopyInput"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const serviceHookSettingsForm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/project/serviceHookSettingsForm"));
class HookStats extends asyncComponent_1.default {
    getEndpoints() {
        const until = Math.floor(new Date().getTime() / 1000);
        const since = until - 3600 * 24 * 30;
        const { hookId, orgId, projectId } = this.props.params;
        return [
            [
                'stats',
                `/projects/${orgId}/${projectId}/hooks/${hookId}/stats/`,
                {
                    query: {
                        since,
                        until,
                        resolution: '1d',
                    },
                },
            ],
        ];
    }
    renderBody() {
        const { stats } = this.state;
        if (stats === null) {
            return null;
        }
        let emptyStats = true;
        const series = {
            seriesName: (0, locale_1.t)('Events'),
            data: stats.map(p => {
                if (p.total) {
                    emptyStats = false;
                }
                return {
                    name: p.ts * 1000,
                    value: p.total,
                };
            }),
        };
        return (<panels_1.Panel>
        <panels_1.PanelHeader>{(0, locale_1.t)('Events in the last 30 days (by day)')}</panels_1.PanelHeader>
        <panels_1.PanelBody withPadding>
          {!emptyStats ? (<miniBarChart_1.default isGroupedByDate showTimeInTooltip labelYAxisExtents series={[series]} height={150}/>) : (<emptyMessage_1.default title={(0, locale_1.t)('Nothing recorded in the last 30 days.')} description={(0, locale_1.t)('Total webhooks fired for this configuration.')}/>)}
        </panels_1.PanelBody>
      </panels_1.Panel>);
    }
}
class ProjectServiceHookDetails extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.onDelete = () => {
            const { orgId, projectId, hookId } = this.props.params;
            (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Saving changes\u2026'));
            this.api.request(`/projects/${orgId}/${projectId}/hooks/${hookId}/`, {
                method: 'DELETE',
                success: () => {
                    (0, indicator_1.clearIndicators)();
                    react_router_1.browserHistory.push(`/settings/${orgId}/projects/${projectId}/hooks/`);
                },
                error: () => {
                    (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to remove application. Please try again.'));
                },
            });
        };
    }
    getEndpoints() {
        const { orgId, projectId, hookId } = this.props.params;
        return [['hook', `/projects/${orgId}/${projectId}/hooks/${hookId}/`]];
    }
    renderBody() {
        const { orgId, projectId, hookId } = this.props.params;
        const { hook } = this.state;
        if (!hook) {
            return null;
        }
        return (<react_1.Fragment>
        <settingsPageHeader_1.default title={(0, locale_1.t)('Service Hook Details')}/>

        <errorBoundary_1.default>
          <HookStats params={this.props.params}/>
        </errorBoundary_1.default>

        <serviceHookSettingsForm_1.default orgId={orgId} projectId={projectId} hookId={hookId} initialData={Object.assign(Object.assign({}, hook), { isActive: hook.status !== 'disabled' })}/>
        <panels_1.Panel>
          <panels_1.PanelHeader>{(0, locale_1.t)('Event Validation')}</panels_1.PanelHeader>
          <panels_1.PanelBody>
            <panels_1.PanelAlert type="info" icon={<icons_1.IconFlag size="md"/>}>
              Sentry will send the <code>X-ServiceHook-Signature</code> header built using{' '}
              <code>HMAC(SHA256, [secret], [payload])</code>. You should always verify
              this signature before trusting the information provided in the webhook.
            </panels_1.PanelAlert>
            <field_1.default label={(0, locale_1.t)('Secret')} flexibleControlStateSize inline={false} help={(0, locale_1.t)('The shared secret used for generating event HMAC signatures.')}>
              <textCopyInput_1.default>
                {(0, getDynamicText_1.default)({
                value: hook.secret,
                fixed: 'a dynamic secret value',
            })}
              </textCopyInput_1.default>
            </field_1.default>
          </panels_1.PanelBody>
        </panels_1.Panel>
        <panels_1.Panel>
          <panels_1.PanelHeader>{(0, locale_1.t)('Delete Hook')}</panels_1.PanelHeader>
          <panels_1.PanelBody>
            <field_1.default label={(0, locale_1.t)('Delete Hook')} help={(0, locale_1.t)('Removing this hook is immediate and permanent.')}>
              <div>
                <button_1.default priority="danger" onClick={this.onDelete}>
                  {(0, locale_1.t)('Delete Hook')}
                </button_1.default>
              </div>
            </field_1.default>
          </panels_1.PanelBody>
        </panels_1.Panel>
      </react_1.Fragment>);
    }
}
exports.default = ProjectServiceHookDetails;
//# sourceMappingURL=projectServiceHookDetails.jsx.map