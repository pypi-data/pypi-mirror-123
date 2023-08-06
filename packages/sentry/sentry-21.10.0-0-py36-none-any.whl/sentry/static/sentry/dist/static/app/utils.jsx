Object.defineProperty(exports, "__esModule", { value: true });
exports.escapeDoubleQuotes = exports.isFunction = exports.generateQueryWithTag = exports.deepFreeze = exports.isWebpackChunkLoadingError = exports.descopeFeatureName = exports.buildTeamId = exports.buildUserId = exports.sortProjects = exports.convertMultilineFieldValue = exports.extractMultilineFields = exports.parseRepo = exports.getShortCommitHash = exports.formatBytesBase2 = exports.formatBytesBase10 = exports.toTitleCase = exports.percent = exports.escape = exports.isUrl = exports.nl2br = exports.defined = exports.explodeSlug = exports.trim = exports.objectIsEmpty = exports.sortArray = exports.intcomma = exports.valueIsEqual = void 0;
const tslib_1 = require("tslib");
const isArray_1 = (0, tslib_1.__importDefault)(require("lodash/isArray"));
const isObject_1 = (0, tslib_1.__importDefault)(require("lodash/isObject"));
const isString_1 = (0, tslib_1.__importDefault)(require("lodash/isString"));
const isUndefined_1 = (0, tslib_1.__importDefault)(require("lodash/isUndefined"));
const queryString_1 = require("app/utils/queryString");
function arrayIsEqual(arr, other, deep) {
    // if the other array is a falsy value, return
    if (!arr && !other) {
        return true;
    }
    if (!arr || !other) {
        return false;
    }
    // compare lengths - can save a lot of time
    if (arr.length !== other.length) {
        return false;
    }
    return arr.every((val, idx) => valueIsEqual(val, other[idx], deep));
}
function valueIsEqual(value, other, deep) {
    if (value === other) {
        return true;
    }
    else if ((0, isArray_1.default)(value) || (0, isArray_1.default)(other)) {
        if (arrayIsEqual(value, other, deep)) {
            return true;
        }
    }
    else if ((0, isObject_1.default)(value) || (0, isObject_1.default)(other)) {
        if (objectMatchesSubset(value, other, deep)) {
            return true;
        }
    }
    return false;
}
exports.valueIsEqual = valueIsEqual;
function objectMatchesSubset(obj, other, deep) {
    let k;
    if (obj === other) {
        return true;
    }
    if (!obj || !other) {
        return false;
    }
    if (deep !== true) {
        for (k in other) {
            if (obj[k] !== other[k]) {
                return false;
            }
        }
        return true;
    }
    for (k in other) {
        if (!valueIsEqual(obj[k], other[k], deep)) {
            return false;
        }
    }
    return true;
}
function intcomma(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}
exports.intcomma = intcomma;
function sortArray(arr, score_fn) {
    arr.sort((a, b) => {
        const a_score = score_fn(a), b_score = score_fn(b);
        for (let i = 0; i < a_score.length; i++) {
            if (a_score[i] > b_score[i]) {
                return 1;
            }
            if (a_score[i] < b_score[i]) {
                return -1;
            }
        }
        return 0;
    });
    return arr;
}
exports.sortArray = sortArray;
function objectIsEmpty(obj = {}) {
    for (const prop in obj) {
        if (obj.hasOwnProperty(prop)) {
            return false;
        }
    }
    return true;
}
exports.objectIsEmpty = objectIsEmpty;
function trim(str) {
    return str.replace(/^\s+|\s+$/g, '');
}
exports.trim = trim;
/**
 * Replaces slug special chars with a space
 */
function explodeSlug(slug) {
    return trim(slug.replace(/[-_]+/g, ' '));
}
exports.explodeSlug = explodeSlug;
function defined(item) {
    return !(0, isUndefined_1.default)(item) && item !== null;
}
exports.defined = defined;
function nl2br(str) {
    return str.replace(/(?:\r\n|\r|\n)/g, '<br />');
}
exports.nl2br = nl2br;
/**
 * This function has a critical security impact, make sure to check all usages before changing this function.
 * In some parts of our code we rely on that this only really is a string starting with http(s).
 */
function isUrl(str) {
    return (!!str &&
        (0, isString_1.default)(str) &&
        (str.indexOf('http://') === 0 || str.indexOf('https://') === 0));
}
exports.isUrl = isUrl;
function escape(str) {
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}
exports.escape = escape;
function percent(value, totalValue) {
    // prevent division by zero
    if (totalValue === 0) {
        return 0;
    }
    return (value / totalValue) * 100;
}
exports.percent = percent;
function toTitleCase(str) {
    return str.replace(/\w\S*/g, txt => txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase());
}
exports.toTitleCase = toTitleCase;
/**
 * Note the difference between *a-bytes (base 10) vs *i-bytes (base 2), which
 * means that:
 * - 1000 megabytes is equal to 1 gigabyte
 * - 1024 mebibytes is equal to 1 gibibytes
 *
 * We will use base 10 throughout billing for attachments. This function formats
 * quota/usage values for display.
 *
 * For storage/memory/file sizes, please take a look at formatBytesBase2
 */
