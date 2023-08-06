Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const getDisplayName_1 = (0, tslib_1.__importDefault)(require("app/utils/getDisplayName"));
const getProjectsByTeams_1 = (0, tslib_1.__importDefault)(require("app/utils/getProjectsByTeams"));
const analytics_1 = require("./analytics");
const withTeamsForUser = (WrappedComponent) => { var _a; return _a = class extends React.Component {
        constructor() {
            super(...arguments);
            this.state = {
                teams: [],
                loadingTeams: true,
                error: null,
            };
        }
        componentDidMount() {
            this.fetchTeams();
        }
        fetchTeams() {
            return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
                this.setState({
                    loadingTeams: true,
                });
                try {
                    analytics_1.metric.mark({ name: 'user-teams-fetch-start' });
                    const teamsWithProjects = yield this.props.api.requestPromise(this.getUsersTeamsEndpoint());
                    this.setState({
                        teams: teamsWithProjects,
                        loadingTeams: false,
                    }, () => {
                        analytics_1.metric.measure({
                            name: 'app.component.perf',
                            start: 'user-teams-fetch-start',
                            data: {
                                name: 'user-teams',
                                route: '/organizations/:orgid/user-teams',
                                organization_id: parseInt(this.props.organization.id, 10),
                            },
                        });
                    });
                }
                catch (error) {
                    this.setState({
                        error,
                        loadingTeams: false,
                    });
                }
            });
        }
        populateTeamsWithProjects(teams, projects) {
            const { isSuperuser } = configStore_1.default.get('user');
            const { projectsByTeam } = (0, getProjectsByTeams_1.default)(teams, projects, isSuperuser);
            const teamsWithProjects = teams.map(team => {
                const teamProjects = projectsByTeam[team.slug] || [];
                return Object.assign(Object.assign({}, team), { projects: teamProjects });
            });
            this.setState({
                teams: teamsWithProjects,
                loadingTeams: false,
            });
        }
        getUsersTeamsEndpoint() {
            return `/organizations/${this.props.organization.slug}/user-teams/`;
        }
        render() {
            return <WrappedComponent {...this.props} {...this.state}/>;
        }
    },
    _a.displayName = `withUsersTeams(${(0, getDisplayName_1.default)(WrappedComponent)})`,
    _a; };
exports.default = withTeamsForUser;
//# sourceMappingURL=withTeamsForUser.jsx.map