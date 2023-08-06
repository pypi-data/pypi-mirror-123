Object.defineProperty(exports, "__esModule", { value: true });
exports.isActiveSuperuser = void 0;
const tslib_1 = require("tslib");
const js_cookie_1 = (0, tslib_1.__importDefault)(require("js-cookie"));
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const SUPERUSER_COOKIE_NAME = 'su';
/**
 * Checking for just isSuperuser on a config object may not be enough as backend often checks for *active* superuser.
 * We therefore check both isSuperuser flag AND superuser session cookie.
 */
function isActiveSuperuser() {
    const { isSuperuser } = configStore_1.default.get('user') || {};
    if (isSuperuser) {
        /**
         * Superuser cookie cannot be checked for existence as it is HttpOnly.
         * As a workaround, we try to change it to something else and if that fails we can assume that it's being present.
         * There may be an edgecase where it's present and expired but for current usage it's not a big deal.
         */
        js_cookie_1.default.set(SUPERUSER_COOKIE_NAME, 'test');
        if (js_cookie_1.default.get(SUPERUSER_COOKIE_NAME) === undefined) {
            return true;
        }
    }
    return false;
}
exports.isActiveSuperuser = isActiveSuperuser;
//# sourceMappingURL=isActiveSuperuser.jsx.map