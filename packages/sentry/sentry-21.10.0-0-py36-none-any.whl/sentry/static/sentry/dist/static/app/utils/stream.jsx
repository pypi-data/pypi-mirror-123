/**
 * Converts a stream query to an object representation, with
 * keys representing tag names, and the magic __text key
 * representing the text component of the search.
 *
 * Example:
 *
 * "python is:unresolved assigned:foo@bar.com"
 * => {
 *      __text: "python",
 *      is: "unresolved",
 *      assigned: "foo@bar.com"
 *    }
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.objToQuery = exports.queryToObj = void 0;
const tslib_1 = require("tslib");
function queryToObj(queryStr = '') {
    const text = [];
    const queryItems = queryStr.match(/\S+:"[^"]*"?|\S+/g);
    const queryObj = (queryItems || []).reduce((obj, item) => {
        const index = item.indexOf(':');
        if (index === -1) {
            text.push(item);
        }
        else {
            const tagKey = item.slice(0, index);
            const value = item.slice(index + 1).replace(/^"|"$/g, '');
            obj[tagKey] = value;
        }
        return obj;
    }, {});
    queryObj.__text = '';
    if (text.length) {
        queryObj.__text = text.join(' ');
    }
    return queryObj;
}
exports.queryToObj = queryToObj;
/**
 * Converts an object representation of a stream query to a string
 * (consumable by the Sentry stream HTTP API).
 */
function objToQuery(queryObj) {
    const { __text } = queryObj, tags = (0, tslib_1.__rest)(queryObj, ["__text"]);
    const parts = Object.entries(tags).map(([tagKey, value]) => {
        if (value.indexOf(' ') > -1) {
            value = `"${value}"`;
        }
        return `${tagKey}:${value}`;
    });
    if (queryObj.__text) {
        parts.push(queryObj.__text);
    }
    return parts.join(' ');
}
exports.objToQuery = objToQuery;
//# sourceMappingURL=stream.jsx.map