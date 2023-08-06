Object.defineProperty(exports, "__esModule", { value: true });
exports.decodeInteger = exports.decodeList = exports.decodeScalar = exports.appendTagCondition = exports.addQueryParamsToExistingUrl = exports.formatQueryString = void 0;
const tslib_1 = require("tslib");
const isString_1 = (0, tslib_1.__importDefault)(require("lodash/isString"));
const queryString = (0, tslib_1.__importStar)(require("query-string"));
const utils_1 = require("app/utils");
// remove leading and trailing whitespace and remove double spaces
function formatQueryString(qs) {
    return qs.trim().replace(/\s+/g, ' ');
}
exports.formatQueryString = formatQueryString;
function addQueryParamsToExistingUrl(origUrl, queryParams) {
    let url;
    try {
        url = new URL(origUrl);
    }
    catch (_a) {
        return '';
    }
    const searchEntries = url.searchParams.entries();
    // Order the query params alphabetically.
    // Otherwise ``queryString`` orders them randomly and it's impossible to test.
    const params = JSON.parse(JSON.stringify(queryParams));
    const query = Object.assign(Object.assign({}, Object.fromEntries(searchEntries)), params);
    return `${url.protocol}//${url.host}${url.pathname}?${queryString.stringify(query)}`;
}
exports.addQueryParamsToExistingUrl = addQueryParamsToExistingUrl;
/**
 * Append a tag key:value to a query string.
 *
 * Handles spacing and quoting if necessary.
 */
function appendTagCondition(query, key, value) {
    let currentQuery = Array.isArray(query) ? query.pop() : (0, isString_1.default)(query) ? query : '';
    if (typeof value === 'string' && /[:\s\(\)\\"]/g.test(value)) {
        value = `"${(0, utils_1.escapeDoubleQuotes)(value)}"`;
    }
    if (currentQuery) {
        currentQuery += ` ${key}:${value}`;
    }
    else {
        currentQuery = `${key}:${value}`;
    }
    return currentQuery;
}
exports.appendTagCondition = appendTagCondition;
function decodeScalar(value, fallback) {
    if (!value) {
        return fallback;
    }
    const unwrapped = Array.isArray(value) && value.length > 0
        ? value[0]
        : (0, isString_1.default)(value)
            ? value
            : fallback;
    return (0, isString_1.default)(unwrapped) ? unwrapped : fallback;
}
exports.decodeScalar = decodeScalar;
function decodeList(value) {
    if (!value) {
        return [];
    }
    return Array.isArray(value) ? value : (0, isString_1.default)(value) ? [value] : [];
}
exports.decodeList = decodeList;
function decodeInteger(value, fallback) {
    const unwrapped = decodeScalar(value);
    if (unwrapped === undefined) {
        return fallback;
    }
    const parsed = parseInt(unwrapped, 10);
    if (isFinite(parsed)) {
        return parsed;
    }
    return fallback;
}
exports.decodeInteger = decodeInteger;
exports.default = {
    decodeInteger,
    decodeList,
    decodeScalar,
    formatQueryString,
    addQueryParamsToExistingUrl,
    appendTagCondition,
};
//# sourceMappingURL=queryString.jsx.map