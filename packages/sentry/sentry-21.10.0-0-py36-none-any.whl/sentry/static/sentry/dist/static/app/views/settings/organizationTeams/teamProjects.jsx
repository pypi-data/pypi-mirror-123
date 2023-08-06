Object.defineProperty(exports, "__esModule", { value: true });
exports.TeamProjects = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const projectActions_1 = (0, tslib_1.__importDefault)(require("app/actions/projectActions"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const dropdownAutoComplete_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownAutoComplete"));
const dropdownButton_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownButton"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const panels_1 = require("app/components/panels");
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const settingsProjectItem_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsProjectItem"));
class TeamProjects extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            error: false,
            loading: true,
            pageLinks: null,
            unlinkedProjects: [],
            linkedProjects: [],
        };
        this.fetchAll = () => {
            this.fetchTeamProjects();
            this.fetchUnlinkedProjects();
        };
        this.handleLinkProject = (project, action) => {
            const { orgId, teamId } = this.props.params;
            this.props.api.request(`/projects/${orgId}/${project.slug}/teams/${teamId}/`, {
                method: action === 'add' ? 'POST' : 'DELETE',
                success: resp => {
                    this.fetchAll();
                    projectActions_1.default.updateSuccess(resp);
                    (0, indicator_1.addSuccessMessage)(action === 'add'
                        ? (0, locale_1.t)('Successfully added project to team.')
                        : (0, locale_1.t)('Successfully removed project from team'));
                },
                error: () => {
                    (0, indicator_1.addErrorMessage)((0, locale_1.t)("Wasn't able to change project association."));
                },
            });
        };
        this.handleProjectSelected = (selection) => {
            const project = this.state.unlinkedProjects.find(p => p.id === selection.value);
            if (project) {
                this.handleLinkProject(project, 'add');
            }
        };
        this.handleQueryUpdate = (evt) => {
            this.fetchUnlinkedProjects(evt.target.value);
        };
    }
    componentDidMount() {
        this.fetchAll();
    }
    componentDidUpdate(prevProps) {
        if (prevProps.params.orgId !== this.props.params.orgId ||
            prevProps.params.teamId !== this.props.params.teamId) {
            this.fetchAll();
        }
        if (prevProps.location !== this.props.location) {
            this.fetchTeamProjects();
        }
    }
    fetchTeamProjects() {
        const { location, params: { orgId, teamId }, } = this.props;
        this.setState({ loading: true });
        this.props.api
            .requestPromise(`/organizations/${orgId}/projects/`, {
            query: {
                query: `team:${teamId}`,
                cursor: location.query.cursor || '',
            },
            includeAllArgs: true,
        })
            .then(([linkedProjects, _, resp]) => {
            var _a;
            this.setState({
                loading: false,
                error: false,
                linkedProjects,
                pageLinks: (_a = resp === null || resp === void 0 ? void 0 : resp.getResponseHeader('Link')) !== null && _a !== void 0 ? _a : null,
            });
        })
            .catch(() => {
            this.setState({ loading: false, error: true });
        });
    }
    fetchUnlinkedProjects(query = '') {
        const { params: { orgId, teamId }, } = this.props;
        this.props.api
            .requestPromise(`/organizations/${orgId}/projects/`, {
            query: {
                query: query ? `!team:${teamId} ${query}` : `!team:${teamId}`,
            },
        })
            .then(unlinkedProjects => {
            this.setState({ unlinkedProjects });
        });
    }
    projectPanelContents(projects) {
        const { organization } = this.props;
        const access = new Set(organization.access);
        const canWrite = access.has('org:write');
        return projects.length ? ((0, utils_1.sortProjects)(projects).map(project => (<StyledPanelItem key={project.id}>
          <settingsProjectItem_1.default project={project} organization={organization}/>
          <tooltip_1.default disabled={canWrite} title={(0, locale_1.t)('You do not have enough permission to change project association.')}>
            <button_1.default size="small" disabled={!canWrite} icon={<icons_1.IconSubtract isCircled size="xs"/>} onClick={() => {
                this.handleLinkProject(project, 'remove');
            }}>
              {(0, locale_1.t)('Remove')}
            </button_1.default>
          </tooltip_1.default>
        </StyledPanelItem>))) : (<emptyMessage_1.default size="large" icon={<icons_1.IconFlag size="xl"/>}>
        {(0, locale_1.t)("This team doesn't have access to any projects.")}
      </emptyMessage_1.default>);
    }
    render() {
        const { linkedProjects, unlinkedProjects, error, loading } = this.state;
        if (error) {
            return <loadingError_1.default onRetry={() => this.fetchAll()}/>;
        }
        if (loading) {
            return <loadingIndicator_1.default />;
        }
        const access = new Set(this.props.organization.access);
        const otherProjects = unlinkedProjects.map(p => ({
            value: p.id,
            searchKey: p.slug,
            label: <ProjectListElement>{p.slug}</ProjectListElement>,
        }));
        return (<React.Fragment>
        <panels_1.Panel>
          <panels_1.PanelHeader hasButtons>
            <div>{(0, locale_1.t)('Projects')}</div>
            <div style={{ textTransform: 'none' }}>
              {!access.has('org:write') ? (<dropdownButton_1.default disabled title={(0, locale_1.t)('You do not have enough permission to associate a project.')} size="xsmall">
                  {(0, locale_1.t)('Add Project')}
                </dropdownButton_1.default>) : (<dropdownAutoComplete_1.default items={otherProjects} onChange={this.handleQueryUpdate} onSelect={this.handleProjectSelected} emptyMessage={(0, locale_1.t)('No projects')} alignMenu="right">
                  {({ isOpen }) => (<dropdownButton_1.default isOpen={isOpen} size="xsmall">
                      {(0, locale_1.t)('Add Project')}
                    </dropdownButton_1.default>)}
                </dropdownAutoComplete_1.default>)}
            </div>
          </panels_1.PanelHeader>
          <panels_1.PanelBody>{this.projectPanelContents(linkedProjects)}</panels_1.PanelBody>
        </panels_1.Panel>
        <pagination_1.default pageLinks={this.state.pageLinks} {...this.props}/>
      </React.Fragment>);
    }
}
exports.TeamProjects = TeamProjects;
const StyledPanelItem = (0, styled_1.default)(panels_1.PanelItem) `
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: ${(0, space_1.default)(2)};
`;
const ProjectListElement = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(0.25)} 0;
`;
exports.default = (0, withApi_1.default)((0, withOrganization_1.default)(TeamProjects));
//# sourceMappingURL=teamProjects.jsx.map