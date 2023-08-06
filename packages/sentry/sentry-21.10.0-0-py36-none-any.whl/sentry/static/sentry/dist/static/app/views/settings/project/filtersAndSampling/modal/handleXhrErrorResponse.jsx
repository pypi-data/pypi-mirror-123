Object.defineProperty(exports, "__esModule", { value: true });
const locale_1 = require("app/locale");
function handleXhrErrorResponse(error, currentRuleIndex) {
    var _a, _b, _c;
    const responseErrors = (_c = (_b = (_a = error.responseJSON) === null || _a === void 0 ? void 0 : _a.dynamicSampling) === null || _b === void 0 ? void 0 : _b.rules[currentRuleIndex]) !== null && _c !== void 0 ? _c : {};
    const [type, value] = Object.entries(responseErrors)[0];
    if (type === 'sampleRate') {
        const message = Array.isArray(value) ? value[0] : value;
        if (message === 'Ensure this value is less than or equal to 1.') {
            return {
                type: 'sampleRate',
                message: (0, locale_1.t)('Ensure this value is a floating number between 0 and 100'),
            };
        }
    }
    return {
        type: 'unknown',
        message: (0, locale_1.t)('An internal error occurred while saving dynamic sampling rule'),
    };
}
exports.default = handleXhrErrorResponse;
//# sourceMappingURL=handleXhrErrorResponse.jsx.map