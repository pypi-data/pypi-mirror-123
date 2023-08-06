Object.defineProperty(exports, "__esModule", { value: true });
exports.fetchOrganizationDetails = void 0;
const tslib_1 = require("tslib");
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const indicator_1 = require("app/actionCreators/indicator");
const organizations_1 = require("app/actionCreators/organizations");
const globalSelectionActions_1 = (0, tslib_1.__importDefault)(require("app/actions/globalSelectionActions"));
const organizationActions_1 = (0, tslib_1.__importDefault)(require("app/actions/organizationActions"));
const projectActions_1 = (0, tslib_1.__importDefault)(require("app/actions/projectActions"));
const teamActions_1 = (0, tslib_1.__importDefault)(require("app/actions/teamActions"));
const api_1 = require("app/api");
const getPreloadedData_1 = require("app/utils/getPreloadedData");
function fetchOrg(api, slug, isInitialFetch) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const org = yield (0, getPreloadedData_1.getPreloadedDataPromise)('organization', slug, () => 
        // This data should get preloaded in static/sentry/index.ejs
        // If this url changes make sure to update the preload
        api.requestPromise(`/organizations/${slug}/`, { query: { detailed: 0 } }), isInitialFetch);
        if (!org) {
            throw new Error('retrieved organization is falsey');
        }
        organizationActions_1.default.update(org, { replace: true });
        (0, organizations_1.setActiveOrganization)(org);
        return org;
    });
}
function fetchProjectsAndTeams(slug, isInitialFetch) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        // Create a new client so the request is not cancelled
        const uncancelableApi = new api_1.Client();
        const projectsPromise = (0, getPreloadedData_1.getPreloadedDataPromise)('projects', slug, () => 
        // This data should get preloaded in static/sentry/index.ejs
        // If this url changes make sure to update the preload
        uncancelableApi.requestPromise(`/organizations/${slug}/projects/`, {
            query: {
                all_projects: 1,
                collapse: 'latestDeploys',
            },
        }), isInitialFetch);
        const teamsPromise = (0, getPreloadedData_1.getPreloadedDataPromise)('teams', slug, 
        // This data should get preloaded in static/sentry/index.ejs
        // If this url changes make sure to update the preload
        () => uncancelableApi.requestPromise(`/organizations/${slug}/teams/`), isInitialFetch);
        try {
            return yield Promise.all([projectsPromise, teamsPromise]);
        }
        catch (err) {
            // It's possible these requests fail with a 403 if the user has a role with
            // insufficient access to projects and teams, but *can* access org details
            // (e.g. billing). An example of this is in org settings.
            //
            // Ignore 403s and bubble up other API errors
            if (err.status !== 403) {
                throw err;
            }
        }
        return [[], []];
    });
}
/**
 * Fetches an organization's details
 *
 * @param api A reference to the api client
 * @param slug The organization slug
 * @param silent Should we silently update the organization (do not clear the
 *               current organization in the store)
 */
function fetchOrganizationDetails(api, slug, silent, isInitialFetch) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        if (!silent) {
            organizationActions_1.default.reset();
            projectActions_1.default.reset();
            globalSelectionActions_1.default.reset();
        }
        const loadOrganization = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            var _a, _b, _c, _d, _e;
            try {
                yield fetchOrg(api, slug, isInitialFetch);
            }
            catch (err) {
                if (!err) {
                    return;
                }
                organizationActions_1.default.fetchOrgError(err);
                if (err.status === 403 || err.status === 401) {
                    const errMessage = typeof ((_a = err.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) === 'string'
                        ? (_b = err.responseJSON) === null || _b === void 0 ? void 0 : _b.detail
                        : typeof ((_d = (_c = err.responseJSON) === null || _c === void 0 ? void 0 : _c.detail) === null || _d === void 0 ? void 0 : _d.message) === 'string'
                            ? (_e = err.responseJSON) === null || _e === void 0 ? void 0 : _e.detail.message
                            : null;
                    if (errMessage) {
                        (0, indicator_1.addErrorMessage)(errMessage);
                    }
                    return;
                }
                Sentry.captureException(err);
            }
        });
        const loadTeamsAndProjects = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const [projects, teams] = yield fetchProjectsAndTeams(slug, isInitialFetch);
            projectActions_1.default.loadProjects(projects);
            teamActions_1.default.loadTeams(teams);
        });
        return Promise.all([loadOrganization(), loadTeamsAndProjects()]);
    });
}
exports.fetchOrganizationDetails = fetchOrganizationDetails;
//# sourceMappingURL=organization.jsx.map