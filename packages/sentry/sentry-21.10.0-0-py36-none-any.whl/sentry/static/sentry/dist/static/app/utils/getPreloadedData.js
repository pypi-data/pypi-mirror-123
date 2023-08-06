Object.defineProperty(exports, "__esModule", { value: true });
exports.getPreloadedDataPromise = void 0;
const tslib_1 = require("tslib");
function getPreloadedDataPromise(name, slug, fallback, isInitialFetch) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        try {
            const data = window.__sentry_preload;
            if (!isInitialFetch ||
                !data ||
                !data.orgSlug ||
                data.orgSlug.toLowerCase() !== slug.toLowerCase() ||
                !data[name] ||
                !data[name].then) {
                return yield fallback();
            }
            const result = yield data[name].catch(fallback);
            if (!result) {
                return yield fallback();
            }
            return yield result;
        }
        catch (_) {
            //
        }
        return yield fallback();
    });
}
exports.getPreloadedDataPromise = getPreloadedDataPromise;
//# sourceMappingURL=getPreloadedData.js.map