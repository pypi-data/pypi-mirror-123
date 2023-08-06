Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_document_title_1 = (0, tslib_1.__importDefault)(require("react-document-title"));
function SentryDocumentTitle({ title, orgSlug, projectSlug, children }) {
    function getDocTitle() {
        if (!orgSlug && !projectSlug) {
            return title;
        }
        if (orgSlug && projectSlug) {
            return `${title} - ${orgSlug} - ${projectSlug}`;
        }
        if (orgSlug) {
            return `${title} - ${orgSlug}`;
        }
        return `${title} - ${projectSlug}`;
    }
    const docTitle = getDocTitle();
    return (<react_document_title_1.default title={`${docTitle} - Sentry`}>
      {children}
    </react_document_title_1.default>);
}
exports.default = SentryDocumentTitle;
//# sourceMappingURL=sentryDocumentTitle.jsx.map