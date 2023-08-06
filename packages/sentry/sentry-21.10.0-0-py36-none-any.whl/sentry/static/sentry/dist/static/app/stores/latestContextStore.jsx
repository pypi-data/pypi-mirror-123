Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reflux_1 = (0, tslib_1.__importDefault)(require("reflux"));
const navigationActions_1 = (0, tslib_1.__importDefault)(require("app/actions/navigationActions"));
const organizationActions_1 = (0, tslib_1.__importDefault)(require("app/actions/organizationActions"));
const organizationsActions_1 = (0, tslib_1.__importDefault)(require("app/actions/organizationsActions"));
const projectActions_1 = (0, tslib_1.__importDefault)(require("app/actions/projectActions"));
/**
 * Keeps track of last usable project/org this currently won't track when users
 * navigate out of a org/project completely, it tracks only if a user switches
 * into a new org/project.
 *
 * Only keep slug so that people don't get the idea to access org/project data
 * here Org/project data is currently in organizationsStore/projectsStore
 */
const storeConfig = {
    state: {
        project: null,
        lastProject: null,
        organization: null,
        environment: null,
        lastRoute: null,
    },
    get() {
        return this.state;
    },
    init() {
        this.reset();
        this.listenTo(projectActions_1.default.setActive, this.onSetActiveProject);
        this.listenTo(projectActions_1.default.updateSuccess, this.onUpdateProject);
        this.listenTo(organizationsActions_1.default.setActive, this.onSetActiveOrganization);
        this.listenTo(organizationsActions_1.default.update, this.onUpdateOrganization);
        this.listenTo(organizationActions_1.default.update, this.onUpdateOrganization);
        this.listenTo(navigationActions_1.default.setLastRoute, this.onSetLastRoute);
    },
    reset() {
        this.state = {
            project: null,
            lastProject: null,
            organization: null,
            environment: null,
            lastRoute: null,
        };
        return this.state;
    },
    onSetLastRoute(route) {
        this.state = Object.assign(Object.assign({}, this.state), { lastRoute: route });
        this.trigger(this.state);
    },
    onUpdateOrganization(org) {
        // Don't do anything if base/target orgs are falsey
        if (!this.state.organization) {
            return;
        }
        if (!org) {
            return;
        }
        // Check to make sure current active org is what has been updated
        if (org.slug !== this.state.organization.slug) {
            return;
        }
        this.state = Object.assign(Object.assign({}, this.state), { organization: org });
        this.trigger(this.state);
    },
    onSetActiveOrganization(org) {
        if (!org) {
            this.state = Object.assign(Object.assign({}, this.state), { organization: null, project: null });
        }
        else if (!this.state.organization || this.state.organization.slug !== org.slug) {
            // Update only if different
            this.state = Object.assign(Object.assign({}, this.state), { organization: org, project: null });
        }
        this.trigger(this.state);
    },
    onSetActiveProject(project) {
        if (!project) {
            this.state = Object.assign(Object.assign({}, this.state), { lastProject: this.state.project, project: null });
        }
        else if (!this.state.project || this.state.project.slug !== project.slug) {
            // Update only if different
            this.state = Object.assign(Object.assign({}, this.state), { lastProject: this.state.project, project });
        }
        this.trigger(this.state);
    },
    onUpdateProject(project) {
        this.state = Object.assign(Object.assign({}, this.state), { project });
        this.trigger(this.state);
    },
};
const LatestContextStore = reflux_1.default.createStore(storeConfig);
exports.default = LatestContextStore;
//# sourceMappingURL=latestContextStore.jsx.map