Object.defineProperty(exports, "__esModule", { value: true });
exports.ApiSource = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const debounce_1 = (0, tslib_1.__importDefault)(require("lodash/debounce"));
const flatten_1 = (0, tslib_1.__importDefault)(require("lodash/flatten"));
const api_1 = require("app/api");
const locale_1 = require("app/locale");
const utils_1 = require("app/utils");
const createFuzzySearch_1 = require("app/utils/createFuzzySearch");
const marked_1 = require("app/utils/marked");
const withLatestContext_1 = (0, tslib_1.__importDefault)(require("app/utils/withLatestContext"));
const constants_1 = require("app/views/organizationIntegrations/constants");
// event ids must have string length of 32
const shouldSearchEventIds = (query) => typeof query === 'string' && query.length === 32;
// STRING-HEXVAL
const shouldSearchShortIds = (query) => /[\w\d]+-[\w\d]+/.test(query);
// Helper functions to create result objects
function createOrganizationResults(organizationsPromise) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const organizations = (yield organizationsPromise) || [];
        return (0, flatten_1.default)(organizations.map(org => [
            {
                title: (0, locale_1.t)('%s Dashboard', org.slug),
                description: (0, locale_1.t)('Organization Dashboard'),
                model: org,
                sourceType: 'organization',
                resultType: 'route',
                to: `/${org.slug}/`,
            },
            {
                title: (0, locale_1.t)('%s Settings', org.slug),
                description: (0, locale_1.t)('Organization Settings'),
                model: org,
                sourceType: 'organization',
                resultType: 'settings',
                to: `/settings/${org.slug}/`,
            },
        ]));
    });
}
function createProjectResults(projectsPromise, orgId) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const projects = (yield projectsPromise) || [];
        return (0, flatten_1.default)(projects.map(project => {
            const projectResults = [
                {
                    title: (0, locale_1.t)('%s Settings', project.slug),
                    description: (0, locale_1.t)('Project Settings'),
                    model: project,
                    sourceType: 'project',
                    resultType: 'settings',
                    to: `/settings/${orgId}/projects/${project.slug}/`,
                },
            ];
            projectResults.unshift({
                title: (0, locale_1.t)('%s Dashboard', project.slug),
                description: (0, locale_1.t)('Project Details'),
                model: project,
                sourceType: 'project',
                resultType: 'route',
                to: `/organizations/${orgId}/projects/${project.slug}/?project=${project.id}`,
            });
            return projectResults;
        }));
    });
}
function createTeamResults(teamsPromise, orgId) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const teams = (yield teamsPromise) || [];
        return teams.map(team => ({
            title: `#${team.slug}`,
            description: 'Team Settings',
            model: team,
            sourceType: 'team',
            resultType: 'settings',
            to: `/settings/${orgId}/teams/${team.slug}/`,
        }));
    });
}
function createMemberResults(membersPromise, orgId) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const members = (yield membersPromise) || [];
        return members.map(member => ({
            title: member.name,
            description: member.email,
            model: member,
            sourceType: 'member',
            resultType: 'settings',
            to: `/settings/${orgId}/members/${member.id}/`,
        }));
    });
}
function createPluginResults(pluginsPromise, orgId) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const plugins = (yield pluginsPromise) || [];
        return plugins
            .filter(plugin => {
            // show a plugin if it is not hidden (aka legacy) or if we have projects with it configured
            return !plugin.isHidden || !!plugin.projectList.length;
        })
            .map(plugin => {
            var _a;
            return ({
                title: plugin.isHidden ? `${plugin.name} (Legacy)` : plugin.name,
                description: (<span dangerouslySetInnerHTML={{
                        __html: (0, marked_1.singleLineRenderer)((_a = plugin.description) !== null && _a !== void 0 ? _a : ''),
                    }}/>),
                model: plugin,
                sourceType: 'plugin',
                resultType: 'integration',
                to: `/settings/${orgId}/plugins/${plugin.id}/`,
            });
        });
    });
}
function createIntegrationResults(integrationsPromise, orgId) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const { providers } = (yield integrationsPromise) || {};
        return ((providers &&
            providers.map(provider => ({
                title: provider.name,
                description: (<span dangerouslySetInnerHTML={{
                        __html: (0, marked_1.singleLineRenderer)(provider.metadata.description),
                    }}/>),
                model: provider,
                sourceType: 'integration',
                resultType: 'integration',
                to: `/settings/${orgId}/integrations/${provider.slug}/`,
                configUrl: `/api/0/organizations/${orgId}/integrations/?provider_key=${provider.slug}&includeConfig=0`,
            }))) ||
            []);
    });
}
function createSentryAppResults(sentryAppPromise, orgId) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const sentryApps = (yield sentryAppPromise) || [];
        return sentryApps.map(sentryApp => ({
            title: sentryApp.name,
            description: (<span dangerouslySetInnerHTML={{
                    __html: (0, marked_1.singleLineRenderer)(sentryApp.overview || ''),
                }}/>),
            model: sentryApp,
            sourceType: 'sentryApp',
            resultType: 'integration',
            to: `/settings/${orgId}/sentry-apps/${sentryApp.slug}/`,
        }));
    });
}
// Not really async but we need to return a promise
function creatDocIntegrationResults(orgId) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        return constants_1.documentIntegrationList.map(integration => ({
            title: integration.name,
            description: (<span dangerouslySetInnerHTML={{
                    __html: (0, marked_1.singleLineRenderer)(integration.description),
                }}/>),
            model: integration,
            sourceType: 'docIntegration',
            resultType: 'integration',
            to: `/settings/${orgId}/document-integrations/${integration.slug}/`,
        }));
    });
}
function createShortIdLookupResult(shortIdLookupPromise) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const shortIdLookup = yield shortIdLookupPromise;
        if (!shortIdLookup) {
            return null;
        }
        const issue = shortIdLookup && shortIdLookup.group;
        return {
            item: {
                title: `${(issue && issue.metadata && issue.metadata.type) || shortIdLookup.shortId}`,
                description: `${(issue && issue.metadata && issue.metadata.value) || (0, locale_1.t)('Issue')}`,
                model: shortIdLookup.group,
                sourceType: 'issue',
                resultType: 'issue',
                to: `/${shortIdLookup.organizationSlug}/${shortIdLookup.projectSlug}/issues/${shortIdLookup.groupId}/`,
            },
            score: 1,
        };
    });
}
function createEventIdLookupResult(eventIdLookupPromise) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const eventIdLookup = yield eventIdLookupPromise;
        if (!eventIdLookup) {
            return null;
        }
        const event = eventIdLookup && eventIdLookup.event;
        return {
            item: {
                title: `${(event && event.metadata && event.metadata.type) || (0, locale_1.t)('Event')}`,
                description: `${event && event.metadata && event.metadata.value}`,
                sourceType: 'event',
                resultType: 'event',
                to: `/${eventIdLookup.organizationSlug}/${eventIdLookup.projectSlug}/issues/${eventIdLookup.groupId}/events/${eventIdLookup.eventId}/`,
            },
            score: 1,
        };
    });
}
class ApiSource extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            loading: false,
            searchResults: null,
            directResults: null,
            fuzzy: null,
        };
        this.api = new api_1.Client();
        // Debounced method to handle querying all API endpoints (when necessary)
        this.doSearch = (0, debounce_1.default)((query) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { params, organization } = this.props;
            const orgId = (params && params.orgId) || (organization && organization.slug);
            let searchUrls = ['/organizations/'];
            let directUrls = [];
            // Only run these queries when we have an org in context
            if (orgId) {
                searchUrls = [
                    ...searchUrls,
                    `/organizations/${orgId}/projects/`,
                    `/organizations/${orgId}/teams/`,
                    `/organizations/${orgId}/members/`,
                    `/organizations/${orgId}/plugins/configs/`,
                    `/organizations/${orgId}/config/integrations/`,
                    '/sentry-apps/?status=published',
                ];
                directUrls = [
                    shouldSearchShortIds(query) ? `/organizations/${orgId}/shortids/${query}/` : null,
                    shouldSearchEventIds(query) ? `/organizations/${orgId}/eventids/${query}/` : null,
                ];
            }
            const searchRequests = searchUrls.map(url => this.api
                .requestPromise(url, {
                query: {
                    query,
                },
            })
                .then(resp => resp, err => {
                this.handleRequestError(err, { orgId, url });
                return null;
            }));
            const directRequests = directUrls.map(url => {
                if (!url) {
                    return Promise.resolve(null);
                }
                return this.api.requestPromise(url).then(resp => resp, (err) => {
                    // No need to log 404 errors
                    if (err && err.status === 404) {
                        return null;
                    }
                    this.handleRequestError(err, { orgId, url });
                    return null;
                });
            });
            this.handleSearchRequest(searchRequests, directRequests);
        }), 150);
        this.handleRequestError = (err, { url, orgId }) => {
            Sentry.withScope(scope => {
                var _a;
                scope.setExtra('url', url.replace(`/organizations/${orgId}/`, '/organizations/:orgId/'));
                Sentry.captureException(new Error(`API Source Failed: ${(_a = err === null || err === void 0 ? void 0 : err.responseJSON) === null || _a === void 0 ? void 0 : _a.detail}`));
            });
        };
    }
    componentDidMount() {
        if (typeof this.props.query !== 'undefined') {
            this.doSearch(this.props.query);
        }
    }
    UNSAFE_componentWillReceiveProps(nextProps) {
        // Limit the number of times we perform API queries by only attempting API queries
        // using first two characters, otherwise perform in-memory search.
        //
        // Otherwise it'd be constant :spinning_loading_wheel:
        if ((nextProps.query.length <= 2 &&
            nextProps.query.substr(0, 2) !== this.props.query.substr(0, 2)) ||
            // Also trigger a search if next query value satisfies an eventid/shortid query
            shouldSearchShortIds(nextProps.query) ||
            shouldSearchEventIds(nextProps.query)) {
            this.setState({ loading: true });
            this.doSearch(nextProps.query);
        }
    }
    // Handles a list of search request promises, and then updates state with response objects
    handleSearchRequest(searchRequests, directRequests) {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { searchOptions } = this.props;
            // Note we don't wait for all requests to resolve here (e.g. `await Promise.all(reqs)`)
            // so that we can start processing before all API requests are resolved
            //
            // This isn't particularly helpful in its current form because we still wait for all requests to finish before
            // updating state, but you could potentially optimize rendering direct results before all requests are finished.
            const [organizations, projects, teams, members, plugins, integrations, sentryApps] = searchRequests;
            const [shortIdLookup, eventIdLookup] = directRequests;
            const [searchResults, directResults] = yield Promise.all([
                this.getSearchableResults([
                    organizations,
                    projects,
                    teams,
                    members,
                    plugins,
                    integrations,
                    sentryApps,
                ]),
                this.getDirectResults([shortIdLookup, eventIdLookup]),
            ]);
            // TODO(XXX): Might consider adding logic to maintain consistent ordering of results so things don't switch positions
            const fuzzy = (0, createFuzzySearch_1.createFuzzySearch)(searchResults, Object.assign(Object.assign({}, searchOptions), { keys: ['title', 'description'] }));
            this.setState({
                loading: false,
                fuzzy: yield fuzzy,
                directResults,
            });
        });
    }
    // Process API requests that create result objects that should be searchable
    getSearchableResults(requests) {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { params, organization } = this.props;
            const orgId = (params && params.orgId) || (organization && organization.slug);
            const [organizations, projects, teams, members, plugins, integrations, sentryApps] = requests;
            const searchResults = (0, flatten_1.default)(yield Promise.all([
                createOrganizationResults(organizations),
                createProjectResults(projects, orgId),
                createTeamResults(teams, orgId),
                createMemberResults(members, orgId),
                createIntegrationResults(integrations, orgId),
                createPluginResults(plugins, orgId),
                createSentryAppResults(sentryApps, orgId),
                creatDocIntegrationResults(orgId),
            ]));
            return searchResults;
        });
    }
    // Create result objects from API requests that do not require fuzzy search
    // i.e. these responses only return 1 object or they should always be displayed regardless of query input
    getDirectResults(requests) {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const [shortIdLookup, eventIdLookup] = requests;
            const directResults = (yield Promise.all([
                createShortIdLookupResult(shortIdLookup),
                createEventIdLookupResult(eventIdLookup),
            ])).filter(utils_1.defined);
            if (!directResults.length) {
                return [];
            }
            return directResults;
        });
    }
    render() {
        const { children, query } = this.props;
        const { fuzzy, directResults } = this.state;
        let results = [];
        if (fuzzy) {
            results = fuzzy.search(query);
        }
        return children({
            isLoading: this.state.loading,
            results: (0, flatten_1.default)([results, directResults].filter(utils_1.defined)) || [],
        });
    }
}
exports.ApiSource = ApiSource;
ApiSource.defaultProps = {
    searchOptions: {},
};
exports.default = (0, withLatestContext_1.default)((0, react_router_1.withRouter)(ApiSource));
//# sourceMappingURL=apiSource.jsx.map