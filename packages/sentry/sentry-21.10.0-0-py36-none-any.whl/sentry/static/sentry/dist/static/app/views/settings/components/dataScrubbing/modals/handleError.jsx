Object.defineProperty(exports, "__esModule", { value: true });
exports.ErrorType = void 0;
const locale_1 = require("app/locale");
var ErrorType;
(function (ErrorType) {
    ErrorType["Unknown"] = "unknown";
    ErrorType["InvalidSelector"] = "invalid-selector";
    ErrorType["RegexParse"] = "regex-parse";
})(ErrorType = exports.ErrorType || (exports.ErrorType = {}));
function handleError(error) {
    var _a;
    const errorMessage = (_a = error.responseJSON) === null || _a === void 0 ? void 0 : _a.relayPiiConfig[0];
    if (!errorMessage) {
        return {
            type: ErrorType.Unknown,
            message: (0, locale_1.t)('Unknown error occurred while saving data scrubbing rule'),
        };
    }
    if (errorMessage.startsWith('invalid selector: ')) {
        for (const line of errorMessage.split('\n')) {
            if (line.startsWith('1 | ')) {
                const selector = line.slice(3);
                return {
                    type: ErrorType.InvalidSelector,
                    message: (0, locale_1.t)('Invalid source value: %s', selector),
                };
            }
        }
    }
    if (errorMessage.startsWith('regex parse error:')) {
        for (const line of errorMessage.split('\n')) {
            if (line.startsWith('error:')) {
                const regex = line.slice(6).replace(/at line \d+ column \d+/, '');
                return {
                    type: ErrorType.RegexParse,
                    message: (0, locale_1.t)('Invalid regex: %s', regex),
                };
            }
        }
    }
    return {
        type: ErrorType.Unknown,
        message: (0, locale_1.t)('An unknown error occurred while saving data scrubbing rule'),
    };
}
exports.default = handleError;
//# sourceMappingURL=handleError.jsx.map