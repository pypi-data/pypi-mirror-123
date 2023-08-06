Object.defineProperty(exports, "__esModule", { value: true });
function routeTitleGen(routeName, orgSlug, withSentry = true, projectSlug) {
    const tmplBase = `${routeName} - ${orgSlug}`;
    const tmpl = projectSlug ? `${tmplBase} - ${projectSlug}` : tmplBase;
    return withSentry ? `${tmpl} - Sentry` : tmpl;
}
exports.default = routeTitleGen;
//# sourceMappingURL=routeTitle.jsx.map