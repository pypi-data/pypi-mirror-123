Object.defineProperty(exports, "__esModule", { value: true });
exports.logException = void 0;
const tslib_1 = require("tslib");
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
function logException(ex, context) {
    Sentry.withScope(scope => {
        if (context) {
            scope.setExtra('context', context);
        }
        Sentry.captureException(ex);
    });
    /* eslint no-console:0 */
    window.console && console.error && console.error(ex);
}
exports.logException = logException;
//# sourceMappingURL=logging.jsx.map