function formatBytesBase10(bytes, u = 0) {
    const units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
    const threshold = 1000;
    while (bytes >= threshold) {
        bytes /= threshold;
        u += 1;
    }
    return bytes.toLocaleString(undefined, { maximumFractionDigits: 2 }) + ' ' + units[u];
}
exports.formatBytesBase10 = formatBytesBase10;
/**
 * Note the difference between *a-bytes (base 10) vs *i-bytes (base 2), which
 * means that:
 * - 1000 megabytes is equal to 1 gigabyte
 * - 1024 mebibytes is equal to 1 gibibytes
 *
 * We will use base 2 to display storage/memory/file sizes as that is commonly
 * used by Windows or RAM or CPU cache sizes, and it is more familiar to the user
 *
 * For billing-related code around attachments. please take a look at
 * formatBytesBase10
 */
function formatBytesBase2(bytes) {
    const units = ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB'];
    const thresh = 1024;
    if (bytes < thresh) {
        return bytes + ' B';
    }
    let u = -1;
    do {
        bytes /= thresh;
        ++u;
    } while (bytes >= thresh);
    return bytes.toFixed(1) + ' ' + units[u];
}
exports.formatBytesBase2 = formatBytesBase2;
function getShortCommitHash(hash) {
    if (hash.match(/^[a-f0-9]{40}$/)) {
        hash = hash.substr(0, 7);
    }
    return hash;
}
exports.getShortCommitHash = getShortCommitHash;
function parseRepo(repo) {
    if (typeof repo === 'string') {
        const re = /(?:github\.com|bitbucket\.org)\/([^\/]+\/[^\/]+)/i;
        const match = repo.match(re);
        const parsedRepo = match ? match[1] : repo;
        return parsedRepo;
    }
    return repo;
}
exports.parseRepo = parseRepo;
/**
 * Converts a multi-line textarea input value into an array,
 * eliminating empty lines
 */
function extractMultilineFields(value) {
    return value
        .split('\n')
        .map(f => trim(f))
        .filter(f => f !== '');
}
exports.extractMultilineFields = extractMultilineFields;
/**
 * If the value is of type Array, converts it to type string, keeping the line breaks, if there is any
 */
function convertMultilineFieldValue(value) {
    if (Array.isArray(value)) {
        return value.join('\n');
    }
    if (typeof value === 'string') {
        return value.split('\n').join('\n');
    }
    return '';
}
exports.convertMultilineFieldValue = convertMultilineFieldValue;
function projectDisplayCompare(a, b) {
    if (a.isBookmarked !== b.isBookmarked) {
        return a.isBookmarked ? -1 : 1;
    }
    return a.slug.localeCompare(b.slug);
}
// Sort a list of projects by bookmarkedness, then by id
function sortProjects(projects) {
    return projects.sort(projectDisplayCompare);
}
exports.sortProjects = sortProjects;
// build actorIds
const buildUserId = (id) => `user:${id}`;
exports.buildUserId = buildUserId;
const buildTeamId = (id) => `team:${id}`;
exports.buildTeamId = buildTeamId;
/**
 * Removes the organization / project scope prefix on feature names.
 */
function descopeFeatureName(feature) {
    if (typeof feature !== 'string') {
        return feature;
    }
    const results = feature.match(/(?:^(?:projects|organizations):)?(.*)/);
    if (results && results.length > 0) {
        return results.pop();
    }
    return feature;
}
exports.descopeFeatureName = descopeFeatureName;
function isWebpackChunkLoadingError(error) {
    return (error &&
        typeof error.message === 'string' &&
        error.message.toLowerCase().includes('loading chunk'));
}
exports.isWebpackChunkLoadingError = isWebpackChunkLoadingError;
function deepFreeze(object) {
    // Retrieve the property names defined on object
    const propNames = Object.getOwnPropertyNames(object);
    // Freeze properties before freezing self
    for (const name of propNames) {
        const value = object[name];
        object[name] = value && typeof value === 'object' ? deepFreeze(value) : value;
    }
    return Object.freeze(object);
}
exports.deepFreeze = deepFreeze;
function generateQueryWithTag(prevQuery, tag) {
    const query = Object.assign({}, prevQuery);
    // some tags are dedicated query strings since other parts of the app consumes this,
    // for example, the global selection header.
    switch (tag.key) {
        case 'environment':
            query.environment = tag.value;
            break;
        case 'project':
            query.project = tag.value;
            break;
        default:
            query.query = (0, queryString_1.appendTagCondition)(query.query, tag.key, tag.value);
    }
    return query;
}
exports.generateQueryWithTag = generateQueryWithTag;
const isFunction = (value) => typeof value === 'function';
exports.isFunction = isFunction;
// NOTE: only escapes a " if it's not already escaped
function escapeDoubleQuotes(str) {
    return str.replace(/\\([\s\S])|(")/g, '\\$1$2');
}
exports.escapeDoubleQuotes = escapeDoubleQuotes;
//# sourceMappingURL=utils.jsx.map