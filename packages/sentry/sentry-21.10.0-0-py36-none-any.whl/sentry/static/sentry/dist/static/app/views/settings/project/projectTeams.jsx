Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const modal_1 = require("app/actionCreators/modal");
const projects_1 = require("app/actionCreators/projects");
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const routeTitle_1 = (0, tslib_1.__importDefault)(require("app/utils/routeTitle"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const teamSelect_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/teamSelect"));
class ProjectTeams extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.canCreateTeam = () => {
            const { organization } = this.props;
            const access = new Set(organization.access);
            return (access.has('org:write') && access.has('team:write') && access.has('project:write'));
        };
        this.handleRemove = (teamSlug) => {
            if (this.state.loading) {
                return;
            }
            const { orgId, projectId } = this.props.params;
            (0, projects_1.removeTeamFromProject)(this.api, orgId, projectId, teamSlug)
                .then(() => this.handleRemovedTeam(teamSlug))
                .catch(() => {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Could not remove the %s team', teamSlug));
                this.setState({ loading: false });
            });
        };
        this.handleRemovedTeam = (teamSlug) => {
            this.setState(prevState => ({
                projectTeams: [
                    ...(prevState.projectTeams || []).filter(team => team.slug !== teamSlug),
                ],
            }));
        };
        this.handleAddedTeam = (team) => {
            this.setState(prevState => ({
                projectTeams: [...(prevState.projectTeams || []), team],
            }));
        };
        this.handleAdd = (team) => {
            if (this.state.loading) {
                return;
            }
            const { orgId, projectId } = this.props.params;
            (0, projects_1.addTeamToProject)(this.api, orgId, projectId, team).then(() => {
                this.handleAddedTeam(team);
            }, () => {
                this.setState({
                    error: true,
                    loading: false,
                });
            });
        };
        this.handleCreateTeam = (e) => {
            const { project, organization } = this.props;
            if (!this.canCreateTeam()) {
                return;
            }
            e.stopPropagation();
            e.preventDefault();
            (0, modal_1.openCreateTeamModal)({
                project,
                organization,
                onClose: data => {
                    (0, projects_1.addTeamToProject)(this.api, organization.slug, project.slug, data).then(this.remountComponent, this.remountComponent);
                },
            });
        };
    }
    getEndpoints() {
        const { orgId, projectId } = this.props.params;
        return [['projectTeams', `/projects/${orgId}/${projectId}/teams/`]];
    }
    getTitle() {
        const { projectId } = this.props.params;
        return (0, routeTitle_1.default)((0, locale_1.t)('Project Teams'), projectId, false);
    }
    renderBody() {
        const { params, organization } = this.props;
        const canCreateTeam = this.canCreateTeam();
        const hasAccess = organization.access.includes('project:write');
        const confirmRemove = (0, locale_1.t)('This is the last team with access to this project. Removing it will mean ' +
            'only organization owners and managers will be able to access the project pages. Are ' +
            'you sure you want to remove this team from the project %s?', params.projectId);
        const { projectTeams } = this.state;
        const menuHeader = (<StyledTeamsLabel>
        {(0, locale_1.t)('Teams')}
        <tooltip_1.default disabled={canCreateTeam} title={(0, locale_1.t)('You must be a project admin to create teams')} position="top">
          <StyledCreateTeamLink to="" disabled={!canCreateTeam} onClick={this.handleCreateTeam}>
            {(0, locale_1.t)('Create Team')}
          </StyledCreateTeamLink>
        </tooltip_1.default>
      </StyledTeamsLabel>);
        return (<div>
        <settingsPageHeader_1.default title={(0, locale_1.t)('%s Teams', params.projectId)}/>
        <teamSelect_1.default organization={organization} selectedTeams={projectTeams !== null && projectTeams !== void 0 ? projectTeams : []} onAddTeam={this.handleAdd} onRemoveTeam={this.handleRemove} menuHeader={menuHeader} confirmLastTeamRemoveMessage={confirmRemove} disabled={!hasAccess}/>
      </div>);
    }
}
const StyledTeamsLabel = (0, styled_1.default)('div') `
  font-size: 0.875em;
  padding: ${(0, space_1.default)(0.5)} 0px;
  text-transform: uppercase;
`;
const StyledCreateTeamLink = (0, styled_1.default)(link_1.default) `
  float: right;
  text-transform: none;
  ${p => p.disabled &&
    (0, react_1.css) `
      cursor: not-allowed;
      color: ${p.theme.gray300};
      opacity: 0.6;
    `};
`;
exports.default = ProjectTeams;
//# sourceMappingURL=projectTeams.jsx.map