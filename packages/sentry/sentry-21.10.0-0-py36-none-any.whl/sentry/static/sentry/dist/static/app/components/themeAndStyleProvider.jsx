Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_dom_1 = (0, tslib_1.__importDefault)(require("react-dom"));
const css_1 = require("@emotion/css"); // eslint-disable-line emotion/no-vanilla
const react_2 = require("@emotion/react"); // This is needed to set "speedy" = false (for percy)
const preferences_1 = require("app/actionCreators/preferences");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const useLegacyStore_1 = require("app/stores/useLegacyStore");
const global_1 = (0, tslib_1.__importDefault)(require("app/styles/global"));
const theme_1 = require("app/utils/theme");
/**
 * Wraps children with emotions ThemeProvider reactively set a theme.
 *
 * Also injects the sentry GlobalStyles .
 */
function ThemeAndStyleProvider({ children }) {
    (0, react_1.useEffect)(() => void (0, preferences_1.loadPreferencesState)(), []);
    const config = (0, useLegacyStore_1.useLegacyStore)(configStore_1.default);
    const theme = config.theme === 'dark' ? theme_1.darkTheme : theme_1.lightTheme;
    return (<react_2.ThemeProvider theme={theme}>
      <global_1.default isDark={config.theme === 'dark'} theme={theme}/>
      <react_2.CacheProvider value={css_1.cache}>{children}</react_2.CacheProvider>
      {react_dom_1.default.createPortal(<meta name="color-scheme" content={config.theme}/>, document.head)}
    </react_2.ThemeProvider>);
}
exports.default = ThemeAndStyleProvider;
//# sourceMappingURL=themeAndStyleProvider.jsx.map