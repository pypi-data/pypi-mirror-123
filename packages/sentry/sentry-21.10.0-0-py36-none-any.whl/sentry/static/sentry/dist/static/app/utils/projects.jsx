Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const memoize_1 = (0, tslib_1.__importDefault)(require("lodash/memoize"));
const partition_1 = (0, tslib_1.__importDefault)(require("lodash/partition"));
const uniqBy_1 = (0, tslib_1.__importDefault)(require("lodash/uniqBy"));
const projectActions_1 = (0, tslib_1.__importDefault)(require("app/actions/projectActions"));
const projectsStore_1 = (0, tslib_1.__importDefault)(require("app/stores/projectsStore"));
const utils_1 = require("app/utils");
const parseLinkHeader_1 = (0, tslib_1.__importDefault)(require("app/utils/parseLinkHeader"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
/**
 * This is a utility component that should be used to fetch an organization's projects (summary).
 * It can either fetch explicit projects (e.g. via slug) or a paginated list of projects.
 * These will be passed down to the render prop (`children`).
 *
 * The legacy way of handling this is that `ProjectSummary[]` is expected to be included in an
 * `Organization` as well as being saved to `ProjectsStore`.
 */
class Projects extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            fetchedProjects: [],
            projectsFromStore: [],
            initiallyLoaded: false,
            fetching: false,
            isIncomplete: null,
            hasMore: null,
            prevSearch: null,
            nextCursor: null,
            fetchError: null,
        };
        /**
         * List of projects that need to be fetched via API
         */
        this.fetchQueue = new Set();
        /**
         * Memoized function that returns a `Map<project.slug, project>`
         */
        this.getProjectsMap = (0, memoize_1.default)(projects => new Map(projects.map(project => [project.slug, project])));
        /**
         * When `props.slugs` is included, identifies what projects we already
         * have summaries for and what projects need to be fetched from API
         */
        this.loadSpecificProjects = () => {
            const { slugs, projects } = this.props;
            const projectsMap = this.getProjectsMap(projects);
            // Split slugs into projects that are in store and not in store
            // (so we can request projects not in store)
            const [inStore, notInStore] = (0, partition_1.default)(slugs, slug => projectsMap.has(slug));
            // Get the actual summaries of projects that are in store
            const projectsFromStore = inStore.map(slug => projectsMap.get(slug)).filter(utils_1.defined);
            // Add to queue
            notInStore.forEach(slug => this.fetchQueue.add(slug));
            this.setState({
                // placeholders for projects we need to fetch
                fetchedProjects: notInStore.map(slug => ({ slug })),
                // set initiallyLoaded if any projects were fetched from store
                initiallyLoaded: !!inStore.length,
                projectsFromStore,
            });
            if (!notInStore.length) {
                return;
            }
            this.fetchSpecificProjects();
        };
        /**
         * These will fetch projects via API (using project slug) provided by `this.fetchQueue`
         */
        this.fetchSpecificProjects = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, orgId, passthroughPlaceholderProject } = this.props;
            if (!this.fetchQueue.size) {
                return;
            }
            this.setState({
                fetching: true,
            });
            let projects = [];
            let fetchError = null;
            try {
                const { results } = yield fetchProjects(api, orgId, {
                    slugs: Array.from(this.fetchQueue),
                });
                projects = results;
            }
            catch (err) {
                console.error(err); // eslint-disable-line no-console
                fetchError = err;
            }
            const projectsMap = this.getProjectsMap(projects);
            // For each item in the fetch queue, lookup the project object and in the case
            // where something wrong has happened and we were unable to get project summary from
            // the server, just fill in with an object with only the slug
            const projectsOrPlaceholder = Array.from(this.fetchQueue)
                .map(slug => projectsMap.has(slug)
                ? projectsMap.get(slug)
                : !!passthroughPlaceholderProject
                    ? { slug }
                    : null)
                .filter(utils_1.defined);
            this.setState({
                fetchedProjects: projectsOrPlaceholder,
                isIncomplete: this.fetchQueue.size !== projects.length,
                initiallyLoaded: true,
                fetching: false,
                fetchError,
            });
            this.fetchQueue.clear();
        });
        /**
         * If `props.slugs` is not provided, request from API a list of paginated project summaries
         * that are in `prop.orgId`.
         *
         * Provide render prop with results as well as `hasMore` to indicate there are more results.
         * Downstream consumers should use this to notify users so that they can e.g. narrow down
         * results using search
         */
        this.loadAllProjects = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, orgId, limit, allProjects } = this.props;
            this.setState({
                fetching: true,
            });
            try {
                const { results, hasMore, nextCursor } = yield fetchProjects(api, orgId, {
                    limit,
                    allProjects,
                });
                this.setState({
                    fetching: false,
                    fetchedProjects: results,
                    initiallyLoaded: true,
                    hasMore,
                    nextCursor,
                });
            }
            catch (err) {
                console.error(err); // eslint-disable-line no-console
                this.setState({
                    fetching: false,
                    fetchedProjects: [],
                    initiallyLoaded: true,
                    fetchError: err,
                });
            }
        });
        /**
         * This is an action provided to consumers for them to update the current projects
         * result set using a simple search query. You can allow the new results to either
         * be appended or replace the existing results.
         *
         * @param {String} search The search term to use
         * @param {Object} options Options object
         * @param {Boolean} options.append Results should be appended to existing list (otherwise, will replace)
         */
        this.handleSearch = (search, { append } = {}) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, orgId, limit } = this.props;
            const { prevSearch } = this.state;
            const cursor = this.state.nextCursor;
            this.setState({ fetching: true });
            try {
                const { results, hasMore, nextCursor } = yield fetchProjects(api, orgId, {
                    search,
                    limit,
                    prevSearch,
                    cursor,
                });
                this.setState((state) => {
                    let fetchedProjects;
                    if (append) {
                        // Remove duplicates
                        fetchedProjects = (0, uniqBy_1.default)([...state.fetchedProjects, ...results], ({ slug }) => slug);
                    }
                    else {
                        fetchedProjects = results;
                    }
                    return {
                        fetchedProjects,
                        hasMore,
                        fetching: false,
                        prevSearch: search,
                        nextCursor,
                    };
                });
            }
            catch (err) {
                console.error(err); // eslint-disable-line no-console
                this.setState({
                    fetching: false,
                    fetchError: err,
                });
            }
        });
    }
    componentDidMount() {
        const { slugs } = this.props;
        if (!!(slugs === null || slugs === void 0 ? void 0 : slugs.length)) {
            this.loadSpecificProjects();
        }
        else {
            this.loadAllProjects();
        }
    }
    componentDidUpdate(prevProps) {
        const { projects } = this.props;
        if (projects !== prevProps.projects) {
            this.updateProjectsFromStore();
        }
    }
    /**
     * Function to update projects when the store emits updates
     */
    updateProjectsFromStore() {
        const { allProjects, projects, slugs } = this.props;
        if (allProjects) {
            this.setState({ fetchedProjects: projects });
            return;
        }
        if (!!(slugs === null || slugs === void 0 ? void 0 : slugs.length)) {
            // Extract the requested projects from the store based on props.slugs
            const projectsMap = this.getProjectsMap(projects);
            const projectsFromStore = slugs.map(slug => projectsMap.get(slug)).filter(utils_1.defined);
            this.setState({ projectsFromStore });
        }
    }
    render() {
        const { slugs, children } = this.props;
        const renderProps = {
            // We want to make sure that at the minimum, we return a list of objects with only `slug`
            // while we load actual project data
            projects: this.state.initiallyLoaded
                ? [...this.state.fetchedProjects, ...this.state.projectsFromStore]
                : (slugs && slugs.map(slug => ({ slug }))) || [],
            // This is set when we fail to find some slugs from both store and API
            isIncomplete: this.state.isIncomplete,
            // This is state for when fetching data from API
            fetching: this.state.fetching,
            // Project results (from API) are paginated and there are more projects
            // that are not in the initial queryset
            hasMore: this.state.hasMore,
            // Calls API and searches for project, accepts a callback function with signature:
            //
            // fn(searchTerm, {append: bool})
            onSearch: this.handleSearch,
            // Reflects whether or not the initial fetch for the requested projects
            // was fulfilled
            initiallyLoaded: this.state.initiallyLoaded,
            // The error that occurred if fetching failed
            fetchError: this.state.fetchError,
        };
        return children(renderProps);
    }
}
Projects.defaultProps = {
    passthroughPlaceholderProject: true,
};
exports.default = (0, withProjects_1.default)((0, withApi_1.default)(Projects));
function fetchProjects(api, orgId, { slugs, search, limit, prevSearch, cursor, allProjects } = {}) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const query = {
            // Never return latestDeploys project property from api
            collapse: ['latestDeploys'],
        };
        if (slugs && slugs.length) {
            query.query = slugs.map(slug => `slug:${slug}`).join(' ');
        }
        if (search) {
            query.query = `${query.query ? `${query.query} ` : ''}${search}`;
        }
        if (((!prevSearch && !search) || prevSearch === search) && cursor) {
            query.cursor = cursor;
        }
        // "0" shouldn't be a valid value, so this check is fine
        if (limit) {
            query.per_page = limit;
        }
        if (allProjects) {
            const projects = projectsStore_1.default.getAll();
            const loading = projectsStore_1.default.isLoading();
            // If the projects store is loaded then return all projects from the store
            if (!loading) {
                return {
                    results: projects,
                    hasMore: false,
                };
            }
            // Otherwise mark the query to fetch all projects from the API
            query.all_projects = 1;
        }
        let hasMore = false;
        let nextCursor = null;
        const [data, , resp] = yield api.requestPromise(`/organizations/${orgId}/projects/`, {
            includeAllArgs: true,
            query,
        });
        const pageLinks = resp === null || resp === void 0 ? void 0 : resp.getResponseHeader('Link');
        if (pageLinks) {
            const paginationObject = (0, parseLinkHeader_1.default)(pageLinks);
            hasMore =
                paginationObject &&
                    (paginationObject.next.results || paginationObject.previous.results);
            nextCursor = paginationObject.next.cursor;
        }
        // populate the projects store if all projects were fetched
        if (allProjects) {
            projectActions_1.default.loadProjects(data);
        }
        return {
            results: data,
            hasMore,
            nextCursor,
        };
    });
}
//# sourceMappingURL=projects.jsx.map