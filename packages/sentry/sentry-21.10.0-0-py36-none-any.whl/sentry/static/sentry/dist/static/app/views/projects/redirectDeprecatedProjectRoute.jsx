Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const isString_1 = (0, tslib_1.__importDefault)(require("lodash/isString"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const getRouteStringFromRoutes_1 = (0, tslib_1.__importDefault)(require("app/utils/getRouteStringFromRoutes"));
const redirect_1 = (0, tslib_1.__importDefault)(require("app/utils/redirect"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
class ProjectDetailsInner extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            loading: true,
            error: null,
            project: null,
        };
        this.fetchData = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            this.setState({
                loading: true,
                error: null,
            });
            const { orgId, projectSlug } = this.props;
            try {
                const project = yield this.props.api.requestPromise(`/projects/${orgId}/${projectSlug}/`);
                this.setState({
                    loading: false,
                    error: null,
                    project,
                });
            }
            catch (error) {
                this.setState({
                    loading: false,
                    error,
                    project: null,
                });
            }
        });
    }
    componentDidMount() {
        this.fetchData();
    }
    getProjectId() {
        if (this.state.project) {
            return this.state.project.id;
        }
        return null;
    }
    hasProjectId() {
        const projectID = this.getProjectId();
        return (0, isString_1.default)(projectID) && projectID.length > 0;
    }
    getOrganizationId() {
        if (this.state.project) {
            return this.state.project.organization.id;
        }
        return null;
    }
    render() {
        const childrenProps = Object.assign(Object.assign({}, this.state), { projectId: this.getProjectId(), hasProjectId: this.hasProjectId(), organizationId: this.getOrganizationId() });
        return this.props.children(childrenProps);
    }
}
const ProjectDetails = (0, withApi_1.default)(ProjectDetailsInner);
const redirectDeprecatedProjectRoute = (generateRedirectRoute) => {
    class RedirectDeprecatedProjectRoute extends React.Component {
        constructor() {
            super(...arguments);
            this.trackRedirect = (organizationId, nextRoute) => {
                const payload = {
                    feature: 'global_views',
                    url: (0, getRouteStringFromRoutes_1.default)(this.props.routes),
                    org_id: parseInt(organizationId, 10),
                };
                // track redirects of deprecated URLs for analytics
                (0, analytics_1.analytics)('deprecated_urls.redirect', payload);
                return nextRoute;
            };
        }
        render() {
            const { params } = this.props;
            const { orgId } = params;
            return (<Wrapper>
          <ProjectDetails orgId={orgId} projectSlug={params.projectId}>
            {({ loading, error, hasProjectId, projectId, organizationId }) => {
                    if (loading) {
                        return <loadingIndicator_1.default />;
                    }
                    if (!hasProjectId || !organizationId) {
                        if (error && error.status === 404) {
                            return (<alert_1.default type="error">
                      {(0, locale_1.t)('The project you were looking for was not found.')}
                    </alert_1.default>);
                        }
                        return <loadingError_1.default />;
                    }
                    const routeProps = {
                        orgId,
                        projectId,
                        router: { params },
                    };
                    return (<redirect_1.default router={this.props.router} to={this.trackRedirect(organizationId, generateRedirectRoute(routeProps))}/>);
                }}
          </ProjectDetails>
        </Wrapper>);
        }
    }
    return RedirectDeprecatedProjectRoute;
};
exports.default = redirectDeprecatedProjectRoute;
const Wrapper = (0, styled_1.default)('div') `
  flex: 1;
  padding: ${(0, space_1.default)(3)};
`;
//# sourceMappingURL=redirectDeprecatedProjectRoute.jsx.map