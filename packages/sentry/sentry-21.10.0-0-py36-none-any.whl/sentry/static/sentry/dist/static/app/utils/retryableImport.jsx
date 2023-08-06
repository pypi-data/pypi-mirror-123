Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const utils_1 = require("app/utils");
const MAX_RETRIES = 2;
function retryableImport(fn) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        let retries = 0;
        const tryLoad = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            var _a;
            try {
                const module = yield fn();
                return (_a = module.default) !== null && _a !== void 0 ? _a : module;
            }
            catch (err) {
                if ((0, utils_1.isWebpackChunkLoadingError)(err) && retries < MAX_RETRIES) {
                    retries++;
                    return tryLoad();
                }
                throw err;
            }
        });
        return tryLoad();
    });
}
exports.default = retryableImport;
//# sourceMappingURL=retryableImport.jsx.map