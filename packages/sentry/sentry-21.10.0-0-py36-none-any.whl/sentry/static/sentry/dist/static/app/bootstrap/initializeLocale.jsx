Object.defineProperty(exports, "__esModule", { value: true });
exports.initializeLocale = void 0;
const tslib_1 = require("tslib");
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const moment = (0, tslib_1.__importStar)(require("moment"));
const qs = (0, tslib_1.__importStar)(require("query-string"));
const locale_1 = require("app/locale");
// zh-cn => zh_CN
function convertToDjangoLocaleFormat(language) {
    const [left, right] = language.split('-');
    return left + (right ? '_' + right.toUpperCase() : '');
}
function getTranslations(language) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        language = convertToDjangoLocaleFormat(language);
        // No need to load the english locale
        if (language === 'en') {
            return locale_1.DEFAULT_LOCALE_DATA;
        }
        try {
            return yield Promise.resolve().then(() => (0, tslib_1.__importStar)(require(`sentry-locale/${language}/LC_MESSAGES/django.po`)));
        }
        catch (e) {
            Sentry.withScope(scope => {
                scope.setLevel(Sentry.Severity.Warning);
                scope.setFingerprint(['sentry-locale-not-found']);
                scope.setExtra('locale', language);
                Sentry.captureException(e);
            });
            // Default locale if not found
            return locale_1.DEFAULT_LOCALE_DATA;
        }
    });
}
/**
 * Initialize locale
 *
 * This *needs* to be initialized as early as possible (e.g. before `app/locale` is used),
 * otherwise the rest of the application will fail to load.
 *
 * Priority:
 *
 * - URL params (`?lang=en`)
 * - User configuration options
 * - User's system language code (from request)
 * - "en" as default
 */
function initializeLocale(config) {
    var _a, _b;
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        let queryString = {};
        // Parse query string for `lang`
        try {
            queryString = qs.parse(window.location.search) || {};
        }
        catch (_c) {
            // ignore if this fails to parse
            // this can happen if we have an invalid query string
            // e.g. unencoded "%"
        }
        const queryStringLang = Array.isArray(queryString.lang)
            ? queryString.lang[0]
            : queryString.lang;
        const languageCode = queryStringLang || ((_b = (_a = config.user) === null || _a === void 0 ? void 0 : _a.options) === null || _b === void 0 ? void 0 : _b.language) || config.languageCode || 'en';
        try {
            const translations = yield getTranslations(languageCode);
            (0, locale_1.setLocale)(translations);
            // No need to import english
            if (languageCode !== 'en') {
                yield Promise.resolve().then(() => (0, tslib_1.__importStar)(require(`moment/locale/${languageCode}`)));
                moment.locale(languageCode);
            }
        }
        catch (err) {
            Sentry.captureException(err);
        }
    });
}
exports.initializeLocale = initializeLocale;
//# sourceMappingURL=initializeLocale.jsx.map