Object.defineProperty(exports, "__esModule", { value: true });
exports.getAppConnectStoreUpdateAlertMessage = exports.appStoreConnectAlertMessage = void 0;
const locale_1 = require("app/locale");
exports.appStoreConnectAlertMessage = {
    iTunesSessionInvalid: (0, locale_1.t)('The iTunes session of your configured App Store Connect needs to be refreshed.'),
    appStoreCredentialsInvalid: (0, locale_1.t)('The credentials of your configured App Store Connect are invalid.'),
};
function getAppConnectStoreUpdateAlertMessage(appConnectValidationData) {
    if (appConnectValidationData.promptItunesSession) {
        return exports.appStoreConnectAlertMessage.iTunesSessionInvalid;
    }
    if (appConnectValidationData.appstoreCredentialsValid === false) {
        return exports.appStoreConnectAlertMessage.appStoreCredentialsInvalid;
    }
    return undefined;
}
exports.getAppConnectStoreUpdateAlertMessage = getAppConnectStoreUpdateAlertMessage;
//# sourceMappingURL=utils.jsx.map