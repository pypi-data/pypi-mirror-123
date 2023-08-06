Object.defineProperty(exports, "__esModule", { value: true });
exports.removeGlobalSelectionStorage = exports.isSelectionEqual = exports.getDefaultSelection = exports.extractDatetimeSelectionParameters = exports.extractSelectionParameters = exports.getStateFromQuery = void 0;
const tslib_1 = require("tslib");
const identity_1 = (0, tslib_1.__importDefault)(require("lodash/identity"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const pickBy_1 = (0, tslib_1.__importDefault)(require("lodash/pickBy"));
const globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
const utils_1 = require("app/utils");
const dates_1 = require("app/utils/dates");
const localStorage_1 = (0, tslib_1.__importDefault)(require("app/utils/localStorage"));
const getParams_1 = require("./getParams");
const DEFAULT_PARAMS = (0, getParams_1.getParams)({});
function getStateFromQuery(query, { allowEmptyPeriod = false, allowAbsoluteDatetime = true } = {}) {
    const parsedParams = (0, getParams_1.getParams)(query, { allowEmptyPeriod, allowAbsoluteDatetime });
    const projectFromQuery = query[globalSelectionHeader_1.URL_PARAM.PROJECT];
    const environmentFromQuery = query[globalSelectionHeader_1.URL_PARAM.ENVIRONMENT];
    const period = parsedParams.statsPeriod;
    const utc = parsedParams.utc;
    const hasAbsolute = allowAbsoluteDatetime && !!parsedParams.start && !!parsedParams.end;
    let project;
    if ((0, utils_1.defined)(projectFromQuery) && Array.isArray(projectFromQuery)) {
        project = projectFromQuery.map(p => parseInt(p, 10));
    }
    else if ((0, utils_1.defined)(projectFromQuery)) {
        const projectFromQueryIdInt = parseInt(projectFromQuery, 10);
        project = isNaN(projectFromQueryIdInt) ? [] : [projectFromQueryIdInt];
    }
    else {
        project = projectFromQuery;
    }
    const environment = (0, utils_1.defined)(environmentFromQuery) && !Array.isArray(environmentFromQuery)
        ? [environmentFromQuery]
        : environmentFromQuery;
    const start = hasAbsolute ? (0, dates_1.getUtcToLocalDateObject)(parsedParams.start) : null;
    const end = hasAbsolute ? (0, dates_1.getUtcToLocalDateObject)(parsedParams.end) : null;
    return {
        project,
        environment,
        period: period || null,
        start: start || null,
        end: end || null,
        // params from URL will be a string
        utc: typeof utc !== 'undefined' ? utc === 'true' : null,
    };
}
exports.getStateFromQuery = getStateFromQuery;
/**
 * Extract the global selection parameters from an object
 * Useful for extracting global selection properties from the current URL
 * when building another URL.
 */
function extractSelectionParameters(query) {
    return (0, pickBy_1.default)((0, pick_1.default)(query, Object.values(globalSelectionHeader_1.URL_PARAM)), identity_1.default);
}
exports.extractSelectionParameters = extractSelectionParameters;
/**
 * Extract the global selection datetime parameters from an object.
 */
function extractDatetimeSelectionParameters(query) {
    return (0, pickBy_1.default)((0, pick_1.default)(query, Object.values(globalSelectionHeader_1.DATE_TIME_KEYS)), identity_1.default);
}
exports.extractDatetimeSelectionParameters = extractDatetimeSelectionParameters;
function getDefaultSelection() {
    const utc = DEFAULT_PARAMS.utc;
    return {
        projects: [],
        environments: [],
        datetime: {
            start: DEFAULT_PARAMS.start || null,
            end: DEFAULT_PARAMS.end || null,
            period: DEFAULT_PARAMS.statsPeriod || '',
            utc: typeof utc !== 'undefined' ? utc === 'true' : null,
        },
    };
}
exports.getDefaultSelection = getDefaultSelection;
/**
 * Compare the non-utc values of two selections.
 * Useful when re-fetching data based on globalselection changing.
 *
 * utc is not compared as there is a problem somewhere in the selection
 * data flow that results in it being undefined | null | boolean instead of null | boolean.
 * The additional undefined state makes this function just as unreliable as isEqual(selection, other)
 */
function isSelectionEqual(selection, other) {
    var _a, _b, _c, _d;
    if (!(0, isEqual_1.default)(selection.projects, other.projects) ||
        !(0, isEqual_1.default)(selection.environments, other.environments)) {
        return false;
    }
    // Use string comparison as we aren't interested in the identity of the datetimes.
    if (selection.datetime.period !== other.datetime.period ||
        ((_a = selection.datetime.start) === null || _a === void 0 ? void 0 : _a.toString()) !== ((_b = other.datetime.start) === null || _b === void 0 ? void 0 : _b.toString()) ||
        ((_c = selection.datetime.end) === null || _c === void 0 ? void 0 : _c.toString()) !== ((_d = other.datetime.end) === null || _d === void 0 ? void 0 : _d.toString())) {
        return false;
    }
    return true;
}
exports.isSelectionEqual = isSelectionEqual;
/**
 * Removes globalselection from localstorage
 */
function removeGlobalSelectionStorage(orgId) {
    const localStorageKey = `${globalSelectionHeader_1.LOCAL_STORAGE_KEY}:${orgId}`;
    localStorage_1.default.removeItem(localStorageKey);
}
exports.removeGlobalSelectionStorage = removeGlobalSelectionStorage;
//# sourceMappingURL=utils.jsx.map