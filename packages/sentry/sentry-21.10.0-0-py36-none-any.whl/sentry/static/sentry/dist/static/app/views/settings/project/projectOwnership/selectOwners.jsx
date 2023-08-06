Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_dom_1 = (0, tslib_1.__importDefault)(require("react-dom"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const debounce_1 = (0, tslib_1.__importDefault)(require("lodash/debounce"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const projects_1 = require("app/actionCreators/projects");
const actorAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/actorAvatar"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const multiSelectControl_1 = (0, tslib_1.__importDefault)(require("app/components/forms/multiSelectControl"));
const idBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const memberListStore_1 = (0, tslib_1.__importDefault)(require("app/stores/memberListStore"));
const projectsStore_1 = (0, tslib_1.__importDefault)(require("app/stores/projectsStore"));
const teamStore_1 = (0, tslib_1.__importDefault)(require("app/stores/teamStore"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
function ValueComponent({ data, removeProps }) {
    return (<ValueWrapper onClick={removeProps.onClick}>
      <actorAvatar_1.default actor={data.actor} size={28}/>
    </ValueWrapper>);
}
const getSearchKeyForUser = (user) => `${user.email && user.email.toLowerCase()} ${user.name && user.name.toLowerCase()}`;
class SelectOwners extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            loading: false,
            inputValue: '',
        };
        this.selectRef = React.createRef();
        this.renderUserBadge = (user) => (<idBadge_1.default avatarSize={24} user={user} hideEmail useLink={false}/>);
        this.createMentionableUser = (user) => ({
            value: (0, utils_1.buildUserId)(user.id),
            label: this.renderUserBadge(user),
            searchKey: getSearchKeyForUser(user),
            actor: {
                type: 'user',
                id: user.id,
                name: user.name,
            },
        });
        this.createUnmentionableUser = ({ user }) => (Object.assign(Object.assign({}, this.createMentionableUser(user)), { disabled: true, label: (<DisabledLabel>
        <tooltip_1.default position="left" title={(0, locale_1.t)('%s is not a member of project', user.name || user.email)}>
          {this.renderUserBadge(user)}
        </tooltip_1.default>
      </DisabledLabel>) }));
        this.createMentionableTeam = (team) => ({
            value: (0, utils_1.buildTeamId)(team.id),
            label: <idBadge_1.default team={team}/>,
            searchKey: `#${team.slug}`,
            actor: {
                type: 'team',
                id: team.id,
                name: team.slug,
            },
        });
        this.createUnmentionableTeam = (team) => {
            const { organization } = this.props;
            const canAddTeam = organization.access.includes('project:write');
            return Object.assign(Object.assign({}, this.createMentionableTeam(team)), { disabled: true, label: (<Container>
          <DisabledLabel>
            <tooltip_1.default position="left" title={(0, locale_1.t)('%s is not a member of project', `#${team.slug}`)}>
              <idBadge_1.default team={team}/>
            </tooltip_1.default>
          </DisabledLabel>
          <tooltip_1.default title={canAddTeam
                        ? (0, locale_1.t)('Add %s to project', `#${team.slug}`)
                        : (0, locale_1.t)('You do not have permission to add team to project.')}>
            <AddToProjectButton size="zero" borderless disabled={!canAddTeam} onClick={this.handleAddTeamToProject.bind(this, team)} icon={<icons_1.IconAdd isCircled/>}/>
          </tooltip_1.default>
        </Container>) });
        };
        this.handleChange = (newValue) => {
            this.props.onChange(newValue);
        };
        this.handleInputChange = (inputValue) => {
            this.setState({ inputValue });
            if (this.props.onInputChange) {
                this.props.onInputChange(inputValue);
            }
        };
        this.queryMembers = (0, debounce_1.default)((query, cb) => {
            const { api, organization } = this.props;
            // Because this function is debounced, the component can potentially be
            // unmounted before this fires, in which case, `this.api` is null
            if (!api) {
                return null;
            }
            return api
                .requestPromise(`/organizations/${organization.slug}/members/`, {
                query: { query },
            })
                .then((data) => cb(null, data), err => cb(err));
        }, 250);
        this.handleLoadOptions = () => {
            const usersInProject = this.getMentionableUsers();
            const teamsInProject = this.getMentionableTeams();
            const teamsNotInProject = this.getTeamsNotInProject(teamsInProject);
            const usersInProjectById = usersInProject.map(({ actor }) => actor.id);
            // Return a promise for `react-select`
            return new Promise((resolve, reject) => {
                this.queryMembers(this.state.inputValue, (err, result) => {
                    if (err) {
                        reject(err);
                    }
                    else {
                        resolve(result);
                    }
                });
            })
                .then(members => 
            // Be careful here as we actually want the `users` object, otherwise it means user
            // has not registered for sentry yet, but has been invited
            members
                ? members
                    .filter(({ user }) => user && usersInProjectById.indexOf(user.id) === -1)
                    .map(this.createUnmentionableUser)
                : [])
                .then(members => {
                return [...usersInProject, ...teamsInProject, ...teamsNotInProject, ...members];
            });
        };
    }
    componentDidUpdate(prevProps) {
        // Once a team has been added to the project the menu can be closed.
        if (!(0, isEqual_1.default)(this.props.projects, prevProps.projects)) {
            this.closeSelectMenu();
        }
    }
    getMentionableUsers() {
        return memberListStore_1.default.getAll().map(this.createMentionableUser);
    }
    getMentionableTeams() {
        const { project } = this.props;
        const projectData = projectsStore_1.default.getBySlug(project.slug);
        if (!projectData) {
            return [];
        }
        return projectData.teams.map(this.createMentionableTeam);
    }
    /**
     * Get list of teams that are not in the current project, for use in `MultiSelectMenu`
     */
    getTeamsNotInProject(teamsInProject = []) {
        const teams = teamStore_1.default.getAll() || [];
        const excludedTeamIds = teamsInProject.map(({ actor }) => actor.id);
        return teams
            .filter(team => excludedTeamIds.indexOf(team.id) === -1)
            .map(this.createUnmentionableTeam);
    }
    /**
     * Closes the select menu by blurring input if possible since that seems to be the only
     * way to close it.
     */
    closeSelectMenu() {
        var _a;
        // Close select menu
        if (this.selectRef.current) {
            // eslint-disable-next-line react/no-find-dom-node
            const node = react_dom_1.default.findDOMNode(this.selectRef.current);
            const input = (_a = node) === null || _a === void 0 ? void 0 : _a.querySelector('.Select-input input');
            if (input) {
                // I don't think there's another way to close `react-select`
                input.blur();
            }
        }
    }
    handleAddTeamToProject(team) {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, organization, project, value } = this.props;
            // Copy old value
            const oldValue = [...value];
            // Optimistic update
            this.props.onChange([...this.props.value, this.createMentionableTeam(team)]);
            try {
                // Try to add team to project
                // Note: we can't close select menu here because we have to wait for ProjectsStore to update first
                // The reason for this is because we have little control over `react-select`'s `AsyncSelect`
                // We can't control when `handleLoadOptions` gets called, but it gets called when select closes, so
                // wait for store to update before closing the menu. Otherwise, we'll have stale items in the select menu
                yield (0, projects_1.addTeamToProject)(api, organization.slug, project.slug, team);
            }
            catch (err) {
                // Unable to add team to project, revert select menu value
                this.props.onChange(oldValue);
                this.closeSelectMenu();
            }
        });
    }
    render() {
        return (<multiSelectControl_1.default name="owners" filterOption={(option, filterText) => option.data.searchKey.indexOf(filterText) > -1} ref={this.selectRef} loadOptions={this.handleLoadOptions} defaultOptions async clearable disabled={this.props.disabled} cache={false} placeholder={(0, locale_1.t)('owners')} components={{
                MultiValue: ValueComponent,
            }} onInputChange={this.handleInputChange} onChange={this.handleChange} value={this.props.value} css={{ width: 200 }}/>);
    }
}
exports.default = (0, withApi_1.default)((0, withProjects_1.default)(SelectOwners));
const Container = (0, styled_1.default)('div') `
  display: flex;
  justify-content: space-between;
`;
const DisabledLabel = (0, styled_1.default)('div') `
  opacity: 0.5;
  overflow: hidden; /* Needed so that "Add to team" button can fit */
`;
const AddToProjectButton = (0, styled_1.default)(button_1.default) `
  flex-shrink: 0;
`;
const ValueWrapper = (0, styled_1.default)('a') `
  margin-right: ${(0, space_1.default)(0.5)};
`;
//# sourceMappingURL=selectOwners.jsx.map