Object.defineProperty(exports, "__esModule", { value: true });
exports.RouteError = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const getRouteStringFromRoutes_1 = (0, tslib_1.__importDefault)(require("app/utils/getRouteStringFromRoutes"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const withProject_1 = (0, tslib_1.__importDefault)(require("app/utils/withProject"));
class RouteError extends react_1.Component {
    UNSAFE_componentWillMount() {
        const { error } = this.props;
        const { disableLogSentry, disableReport, organization, project, routes } = this.props;
        if (disableLogSentry) {
            return;
        }
        if (!error) {
            return;
        }
        const route = (0, getRouteStringFromRoutes_1.default)(routes);
        const enrichScopeContext = scope => {
            scope.setExtra('route', route);
            scope.setExtra('orgFeatures', (organization && organization.features) || []);
            scope.setExtra('orgAccess', (organization && organization.access) || []);
            scope.setExtra('projectFeatures', (project && project.features) || []);
            return scope;
        };
        if (route) {
            /**
             * Unexpectedly, error.message would sometimes not have a setter property, causing another exception to be thrown,
             * and losing the original error in the process. Wrapping the mutation in a try-catch in an attempt to preserve
             * the original error for logging.
             * See https://github.com/getsentry/sentry/issues/16314 for more details.
             */
            try {
                error.message = `${error.message}: ${route}`;
            }
            catch (e) {
                Sentry.withScope(scope => {
                    enrichScopeContext(scope);
                    Sentry.captureException(e);
                });
            }
        }
        // TODO(dcramer): show something in addition to embed (that contains it?)
        // throw this in a timeout so if it errors we don't fall over
        this._timeout = window.setTimeout(() => {
            Sentry.withScope(scope => {
                enrichScopeContext(scope);
                Sentry.captureException(error);
            });
            if (!disableReport) {
                Sentry.showReportDialog();
            }
        });
    }
    componentWillUnmount() {
        var _a;
        if (this._timeout) {
            window.clearTimeout(this._timeout);
        }
        (_a = document.querySelector('.sentry-error-embed-wrapper')) === null || _a === void 0 ? void 0 : _a.remove();
    }
    render() {
        // TODO(dcramer): show additional resource links
        return (<alert_1.default icon={<icons_1.IconWarning size="md"/>} type="error">
        <Heading>
          <span>{(0, locale_1.t)('Oops! Something went wrong')}</span>
        </Heading>
        <p>
          {(0, locale_1.t)(`
          It looks like you've hit an issue in our client application. Don't worry though!
          We use Sentry to monitor Sentry and it's likely we're already looking into this!
          `)}
        </p>
        <p>{(0, locale_1.t)("If you're daring, you may want to try the following:")}</p>
        <ul>
          {window && window.adblockSuspected && (<li>
              {(0, locale_1.t)("We detected something AdBlock-like. Try disabling it, as it's known to cause issues.")}
            </li>)}
          <li>
            {(0, locale_1.tct)(`Give it a few seconds and [link:reload the page].`, {
                link: (<a onClick={() => {
                        window.location.href = window.location.href;
                    }}/>),
            })}
          </li>
          <li>
            {(0, locale_1.tct)(`If all else fails, [link:contact us] with more details.`, {
                link: <a href="https://github.com/getsentry/sentry/issues/new/choose"/>,
            })}
          </li>
        </ul>
      </alert_1.default>);
    }
}
exports.RouteError = RouteError;
const Heading = (0, styled_1.default)('h3') `
  display: flex;
  align-items: center;

  font-size: ${p => p.theme.headerFontSize};
  font-weight: normal;

  margin-bottom: ${(0, space_1.default)(1.5)};
`;
exports.default = (0, react_router_1.withRouter)((0, withOrganization_1.default)((0, withProject_1.default)(RouteError)));
//# sourceMappingURL=routeError.jsx.map