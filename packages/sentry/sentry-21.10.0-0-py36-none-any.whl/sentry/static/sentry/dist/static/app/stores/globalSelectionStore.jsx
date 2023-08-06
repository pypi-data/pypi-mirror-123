Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const reflux_1 = (0, tslib_1.__importDefault)(require("reflux"));
const globalSelectionActions_1 = (0, tslib_1.__importDefault)(require("app/actions/globalSelectionActions"));
const utils_1 = require("app/components/organizations/globalSelectionHeader/utils");
const globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
const organizationsStore_1 = (0, tslib_1.__importDefault)(require("app/stores/organizationsStore"));
const isEqualWithDates_1 = require("app/utils/isEqualWithDates");
const localStorage_1 = (0, tslib_1.__importDefault)(require("app/utils/localStorage"));
const storeConfig = {
    state: (0, utils_1.getDefaultSelection)(),
    init() {
        this.reset(this.state);
        this.listenTo(globalSelectionActions_1.default.reset, this.onReset);
        this.listenTo(globalSelectionActions_1.default.initializeUrlState, this.onInitializeUrlState);
        this.listenTo(globalSelectionActions_1.default.setOrganization, this.onSetOrganization);
        this.listenTo(globalSelectionActions_1.default.save, this.onSave);
        this.listenTo(globalSelectionActions_1.default.updateProjects, this.updateProjects);
        this.listenTo(globalSelectionActions_1.default.updateDateTime, this.updateDateTime);
        this.listenTo(globalSelectionActions_1.default.updateEnvironments, this.updateEnvironments);
    },
    reset(state) {
        // Has passed the enforcement state
        this._hasEnforcedProject = false;
        this._hasInitialState = false;
        this.state = state || (0, utils_1.getDefaultSelection)();
    },
    isReady() {
        return this._hasInitialState;
    },
    onSetOrganization(organization) {
        this.organization = organization;
    },
    /**
     * Initializes the global selection store data
     */
    onInitializeUrlState(newSelection) {
        this._hasInitialState = true;
        this.state = newSelection;
        this.trigger(this.get());
    },
    get() {
        return {
            selection: this.state,
            isReady: this.isReady(),
        };
    },
    onReset() {
        this.reset();
        this.trigger(this.get());
    },
    updateProjects(projects = [], environments = null) {
        if ((0, isEqual_1.default)(this.state.projects, projects)) {
            return;
        }
        this.state = Object.assign(Object.assign({}, this.state), { projects, environments: environments === null ? this.state.environments : environments });
        this.trigger(this.get());
    },
    updateDateTime(datetime) {
        if ((0, isEqualWithDates_1.isEqualWithDates)(this.state.datetime, datetime)) {
            return;
        }
        this.state = Object.assign(Object.assign({}, this.state), { datetime });
        this.trigger(this.get());
    },
    updateEnvironments(environments) {
        if ((0, isEqual_1.default)(this.state.environments, environments)) {
            return;
        }
        this.state = Object.assign(Object.assign({}, this.state), { environments: environments !== null && environments !== void 0 ? environments : [] });
        this.trigger(this.get());
    },
    /**
     * Save to local storage when user explicitly changes header values.
     *
     * e.g. if localstorage is empty, user loads issue details for project "foo"
     * this should not consider "foo" as last used and should not save to local storage.
     *
     * However, if user then changes environment, it should...? Currently it will
     * save the current project alongside environment to local storage. It's debatable if
     * this is the desired behavior.
     */
    onSave(updateObj) {
        // Do nothing if no org is loaded or user is not an org member. Only
        // organizations that a user has membership in will be available via the
        // organizations store
        if (!this.organization || !organizationsStore_1.default.get(this.organization.slug)) {
            return;
        }
        const { project, environment } = updateObj;
        const validatedProject = typeof project === 'string' ? [Number(project)] : project;
        const validatedEnvironment = typeof environment === 'string' ? [environment] : environment;
        try {
            const localStorageKey = `${globalSelectionHeader_1.LOCAL_STORAGE_KEY}:${this.organization.slug}`;
            const dataToSave = {
                projects: validatedProject || this.selection.projects,
                environments: validatedEnvironment || this.selection.environments,
            };
            localStorage_1.default.setItem(localStorageKey, JSON.stringify(dataToSave));
        }
        catch (ex) {
            // Do nothing
        }
    },
};
const GlobalSelectionStore = reflux_1.default.createStore(storeConfig);
exports.default = GlobalSelectionStore;
//# sourceMappingURL=globalSelectionStore.jsx.map