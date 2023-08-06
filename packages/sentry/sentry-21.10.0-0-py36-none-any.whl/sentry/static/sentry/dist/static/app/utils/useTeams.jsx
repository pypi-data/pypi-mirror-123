Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const uniqBy_1 = (0, tslib_1.__importDefault)(require("lodash/uniqBy"));
const teams_1 = require("app/actionCreators/teams");
const teamActions_1 = (0, tslib_1.__importDefault)(require("app/actions/teamActions"));
const organizationStore_1 = (0, tslib_1.__importDefault)(require("app/stores/organizationStore"));
const teamStore_1 = (0, tslib_1.__importDefault)(require("app/stores/teamStore"));
const useLegacyStore_1 = require("app/stores/useLegacyStore");
const parseLinkHeader_1 = (0, tslib_1.__importDefault)(require("app/utils/parseLinkHeader"));
const useApi_1 = (0, tslib_1.__importDefault)(require("app/utils/useApi"));
/**
 * Helper function to actually load teams
 */
function fetchTeams(api, orgId, { slugs, search, limit, lastSearch, cursor } = {}) {
    var _a, _b, _c, _d;
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const query = {};
        if (slugs !== undefined && slugs.length > 0) {
            query.query = slugs.map(slug => `slug:${slug}`).join(' ');
        }
        if (search) {
            query.query = `${(_a = query.query) !== null && _a !== void 0 ? _a : ''} ${search}`.trim();
        }
        const isSameSearch = lastSearch === search || (!lastSearch && !search);
        if (isSameSearch && cursor) {
            query.cursor = cursor;
        }
        if (limit !== undefined) {
            query.per_page = limit;
        }
        let hasMore = false;
        let nextCursor = null;
        const [data, , resp] = yield api.requestPromise(`/organizations/${orgId}/teams/`, {
            includeAllArgs: true,
            query,
        });
        const pageLinks = resp === null || resp === void 0 ? void 0 : resp.getResponseHeader('Link');
        if (pageLinks) {
            const paginationObject = (0, parseLinkHeader_1.default)(pageLinks);
            hasMore = ((_b = paginationObject === null || paginationObject === void 0 ? void 0 : paginationObject.next) === null || _b === void 0 ? void 0 : _b.results) || ((_c = paginationObject === null || paginationObject === void 0 ? void 0 : paginationObject.previous) === null || _c === void 0 ? void 0 : _c.results);
            nextCursor = (_d = paginationObject === null || paginationObject === void 0 ? void 0 : paginationObject.next) === null || _d === void 0 ? void 0 : _d.cursor;
        }
        return { results: data, hasMore, nextCursor };
    });
}
function useTeams({ limit, slugs, provideUserTeams } = {}) {
    var _a;
    const api = (0, useApi_1.default)();
    const { organization } = (0, useLegacyStore_1.useLegacyStore)(organizationStore_1.default);
    const store = (0, useLegacyStore_1.useLegacyStore)(teamStore_1.default);
    const storeSlugs = new Set(store.teams.map(t => t.slug));
    const slugsToLoad = (_a = slugs === null || slugs === void 0 ? void 0 : slugs.filter(slug => !storeSlugs.has(slug))) !== null && _a !== void 0 ? _a : [];
    const shouldLoadSlugs = slugsToLoad.length > 0;
    const shouldLoadTeams = provideUserTeams && !store.loadedUserTeams;
    // If we don't need to make a request either for slugs or user teams, set initiallyLoaded to true
    const initiallyLoaded = !shouldLoadSlugs && !shouldLoadTeams;
    const [state, setState] = (0, react_1.useState)({
        initiallyLoaded,
        fetching: false,
        hasMore: null,
        lastSearch: null,
        nextCursor: null,
        fetchError: null,
    });
    const slugsRef = (0, react_1.useRef)(null);
    // Only initialize slugsRef.current once and modify it when we receive new slugs determined through set equality
    if (slugs !== undefined) {
        if (slugsRef.current === null) {
            slugsRef.current = new Set(slugs);
        }
        if (slugs.length !== slugsRef.current.size ||
            slugs.some(slug => { var _a; return !((_a = slugsRef.current) === null || _a === void 0 ? void 0 : _a.has(slug)); })) {
            slugsRef.current = new Set(slugs);
        }
    }
    function loadUserTeams() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const orgId = organization === null || organization === void 0 ? void 0 : organization.slug;
            if (orgId === undefined) {
                return;
            }
            setState(Object.assign(Object.assign({}, state), { fetching: true }));
            try {
                yield (0, teams_1.fetchUserTeams)(api, { orgId });
                setState(Object.assign(Object.assign({}, state), { fetching: false, initiallyLoaded: true }));
            }
            catch (err) {
                console.error(err); // eslint-disable-line no-console
                setState(Object.assign(Object.assign({}, state), { fetching: false, initiallyLoaded: true, fetchError: err }));
            }
        });
    }
    function loadTeamsBySlug() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const orgId = organization === null || organization === void 0 ? void 0 : organization.slug;
            if (orgId === undefined) {
                return;
            }
            setState(Object.assign(Object.assign({}, state), { fetching: true }));
            try {
                const { results, hasMore, nextCursor } = yield fetchTeams(api, orgId, {
                    slugs: slugsToLoad,
                    limit,
                });
                const fetchedTeams = (0, uniqBy_1.default)([...store.teams, ...results], ({ slug }) => slug);
                teamActions_1.default.loadTeams(fetchedTeams);
                setState(Object.assign(Object.assign({}, state), { hasMore, fetching: false, initiallyLoaded: true, nextCursor }));
            }
            catch (err) {
                console.error(err); // eslint-disable-line no-console
                setState(Object.assign(Object.assign({}, state), { fetching: false, initiallyLoaded: true, fetchError: err }));
            }
        });
    }
    function handleSearch(search) {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { lastSearch } = state;
            const cursor = state.nextCursor;
            if (search === '') {
                return;
            }
            const orgId = organization === null || organization === void 0 ? void 0 : organization.slug;
            if (orgId === undefined) {
                // eslint-disable-next-line no-console
                console.error('Cannot use useTeam.onSearch without an orgId passed to useTeam');
                return;
            }
            setState(Object.assign(Object.assign({}, state), { fetching: true }));
            try {
                api.clear();
                const { results, hasMore, nextCursor } = yield fetchTeams(api, orgId, {
                    search,
                    limit,
                    lastSearch,
                    cursor,
                });
                const fetchedTeams = (0, uniqBy_1.default)([...store.teams, ...results], ({ slug }) => slug);
                // Only update the store if we have more items
                if (fetchedTeams.length > store.teams.length) {
                    teamActions_1.default.loadTeams(fetchedTeams);
                }
                setState(Object.assign(Object.assign({}, state), { hasMore, fetching: false, lastSearch: search, nextCursor }));
            }
            catch (err) {
                console.error(err); // eslint-disable-line no-console
                setState(Object.assign(Object.assign({}, state), { fetching: false, fetchError: err }));
            }
        });
    }
    (0, react_1.useEffect)(() => {
        // Load specified team slugs
        if (shouldLoadSlugs) {
            loadTeamsBySlug();
            return;
        }
        // Load user teams
        if (shouldLoadTeams) {
            loadUserTeams();
        }
    }, [slugsRef.current, provideUserTeams]);
    let filteredTeams = store.teams;
    if (slugs) {
        filteredTeams = filteredTeams.filter(t => slugs.includes(t.slug));
    }
    else if (provideUserTeams) {
        filteredTeams = filteredTeams.filter(t => t.isMember);
    }
    const result = {
        teams: filteredTeams,
        fetching: state.fetching || store.loading,
        initiallyLoaded: state.initiallyLoaded,
        fetchError: state.fetchError,
        hasMore: state.hasMore,
        onSearch: handleSearch,
    };
    return result;
}
exports.default = useTeams;
//# sourceMappingURL=useTeams.jsx.map