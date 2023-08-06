Object.defineProperty(exports, "__esModule", { value: true });
exports.extraQueryParameter = exports.emailQueryParameter = void 0;
const tslib_1 = require("tslib");
const getCookie_1 = (0, tslib_1.__importDefault)(require("app/utils/getCookie"));
// return email query parameter
function emailQueryParameter() {
    const email = localStorage.getItem('email');
    const queryParameter = email ? `?email=${email}` : '';
    return queryParameter;
}
exports.emailQueryParameter = emailQueryParameter;
// return extra query depending, depending on if used in getStartedUrl
function extraQueryParameter(getStarted) {
    const email = localStorage.getItem('email');
    const extraQueryString = (0, getCookie_1.default)('extra_query_string');
    // cookies that have = sign are quotes so extra quotes need to be removed
    const extraQuery = extraQueryString ? extraQueryString.replaceAll('"', '') : '';
    if (getStarted) {
        const emailSeparator = email ? '&' : '?';
        const getStartedSeparator = extraQueryString ? emailSeparator : '';
        return getStartedSeparator + extraQuery;
    }
    const extraSeparator = extraQueryString ? `?` : '';
    return extraSeparator + extraQuery;
}
exports.extraQueryParameter = extraQueryParameter;
//# sourceMappingURL=demoMode.jsx.map