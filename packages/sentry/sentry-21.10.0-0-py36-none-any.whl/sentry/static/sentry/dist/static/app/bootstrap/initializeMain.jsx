Object.defineProperty(exports, "__esModule", { value: true });
exports.initializeMain = void 0;
const tslib_1 = require("tslib");
const initializeLocale_1 = require("./initializeLocale");
function initializeMain(config) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        // This needs to be loaded as early as possible, or else the locale library can
        // throw an exception and prevent the application from being loaded.
        //
        // e.g. `app/constants` uses `t()` and is imported quite early
        yield (0, initializeLocale_1.initializeLocale)(config);
        // This is dynamically imported because we need to make sure locale is configured
        // before proceeding.
        const { initializeApp } = yield Promise.resolve().then(() => (0, tslib_1.__importStar)(require('./initializeApp')));
        yield initializeApp(config);
    });
}
exports.initializeMain = initializeMain;
//# sourceMappingURL=initializeMain.jsx.map