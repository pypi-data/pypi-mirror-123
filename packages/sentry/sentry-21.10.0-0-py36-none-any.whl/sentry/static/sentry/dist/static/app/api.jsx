Object.defineProperty(exports, "__esModule", { value: true });
exports.Client = exports.hasProjectBeenRenamed = exports.initApiClientErrorHandling = exports.Request = void 0;
const tslib_1 = require("tslib");
const react_router_1 = require("react-router");
const react_1 = require("@sentry/react");
const js_cookie_1 = (0, tslib_1.__importDefault)(require("js-cookie"));
const isUndefined_1 = (0, tslib_1.__importDefault)(require("lodash/isUndefined"));
const qs = (0, tslib_1.__importStar)(require("query-string"));
const modal_1 = require("app/actionCreators/modal");
const constants_1 = require("app/constants");
const apiErrorCodes_1 = require("app/constants/apiErrorCodes");
const analytics_1 = require("app/utils/analytics");
const apiSentryClient_1 = require("app/utils/apiSentryClient");
const getCsrfToken_1 = (0, tslib_1.__importDefault)(require("app/utils/getCsrfToken"));
const guid_1 = require("app/utils/guid");
const createRequestError_1 = (0, tslib_1.__importDefault)(require("app/utils/requestError/createRequestError"));
class Request {
    constructor(requestPromise, aborter) {
        this.requestPromise = requestPromise;
        this.aborter = aborter;
        this.alive = true;
    }
    cancel() {
        var _a;
        this.alive = false;
        (_a = this.aborter) === null || _a === void 0 ? void 0 : _a.abort();
        (0, analytics_1.metric)('app.api.request-abort', 1);
    }
}
exports.Request = Request;
/**
 * Check if the requested method does not require CSRF tokens
 */
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method !== null && method !== void 0 ? method : '');
}
// TODO: Need better way of identifying anonymous pages that don't trigger redirect
const ALLOWED_ANON_PAGES = [
    /^\/accept\//,
    /^\/share\//,
    /^\/auth\/login\//,
    /^\/join-request\//,
];
const globalErrorHandlers = [];
const initApiClientErrorHandling = () => globalErrorHandlers.push((resp) => {
    var _a, _b, _c, _d;
    const pageAllowsAnon = ALLOWED_ANON_PAGES.find(regex => regex.test(window.location.pathname));
    // Ignore error unless it is a 401
    if (!resp || resp.status !== 401 || pageAllowsAnon) {
        return;
    }
    const code = (_b = (_a = resp === null || resp === void 0 ? void 0 : resp.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) === null || _b === void 0 ? void 0 : _b.code;
    const extra = (_d = (_c = resp === null || resp === void 0 ? void 0 : resp.responseJSON) === null || _c === void 0 ? void 0 : _c.detail) === null || _d === void 0 ? void 0 : _d.extra;
    // 401s can also mean sudo is required or it's a request that is allowed to fail
    // Ignore if these are the cases
    if ([
        'sudo-required',
        'ignore',
        '2fa-required',
        'app-connect-authentication-error',
        'itunes-authentication-error',
        'itunes-2fa-required',
        'itunes-sms-blocked-error',
    ].includes(code)) {
        return;
    }
    // If user must login via SSO, redirect to org login page
    if (code === 'sso-required') {
        window.location.assign(extra.loginUrl);
        return;
    }
    if (code === 'member-disabled-over-limit') {
        react_router_1.browserHistory.replace(extra.next);
    }
    // Otherwise, the user has become unauthenticated. Send them to auth
    js_cookie_1.default.set('session_expired', '1');
    if (constants_1.EXPERIMENTAL_SPA) {
        react_router_1.browserHistory.replace('/auth/login/');
    }
    else {
        window.location.reload();
    }
});
exports.initApiClientErrorHandling = initApiClientErrorHandling;
/**
 * Construct a full request URL
 */
function buildRequestUrl(baseUrl, path, query) {
    let params;
    try {
        params = qs.stringify(query !== null && query !== void 0 ? query : []);
    }
    catch (err) {
        (0, apiSentryClient_1.run)(Sentry => Sentry.withScope(scope => {
            scope.setExtra('path', path);
            scope.setExtra('query', query);
            Sentry.captureException(err);
        }));
        throw err;
    }
    // Append the baseUrl
    let fullUrl = path.includes(baseUrl) ? path : baseUrl + path;
    // Append query parameters
    if (params) {
        fullUrl += fullUrl.includes('?') ? `&${params}` : `?${params}`;
    }
    return fullUrl;
}
/**
 * Check if the API response says project has been renamed.  If so, redirect
 * user to new project slug
 */
// TODO(ts): refine this type later
function hasProjectBeenRenamed(response) {
    var _a, _b, _c, _d, _e;
    const code = (_b = (_a = response === null || response === void 0 ? void 0 : response.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) === null || _b === void 0 ? void 0 : _b.code;
    // XXX(billy): This actually will never happen because we can't intercept the 302
    // jQuery ajax will follow the redirect by default...
    //
    // TODO(epurkhiser): We use fetch now, is the above comment still true?
    if (code !== apiErrorCodes_1.PROJECT_MOVED) {
        return false;
    }
    const slug = (_e = (_d = (_c = response === null || response === void 0 ? void 0 : response.responseJSON) === null || _c === void 0 ? void 0 : _c.detail) === null || _d === void 0 ? void 0 : _d.extra) === null || _e === void 0 ? void 0 : _e.slug;
    (0, modal_1.redirectToProject)(slug);
    return true;
}
exports.hasProjectBeenRenamed = hasProjectBeenRenamed;
/**
 * The API client is used to make HTTP requests to Sentry's backend.
 *
 * This is they preferred way to talk to the backend.
 */
class Client {
    constructor(options = {}) {
        var _a;
        this.baseUrl = (_a = options.baseUrl) !== null && _a !== void 0 ? _a : '/api/0';
        this.activeRequests = {};
    }
    wrapCallback(id, func, cleanup = false) {
        return (...args) => {
            const req = this.activeRequests[id];
            if (cleanup === true) {
                delete this.activeRequests[id];
            }
            if (!(req === null || req === void 0 ? void 0 : req.alive)) {
                return;
            }
            // Check if API response is a 302 -- means project slug was renamed and user
            // needs to be redirected
            // @ts-expect-error
            if (hasProjectBeenRenamed(...args)) {
                return;
            }
            if ((0, isUndefined_1.default)(func)) {
                return;
            }
            // Call success callback
            return func.apply(req, args); // eslint-disable-line
        };
    }
    /**
     * Attempt to cancel all active fetch requests
     */
    clear() {
        Object.values(this.activeRequests).forEach(r => r.cancel());
    }
    handleRequestError({ id, path, requestOptions }, response, textStatus, errorThrown) {
        var _a, _b;
        const code = (_b = (_a = response === null || response === void 0 ? void 0 : response.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) === null || _b === void 0 ? void 0 : _b.code;
        const isSudoRequired = code === apiErrorCodes_1.SUDO_REQUIRED || code === apiErrorCodes_1.SUPERUSER_REQUIRED;
        let didSuccessfullyRetry = false;
        if (isSudoRequired) {
            (0, modal_1.openSudo)({
                superuser: code === apiErrorCodes_1.SUPERUSER_REQUIRED,
                sudo: code === apiErrorCodes_1.SUDO_REQUIRED,
                retryRequest: () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
                    var _c, _d;
                    try {
                        const data = yield this.requestPromise(path, requestOptions);
                        (_c = requestOptions.success) === null || _c === void 0 ? void 0 : _c.call(requestOptions, data);
                        didSuccessfullyRetry = true;
                    }
                    catch (err) {
                        (_d = requestOptions.error) === null || _d === void 0 ? void 0 : _d.call(requestOptions, err);
                    }
                }),
                onClose: () => { var _a; 
                // If modal was closed, then forward the original response
                return !didSuccessfullyRetry && ((_a = requestOptions.error) === null || _a === void 0 ? void 0 : _a.call(requestOptions, response)); },
            });
            return;
        }
        // Call normal error callback
        const errorCb = this.wrapCallback(id, requestOptions.error);
        errorCb === null || errorCb === void 0 ? void 0 : errorCb(response, textStatus, errorThrown);
    }
    /**
     * Initate a request to the backend API.
     *
     * Consider using `requestPromise` for the async Promise version of this method.
     */
    request(path, options = {}) {
        const method = options.method || (options.data ? 'POST' : 'GET');
        let fullUrl = buildRequestUrl(this.baseUrl, path, options.query);
        let data = options.data;
        if (!(0, isUndefined_1.default)(data) && method !== 'GET') {
            data = JSON.stringify(data);
        }
        // TODO(epurkhiser): Mimicking the old jQuery API, data could be a string /
        // object for GET requets. jQuery just sticks it onto the URL as query
        // parameters
        if (method === 'GET' && data) {
            const queryString = typeof data === 'string' ? data : qs.stringify(data);
            if (queryString.length > 0) {
                fullUrl = fullUrl + (fullUrl.indexOf('?') !== -1 ? '&' : '?') + queryString;
            }
        }
        const id = (0, guid_1.uniqueId)();
        const startMarker = `api-request-start-${id}`;
        analytics_1.metric.mark({ name: startMarker });
        const errorObject = new Error();
        /**
         * Called when the request completes with a 2xx status
         */
        const successHandler = (resp, textStatus, responseData) => {
            analytics_1.metric.measure({
                name: 'app.api.request-success',
                start: startMarker,
                data: { status: resp === null || resp === void 0 ? void 0 : resp.status },
            });
            if (!(0, isUndefined_1.default)(options.success)) {
                this.wrapCallback(id, options.success)(responseData, textStatus, resp);
            }
        };
        /**
         * Called when the request is non-2xx
         */
        const errorHandler = (resp, textStatus, errorThrown) => {
            analytics_1.metric.measure({
                name: 'app.api.request-error',
                start: startMarker,
                data: { status: resp === null || resp === void 0 ? void 0 : resp.status },
            });
            if (resp &&
                resp.status !== 0 &&
                resp.status !== 404 &&
                errorThrown !== 'Request was aborted') {
                (0, apiSentryClient_1.run)(Sentry => Sentry.withScope(scope => {
                    var _a;
                    // `requestPromise` can pass its error object
                    const preservedError = (_a = options.preservedError) !== null && _a !== void 0 ? _a : errorObject;
                    const errorObjectToUse = (0, createRequestError_1.default)(resp, preservedError.stack, method, path);
                    errorObjectToUse.removeFrames(3);
                    // Setting this to warning because we are going to capture all failed requests
                    scope.setLevel(react_1.Severity.Warning);
                    scope.setTag('http.statusCode', String(resp.status));
                    scope.setTag('error.reason', errorThrown);
                    Sentry.captureException(errorObjectToUse);
                }));
            }
            this.handleRequestError({ id, path, requestOptions: options }, resp, textStatus, errorThrown);
        };
        /**
         * Called when the request completes
         */
        const completeHandler = (resp, textStatus) => this.wrapCallback(id, options.complete, true)(resp, textStatus);
        // AbortController is optional, though most browser should support it.
        const aborter = typeof AbortController !== 'undefined' ? new AbortController() : undefined;
        // GET requests may not have a body
        const body = method !== 'GET' ? data : undefined;
        const headers = new Headers({
            Accept: 'application/json; charset=utf-8',
            'Content-Type': 'application/json',
        });
        // Do not set the X-CSRFToken header when making a request outside of the
        // current domain
        const absoluteUrl = new URL(fullUrl, window.location.origin);
        const isSameOrigin = window.location.origin === absoluteUrl.origin;
        if (!csrfSafeMethod(method) && isSameOrigin) {
            headers.set('X-CSRFToken', (0, getCsrfToken_1.default)());
        }
        const fetchRequest = fetch(fullUrl, {
            method,
            body,
            headers,
            credentials: 'same-origin',
            signal: aborter === null || aborter === void 0 ? void 0 : aborter.signal,
        });
        // XXX(epurkhiser): We migrated off of jquery, so for now we have a
        // compatibility layer which mimics that of the jquery response objects.
        fetchRequest
            .then((response) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            // The Response's body can only be resolved/used at most once.
            // So we clone the response so we can resolve the body content as text content.
            // Response objects need to be cloned before its body can be used.
            const responseClone = response.clone();
            let responseJSON;
            let responseText;
            const { status, statusText } = response;
            let { ok } = response;
            let errorReason = 'Request not OK'; // the default error reason
            // Try to get text out of the response no matter the status
            try {
                responseText = yield response.text();
            }
            catch (error) {
                ok = false;
                if (error.name === 'AbortError') {
                    errorReason = 'Request was aborted';
                }
                else {
                    errorReason = error.toString();
                }
            }
            const responseContentType = response.headers.get('content-type');
            const isResponseJSON = responseContentType === null || responseContentType === void 0 ? void 0 : responseContentType.includes('json');
            const isStatus3XX = status >= 300 && status < 400;
            if (status !== 204 && !isStatus3XX) {
                try {
                    responseJSON = yield responseClone.json();
                }
                catch (error) {
                    if (error.name === 'AbortError') {
                        ok = false;
                        errorReason = 'Request was aborted';
                    }
                    else if (isResponseJSON && error instanceof SyntaxError) {
                        // If the MIME type is `application/json` but decoding failed,
                        // this should be an error.
                        ok = false;
                        errorReason = 'JSON parse error';
                    }
                }
            }
            const responseMeta = {
                status,
                statusText,
                responseJSON,
                responseText,
                getResponseHeader: (header) => response.headers.get(header),
            };
            // Respect the response content-type header
            const responseData = isResponseJSON ? responseJSON : responseText;
            if (ok) {
                successHandler(responseMeta, statusText, responseData);
            }
            else {
                globalErrorHandlers.forEach(handler => handler(responseMeta));
                errorHandler(responseMeta, statusText, errorReason);
            }
            completeHandler(responseMeta, statusText);
        }))
            .catch(err => {
            // Aborts are expected
            if ((err === null || err === void 0 ? void 0 : err.name) === 'AbortError') {
                return;
            }
            // The request failed for other reason
            (0, apiSentryClient_1.run)(Sentry => Sentry.withScope(scope => {
                scope.setLevel(react_1.Severity.Warning);
                Sentry.captureException(err);
            }));
        });
        const request = new Request(fetchRequest, aborter);
        this.activeRequests[id] = request;
        return request;
    }
    requestPromise(path, _a = {}) {
        var { includeAllArgs } = _a, options = (0, tslib_1.__rest)(_a, ["includeAllArgs"]);
        // Create an error object here before we make any async calls so that we
        // have a helpful stack trace if it errors
        //
        // This *should* get logged to Sentry only if the promise rejection is not handled
        // (since SDK captures unhandled rejections). Ideally we explicitly ignore rejection
        // or handle with a user friendly error message
        const preservedError = new Error();
        return new Promise((resolve, reject) => this.request(path, Object.assign(Object.assign({}, options), { preservedError, success: (data, textStatus, resp) => {
                if (includeAllArgs) {
                    resolve([data, textStatus, resp]);
                }
                else {
                    resolve(data);
                }
            }, error: (resp) => {
                const errorObjectToUse = (0, createRequestError_1.default)(resp, preservedError.stack, options.method, path);
                errorObjectToUse.removeFrames(2);
                // Although `this.request` logs all error responses, this error object can
                // potentially be logged by Sentry's unhandled rejection handler
                reject(errorObjectToUse);
            } })));
    }
}
exports.Client = Client;
//# sourceMappingURL=api.jsx.map