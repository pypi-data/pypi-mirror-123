Object.defineProperty(exports, "__esModule", { value: true });
exports.updateParamsWithoutHistory = exports.updateParams = exports.updateEnvironments = exports.updateDateTime = exports.updateProjects = exports.initializeUrlState = exports.resetGlobalSelection = void 0;
const tslib_1 = require("tslib");
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const isInteger_1 = (0, tslib_1.__importDefault)(require("lodash/isInteger"));
const omit_1 = (0, tslib_1.__importDefault)(require("lodash/omit"));
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const qs = (0, tslib_1.__importStar)(require("query-string"));
const globalSelectionActions_1 = (0, tslib_1.__importDefault)(require("app/actions/globalSelectionActions"));
const utils_1 = require("app/components/organizations/globalSelectionHeader/utils");
const globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
const utils_2 = require("app/utils");
const dates_1 = require("app/utils/dates");
const localStorage_1 = (0, tslib_1.__importDefault)(require("app/utils/localStorage"));
// Reset values in global selection store
function resetGlobalSelection() {
    globalSelectionActions_1.default.reset();
}
exports.resetGlobalSelection = resetGlobalSelection;
function getProjectIdFromProject(project) {
    return parseInt(project.id, 10);
}
function initializeUrlState({ organization, queryParams, router, memberProjects, skipLoadLastUsed, shouldForceProject, shouldEnforceSingleProject, defaultSelection, forceProject, showAbsolute = true, }) {
    const orgSlug = organization.slug;
    const query = (0, pick_1.default)(queryParams, [globalSelectionHeader_1.URL_PARAM.PROJECT, globalSelectionHeader_1.URL_PARAM.ENVIRONMENT]);
    const hasProjectOrEnvironmentInUrl = Object.keys(query).length > 0;
    const parsed = (0, utils_1.getStateFromQuery)(queryParams, {
        allowAbsoluteDatetime: showAbsolute,
        allowEmptyPeriod: true,
    });
    const _a = (0, utils_1.getDefaultSelection)(), { datetime: defaultDateTime } = _a, retrievedDefaultSelection = (0, tslib_1.__rest)(_a, ["datetime"]);
    const _b = defaultSelection || {}, { datetime: customizedDefaultDateTime } = _b, customizedDefaultSelection = (0, tslib_1.__rest)(_b, ["datetime"]);
    let globalSelection = Object.assign(Object.assign(Object.assign({}, retrievedDefaultSelection), customizedDefaultSelection), { datetime: {
            [globalSelectionHeader_1.DATE_TIME.START]: parsed.start || (customizedDefaultDateTime === null || customizedDefaultDateTime === void 0 ? void 0 : customizedDefaultDateTime.start) || null,
            [globalSelectionHeader_1.DATE_TIME.END]: parsed.end || (customizedDefaultDateTime === null || customizedDefaultDateTime === void 0 ? void 0 : customizedDefaultDateTime.end) || null,
            [globalSelectionHeader_1.DATE_TIME.PERIOD]: parsed.period || (customizedDefaultDateTime === null || customizedDefaultDateTime === void 0 ? void 0 : customizedDefaultDateTime.period) || defaultDateTime.period,
            [globalSelectionHeader_1.DATE_TIME.UTC]: parsed.utc || (customizedDefaultDateTime === null || customizedDefaultDateTime === void 0 ? void 0 : customizedDefaultDateTime.utc) || null,
        } });
    if (globalSelection.datetime.start && globalSelection.datetime.end) {
        globalSelection.datetime.period = null;
    }
    // We only save environment and project, so if those exist in
    // URL, do not touch local storage
    if (hasProjectOrEnvironmentInUrl) {
        globalSelection.projects = parsed.project || [];
        globalSelection.environments = parsed.environment || [];
    }
    else if (!skipLoadLastUsed) {
        try {
            const localStorageKey = `${globalSelectionHeader_1.LOCAL_STORAGE_KEY}:${orgSlug}`;
            const storedValue = localStorage_1.default.getItem(localStorageKey);
            if (storedValue) {
                globalSelection = Object.assign({ datetime: globalSelection.datetime }, JSON.parse(storedValue));
            }
        }
        catch (err) {
            // use default if invalid
            Sentry.captureException(err);
            console.error(err); // eslint-disable-line no-console
        }
    }
    const { projects, environments: environment, datetime } = globalSelection;
    let newProject = null;
    let project = projects;
    /**
     * Skip enforcing a single project if `shouldForceProject` is true,
     * since a component is controlling what that project needs to be.
     * This is true regardless if user has access to multi projects
     */
    if (shouldForceProject && forceProject) {
        newProject = [getProjectIdFromProject(forceProject)];
    }
    else if (shouldEnforceSingleProject && !shouldForceProject) {
        /**
         * If user does not have access to `global-views` (e.g. multi project select) *and* there is no
         * `project` URL parameter, then we update URL params with:
         * 1) the first project from the list of requested projects from URL params,
         * 2) first project user is a member of from org
         *
         * Note this is intentionally skipped if `shouldForceProject == true` since we want to initialize store
         * and wait for the forced project
         */
        if (projects && projects.length > 0) {
            // If there is a list of projects from URL params, select first project from that list
            newProject = typeof projects === 'string' ? [Number(projects)] : [projects[0]];
        }
        else {
            // When we have finished loading the organization into the props,  i.e. the organization slug is consistent with
            // the URL param--Sentry will get the first project from the organization that the user is a member of.
            newProject = [...memberProjects].slice(0, 1).map(getProjectIdFromProject);
        }
    }
    if (newProject) {
        globalSelection.projects = newProject;
        project = newProject;
    }
    globalSelectionActions_1.default.initializeUrlState(globalSelection);
    globalSelectionActions_1.default.setOrganization(organization);
    // To keep URLs clean, don't push default period if url params are empty
    const parsedWithNoDefaultPeriod = (0, utils_1.getStateFromQuery)(queryParams, {
        allowEmptyPeriod: true,
        allowAbsoluteDatetime: showAbsolute,
    });
    const newDatetime = Object.assign(Object.assign({}, datetime), { period: !parsedWithNoDefaultPeriod.start &&
            !parsedWithNoDefaultPeriod.end &&
            !parsedWithNoDefaultPeriod.period
            ? null
            : datetime.period, utc: !parsedWithNoDefaultPeriod.utc ? null : datetime.utc });
    updateParamsWithoutHistory(Object.assign({ project, environment }, newDatetime), router, {
        keepCursor: true,
    });
}
exports.initializeUrlState = initializeUrlState;
/**
 * Updates store and global project selection URL param if `router` is supplied
 *
 * This accepts `environments` from `options` to also update environments simultaneously
 * as environments are tied to a project, so if you change projects, you may need
 * to clear environments.
 */
