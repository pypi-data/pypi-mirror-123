Object.defineProperty(exports, "__esModule", { value: true });
exports.singleLineRenderer = void 0;
const tslib_1 = require("tslib");
const dompurify_1 = (0, tslib_1.__importDefault)(require("dompurify"));
const marked_1 = (0, tslib_1.__importDefault)(require("marked")); // eslint-disable-line no-restricted-imports
const constants_1 = require("app/constants");
// Only https and mailto, (e.g. no javascript, vbscript, data protocols)
const safeLinkPattern = /^(https?:|mailto:)/i;
const safeImagePattern = /^https?:\/\/./i;
function isSafeHref(href, pattern) {
    try {
        return pattern.test(decodeURIComponent(unescape(href)));
    }
    catch (_a) {
        return false;
    }
}
/**
 * Implementation of marked.Renderer which additonally sanitizes URLs.
 */
class SafeRenderer extends marked_1.default.Renderer {
    link(href, title, text) {
        // For a bad link, just return the plain text href
        if (!isSafeHref(href, safeLinkPattern)) {
            return href;
        }
        const out = `<a href="${href}"${title ? ` title="${title}"` : ''}>${text}</a>`;
        return dompurify_1.default.sanitize(out);
    }
    image(href, title, text) {
        // For a bad image, return an empty string
        if (this.options.sanitize && !isSafeHref(href, safeImagePattern)) {
            return '';
        }
        return `<img src="${href}" alt="${text}"${title ? ` title="${title}"` : ''} />`;
    }
}
class NoParagraphRenderer extends SafeRenderer {
    paragraph(text) {
        return text;
    }
}
marked_1.default.setOptions({
    renderer: new SafeRenderer(),
    sanitize: true,
    // Silence sanitize deprecation warning in test / ci (CI sets NODE_NV
    // to production, but specifies `CI`).
    //
    // [!!] This has the side effect of causing failed markdown content to render
    //      as a html error, instead of throwing an exception, however none of
    //      our tests are rendering failed markdown so this is likely a safe
    //      tradeoff to turn off off the deprecation warning.
    silent: !!constants_1.IS_ACCEPTANCE_TEST || constants_1.NODE_ENV === 'test',
});
const sanitizedMarked = (...args) => dompurify_1.default.sanitize((0, marked_1.default)(...args));
const singleLineRenderer = (text, options = {}) => sanitizedMarked(text, Object.assign(Object.assign({}, options), { renderer: new NoParagraphRenderer() }));
exports.singleLineRenderer = singleLineRenderer;
exports.default = sanitizedMarked;
//# sourceMappingURL=marked.jsx.map