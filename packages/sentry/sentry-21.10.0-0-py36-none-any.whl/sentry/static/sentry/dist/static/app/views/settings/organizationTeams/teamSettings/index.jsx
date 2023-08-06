Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const indicator_1 = require("app/actionCreators/indicator");
const teams_1 = require("app/actionCreators/teams");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const panels_1 = require("app/components/panels");
const teamSettingsFields_1 = (0, tslib_1.__importDefault)(require("app/data/forms/teamSettingsFields"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const field_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field"));
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const jsonForm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/jsonForm"));
const model_1 = (0, tslib_1.__importDefault)(require("./model"));
class TeamSettings extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.model = new model_1.default(this.props.params.orgId, this.props.params.teamId);
        this.handleSubmitSuccess = (resp, model, id) => {
            (0, teams_1.updateTeamSuccess)(resp.slug, resp);
            if (id === 'slug') {
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Team name changed'));
                react_router_1.browserHistory.replace(`/settings/${this.props.params.orgId}/teams/${model.getValue(id)}/settings/`);
                this.setState({ loading: true });
            }
        };
        this.handleRemoveTeam = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            yield (0, teams_1.removeTeam)(this.api, this.props.params);
            react_router_1.browserHistory.replace(`/settings/${this.props.params.orgId}/teams/`);
        });
    }
    getTitle() {
        return 'Team Settings';
    }
    getEndpoints() {
        return [];
    }
    renderBody() {
        const { organization, team } = this.props;
        const access = new Set(organization.access);
        return (<react_1.Fragment>
        <form_1.default model={this.model} apiMethod="PUT" saveOnBlur allowUndo onSubmitSuccess={this.handleSubmitSuccess} onSubmitError={() => (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to save change'))} initialData={{
                name: team.name,
                slug: team.slug,
            }}>
          <jsonForm_1.default access={access} forms={teamSettingsFields_1.default}/>
        </form_1.default>

        <panels_1.Panel>
          <panels_1.PanelHeader>{(0, locale_1.t)('Remove Team')}</panels_1.PanelHeader>
          <field_1.default help={(0, locale_1.t)("This may affect team members' access to projects and associated alert delivery.")}>
            <div>
              <confirm_1.default disabled={!access.has('team:admin')} onConfirm={this.handleRemoveTeam} priority="danger" message={(0, locale_1.tct)('Are you sure you want to remove the team [team]?', {
                team: `#${team.slug}`,
            })}>
                <button_1.default icon={<icons_1.IconDelete />} priority="danger" disabled={!access.has('team:admin')}>
                  {(0, locale_1.t)('Remove Team')}
                </button_1.default>
              </confirm_1.default>
            </div>
          </field_1.default>
        </panels_1.Panel>
      </react_1.Fragment>);
    }
}
exports.default = (0, withOrganization_1.default)(TeamSettings);
//# sourceMappingURL=index.jsx.map