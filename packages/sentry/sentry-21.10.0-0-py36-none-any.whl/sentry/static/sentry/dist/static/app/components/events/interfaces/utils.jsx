Object.defineProperty(exports, "__esModule", { value: true });
exports.stackTracePlatformIcon = exports.parseAssembly = exports.getImageRange = exports.parseAddress = exports.formatAddress = exports.removeFilterMaskedEntries = exports.objectToSortedTupleArray = exports.getFullUrl = exports.stringifyQueryList = exports.getCurlCommand = exports.escapeQuotes = void 0;
const tslib_1 = require("tslib");
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const compact_1 = (0, tslib_1.__importDefault)(require("lodash/compact"));
const isString_1 = (0, tslib_1.__importDefault)(require("lodash/isString"));
const uniq_1 = (0, tslib_1.__importDefault)(require("lodash/uniq"));
const qs = (0, tslib_1.__importStar)(require("query-string"));
const constants_1 = require("app/constants");
const utils_1 = require("app/utils");
const fileExtension_1 = require("app/utils/fileExtension");
function escapeQuotes(v) {
    return v.replace(/\\/g, '\\\\').replace(/"/g, '\\"');
}
exports.escapeQuotes = escapeQuotes;
// TODO(dcramer): support cookies
function getCurlCommand(data) {
    var _a, _b, _c;
    let result = 'curl';
    if ((0, utils_1.defined)(data.method) && data.method !== 'GET') {
        result += ' \\\n -X ' + data.method;
    }
    // TODO(benvinegar): just gzip? what about deflate?
    const compressed = (_a = data.headers) === null || _a === void 0 ? void 0 : _a.find(h => h[0] === 'Accept-Encoding' && h[1].indexOf('gzip') !== -1);
    if (compressed) {
        result += ' \\\n --compressed';
    }
    // sort headers
    const headers = (_c = (_b = data.headers) === null || _b === void 0 ? void 0 : _b.sort(function (a, b) {
        return a[0] === b[0] ? 0 : a[0] < b[0] ? -1 : 1;
    })) !== null && _c !== void 0 ? _c : [];
    for (const header of headers) {
        result += ' \\\n -H "' + header[0] + ': ' + escapeQuotes(header[1] + '') + '"';
    }
    if ((0, utils_1.defined)(data.data)) {
        switch (data.inferredContentType) {
            case 'application/json':
                result += ' \\\n --data "' + escapeQuotes(JSON.stringify(data.data)) + '"';
                break;
            case 'application/x-www-form-urlencoded':
                result +=
                    ' \\\n --data "' +
                        escapeQuotes(qs.stringify(data.data)) +
                        '"';
                break;
            default:
                if ((0, isString_1.default)(data.data)) {
                    result += ' \\\n --data "' + escapeQuotes(data.data) + '"';
                }
                else if (Object.keys(data.data).length === 0) {
                    // Do nothing with empty object data.
                }
                else {
                    Sentry.withScope(scope => {
                        scope.setExtra('data', data);
                        Sentry.captureException(new Error('Unknown event data'));
                    });
                }
        }
    }
    result += ' \\\n "' + getFullUrl(data) + '"';
    return result;
}
exports.getCurlCommand = getCurlCommand;
function stringifyQueryList(query) {
    if ((0, isString_1.default)(query)) {
        return query;
    }
    const queryObj = {};
    for (const kv of query) {
        if (kv !== null && kv.length === 2) {
            const [key, value] = kv;
            if (value !== null) {
                if (Array.isArray(queryObj[key])) {
                    queryObj[key].push(value);
                }
                else {
                    queryObj[key] = [value];
                }
            }
        }
    }
    return qs.stringify(queryObj);
}
exports.stringifyQueryList = stringifyQueryList;
function getFullUrl(data) {
    var _a;
    let fullUrl = data === null || data === void 0 ? void 0 : data.url;
    if (!fullUrl) {
        return fullUrl;
    }
    if ((_a = data === null || data === void 0 ? void 0 : data.query) === null || _a === void 0 ? void 0 : _a.length) {
        fullUrl += '?' + stringifyQueryList(data.query);
    }
    if (data.fragment) {
        fullUrl += '#' + data.fragment;
    }
    return fullUrl;
}
exports.getFullUrl = getFullUrl;
/**
 * Converts an object of body/querystring key/value pairs
 * into a tuple of [key, value] pairs, and sorts them.
 *
 * This handles the case for query strings that were decoded like so:
 *
 *   ?foo=bar&foo=baz => { foo: ['bar', 'baz'] }
 *
 * By converting them to [['foo', 'bar'], ['foo', 'baz']]
 */
function objectToSortedTupleArray(obj) {
    return Object.keys(obj)
        .reduce((out, k) => {
        const val = obj[k];
        return out.concat(Array.isArray(val)
            ? val.map(v => [k, v]) // key has multiple values (array)
            : [[k, val]] // key has single value
        );
    }, [])
        .sort(function ([keyA, valA], [keyB, valB]) {
        // if keys are identical, sort on value
        if (keyA === keyB) {
            return valA < valB ? -1 : 1;
        }
        return keyA < keyB ? -1 : 1;
    });
}
exports.objectToSortedTupleArray = objectToSortedTupleArray;
// for context summaries and avatars
function removeFilterMaskedEntries(rawData) {
    const cleanedData = {};
    for (const key of Object.getOwnPropertyNames(rawData)) {
        if (rawData[key] !== constants_1.FILTER_MASK) {
            cleanedData[key] = rawData[key];
        }
    }
    return cleanedData;
}
exports.removeFilterMaskedEntries = removeFilterMaskedEntries;
function formatAddress(address, imageAddressLength) {
    return `0x${address.toString(16).padStart(imageAddressLength !== null && imageAddressLength !== void 0 ? imageAddressLength : 0, '0')}`;
}
exports.formatAddress = formatAddress;
function parseAddress(address) {
    if (!address) {
        return 0;
    }
    try {
        return parseInt(address, 16) || 0;
    }
    catch (_e) {
        return 0;
    }
}
exports.parseAddress = parseAddress;
function getImageRange(image) {
    // The start address is normalized to a `0x` prefixed hex string. The event
    // schema also allows ingesting plain numbers, but this is converted during
    // ingestion.
    const startAddress = parseAddress(image === null || image === void 0 ? void 0 : image.image_addr);
    // The image size is normalized to a regular number. However, it can also be
    // `null`, in which case we assume that it counts up to the next image.
    const endAddress = startAddress + ((image === null || image === void 0 ? void 0 : image.image_size) || 0);
    return [startAddress, endAddress];
}
exports.getImageRange = getImageRange;
function parseAssembly(assembly) {
    let name;
    let version;
    let culture;
    let publicKeyToken;
    const pieces = assembly ? assembly.split(',') : [];
    if (pieces.length === 4) {
        name = pieces[0];
        version = pieces[1].split('Version=')[1];
        culture = pieces[2].split('Culture=')[1];
        publicKeyToken = pieces[3].split('PublicKeyToken=')[1];
    }
    return { name, version, culture, publicKeyToken };
}
exports.parseAssembly = parseAssembly;
function stackTracePlatformIcon(platform, frames) {
    const fileExtensions = (0, uniq_1.default)((0, compact_1.default)(frames.map(frame => { var _a; return (0, fileExtension_1.getFileExtension)((_a = frame.filename) !== null && _a !== void 0 ? _a : ''); })));
    if (fileExtensions.length === 1) {
        const newPlatform = (0, fileExtension_1.fileExtensionToPlatform)(fileExtensions[0]);
        return newPlatform !== null && newPlatform !== void 0 ? newPlatform : platform;
    }
    return platform;
}
exports.stackTracePlatformIcon = stackTracePlatformIcon;
//# sourceMappingURL=utils.jsx.map