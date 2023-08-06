Object.defineProperty(exports, "__esModule", { value: true });
exports.bootstrap = void 0;
const tslib_1 = require("tslib");
const BOOTSTRAP_URL = '/api/client-config/';
const bootApplication = (data) => {
    window.csrfCookieName = data.csrfCookieName;
    return data;
};
/**
 * Load the client configuration data using the BOOTSTRAP_URL. Used when
 * running in standalone SPA mode.
 */
function bootWithHydration() {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const response = yield fetch(BOOTSTRAP_URL);
        const data = yield response.json();
        window.__initialData = data;
        return bootApplication(data);
    });
}
/**
 * Load client configuration bootstrap data. This will detect if the app is
 * running in SPA mode or being booted from the django-rendered layout.html
 * template.
 */
function bootstrap() {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const bootstrapData = window.__initialData;
        // If __initialData is not already set on the window, we are likely running in
        // pure SPA mode, meaning django is not serving our frontend application and we
        // need to make an API request to hydrate the bootstrap data to boot the app.
        if (bootstrapData === undefined) {
            return yield bootWithHydration();
        }
        return bootApplication(bootstrapData);
    });
}
exports.bootstrap = bootstrap;
//# sourceMappingURL=index.jsx.map