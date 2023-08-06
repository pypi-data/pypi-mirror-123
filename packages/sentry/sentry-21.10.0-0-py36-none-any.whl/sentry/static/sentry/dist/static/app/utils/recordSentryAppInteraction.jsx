Object.defineProperty(exports, "__esModule", { value: true });
exports.recordInteraction = void 0;
const tslib_1 = require("tslib");
const api_1 = require("app/api");
const recordInteraction = (sentryAppSlug, field, data) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
    const api = new api_1.Client();
    const endpoint = `/sentry-apps/${sentryAppSlug}/interaction/`;
    return yield api.requestPromise(endpoint, {
        method: 'POST',
        data: Object.assign({ tsdbField: field }, data),
    });
});
exports.recordInteraction = recordInteraction;
//# sourceMappingURL=recordSentryAppInteraction.jsx.map