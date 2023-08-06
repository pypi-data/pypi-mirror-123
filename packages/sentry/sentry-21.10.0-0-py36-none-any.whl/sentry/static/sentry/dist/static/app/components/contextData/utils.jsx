Object.defineProperty(exports, "__esModule", { value: true });
exports.analyzeStringForRepr = exports.naturalCaseInsensitiveSort = exports.padNumbersInString = exports.looksLikeMultiLineString = exports.looksLikeObjectRepr = void 0;
function looksLikeObjectRepr(value) {
    const a = value[0];
    const z = value[value.length - 1];
    if (a === '<' && z === '>') {
        return true;
    }
    if (a === '[' && z === ']') {
        return true;
    }
    if (a === '(' && z === ')') {
        return true;
    }
    if (z === ')' && value.match(/^[\w\d._-]+\(/)) {
        return true;
    }
    return false;
}
exports.looksLikeObjectRepr = looksLikeObjectRepr;
function looksLikeMultiLineString(value) {
    return !!value.match(/[\r\n]/);
}
exports.looksLikeMultiLineString = looksLikeMultiLineString;
function padNumbersInString(string) {
    return string.replace(/(\d+)/g, (num) => {
        let isNegative = false;
        let realNum = parseInt(num, 10);
        if (realNum < 0) {
            realNum *= -1;
            isNegative = true;
        }
        let s = '0000000000000' + realNum;
        s = s.substr(s.length - (isNegative ? 11 : 12));
        if (isNegative) {
            s = '-' + s;
        }
        return s;
    });
}
exports.padNumbersInString = padNumbersInString;
function naturalCaseInsensitiveSort(a, b) {
    a = padNumbersInString(a).toLowerCase();
    b = padNumbersInString(b).toLowerCase();
    return a === b ? 0 : a < b ? -1 : 1;
}
exports.naturalCaseInsensitiveSort = naturalCaseInsensitiveSort;
function analyzeStringForRepr(value) {
    const rv = {
        repr: value,
        isString: true,
        isMultiLine: false,
        isStripped: false,
    };
    // stripped for security reasons
    if (value.match(/^['"]?\*{8,}['"]?$/)) {
        rv.isStripped = true;
        return rv;
    }
    if (looksLikeObjectRepr(value)) {
        rv.isString = false;
        return rv;
    }
    rv.isMultiLine = looksLikeMultiLineString(value);
    return rv;
}
exports.analyzeStringForRepr = analyzeStringForRepr;
//# sourceMappingURL=utils.jsx.map