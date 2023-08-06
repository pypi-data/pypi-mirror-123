Object.defineProperty(exports, "__esModule", { value: true });
const locale_1 = require("app/locale");
function handleError(error) {
    var _a;
    const errorMessage = (_a = error.responseJSON) === null || _a === void 0 ? void 0 : _a.trustedRelays[0];
    if (!errorMessage) {
        return {
            type: 'unknown',
            message: (0, locale_1.t)('An unknown error occurred while saving Relay public key.'),
        };
    }
    if (errorMessage === 'Bad structure received for Trusted Relays') {
        return {
            type: 'bad-structure',
            message: (0, locale_1.t)('An invalid structure was sent.'),
        };
    }
    if (errorMessage === 'Relay key info with missing name in Trusted Relays') {
        return {
            type: 'missing-name',
            message: (0, locale_1.t)('Field Required'),
        };
    }
    if (errorMessage === 'Relay key info with empty name in Trusted Relays') {
        return {
            type: 'empty-name',
            message: (0, locale_1.t)('Invalid Field'),
        };
    }
    if (errorMessage.startsWith('Missing public key for Relay key info with name:')) {
        return {
            type: 'missing-key',
            message: (0, locale_1.t)('Field Required'),
        };
    }
    if (errorMessage.startsWith('Invalid public key for relay key info with name:')) {
        return {
            type: 'invalid-key',
            message: (0, locale_1.t)('Invalid Relay key'),
        };
    }
    if (errorMessage.startsWith('Duplicated key in Trusted Relays:')) {
        return {
            type: 'duplicated-key',
            message: (0, locale_1.t)('Relay key already taken'),
        };
    }
    return {
        type: 'unknown',
        message: (0, locale_1.t)('An unknown error occurred while saving Relay public key.'),
    };
}
exports.default = handleError;
//# sourceMappingURL=handleXhrErrorResponse.jsx.map