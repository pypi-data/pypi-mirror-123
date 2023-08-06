Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reflux_1 = (0, tslib_1.__importDefault)(require("reflux"));
const teamActions_1 = (0, tslib_1.__importDefault)(require("app/actions/teamActions"));
const MAX_TEAMS = 100;
const teamStoreConfig = {
    initialized: false,
    state: {
        teams: [],
        loadedUserTeams: false,
        loading: true,
        hasMore: null,
    },
    init() {
        this.reset();
        this.listenTo(teamActions_1.default.createTeamSuccess, this.onCreateSuccess);
        this.listenTo(teamActions_1.default.fetchDetailsSuccess, this.onUpdateSuccess);
        this.listenTo(teamActions_1.default.loadTeams, this.loadInitialData);
        this.listenTo(teamActions_1.default.loadUserTeams, this.loadUserTeams);
        this.listenTo(teamActions_1.default.removeTeamSuccess, this.onRemoveSuccess);
        this.listenTo(teamActions_1.default.updateSuccess, this.onUpdateSuccess);
    },
    reset() {
        this.state = { teams: [], loadedUserTeams: false, loading: true, hasMore: null };
    },
    loadInitialData(items, hasMore = null) {
        this.initialized = true;
        this.state = {
            teams: items.sort((a, b) => a.slug.localeCompare(b.slug)),
            // TODO(davidenwang): Replace with a more reliable way of knowing when we have loaded all teams
            loadedUserTeams: items.length < MAX_TEAMS,
            loading: false,
            hasMore,
        };
        this.trigger(new Set(items.map(item => item.id)));
    },
    loadUserTeams(userTeams) {
        const teamIdMap = this.state.teams.reduce((acc, team) => {
            acc[team.id] = team;
            return acc;
        }, {});
        // Replace or insert new user teams
        userTeams.reduce((acc, userTeam) => {
            acc[userTeam.id] = userTeam;
            return acc;
        }, teamIdMap);
        const teams = Object.values(teamIdMap).sort((a, b) => a.slug.localeCompare(b.slug));
        this.state = Object.assign(Object.assign({}, this.state), { loadedUserTeams: true, teams });
        this.trigger(new Set(Object.keys(teamIdMap)));
    },
    onUpdateSuccess(itemId, response) {
        if (!response) {
            return;
        }
        const item = this.getBySlug(itemId);
        if (!item) {
            this.state = Object.assign(Object.assign({}, this.state), { teams: [...this.state.teams, response] });
            this.trigger(new Set([itemId]));
            return;
        }
        // Slug was changed
        // Note: This is the proper way to handle slug changes but unfortunately not all of our
        // components use stores correctly. To be safe reload browser :((
        if (response.slug !== itemId) {
            // Replace the team
            const teams = [...this.state.teams.filter(({ slug }) => slug !== itemId), response];
            this.state = Object.assign(Object.assign({}, this.state), { teams });
            this.trigger(new Set([response.slug]));
            return;
        }
        const newTeams = [...this.state.teams];
        const index = newTeams.findIndex(team => team.slug === response.slug);
        newTeams[index] = response;
        this.state = Object.assign(Object.assign({}, this.state), { teams: newTeams });
        this.trigger(new Set([itemId]));
    },
    onRemoveSuccess(slug) {
        const { teams } = this.state;
        this.loadInitialData(teams.filter(team => team.slug !== slug));
    },
    onCreateSuccess(team) {
        this.loadInitialData([...this.state.teams, team]);
    },
    getState() {
        return this.state;
    },
    getById(id) {
        const { teams } = this.state;
        return teams.find(item => item.id.toString() === id.toString()) || null;
    },
    getBySlug(slug) {
        const { teams } = this.state;
        return teams.find(item => item.slug === slug) || null;
    },
    getAll() {
        return this.state.teams;
    },
};
const TeamStore = reflux_1.default.createStore(teamStoreConfig);
exports.default = TeamStore;
//# sourceMappingURL=teamStore.jsx.map