Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reflux_1 = (0, tslib_1.__importDefault)(require("reflux"));
const projectActions_1 = (0, tslib_1.__importDefault)(require("app/actions/projectActions"));
const teamActions_1 = (0, tslib_1.__importDefault)(require("app/actions/teamActions"));
const storeConfig = {
    itemsById: {},
    loading: true,
    init() {
        this.reset();
        this.listenTo(projectActions_1.default.addTeamSuccess, this.onAddTeam);
        this.listenTo(projectActions_1.default.changeSlug, this.onChangeSlug);
        this.listenTo(projectActions_1.default.createSuccess, this.onCreateSuccess);
        this.listenTo(projectActions_1.default.loadProjects, this.loadInitialData);
        this.listenTo(projectActions_1.default.loadStatsSuccess, this.onStatsLoadSuccess);
        this.listenTo(projectActions_1.default.removeTeamSuccess, this.onRemoveTeam);
        this.listenTo(projectActions_1.default.reset, this.reset);
        this.listenTo(projectActions_1.default.updateSuccess, this.onUpdateSuccess);
        this.listenTo(teamActions_1.default.removeTeamSuccess, this.onDeleteTeam);
    },
    reset() {
        this.itemsById = {};
        this.loading = true;
    },
    loadInitialData(items) {
        this.itemsById = items.reduce((map, project) => {
            map[project.id] = project;
            return map;
        }, {});
        this.loading = false;
        this.trigger(new Set(Object.keys(this.itemsById)));
    },
    onChangeSlug(prevSlug, newSlug) {
        const prevProject = this.getBySlug(prevSlug);
        // This shouldn't happen
        if (!prevProject) {
            return;
        }
        const newProject = Object.assign(Object.assign({}, prevProject), { slug: newSlug });
        this.itemsById = Object.assign(Object.assign({}, this.itemsById), { [newProject.id]: newProject });
        // Ideally we'd always trigger this.itemsById, but following existing patterns
        // so we don't break things
        this.trigger(new Set([prevProject.id]));
    },
    onCreateSuccess(project) {
        this.itemsById = Object.assign(Object.assign({}, this.itemsById), { [project.id]: project });
        this.trigger(new Set([project.id]));
    },
    onUpdateSuccess(data) {
        const project = this.getById(data.id);
        if (!project) {
            return;
        }
        const newProject = Object.assign({}, project, data);
        this.itemsById = Object.assign(Object.assign({}, this.itemsById), { [project.id]: newProject });
        this.trigger(new Set([data.id]));
    },
    onStatsLoadSuccess(data) {
        const touchedIds = [];
        Object.entries(data || {}).forEach(([projectId, stats]) => {
            if (projectId in this.itemsById) {
                this.itemsById[projectId].stats = stats;
                touchedIds.push(projectId);
            }
        });
        this.trigger(new Set(touchedIds));
    },
    /**
     * Listener for when a team is completely removed
     *
     * @param teamSlug Team Slug
     */
    onDeleteTeam(teamSlug) {
        // Look for team in all projects
        const projectIds = this.getWithTeam(teamSlug).map(projectWithTeam => {
            this.removeTeamFromProject(teamSlug, projectWithTeam);
            return projectWithTeam.id;
        });
        this.trigger(new Set([projectIds]));
    },
    onRemoveTeam(teamSlug, projectSlug) {
        const project = this.getBySlug(projectSlug);
        if (!project) {
            return;
        }
        this.removeTeamFromProject(teamSlug, project);
        this.trigger(new Set([project.id]));
    },
    onAddTeam(team, projectSlug) {
        const project = this.getBySlug(projectSlug);
        // Don't do anything if we can't find a project
        if (!project) {
            return;
        }
        this.itemsById = Object.assign(Object.assign({}, this.itemsById), { [project.id]: Object.assign(Object.assign({}, project), { teams: [...project.teams, team] }) });
        this.trigger(new Set([project.id]));
    },
    // Internal method, does not trigger
    removeTeamFromProject(teamSlug, project) {
        const newTeams = project.teams.filter(({ slug }) => slug !== teamSlug);
        this.itemsById = Object.assign(Object.assign({}, this.itemsById), { [project.id]: Object.assign(Object.assign({}, project), { teams: newTeams }) });
    },
    /**
     * Returns a list of projects that has the specified team
     *
     * @param {String} teamSlug Slug of team to find in projects
     */
    getWithTeam(teamSlug) {
        return this.getAll().filter(({ teams }) => teams.find(({ slug }) => slug === teamSlug));
    },
    isLoading() {
        return this.loading;
    },
    getAll() {
        return Object.values(this.itemsById).sort((a, b) => a.slug.localeCompare(b.slug));
    },
    getById(id) {
        return this.getAll().find(project => project.id === id);
    },
    getBySlug(slug) {
        return this.getAll().find(project => project.slug === slug);
    },
    getState() {
        return {
            projects: this.getAll(),
            loading: this.loading,
        };
    },
};
const ProjectsStore = reflux_1.default.createStore(storeConfig);
exports.default = ProjectsStore;
//# sourceMappingURL=projectsStore.jsx.map