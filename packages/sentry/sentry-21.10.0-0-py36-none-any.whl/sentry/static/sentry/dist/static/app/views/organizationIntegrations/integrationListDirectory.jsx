Object.defineProperty(exports, "__esModule", { value: true });
exports.IntegrationListDirectory = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const debounce_1 = (0, tslib_1.__importDefault)(require("lodash/debounce"));
const flatten_1 = (0, tslib_1.__importDefault)(require("lodash/flatten"));
const groupBy_1 = (0, tslib_1.__importDefault)(require("lodash/groupBy"));
const startCase_1 = (0, tslib_1.__importDefault)(require("lodash/startCase"));
const uniq_1 = (0, tslib_1.__importDefault)(require("lodash/uniq"));
const queryString = (0, tslib_1.__importStar)(require("query-string"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const selectControl_1 = (0, tslib_1.__importDefault)(require("app/components/forms/selectControl"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const panels_1 = require("app/components/panels");
const searchBar_1 = (0, tslib_1.__importDefault)(require("app/components/searchBar"));
const sentryDocumentTitle_1 = (0, tslib_1.__importDefault)(require("app/components/sentryDocumentTitle"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const createFuzzySearch_1 = require("app/utils/createFuzzySearch");
const integrationUtil_1 = require("app/utils/integrationUtil");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const permissionAlert_1 = (0, tslib_1.__importDefault)(require("app/views/settings/organization/permissionAlert"));
const constants_1 = require("./constants");
const integrationRow_1 = (0, tslib_1.__importDefault)(require("./integrationRow"));
const fuseOptions = {
    threshold: 0.3,
    location: 0,
    distance: 100,
    includeScore: true,
    keys: ['slug', 'key', 'name', 'id'],
};
const TEXT_SEARCH_ANALYTICS_DEBOUNCE_IN_MS = 1000;
class IntegrationListDirectory extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        // Some integrations require visiting a different website to add them. When
        // we come back to the tab we want to show our integrations as soon as we can.
        this.shouldReload = true;
        this.reloadOnVisible = true;
        this.shouldReloadOnVisible = true;
        this.getAppInstall = (app) => { var _a; return (_a = this.state.appInstalls) === null || _a === void 0 ? void 0 : _a.find(i => i.app.slug === app.slug); };
        this.getPopularityWeight = (integration) => { var _a; return (_a = constants_1.POPULARITY_WEIGHT[integration.slug]) !== null && _a !== void 0 ? _a : 1; };
        this.sortByName = (a, b) => a.slug.localeCompare(b.slug);
        this.sortByPopularity = (a, b) => {
            const weightA = this.getPopularityWeight(a);
            const weightB = this.getPopularityWeight(b);
            return weightB - weightA;
        };
        this.sortByInstalled = (a, b) => this.getInstallValue(b) - this.getInstallValue(a);
        this.debouncedTrackIntegrationSearch = (0, debounce_1.default)((search, numResults) => {
            (0, integrationUtil_1.trackIntegrationAnalytics)('integrations.directory_item_searched', {
                view: 'integrations_directory',
                search_term: search,
                num_results: numResults,
                organization: this.props.organization,
            });
        }, TEXT_SEARCH_ANALYTICS_DEBOUNCE_IN_MS);
        /**
         * Get filter parameters and guard against `queryString.parse` returning arrays.
         */
        this.getFilterParameters = () => {
            const { category, search } = queryString.parse(this.props.location.search);
            const selectedCategory = Array.isArray(category) ? category[0] : category || '';
            const searchInput = Array.isArray(search) ? search[0] : search || '';
            return { searchInput, selectedCategory };
        };
        /**
         * Update the query string with the current filter parameter values.
         */
        this.updateQueryString = () => {
            const { searchInput, selectedCategory } = this.state;
            const searchString = queryString.stringify(Object.assign(Object.assign({}, queryString.parse(this.props.location.search)), { search: searchInput ? searchInput : undefined, category: selectedCategory ? selectedCategory : undefined }));
            react_router_1.browserHistory.replace({
                pathname: this.props.location.pathname,
                search: searchString ? `?${searchString}` : undefined,
            });
        };
        /**
         * Filter the integrations list by ANDing together the search query and the category select.
         */
        this.updateDisplayedList = () => {
            const { fuzzy, list, searchInput, selectedCategory } = this.state;
            let displayedList = list;
            if (searchInput && fuzzy) {
                const searchResults = fuzzy.search(searchInput);
                displayedList = this.sortIntegrations(searchResults.map(i => i.item));
            }
            if (selectedCategory) {
                displayedList = displayedList.filter(integration => (0, integrationUtil_1.getCategoriesForIntegration)(integration).includes(selectedCategory));
            }
            this.setState({ displayedList });
            return displayedList;
        };
        this.handleSearchChange = (value) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            this.setState({ searchInput: value }, () => {
                this.updateQueryString();
                const result = this.updateDisplayedList();
                if (value) {
                    this.debouncedTrackIntegrationSearch(value, result.length);
                }
            });
        });
        this.onCategorySelect = ({ value: category }) => {
            this.setState({ selectedCategory: category }, () => {
                this.updateQueryString();
                this.updateDisplayedList();
                if (category) {
                    (0, integrationUtil_1.trackIntegrationAnalytics)('integrations.directory_category_selected', {
                        view: 'integrations_directory',
                        category,
                        organization: this.props.organization,
                    });
                }
            });
        };
        // Rendering
        this.renderProvider = (provider) => {
            var _a, _b;
            const { organization } = this.props;
            // find the integration installations for that provider
            const integrations = (_b = (_a = this.state.integrations) === null || _a === void 0 ? void 0 : _a.filter(i => i.provider.key === provider.key)) !== null && _b !== void 0 ? _b : [];
            return (<integrationRow_1.default key={`row-${provider.key}`} data-test-id="integration-row" organization={organization} type="firstParty" slug={provider.slug} displayName={provider.name} status={integrations.length ? 'Installed' : 'Not Installed'} publishStatus="published" configurations={integrations.length} categories={(0, integrationUtil_1.getCategoriesForIntegration)(provider)} alertText={(0, integrationUtil_1.getAlertText)(integrations)} resolveText={(0, locale_1.t)('Update Now')}/>);
        };
        this.renderPlugin = (plugin) => {
            const { organization } = this.props;
            const isLegacy = plugin.isHidden;
            const displayName = `${plugin.name} ${isLegacy ? '(Legacy)' : ''}`;
            // hide legacy integrations if we don't have any projects with them
            if (isLegacy && !plugin.projectList.length) {
                return null;
            }
            return (<integrationRow_1.default key={`row-plugin-${plugin.id}`} data-test-id="integration-row" organization={organization} type="plugin" slug={plugin.slug} displayName={displayName} status={plugin.projectList.length ? 'Installed' : 'Not Installed'} publishStatus="published" configurations={plugin.projectList.length} categories={(0, integrationUtil_1.getCategoriesForIntegration)(plugin)} plugin={plugin}/>);
        };
        // render either an internal or non-internal app
        this.renderSentryApp = (app) => {
            const { organization } = this.props;
            const status = (0, integrationUtil_1.getSentryAppInstallStatus)(this.getAppInstall(app));
            const categories = (0, integrationUtil_1.getCategoriesForIntegration)(app);
            return (<integrationRow_1.default key={`sentry-app-row-${app.slug}`} data-test-id="integration-row" organization={organization} type="sentryApp" slug={app.slug} displayName={app.name} status={status} publishStatus={app.status} configurations={0} categories={categories}/>);
        };
        this.renderDocumentIntegration = (integration) => {
            const { organization } = this.props;
            return (<integrationRow_1.default key={`doc-int-${integration.slug}`} organization={organization} type="documentIntegration" slug={integration.slug} displayName={integration.name} publishStatus="published" configurations={0} categories={(0, integrationUtil_1.getCategoriesForIntegration)(integration)}/>);
        };
        this.renderIntegration = (integration) => {
            if ((0, integrationUtil_1.isSentryApp)(integration)) {
                return this.renderSentryApp(integration);
            }
            if ((0, integrationUtil_1.isPlugin)(integration)) {
                return this.renderPlugin(integration);
            }
            if ((0, integrationUtil_1.isDocumentIntegration)(integration)) {
                return this.renderDocumentIntegration(integration);
            }
            return this.renderProvider(integration);
        };
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { list: [], displayedList: [], selectedCategory: '' });
    }
    onLoadAllEndpointsSuccess() {
        const { publishedApps, orgOwnedApps, extraApp, plugins } = this.state;
        const published = publishedApps || [];
        // If we have an extra app in state from query parameter, add it as org owned app
        if (orgOwnedApps !== null && extraApp) {
            orgOwnedApps.push(extraApp);
        }
        // we don't want the app to render twice if its the org that created
        // the published app.
        const orgOwned = orgOwnedApps === null || orgOwnedApps === void 0 ? void 0 : orgOwnedApps.filter(app => !published.find(p => p.slug === app.slug));
        /**
         * We should have three sections:
         * 1. Public apps and integrations available to everyone
         * 2. Unpublished apps available to that org
         * 3. Internal apps available to that org
         */
        const combined = []
            .concat(published)
            .concat(orgOwned !== null && orgOwned !== void 0 ? orgOwned : [])
            .concat(this.providers)
            .concat(plugins !== null && plugins !== void 0 ? plugins : [])
            .concat(Object.values(constants_1.documentIntegrations));
        const list = this.sortIntegrations(combined);
        const { searchInput, selectedCategory } = this.getFilterParameters();
        this.setState({ list, searchInput, selectedCategory }, () => {
            this.updateDisplayedList();
            this.trackPageViewed();
        });
    }
    trackPageViewed() {
        // count the number of installed apps
        const { integrations, publishedApps, plugins } = this.state;
        const integrationsInstalled = new Set();
        // add installed integrations
        integrations === null || integrations === void 0 ? void 0 : integrations.forEach((integration) => {
            integrationsInstalled.add(integration.provider.key);
        });
        // add sentry apps
        publishedApps === null || publishedApps === void 0 ? void 0 : publishedApps.filter(this.getAppInstall).forEach((sentryApp) => {
            integrationsInstalled.add(sentryApp.slug);
        });
        // add plugins
        plugins === null || plugins === void 0 ? void 0 : plugins.forEach((plugin) => {
            if (plugin.projectList.length) {
                integrationsInstalled.add(plugin.slug);
            }
        });
        (0, integrationUtil_1.trackIntegrationAnalytics)('integrations.index_viewed', {
            integrations_installed: integrationsInstalled.size,
            view: 'integrations_directory',
            organization: this.props.organization,
        }, { startSession: true });
    }
    getEndpoints() {
        const { orgId } = this.props.params;
        const baseEndpoints = [
            ['config', `/organizations/${orgId}/config/integrations/`],
            [
                'integrations',
                `/organizations/${orgId}/integrations/`,
                { query: { includeConfig: 0 } },
            ],
            ['orgOwnedApps', `/organizations/${orgId}/sentry-apps/`],
            ['publishedApps', '/sentry-apps/', { query: { status: 'published' } }],
            ['appInstalls', `/organizations/${orgId}/sentry-app-installations/`],
            ['plugins', `/organizations/${orgId}/plugins/configs/`],
        ];
        /**
         * optional app to load for super users
         * should only be done for unpublished integrations from another org
         * but no checks are in place to ensure the above condition
         */
        const extraAppSlug = new URLSearchParams(this.props.location.search).get('extra_app');
        if (extraAppSlug) {
            baseEndpoints.push(['extraApp', `/sentry-apps/${extraAppSlug}/`]);
        }
        return baseEndpoints;
    }
    // State
    get unmigratableReposByOrg() {
        // Group by [GitHub|BitBucket|VSTS] Org name
        return (0, groupBy_1.default)(this.state.unmigratableRepos, repo => repo.name.split('/')[0]);
    }
    get providers() {
        var _a, _b;
        return (_b = (_a = this.state.config) === null || _a === void 0 ? void 0 : _a.providers) !== null && _b !== void 0 ? _b : [];
    }
    // Returns 0 if uninstalled, 1 if pending, and 2 if installed
    getInstallValue(integration) {
        const { integrations } = this.state;
        if ((0, integrationUtil_1.isPlugin)(integration)) {
            return integration.projectList.length > 0 ? 2 : 0;
        }
        if ((0, integrationUtil_1.isSentryApp)(integration)) {
            const install = this.getAppInstall(integration);
            if (install) {
                return install.status === 'pending' ? 1 : 2;
            }
            return 0;
        }
        if ((0, integrationUtil_1.isDocumentIntegration)(integration)) {
            return 0;
        }
        return (integrations === null || integrations === void 0 ? void 0 : integrations.find(i => i.provider.key === integration.key)) ? 2 : 0;
    }
    sortIntegrations(integrations) {
        return integrations.sort((a, b) => {
            // sort by whether installed first
            const diffWeight = this.sortByInstalled(a, b);
            if (diffWeight !== 0) {
                return diffWeight;
            }
            // then sort by popularity
            const diffPop = this.sortByPopularity(a, b);
            if (diffPop !== 0) {
                return diffPop;
            }
            // then sort by name
            return this.sortByName(a, b);
        });
    }
    componentDidUpdate(_, prevState) {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            if (this.state.list.length !== prevState.list.length) {
                yield this.createSearch();
            }
        });
    }
    createSearch() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { list } = this.state;
            this.setState({
                fuzzy: yield (0, createFuzzySearch_1.createFuzzySearch)(list || [], fuseOptions),
            });
        });
    }
    renderBody() {
        const { orgId } = this.props.params;
        const { displayedList, list, searchInput, selectedCategory } = this.state;
        const title = (0, locale_1.t)('Integrations');
        const categoryList = (0, uniq_1.default)((0, flatten_1.default)(list.map(integrationUtil_1.getCategoriesForIntegration))).sort();
        return (<react_1.Fragment>
        <sentryDocumentTitle_1.default title={title} orgSlug={orgId}/>

        {!this.props.hideHeader && (<settingsPageHeader_1.default title={title} action={<ActionContainer>
                <selectControl_1.default name="select-categories" onChange={this.onCategorySelect} value={selectedCategory} options={[
                        { value: '', label: (0, locale_1.t)('All Categories') },
                        ...categoryList.map(category => ({
                            value: category,
                            label: (0, startCase_1.default)(category),
                        })),
                    ]}/>
                <searchBar_1.default query={searchInput || ''} onChange={this.handleSearchChange} placeholder={(0, locale_1.t)('Filter Integrations...')} width="25em"/>
              </ActionContainer>}/>)}

        <permissionAlert_1.default access={['org:integrations']}/>
        <panels_1.Panel>
          <panels_1.PanelBody>
            {displayedList.length ? (displayedList.map(this.renderIntegration)) : (<EmptyResultsContainer>
                <EmptyResultsBody>
                  {(0, locale_1.tct)('No Integrations found for "[searchTerm]".', {
                    searchTerm: searchInput,
                })}
                </EmptyResultsBody>
                <EmptyResultsBodyBold>
                  {(0, locale_1.t)("Not seeing what you're looking for?")}
                </EmptyResultsBodyBold>
                <EmptyResultsBody>
                  {(0, locale_1.tct)('[link:Build it on the Sentry Integration Platform.]', {
                    link: (<externalLink_1.default href="https://docs.sentry.io/product/integrations/integration-platform/"/>),
                })}
                </EmptyResultsBody>
              </EmptyResultsContainer>)}
          </panels_1.PanelBody>
        </panels_1.Panel>
      </react_1.Fragment>);
    }
}
exports.IntegrationListDirectory = IntegrationListDirectory;
const ActionContainer = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: 240px max-content;
  grid-gap: ${(0, space_1.default)(2)};
`;
const EmptyResultsContainer = (0, styled_1.default)('div') `
  height: 200px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
`;
const EmptyResultsBody = (0, styled_1.default)('div') `
  font-size: 16px;
  line-height: 28px;
  color: ${p => p.theme.gray300};
  padding-bottom: ${(0, space_1.default)(2)};
`;
const EmptyResultsBodyBold = (0, styled_1.default)(EmptyResultsBody) `
  font-weight: bold;
`;
exports.default = (0, withOrganization_1.default)(IntegrationListDirectory);
//# sourceMappingURL=integrationListDirectory.jsx.map