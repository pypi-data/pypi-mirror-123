Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const rawStacktraceContent_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/rawStacktraceContent"));
function getStacktraceBody(event) {
    var _a;
    if (!event || !event.entries) {
        return [];
    }
    // TODO(billyvg): This only accounts for the first exception, will need navigation to be able to
    // diff multiple exceptions
    //
    // See: https://github.com/getsentry/sentry/issues/6055
    const exc = event.entries.find(({ type }) => type === 'exception');
    if (!exc) {
        // Look for a message if not an exception
        const msg = event.entries.find(({ type }) => type === 'message');
        if (!msg) {
            return [];
        }
        return ((_a = msg === null || msg === void 0 ? void 0 : msg.data) === null || _a === void 0 ? void 0 : _a.formatted) && [msg.data.formatted];
    }
    if (!exc.data) {
        return [];
    }
    // TODO(ts): This should be verified when EntryData has the correct type
    return exc.data.values
        .filter(value => !!value.stacktrace)
        .map(value => (0, rawStacktraceContent_1.default)(value.stacktrace, event.platform, value))
        .reduce((acc, value) => acc.concat(value), []);
}
exports.default = getStacktraceBody;
//# sourceMappingURL=getStacktraceBody.jsx.map