Object.defineProperty(exports, "__esModule", { value: true });
exports.removeAuthenticator = exports.logout = exports.updateUser = exports.disconnectIdentity = void 0;
const tslib_1 = require("tslib");
const indicator_1 = require("app/actionCreators/indicator");
const api_1 = require("app/api");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
function disconnectIdentity(identity) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const api = new api_1.Client();
        try {
            yield api.requestPromise(`/users/me/social-identities/${identity.id}/`, {
                method: 'DELETE',
            });
            (0, indicator_1.addSuccessMessage)(`Disconnected ${identity.providerLabel}`);
        }
        catch (_a) {
            (0, indicator_1.addErrorMessage)('Error disconnecting identity');
        }
    });
}
exports.disconnectIdentity = disconnectIdentity;
function updateUser(user) {
    const previousUser = configStore_1.default.get('user');
    // If the user changed their theme preferences, we should also update
    // the config store
    if (previousUser.options.theme !== user.options.theme &&
        user.options.theme !== 'system') {
        configStore_1.default.set('theme', user.options.theme);
    }
    // Ideally we'd fire an action but this is gonna get refactored soon anyway
    configStore_1.default.set('user', user);
}
exports.updateUser = updateUser;
function logout(api) {
    return api.requestPromise('/auth/', { method: 'DELETE' });
}
exports.logout = logout;
function removeAuthenticator(api, userId, authId) {
    return api.requestPromise(`/users/${userId}/authenticators/${authId}/`, {
        method: 'DELETE',
    });
}
exports.removeAuthenticator = removeAuthenticator;
//# sourceMappingURL=account.jsx.map