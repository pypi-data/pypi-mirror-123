Object.defineProperty(exports, "__esModule", { value: true });
exports.Consumer = exports.Provider = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const performance_1 = require("app/actionCreators/performance");
const locale_1 = require("app/locale");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const TeamKeyTransactionsManagerContext = (0, react_1.createContext)({
    teams: [],
    isLoading: false,
    error: null,
    counts: null,
    getKeyedTeams: () => null,
    handleToggleKeyTransaction: () => { },
});
class UnwrappedProvider extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            keyFetchID: null,
            isLoading: true,
            error: null,
            teamKeyTransactions: [],
        };
        this.getKeyedTeams = (projectId, transactionName) => {
            const { teamKeyTransactions } = this.state;
            const keyedTeams = new Set();
            teamKeyTransactions.forEach(({ team, keyed }) => {
                const isKeyedByTeam = keyed.find(keyedTeam => keyedTeam.project_id === projectId && keyedTeam.transaction === transactionName);
                if (isKeyedByTeam) {
                    keyedTeams.add(team);
                }
            });
            return keyedTeams;
        };
        this.handleToggleKeyTransaction = (selection) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            var _a, _b;
            const { api, organization } = this.props;
            const { teamKeyTransactions } = this.state;
            const { action, project, transactionName, teamIds } = selection;
            const isKeyTransaction = action === 'unkey';
            const teamIdSet = new Set(teamIds);
            const newTeamKeyTransactions = teamKeyTransactions.map(({ team, count, keyed }) => {
                if (!teamIdSet.has(team)) {
                    return { team, count, keyed };
                }
                if (isKeyTransaction) {
                    return {
                        team,
                        count: count - 1,
                        keyed: keyed.filter(keyTransaction => keyTransaction.project_id !== project.id ||
                            keyTransaction.transaction !== transactionName),
                    };
                }
                else {
                    return {
                        team,
                        count: count + 1,
                        keyed: [
                            ...keyed,
                            {
                                project_id: project.id,
                                transaction: transactionName,
                            },
                        ],
                    };
                }
            });
            try {
                yield (0, performance_1.toggleKeyTransaction)(api, isKeyTransaction, organization.slug, [project.id], transactionName, teamIds);
                this.setState({ teamKeyTransactions: newTeamKeyTransactions });
            }
            catch (err) {
                this.setState({
                    error: (_b = (_a = err.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) !== null && _b !== void 0 ? _b : null,
                });
            }
        });
    }
    componentDidMount() {
        this.fetchData();
    }
    componentDidUpdate(prevProps) {
        const orgSlugChanged = prevProps.organization.slug !== this.props.organization.slug;
        const selectedTeamsChanged = !(0, isEqual_1.default)(prevProps.selectedTeams, this.props.selectedTeams);
        const selectedProjectsChanged = !(0, isEqual_1.default)(prevProps.selectedProjects, this.props.selectedProjects);
        if (orgSlugChanged || selectedTeamsChanged || selectedProjectsChanged) {
            this.fetchData();
        }
    }
    fetchData() {
        var _a, _b;
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, organization, selectedTeams, selectedProjects } = this.props;
            const keyFetchID = Symbol('keyFetchID');
            this.setState({ isLoading: true, keyFetchID });
            let teamKeyTransactions = [];
            let error = null;
            try {
                teamKeyTransactions = yield (0, performance_1.fetchTeamKeyTransactions)(api, organization.slug, selectedTeams, selectedProjects);
            }
            catch (err) {
                error = (_b = (_a = err.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) !== null && _b !== void 0 ? _b : (0, locale_1.t)('Error fetching team key transactions');
            }
            this.setState({
                isLoading: false,
                keyFetchID: undefined,
                error,
                teamKeyTransactions,
            });
        });
    }
    getCounts() {
        const { teamKeyTransactions } = this.state;
        const counts = new Map();
        teamKeyTransactions.forEach(({ team, count }) => {
            counts.set(team, count);
        });
        return counts;
    }
    render() {
        const { teams } = this.props;
        const { isLoading, error } = this.state;
        const childrenProps = {
            teams,
            isLoading,
            error,
            counts: this.getCounts(),
            getKeyedTeams: this.getKeyedTeams,
            handleToggleKeyTransaction: this.handleToggleKeyTransaction,
        };
        return (<TeamKeyTransactionsManagerContext.Provider value={childrenProps}>
        {this.props.children}
      </TeamKeyTransactionsManagerContext.Provider>);
    }
}
exports.Provider = (0, withApi_1.default)(UnwrappedProvider);
exports.Consumer = TeamKeyTransactionsManagerContext.Consumer;
//# sourceMappingURL=teamKeyTransactionsManager.jsx.map