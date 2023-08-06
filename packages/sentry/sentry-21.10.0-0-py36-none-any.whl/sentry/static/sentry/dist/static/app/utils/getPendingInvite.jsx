Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const js_cookie_1 = (0, tslib_1.__importDefault)(require("js-cookie"));
const queryString = (0, tslib_1.__importStar)(require("query-string"));
function getPendingInvite() {
    const data = js_cookie_1.default.get('pending-invite');
    if (!data) {
        return null;
    }
    return queryString.parse(data);
}
exports.default = getPendingInvite;
//# sourceMappingURL=getPendingInvite.jsx.map