function updateProjects(projects, router, options) {
    if (!isProjectsValid(projects)) {
        Sentry.withScope(scope => {
            scope.setExtra('projects', projects);
            Sentry.captureException(new Error('Invalid projects selected'));
        });
        return;
    }
    globalSelectionActions_1.default.updateProjects(projects, options === null || options === void 0 ? void 0 : options.environments);
    updateParams({ project: projects, environment: options === null || options === void 0 ? void 0 : options.environments }, router, options);
}
exports.updateProjects = updateProjects;
function isProjectsValid(projects) {
    return Array.isArray(projects) && projects.every(project => (0, isInteger_1.default)(project));
}
/**
 * Updates store and global datetime selection URL param if `router` is supplied
 *
 * @param {Object} datetime Object with start, end, range keys
 * @param {Object} [router] Router object
 * @param {Object} [options] Options object
 * @param {String[]} [options.resetParams] List of parameters to remove when changing URL params
 */
function updateDateTime(datetime, router, options) {
    globalSelectionActions_1.default.updateDateTime(datetime);
    // We only save projects/environments to local storage, do not
    // save anything when date changes.
    updateParams(datetime, router, Object.assign(Object.assign({}, options), { save: false }));
}
exports.updateDateTime = updateDateTime;
/**
 * Updates store and updates global environment selection URL param if `router` is supplied
 *
 * @param {String[]} environments List of environments
 * @param {Object} [router] Router object
 * @param {Object} [options] Options object
 * @param {String[]} [options.resetParams] List of parameters to remove when changing URL params
 */
