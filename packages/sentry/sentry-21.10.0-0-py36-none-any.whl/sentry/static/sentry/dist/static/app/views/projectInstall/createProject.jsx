Object.defineProperty(exports, "__esModule", { value: true });
exports.CreateProject = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const platformicons_1 = require("platformicons");
const modal_1 = require("app/actionCreators/modal");
const projectActions_1 = (0, tslib_1.__importDefault)(require("app/actions/projectActions"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const teamSelector_1 = (0, tslib_1.__importDefault)(require("app/components/forms/teamSelector"));
const pageHeading_1 = (0, tslib_1.__importDefault)(require("app/components/pageHeading"));
const platformPicker_1 = (0, tslib_1.__importDefault)(require("app/components/platformPicker"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const platformCategories_1 = (0, tslib_1.__importDefault)(require("app/data/platformCategories"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const input_1 = require("app/styles/input");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const getPlatformName_1 = (0, tslib_1.__importDefault)(require("app/utils/getPlatformName"));
const slugify_1 = (0, tslib_1.__importDefault)(require("app/utils/slugify"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const withTeams_1 = (0, tslib_1.__importDefault)(require("app/utils/withTeams"));
const issueAlertOptions_1 = (0, tslib_1.__importDefault)(require("app/views/projectInstall/issueAlertOptions"));
const getCategoryName = (category) => { var _a; return (_a = platformCategories_1.default.find(({ id }) => id === category)) === null || _a === void 0 ? void 0 : _a.id; };
class CreateProject extends React.Component {
    constructor(props, context) {
        super(props, context);
        this.createProject = (e) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            e.preventDefault();
            const { organization, api } = this.props;
            const { projectName, platform, team, dataFragment } = this.state;
            const { slug } = organization;
            const { shouldCreateCustomRule, name, conditions, actions, actionMatch, frequency, defaultRules, } = dataFragment || {};
            this.setState({ inFlight: true });
            if (!projectName) {
                Sentry.withScope(scope => {
                    scope.setExtra('props', this.props);
                    scope.setExtra('state', this.state);
                    Sentry.captureMessage('No project name');
                });
            }
            try {
                const projectData = yield api.requestPromise(`/teams/${slug}/${team}/projects/`, {
                    method: 'POST',
                    data: {
                        name: projectName,
                        platform,
                        default_rules: defaultRules !== null && defaultRules !== void 0 ? defaultRules : true,
                    },
                });
                let ruleId;
                if (shouldCreateCustomRule) {
                    const ruleData = yield api.requestPromise(`/projects/${organization.slug}/${projectData.slug}/rules/`, {
                        method: 'POST',
                        data: {
                            name,
                            conditions,
                            actions,
                            actionMatch,
                            frequency,
                        },
                    });
                    ruleId = ruleData.id;
                }
                this.trackIssueAlertOptionSelectedEvent(projectData, defaultRules, shouldCreateCustomRule, ruleId);
                projectActions_1.default.createSuccess(projectData);
                const platformKey = platform || 'other';
                const nextUrl = `/${organization.slug}/${projectData.slug}/getting-started/${platformKey}/`;
                react_router_1.browserHistory.push(nextUrl);
            }
            catch (err) {
                this.setState({
                    inFlight: false,
                    error: err.responseJSON.detail,
                });
                // Only log this if the error is something other than:
                // * The user not having access to create a project, or,
                // * A project with that slug already exists
                if (err.status !== 403 && err.status !== 409) {
                    Sentry.withScope(scope => {
                        scope.setExtra('err', err);
                        scope.setExtra('props', this.props);
                        scope.setExtra('state', this.state);
                        Sentry.captureMessage('Project creation failed');
                    });
                }
            }
        });
        this.setPlatform = (platformId) => this.setState(({ projectName, platform }) => ({
            platform: platformId,
            projectName: !projectName || (platform && (0, getPlatformName_1.default)(platform) === projectName)
                ? (0, getPlatformName_1.default)(platformId) || ''
                : projectName,
        }));
        const { teams, location } = props;
        const { query } = location;
        const accessTeams = teams.filter((team) => team.hasAccess);
        const team = query.team || (accessTeams.length && accessTeams[0].slug);
        const platform = (0, getPlatformName_1.default)(query.platform) ? query.platform : '';
        this.state = {
            error: false,
            projectName: (0, getPlatformName_1.default)(platform) || '',
            team,
            platform,
            inFlight: false,
            dataFragment: undefined,
        };
    }
    get defaultCategory() {
        const { query } = this.props.location;
        return getCategoryName(query.category);
    }
    renderProjectForm() {
        const { organization } = this.props;
        const { projectName, platform, team } = this.state;
        const createProjectForm = (<CreateProjectForm onSubmit={this.createProject}>
        <div>
          <FormLabel>{(0, locale_1.t)('Project name')}</FormLabel>
          <ProjectNameInput>
            <StyledPlatformIcon platform={platform !== null && platform !== void 0 ? platform : ''}/>
            <input type="text" name="name" placeholder={(0, locale_1.t)('Project name')} autoComplete="off" value={projectName} onChange={e => this.setState({ projectName: (0, slugify_1.default)(e.target.value) })}/>
          </ProjectNameInput>
        </div>
        <div>
          <FormLabel>{(0, locale_1.t)('Team')}</FormLabel>
          <TeamSelectInput>
            <teamSelector_1.default name="select-team" clearable={false} value={team} placeholder={(0, locale_1.t)('Select a Team')} onChange={choice => this.setState({ team: choice.value })} teamFilter={(filterTeam) => filterTeam.hasAccess}/>
            <tooltip_1.default title={(0, locale_1.t)('Create a team')}>
              <button_1.default borderless data-test-id="create-team" type="button" icon={<icons_1.IconAdd isCircled/>} onClick={() => (0, modal_1.openCreateTeamModal)({
                organization,
                onClose: ({ slug }) => this.setState({ team: slug }),
            })}/>
            </tooltip_1.default>
          </TeamSelectInput>
        </div>
        <div>
          <button_1.default data-test-id="create-project" priority="primary" disabled={!this.canSubmitForm}>
            {(0, locale_1.t)('Create Project')}
          </button_1.default>
        </div>
      </CreateProjectForm>);
        return (<React.Fragment>
        <pageHeading_1.default withMargins>{(0, locale_1.t)('Give your project a name')}</pageHeading_1.default>
        {createProjectForm}
      </React.Fragment>);
    }
    get canSubmitForm() {
        var _a;
        const { projectName, team, inFlight } = this.state;
        const { shouldCreateCustomRule, conditions } = this.state.dataFragment || {};
        return (!inFlight &&
            team &&
            projectName !== '' &&
            (!shouldCreateCustomRule || ((_a = conditions === null || conditions === void 0 ? void 0 : conditions.every) === null || _a === void 0 ? void 0 : _a.call(conditions, condition => condition.value))));
    }
    trackIssueAlertOptionSelectedEvent(projectData, isDefaultRules, shouldCreateCustomRule, ruleId) {
        const { organization } = this.props;
        let data = {
            eventKey: 'new_project.alert_rule_selected',
            eventName: 'New Project Alert Rule Selected',
            organization_id: organization.id,
            project_id: projectData.id,
            rule_type: isDefaultRules
                ? 'Default'
                : shouldCreateCustomRule
                    ? 'Custom'
                    : 'No Rule',
        };
        if (ruleId !== undefined) {
            data = Object.assign(Object.assign({}, data), { custom_rule_id: ruleId });
        }
        (0, analytics_1.trackAnalyticsEvent)(data);
    }
    render() {
        const { platform, error } = this.state;
        return (<React.Fragment>
        {error && <alert_1.default type="error">{error}</alert_1.default>}

        <div data-test-id="onboarding-info">
          <pageHeading_1.default withMargins>{(0, locale_1.t)('Create a new Project')}</pageHeading_1.default>
          <HelpText>
            {(0, locale_1.t)(`Projects allow you to scope error and transaction events to a specific
               application in your organization. For example, you might have separate
               projects for your API server and frontend client.`)}
          </HelpText>
          <pageHeading_1.default withMargins>{(0, locale_1.t)('Choose a platform')}</pageHeading_1.default>
          <platformPicker_1.default platform={platform} defaultCategory={this.defaultCategory} setPlatform={this.setPlatform} organization={this.props.organization} showOther/>
          <issueAlertOptions_1.default onChange={updatedData => {
                this.setState({ dataFragment: updatedData });
            }}/>
          {this.renderProjectForm()}
        </div>
      </React.Fragment>);
    }
}
exports.CreateProject = CreateProject;
exports.default = (0, withApi_1.default)((0, react_router_1.withRouter)((0, withOrganization_1.default)((0, withTeams_1.default)(CreateProject))));
const CreateProjectForm = (0, styled_1.default)('form') `
  display: grid;
  grid-template-columns: 300px minmax(250px, max-content) max-content;
  grid-gap: ${(0, space_1.default)(2)};
  align-items: end;
  padding: ${(0, space_1.default)(3)} 0;
  box-shadow: 0 -1px 0 rgba(0, 0, 0, 0.1);
  background: ${p => p.theme.background};
`;
const FormLabel = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeExtraLarge};
  margin-bottom: ${(0, space_1.default)(1)};
`;
const StyledPlatformIcon = (0, styled_1.default)(platformicons_1.PlatformIcon) `
  margin-right: ${(0, space_1.default)(1)};
`;
const ProjectNameInput = (0, styled_1.default)('div') `
  ${p => (0, input_1.inputStyles)(p)};
  padding: 5px 10px;
  display: flex;
  align-items: center;

  input {
    background: ${p => p.theme.background};
    border: 0;
    outline: 0;
    flex: 1;
  }
`;
const TeamSelectInput = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: 1fr min-content;
  align-items: center;
`;
const HelpText = (0, styled_1.default)('p') `
  color: ${p => p.theme.subText};
  max-width: 760px;
`;
//# sourceMappingURL=createProject.jsx.map