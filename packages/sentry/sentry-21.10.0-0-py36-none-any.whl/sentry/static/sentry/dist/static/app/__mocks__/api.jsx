Object.defineProperty(exports, "__esModule", { value: true });
exports.Client = exports.initApiClientErrorHandling = exports.Request = void 0;
const tslib_1 = require("tslib");
const RealClient = jest.requireActual('app/api');
class Request {
}
exports.Request = Request;
exports.initApiClientErrorHandling = RealClient.initApiClientErrorHandling;
const respond = (isAsync, fn, ...args) => {
    if (fn) {
        if (isAsync) {
            setTimeout(() => fn(...args), 1);
        }
        else {
            fn(...args);
        }
    }
};
const DEFAULT_MOCK_RESPONSE_OPTIONS = {
    predicate: () => true,
};
class Client {
    constructor() {
        this.handleRequestError = RealClient.Client.prototype.handleRequestError;
    }
    static clearMockResponses() {
        Client.mockResponses = [];
    }
    // Returns a jest mock that represents Client.request calls
    static addMockResponse(response, options = DEFAULT_MOCK_RESPONSE_OPTIONS) {
        const mock = jest.fn();
        Client.mockResponses.unshift([
            Object.assign(Object.assign({ statusCode: 200, body: '', method: 'GET', callCount: 0 }, response), { headers: response.headers || {} }),
            mock,
            options.predicate,
        ]);
        return mock;
    }
    static findMockResponse(url, options) {
        return Client.mockResponses.find(([response, _mock, predicate]) => {
            const matchesURL = url === response.url;
            const matchesMethod = (options.method || 'GET') === response.method;
            const matchesPredicate = predicate(url, options);
            return matchesURL && matchesMethod && matchesPredicate;
        });
    }
    uniqueId() {
        return '123';
    }
    // In the real client, this clears in-flight responses. It's NOT clearMockResponses. You probably don't want to call this from a test.
    clear() { }
    wrapCallback(_id, error) {
        return (...args) => {
            // @ts-expect-error
            if (RealClient.hasProjectBeenRenamed(...args)) {
                return;
            }
            respond(Client.mockAsync, error, ...args);
        };
    }
    requestPromise(path, _a = {}) {
        var { includeAllArgs } = _a, options = (0, tslib_1.__rest)(_a, ["includeAllArgs"]);
        return new Promise((resolve, reject) => {
            this.request(path, Object.assign(Object.assign({}, options), { success: (data, ...args) => {
                    includeAllArgs ? resolve([data, ...args]) : resolve(data);
                }, error: (error, ..._args) => {
                    reject(error);
                } }));
        });
    }
    request(url, options = {}) {
        var _a, _b;
        const [response, mock] = Client.findMockResponse(url, options) || [
            undefined,
            undefined,
        ];
        if (!response || !mock) {
            // Endpoints need to be mocked
            const err = new Error(`No mocked response found for request: ${options.method || 'GET'} ${url}`);
            // Mutate stack to drop frames since test file so that we know where in the test
            // this needs to be mocked
            const lines = (_a = err.stack) === null || _a === void 0 ? void 0 : _a.split('\n');
            const startIndex = lines === null || lines === void 0 ? void 0 : lines.findIndex(line => line.includes('tests/js/spec'));
            err.stack = ['\n', lines === null || lines === void 0 ? void 0 : lines[0], ...((_b = lines === null || lines === void 0 ? void 0 : lines.slice(startIndex)) !== null && _b !== void 0 ? _b : [])].join('\n');
            // Throwing an error here does not do what we want it to do....
            // Because we are mocking an API client, we generally catch errors to show
            // user-friendly error messages, this means in tests this error gets gobbled
            // up and developer frustration ensues. Use `setTimeout` to get around this
            setTimeout(() => {
                throw err;
            });
        }
        else {
            // has mocked response
            // mock gets returned when we add a mock response, will represent calls to api.request
            mock(url, options);
            const body = typeof response.body === 'function' ? response.body(url, options) : response.body;
            if (response.statusCode !== 200) {
                response.callCount++;
                const errorResponse = Object.assign({
                    status: response.statusCode,
                    responseText: JSON.stringify(body),
                    responseJSON: body,
                }, {
                    overrideMimeType: () => { },
                    abort: () => { },
                    then: () => { },
                    error: () => { },
                }, new XMLHttpRequest());
                this.handleRequestError({
                    id: '1234',
                    path: url,
                    requestOptions: options,
                }, errorResponse, 'error', 'error');
            }
            else {
                response.callCount++;
                respond(Client.mockAsync, options.success, body, {}, {
                    getResponseHeader: key => response.headers[key],
                });
            }
        }
        respond(Client.mockAsync, options.complete);
    }
}
exports.Client = Client;
Client.mockResponses = [];
Client.mockAsync = false;
//# sourceMappingURL=api.jsx.map