function updateEnvironments(environment, router, options) {
    globalSelectionActions_1.default.updateEnvironments(environment);
    updateParams({ environment }, router, options);
}
exports.updateEnvironments = updateEnvironments;
/**
 * Updates router/URL with new query params
 *
 * @param obj New query params
 * @param [router] React router object
 * @param [options] Options object
 */
function updateParams(obj, router, options) {
    // Allow another component to handle routing
    if (!router) {
        return;
    }
    const newQuery = getNewQueryParams(obj, router.location.query, options);
    // Only push new location if query params has changed because this will cause a heavy re-render
    if (qs.stringify(newQuery) === qs.stringify(router.location.query)) {
        return;
    }
    if (options === null || options === void 0 ? void 0 : options.save) {
        globalSelectionActions_1.default.save(newQuery);
    }
    router.push({
        pathname: router.location.pathname,
        query: newQuery,
    });
}
exports.updateParams = updateParams;
/**
 * Like updateParams but just replaces the current URL and does not create a
 * new browser history entry
 *
 * @param obj New query params
 * @param [router] React router object
 * @param [options] Options object
 */
function updateParamsWithoutHistory(obj, router, options) {
    // Allow another component to handle routing
    if (!router) {
        return;
    }
    const newQuery = getNewQueryParams(obj, router.location.query, options);
    // Only push new location if query params have changed because this will cause a heavy re-render
    if (qs.stringify(newQuery) === qs.stringify(router.location.query)) {
        return;
    }
    router.replace({
        pathname: router.location.pathname,
        query: newQuery,
    });
}
exports.updateParamsWithoutHistory = updateParamsWithoutHistory;
/**
 * Creates a new query parameter object given new params and old params
 * Preserves the old query params, except for `cursor` (can be overriden with keepCursor option)
 *
 * @param obj New query params
 * @param oldQueryParams Old query params
 * @param [options] Options object
 */
function getNewQueryParams(obj, oldQueryParams, { resetParams, keepCursor } = {}) {
    const { cursor, statsPeriod } = oldQueryParams, oldQuery = (0, tslib_1.__rest)(oldQueryParams, ["cursor", "statsPeriod"]);
    const oldQueryWithoutResetParams = !!(resetParams === null || resetParams === void 0 ? void 0 : resetParams.length)
        ? (0, omit_1.default)(oldQuery, resetParams)
        : oldQuery;
    const newQuery = getParams(Object.assign(Object.assign(Object.assign({}, oldQueryWithoutResetParams), { 
        // Some views update using `period`, and some `statsPeriod`, we should make this uniform
        period: !obj.start && !obj.end ? obj.period || statsPeriod : null }), obj));
    if (newQuery.start) {
        newQuery.start = (0, dates_1.getUtcDateString)(newQuery.start);
    }
    if (newQuery.end) {
        newQuery.end = (0, dates_1.getUtcDateString)(newQuery.end);
    }
    if (keepCursor) {
        newQuery.cursor = cursor;
    }
    return newQuery;
}
function getParams(params) {
    const { start, end, period, statsPeriod } = params, otherParams = (0, tslib_1.__rest)(params, ["start", "end", "period", "statsPeriod"]);
    // `statsPeriod` takes precedence for now
    const coercedPeriod = statsPeriod || period;
    // Filter null values
    return Object.fromEntries(Object.entries(Object.assign({ statsPeriod: coercedPeriod, start: coercedPeriod ? null : start, end: coercedPeriod ? null : end }, otherParams)).filter(([, value]) => (0, utils_2.defined)(value)));
}
//# sourceMappingURL=globalSelection.jsx.map