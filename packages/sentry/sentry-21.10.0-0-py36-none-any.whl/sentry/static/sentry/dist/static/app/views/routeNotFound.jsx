Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_document_title_1 = (0, tslib_1.__importDefault)(require("react-document-title"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const notFound_1 = (0, tslib_1.__importDefault)(require("app/components/errors/notFound"));
const footer_1 = (0, tslib_1.__importDefault)(require("app/components/footer"));
const sidebar_1 = (0, tslib_1.__importDefault)(require("app/components/sidebar"));
const locale_1 = require("app/locale");
function RouteNotFound({ router, location }) {
    const { pathname, search, hash } = location;
    const isMissingSlash = pathname[pathname.length - 1] !== '/';
    (0, react_1.useEffect)(() => {
        // Attempt to fix trailing slashes first
        if (isMissingSlash) {
            router.replace(`${pathname}/${search}${hash}`);
            return;
        }
        Sentry.withScope(scope => {
            scope.setFingerprint(['RouteNotFound']);
            Sentry.captureException(new Error('Route not found'));
        });
    }, [pathname]);
    if (isMissingSlash) {
        return null;
    }
    return (<react_document_title_1.default title={(0, locale_1.t)('Page Not Found')}>
      <div className="app">
        <sidebar_1.default location={location}/>
        <div className="container">
          <div className="content">
            <section className="body">
              <notFound_1.default />
            </section>
          </div>
        </div>
        <footer_1.default />
      </div>
    </react_document_title_1.default>);
}
exports.default = RouteNotFound;
//# sourceMappingURL=routeNotFound.jsx.map