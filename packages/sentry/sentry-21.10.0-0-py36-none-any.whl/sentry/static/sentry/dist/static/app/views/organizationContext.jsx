Object.defineProperty(exports, "__esModule", { value: true });
exports.OrganizationContext = exports.OrganizationLegacyContext = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("react");
const react_document_title_1 = (0, tslib_1.__importDefault)(require("react-document-title"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const modal_1 = require("app/actionCreators/modal");
const organization_1 = require("app/actionCreators/organization");
const projectActions_1 = (0, tslib_1.__importDefault)(require("app/actions/projectActions"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const sidebar_1 = (0, tslib_1.__importDefault)(require("app/components/sidebar"));
const constants_1 = require("app/constants");
const locale_1 = require("app/locale");
const sentryTypes_1 = (0, tslib_1.__importDefault)(require("app/sentryTypes"));
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const hookStore_1 = (0, tslib_1.__importDefault)(require("app/stores/hookStore"));
const organizationStore_1 = (0, tslib_1.__importDefault)(require("app/stores/organizationStore"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const callIfFunction_1 = require("app/utils/callIfFunction");
const getRouteStringFromRoutes_1 = (0, tslib_1.__importDefault)(require("app/utils/getRouteStringFromRoutes"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withOrganizations_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganizations"));
const OrganizationContext = (0, react_1.createContext)(null);
exports.OrganizationContext = OrganizationContext;
class OrganizationContextContainer extends React.Component {
    constructor(props) {
        super(props);
        this.unlisteners = [
            projectActions_1.default.createSuccess.listen(() => this.onProjectCreation(), undefined),
            organizationStore_1.default.listen(data => this.loadOrganization(data), undefined),
        ];
        this.remountComponent = () => {
            this.setState(OrganizationContextContainer.getDefaultState(this.props), this.fetchData);
        };
        this.state = OrganizationContextContainer.getDefaultState(props);
    }
    static getDerivedStateFromProps(props, prevState) {
        const { prevProps } = prevState;
        if (OrganizationContextContainer.shouldRemount(prevProps, props)) {
            return OrganizationContextContainer.getDefaultState(props);
        }
        const { organizationsLoading, location, params } = props;
        const { orgId } = params;
        return Object.assign(Object.assign({}, prevState), { prevProps: {
                orgId,
                organizationsLoading,
                location,
            } });
    }
    static shouldRemount(prevProps, props) {
        const hasOrgIdAndChanged = prevProps.orgId && props.params.orgId && prevProps.orgId !== props.params.orgId;
        const hasOrgId = props.params.orgId ||
            (props.useLastOrganization && configStore_1.default.get('lastOrganization'));
        // protect against the case where we finish fetching org details
        // and then `OrganizationsStore` finishes loading:
        // only fetch in the case where we don't have an orgId
        //
        // Compare `getOrganizationSlug`  because we may have a last used org from server
        // if there is no orgId in the URL
        const organizationLoadingChanged = prevProps.organizationsLoading !== props.organizationsLoading &&
            props.organizationsLoading === false;
        return (hasOrgIdAndChanged ||
            (!hasOrgId && organizationLoadingChanged) ||
            (props.location.state === 'refresh' && prevProps.location.state !== 'refresh'));
    }
    static getDefaultState(props) {
        const prevProps = {
            orgId: props.params.orgId,
            organizationsLoading: props.organizationsLoading,
            location: props.location,
        };
        if (OrganizationContextContainer.isOrgStorePopulatedCorrectly(props)) {
            // retrieve initial state from store
            return Object.assign(Object.assign({}, organizationStore_1.default.get()), { prevProps });
        }
        return {
            loading: true,
            error: null,
            errorType: null,
            organization: null,
            prevProps,
        };
    }
    static getOrganizationSlug(props) {
        var _a, _b;
        return (props.params.orgId ||
            (props.useLastOrganization &&
                (configStore_1.default.get('lastOrganization') ||
                    ((_b = (_a = props.organizations) === null || _a === void 0 ? void 0 : _a[0]) === null || _b === void 0 ? void 0 : _b.slug))));
    }
    static isOrgChanging(props) {
        const { organization } = organizationStore_1.default.get();
        if (!organization) {
            return false;
        }
        return organization.slug !== OrganizationContextContainer.getOrganizationSlug(props);
    }
    static isOrgStorePopulatedCorrectly(props) {
        const { organization, dirty } = organizationStore_1.default.get();
        return !dirty && organization && !OrganizationContextContainer.isOrgChanging(props);
    }
    getChildContext() {
        return {
            organization: this.state.organization,
        };
    }
    componentDidMount() {
        this.fetchData(true);
    }
    componentDidUpdate(prevProps) {
        const remountPrevProps = {
            orgId: prevProps.params.orgId,
            organizationsLoading: prevProps.organizationsLoading,
            location: prevProps.location,
        };
        if (OrganizationContextContainer.shouldRemount(remountPrevProps, this.props)) {
            this.remountComponent();
        }
    }
    componentWillUnmount() {
        this.unlisteners.forEach(callIfFunction_1.callIfFunction);
    }
    onProjectCreation() {
        // If a new project was created, we need to re-fetch the
        // org details endpoint, which will propagate re-rendering
        // for the entire component tree
        (0, organization_1.fetchOrganizationDetails)(this.props.api, OrganizationContextContainer.getOrganizationSlug(this.props), true, false);
    }
    isLoading() {
        // In the absence of an organization slug, the loading state should be
        // derived from this.props.organizationsLoading from OrganizationsStore
        if (!OrganizationContextContainer.getOrganizationSlug(this.props)) {
            return this.props.organizationsLoading;
        }
        return this.state.loading;
    }
    fetchData(isInitialFetch = false) {
        if (!OrganizationContextContainer.getOrganizationSlug(this.props)) {
            return;
        }
        // fetch from the store, then fetch from the API if necessary
        if (OrganizationContextContainer.isOrgStorePopulatedCorrectly(this.props)) {
            return;
        }
        analytics_1.metric.mark({ name: 'organization-details-fetch-start' });
        (0, organization_1.fetchOrganizationDetails)(this.props.api, OrganizationContextContainer.getOrganizationSlug(this.props), !OrganizationContextContainer.isOrgChanging(this.props), // if true, will preserve a lightweight org that was fetched,
        isInitialFetch);
    }
    loadOrganization(orgData) {
        const { organization, error } = orgData;
        const hooks = [];
        if (organization && !error) {
            hookStore_1.default.get('organization:header').forEach(cb => {
                hooks.push(cb(organization));
            });
            // Configure scope to have organization tag
            Sentry.configureScope(scope => {
                // XXX(dcramer): this is duplicated in sdk.py on the backend
                scope.setTag('organization', organization.id);
                scope.setTag('organization.slug', organization.slug);
                scope.setContext('organization', { id: organization.id, slug: organization.slug });
            });
        }
        else if (error) {
            // If user is superuser, open sudo window
            const user = configStore_1.default.get('user');
            if (!user || !user.isSuperuser || error.status !== 403) {
                // This `catch` can swallow up errors in development (and tests)
                // So let's log them. This may create some noise, especially the test case where
                // we specifically test this branch
                console.error(error); // eslint-disable-line no-console
            }
            else {
                (0, modal_1.openSudo)({
                    retryRequest: () => Promise.resolve(this.fetchData()),
                });
            }
        }
        this.setState(Object.assign(Object.assign({}, orgData), { hooks }), () => {
            // Take a measurement for when organization details are done loading and the new state is applied
            if (organization) {
                analytics_1.metric.measure({
                    name: 'app.component.perf',
                    start: 'organization-details-fetch-start',
                    data: {
                        name: 'org-details',
                        route: (0, getRouteStringFromRoutes_1.default)(this.props.routes),
                        organization_id: parseInt(organization.id, 10),
                    },
                });
            }
        });
    }
    getOrganizationDetailsEndpoint() {
        return `/organizations/${OrganizationContextContainer.getOrganizationSlug(this.props)}/`;
    }
    getTitle() {
        if (this.state.organization) {
            return this.state.organization.name;
        }
        return 'Sentry';
    }
    renderSidebar() {
        if (!this.props.includeSidebar) {
            return null;
        }
        const _a = this.props, { children: _ } = _a, props = (0, tslib_1.__rest)(_a, ["children"]);
        return <sidebar_1.default {...props} organization={this.state.organization}/>;
    }
    renderError() {
        let errorComponent;
        switch (this.state.errorType) {
            case constants_1.ORGANIZATION_FETCH_ERROR_TYPES.ORG_NO_ACCESS:
                // We can still render when an org can't be loaded due to 401. The
                // backend will handle redirects when this is a problem.
                return this.renderBody();
            case constants_1.ORGANIZATION_FETCH_ERROR_TYPES.ORG_NOT_FOUND:
                errorComponent = (<alert_1.default type="error">
            {(0, locale_1.t)('The organization you were looking for was not found.')}
          </alert_1.default>);
                break;
            default:
                errorComponent = <loadingError_1.default onRetry={this.remountComponent}/>;
        }
        return <ErrorWrapper>{errorComponent}</ErrorWrapper>;
    }
    renderBody() {
        return (<react_document_title_1.default title={this.getTitle()}>
        <OrganizationContext.Provider value={this.state.organization}>
          <div className="app">
            {this.state.hooks}
            {this.renderSidebar()}
            {this.props.children}
          </div>
        </OrganizationContext.Provider>
      </react_document_title_1.default>);
    }
    render() {
        if (this.isLoading()) {
            return (<loadingIndicator_1.default triangle>
          {(0, locale_1.t)('Loading data for your organization.')}
        </loadingIndicator_1.default>);
        }
        if (this.state.error) {
            return (<React.Fragment>
          {this.renderSidebar()}
          {this.renderError()}
        </React.Fragment>);
        }
        return this.renderBody();
    }
}
exports.OrganizationLegacyContext = OrganizationContextContainer;
OrganizationContextContainer.childContextTypes = {
    organization: sentryTypes_1.default.Organization,
};
exports.default = (0, withApi_1.default)((0, withOrganizations_1.default)(Sentry.withProfiler(OrganizationContextContainer)));
const ErrorWrapper = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(3)};
`;
//# sourceMappingURL=organizationContext.jsx.map