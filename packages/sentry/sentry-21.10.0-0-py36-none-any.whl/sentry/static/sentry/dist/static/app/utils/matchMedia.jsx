Object.defineProperty(exports, "__esModule", { value: true });
exports.setupColorScheme = void 0;
const tslib_1 = require("tslib");
const constants_1 = require("app/constants");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
function changeFavicon(theme) {
    // only on prod because we have a development favicon
    if (constants_1.NODE_ENV !== 'production') {
        return;
    }
    const n = document.querySelector('[rel="icon"][type="image/png"]');
    if (!n) {
        return;
    }
    const path = n.href.split('/sentry/')[0];
    n.href = `${path}/sentry/images/${theme === 'dark' ? 'favicon-dark' : 'favicon'}.png`;
}
function handleColorSchemeChange(e) {
    const isDark = e.media === '(prefers-color-scheme: dark)' && e.matches;
    const type = isDark ? 'dark' : 'light';
    changeFavicon(type);
    configStore_1.default.updateTheme(type);
}
function prefersDark() {
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
}
function setupColorScheme() {
    // Set favicon to dark on load if necessary)
    if (prefersDark()) {
        changeFavicon('dark');
        configStore_1.default.updateTheme('dark');
    }
    // Watch for changes in preferred color scheme
    const lightMediaQuery = window.matchMedia('(prefers-color-scheme: light)');
    const darkMediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    try {
        lightMediaQuery.addEventListener('change', handleColorSchemeChange);
        darkMediaQuery.addEventListener('change', handleColorSchemeChange);
    }
    catch (err) {
        // Safari 13 (maybe lower too) does not support `addEventListener`
        // `addListener` is deprecated
        lightMediaQuery.addListener(handleColorSchemeChange);
        darkMediaQuery.addListener(handleColorSchemeChange);
    }
}
exports.setupColorScheme = setupColorScheme;
//# sourceMappingURL=matchMedia.jsx.map