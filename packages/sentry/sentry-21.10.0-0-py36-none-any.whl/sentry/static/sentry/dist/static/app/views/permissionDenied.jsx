Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_document_title_1 = (0, tslib_1.__importDefault)(require("react-document-title"));
const react_router_1 = require("react-router");
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const locale_1 = require("app/locale");
const organization_1 = require("app/styles/organization");
const getRouteStringFromRoutes_1 = (0, tslib_1.__importDefault)(require("app/utils/getRouteStringFromRoutes"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const withProject_1 = (0, tslib_1.__importDefault)(require("app/utils/withProject"));
const ERROR_NAME = 'Permission Denied';
class PermissionDenied extends react_1.Component {
    componentDidMount() {
        const { organization, project, routes } = this.props;
        const route = (0, getRouteStringFromRoutes_1.default)(routes);
        Sentry.withScope(scope => {
            scope.setFingerprint([ERROR_NAME, route]);
            scope.setExtra('route', route);
            scope.setExtra('orgFeatures', (organization && organization.features) || []);
            scope.setExtra('orgAccess', (organization && organization.access) || []);
            scope.setExtra('projectFeatures', (project && project.features) || []);
            Sentry.captureException(new Error(`${ERROR_NAME}${route ? ` : ${route}` : ''}`));
        });
    }
    render() {
        return (<react_document_title_1.default title={(0, locale_1.t)('Permission Denied')}>
        <organization_1.PageContent>
          <loadingError_1.default message={(0, locale_1.tct)(`Your role does not have the necessary permissions to access this
               resource, please read more about [link:organizational roles]`, {
                link: (<externalLink_1.default href="https://docs.sentry.io/product/accounts/membership/"/>),
            })}/>
        </organization_1.PageContent>
      </react_document_title_1.default>);
    }
}
exports.default = (0, react_router_1.withRouter)((0, withOrganization_1.default)((0, withProject_1.default)(PermissionDenied)));
//# sourceMappingURL=permissionDenied.jsx.map