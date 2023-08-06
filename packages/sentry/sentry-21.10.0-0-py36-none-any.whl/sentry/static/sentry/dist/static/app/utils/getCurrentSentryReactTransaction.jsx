Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
/**
 * Gets the current transaction, if one exists.
 */
function getCurrentSentryReactTransaction() {
    var _a, _b;
    return (_b = (_a = Sentry === null || Sentry === void 0 ? void 0 : Sentry.getCurrentHub()) === null || _a === void 0 ? void 0 : _a.getScope()) === null || _b === void 0 ? void 0 : _b.getTransaction();
}
exports.default = getCurrentSentryReactTransaction;
//# sourceMappingURL=getCurrentSentryReactTransaction.jsx.map