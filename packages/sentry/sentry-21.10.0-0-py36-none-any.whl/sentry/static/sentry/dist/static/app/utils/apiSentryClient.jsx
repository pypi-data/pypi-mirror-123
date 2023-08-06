Object.defineProperty(exports, "__esModule", { value: true });
exports.run = exports.init = void 0;
const tslib_1 = require("tslib");
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
let hub;
function init(dsn) {
    // This client is used to track all API requests that use `app/api`
    // This is a bit noisy so we don't want it in the main project (yet)
    const client = new Sentry.BrowserClient({
        dsn,
    });
    hub = new Sentry.Hub(client);
}
exports.init = init;
const run = cb => {
    if (!hub) {
        return;
    }
    hub.run(cb);
};
exports.run = run;
//# sourceMappingURL=apiSentryClient.jsx.map