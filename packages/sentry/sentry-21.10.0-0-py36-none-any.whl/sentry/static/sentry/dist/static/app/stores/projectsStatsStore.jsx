Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reflux_1 = (0, tslib_1.__importDefault)(require("reflux"));
const projectActions_1 = (0, tslib_1.__importDefault)(require("app/actions/projectActions"));
/**
 * This is a store specifically used by the dashboard, so that we can
 * clear the store when the Dashboard unmounts
 * (as to not disrupt ProjectsStore which a lot more components use)
 */
const storeConfig = {
    itemsBySlug: {},
    init() {
        this.reset();
        this.listenTo(projectActions_1.default.loadStatsForProjectSuccess, this.onStatsLoadSuccess);
        this.listenTo(projectActions_1.default.update, this.onUpdate);
        this.listenTo(projectActions_1.default.updateError, this.onUpdateError);
    },
    getInitialState() {
        return this.itemsBySlug;
    },
    reset() {
        this.itemsBySlug = {};
        this.updatingItems = new Map();
    },
    onStatsLoadSuccess(projects) {
        projects.forEach(project => {
            this.itemsBySlug[project.slug] = project;
        });
        this.trigger(this.itemsBySlug);
    },
    /**
     * Optimistic updates
     * @param projectSlug Project slug
     * @param data Project data
     */
    onUpdate(projectSlug, data) {
        const project = this.getBySlug(projectSlug);
        this.updatingItems.set(projectSlug, project);
        if (!project) {
            return;
        }
        const newProject = Object.assign(Object.assign({}, project), data);
        this.itemsBySlug = Object.assign(Object.assign({}, this.itemsBySlug), { [project.slug]: newProject });
        this.trigger(this.itemsBySlug);
    },
    onUpdateSuccess(data) {
        // Remove project from updating map
        this.updatingItems.delete(data.slug);
    },
    /**
     * Revert project data when there was an error updating project details
     * @param err Error object
     * @param data Previous project data
     */
    onUpdateError(_err, projectSlug) {
        const project = this.updatingItems.get(projectSlug);
        if (!project) {
            return;
        }
        this.updatingItems.delete(projectSlug);
        // Restore old project
        this.itemsBySlug = Object.assign(Object.assign({}, this.itemsBySlug), { [project.slug]: Object.assign({}, project) });
        this.trigger(this.itemsBySlug);
    },
    getAll() {
        return this.itemsBySlug;
    },
    getBySlug(slug) {
        return this.itemsBySlug[slug];
    },
};
const ProjectsStatsStore = reflux_1.default.createStore(storeConfig);
exports.default = ProjectsStatsStore;
//# sourceMappingURL=projectsStatsStore.jsx.map