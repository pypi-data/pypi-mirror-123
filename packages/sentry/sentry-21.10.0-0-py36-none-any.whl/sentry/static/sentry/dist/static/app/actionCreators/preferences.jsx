Object.defineProperty(exports, "__esModule", { value: true });
exports.loadPreferencesState = exports.showSidebar = exports.hideSidebar = void 0;
const tslib_1 = require("tslib");
const js_cookie_1 = (0, tslib_1.__importDefault)(require("js-cookie"));
const preferencesActions_1 = (0, tslib_1.__importDefault)(require("../actions/preferencesActions"));
const SIDEBAR_COOKIE_KEY = 'sidebar_collapsed';
const COOKIE_ENABLED = '1';
const COOKIE_DISABLED = '0';
function hideSidebar() {
    preferencesActions_1.default.hideSidebar();
    js_cookie_1.default.set(SIDEBAR_COOKIE_KEY, COOKIE_ENABLED);
}
exports.hideSidebar = hideSidebar;
function showSidebar() {
    preferencesActions_1.default.showSidebar();
    js_cookie_1.default.set(SIDEBAR_COOKIE_KEY, COOKIE_DISABLED);
}
exports.showSidebar = showSidebar;
function loadPreferencesState() {
    // Set initial "collapsed" state to true or false
    preferencesActions_1.default.loadInitialState({
        collapsed: js_cookie_1.default.get(SIDEBAR_COOKIE_KEY) === COOKIE_ENABLED,
    });
}
exports.loadPreferencesState = loadPreferencesState;
//# sourceMappingURL=preferences.jsx.map