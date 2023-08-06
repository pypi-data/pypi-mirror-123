Object.defineProperty(exports, "__esModule", { value: true });
exports.getAppStoreErrorMessage = void 0;
const tslib_1 = require("tslib");
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const locale_1 = require("app/locale");
const unexpectedErrorMessage = (0, locale_1.t)('An unexpected error occurred while configuring the app store connect');
function getAppStoreErrorMessage(error) {
    var _a, _b, _c, _d;
    if (typeof error === 'string') {
        return error;
    }
    if ((_a = error.responseJSON) === null || _a === void 0 ? void 0 : _a.code) {
        return ((_c = (_b = error.responseJSON) === null || _b === void 0 ? void 0 : _b.code[0]) !== null && _c !== void 0 ? _c : unexpectedErrorMessage);
    }
    switch ((_d = error.responseJSON) === null || _d === void 0 ? void 0 : _d.detail.code) {
        case 'app-connect-authentication-error':
            return (0, locale_1.t)('We could not establish a connection with App Store Connect. Please check the entered App Store Connect credentials');
        case 'app-connect-multiple-sources-error':
            return (0, locale_1.t)('Only one Apple App Store Connect application is allowed in this project');
        case 'itunes-authentication-error':
            return (0, locale_1.t)('The iTunes authentication failed. Please check the provided credentials');
        case 'itunes-sms-blocked-error':
            return (0, locale_1.t)('Blocked from requesting more SMS codes for an unspecified period of time');
        case 'itunes-2fa-required':
            return (0, locale_1.t)('The two factor authentication failed. Please check the entered code');
        default: {
            // this shall not happen
            Sentry.captureException(new Error('Unknown app store connect error'));
            return unexpectedErrorMessage;
        }
    }
}
exports.getAppStoreErrorMessage = getAppStoreErrorMessage;
//# sourceMappingURL=utils.jsx.map