Object.defineProperty(exports, "__esModule", { value: true });
exports.saveToStorage = exports.fetchFromStorage = void 0;
const tslib_1 = require("tslib");
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const localStorage_1 = (0, tslib_1.__importDefault)(require("app/utils/localStorage"));
const ADVANCED_DATA_SCRUBBING_LOCALSTORAGE_KEY = 'advanced-data-scrubbing';
// TODO(Priscila): add the method below in app/utils
function fetchFromStorage() {
    const storage = localStorage_1.default.getItem(ADVANCED_DATA_SCRUBBING_LOCALSTORAGE_KEY);
    if (!storage) {
        return undefined;
    }
    try {
        return JSON.parse(storage);
    }
    catch (err) {
        Sentry.withScope(scope => {
            scope.setExtra('storage', storage);
            Sentry.captureException(err);
        });
        return undefined;
    }
}
exports.fetchFromStorage = fetchFromStorage;
function saveToStorage(obj) {
    try {
        localStorage_1.default.setItem(ADVANCED_DATA_SCRUBBING_LOCALSTORAGE_KEY, JSON.stringify(obj));
    }
    catch (err) {
        Sentry.captureException(err);
        Sentry.withScope(scope => {
            scope.setExtra('storage', obj);
            Sentry.captureException(err);
        });
    }
}
exports.saveToStorage = saveToStorage;
//# sourceMappingURL=localStorage.jsx.map