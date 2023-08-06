/* global process */
/**
 * Common constants here
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.DEFAULT_ERROR_JSON = exports.SENTRY_RELEASE_VERSION = exports.SPA_DSN = exports.DISABLE_RR_WEB = exports.NODE_ENV = exports.IS_ACCEPTANCE_TEST = exports.DISCOVER2_DOCS_URL = exports.CONFIG_DOCS_URL = exports.ORGANIZATION_FETCH_ERROR_TYPES = exports.FILTER_MASK = exports.EXPERIMENTAL_SPA = exports.DEPLOY_PREVIEW_CONFIG = exports.MAX_QUERY_LENGTH = exports.DEFAULT_PER_PAGE = exports.MAX_AUTOCOMPLETE_RELEASES = exports.MAX_AUTOCOMPLETE_RECENT_SEARCHES = exports.SEARCH_WILDCARD = exports.NEGATION_OPERATOR = exports.DEFAULT_RELATIVE_PERIODS = exports.DEFAULT_USE_UTC = exports.DEFAULT_QUERY = exports.DEFAULT_STATS_PERIOD = exports.MAX_PICKABLE_DAYS = exports.MENU_CLOSE_DELAY = exports.AVATAR_URL_MAP = exports.DEFAULT_FUSE_OPTIONS = exports.ALL_ENVIRONMENTS_KEY = exports.DEFAULT_DEBOUNCE_DURATION = exports.DEFAULT_TOAST_DURATION = exports.SENTRY_APP_PERMISSIONS = exports.RELEASE_ADOPTION_STAGES = exports.MEMBER_ROLES = exports.DEFAULT_API_ACCESS_SCOPES = exports.API_ACCESS_SCOPES = exports.DEFAULT_APP_ROUTE = exports.ROOT_ELEMENT = void 0;
const locale_1 = require("app/locale");
// This is the element id where we render our React application to
exports.ROOT_ELEMENT = 'blk_router';
// This is considered the "default" route/view that users should be taken
// to when the application does not have any further context
//
// e.g. loading app root or switching organization
exports.DEFAULT_APP_ROUTE = '/organizations/:orgSlug/issues/';
exports.API_ACCESS_SCOPES = [
    'project:read',
    'project:write',
    'project:admin',
    'project:releases',
    'team:read',
    'team:write',
    'team:admin',
    'event:read',
    'event:write',
    'event:admin',
    'org:read',
    'org:write',
    'org:admin',
    'org:integrations',
    'member:read',
    'member:write',
    'member:admin',
    'alerts:read',
    'alerts:write',
];
// Default API scopes when adding a new API token or org API token
exports.DEFAULT_API_ACCESS_SCOPES = [
    'event:read',
    'event:admin',
    'project:read',
    'project:releases',
    'org:read',
    'team:read',
    'member:read',
];
// These should only be used in the case where we cannot obtain roles through
// the members endpoint (primarily in cases where a user is admining a
// different organization they are not a OrganizationMember of ).
exports.MEMBER_ROLES = [
    {
        id: 'member',
        name: 'Member',
        allowed: true,
        desc: 'Members can view and act on events, as well as view most other data within the organization.',
    },
    {
        id: 'admin',
        name: 'Admin',
        allowed: true,
        desc: "Admin privileges on any teams of which they're a member. They can create new teams and projects, as well as remove teams and projects on which they already hold membership (or all teams, if open membership is enabled). Additionally, they can manage memberships of teams that they are members of. They cannot invite members to the organization.",
    },
    {
        id: 'manager',
        name: 'Manager',
        allowed: true,
        desc: 'Gains admin access on all teams as well as the ability to add and remove members.',
    },
    {
        id: 'owner',
        name: 'Organization Owner',
        allowed: true,
        desc: 'Unrestricted access to the organization, its data, and its settings. Can add, modify, and delete projects and members, as well as make billing and plan changes.',
    },
];
exports.RELEASE_ADOPTION_STAGES = ['low_adoption', 'adopted', 'replaced'];
// We expose permissions for Sentry Apps in a more resource-centric way.
// All of the API_ACCESS_SCOPES from above should be represented in a more
// User-friendly way here.
exports.SENTRY_APP_PERMISSIONS = [
    {
        resource: 'Project',
        help: 'Projects, Tags, Debug Files, and Feedback',
        choices: {
            'no-access': { label: 'No Access', scopes: [] },
            read: { label: 'Read', scopes: ['project:read'] },
            write: { label: 'Read & Write', scopes: ['project:read', 'project:write'] },
            admin: { label: 'Admin', scopes: ['project:read', 'project:write', 'project:admin'] },
        },
    },
    {
        resource: 'Team',
        help: 'Teams of members',
        choices: {
            'no-access': { label: 'No Access', scopes: [] },
            read: { label: 'Read', scopes: ['team:read'] },
            write: { label: 'Read & Write', scopes: ['team:read', 'team:write'] },
            admin: { label: 'Admin', scopes: ['team:read', 'team:write', 'team:admin'] },
        },
    },
    {
        resource: 'Release',
        help: 'Releases, Commits, and related Files',
        choices: {
            'no-access': { label: 'No Access', scopes: [] },
            admin: { label: 'Admin', scopes: ['project:releases'] },
        },
    },
    {
        resource: 'Event',
        label: 'Issue & Event',
        help: 'Issues, Events, and workflow statuses',
        choices: {
            'no-access': { label: 'No Access', scopes: [] },
            read: { label: 'Read', scopes: ['event:read'] },
            write: { label: 'Read & Write', scopes: ['event:read', 'event:write'] },
            admin: { label: 'Admin', scopes: ['event:read', 'event:write', 'event:admin'] },
        },
    },
    {
        resource: 'Organization',
        help: 'Manage Organizations, resolve IDs, retrieve Repositories and Commits',
        choices: {
            'no-access': { label: 'No Access', scopes: [] },
            read: { label: 'Read', scopes: ['org:read'] },
            write: { label: 'Read & Write', scopes: ['org:read', 'org:write'] },
            admin: { label: 'Admin', scopes: ['org:read', 'org:write', 'org:admin'] },
        },
    },
    {
        resource: 'Member',
        help: 'Manage Members within Teams',
        choices: {
            'no-access': { label: 'No Access', scopes: [] },
            read: { label: 'Read', scopes: ['member:read'] },
            write: { label: 'Read & Write', scopes: ['member:read', 'member:write'] },
            admin: { label: 'Admin', scopes: ['member:read', 'member:write', 'member:admin'] },
        },
    },
];
exports.DEFAULT_TOAST_DURATION = 6000;
exports.DEFAULT_DEBOUNCE_DURATION = 300;
exports.ALL_ENVIRONMENTS_KEY = '__all_environments__';
// See http://fusejs.io/ for more information
exports.DEFAULT_FUSE_OPTIONS = {
    includeScore: true,
    includeMatches: true,
    threshold: 0.4,
    location: 0,
    distance: 75,
    maxPatternLength: 24,
    minMatchCharLength: 2,
    // tokenize: true,
    // findAllMatches: true,
};
// Maps a `type: string` -> `url-prefix: string`
exports.AVATAR_URL_MAP = {
    team: 'team-avatar',
    organization: 'organization-avatar',
    project: 'project-avatar',
    user: 'avatar',
};
exports.MENU_CLOSE_DELAY = 200;
exports.MAX_PICKABLE_DAYS = 90;
exports.DEFAULT_STATS_PERIOD = '14d';
exports.DEFAULT_QUERY = 'is:unresolved';
exports.DEFAULT_USE_UTC = true;
exports.DEFAULT_RELATIVE_PERIODS = {
    '1h': (0, locale_1.t)('Last hour'),
    '24h': (0, locale_1.t)('Last 24 hours'),
    '7d': (0, locale_1.t)('Last 7 days'),
    '14d': (0, locale_1.t)('Last 14 days'),
    '30d': (0, locale_1.t)('Last 30 days'),
    '90d': (0, locale_1.t)('Last 90 days'),
};
// Special Search characters
exports.NEGATION_OPERATOR = '!';
exports.SEARCH_WILDCARD = '*';
// SmartSearchBar settings
exports.MAX_AUTOCOMPLETE_RECENT_SEARCHES = 3;
exports.MAX_AUTOCOMPLETE_RELEASES = 5;
exports.DEFAULT_PER_PAGE = 50;
// Limit query length so paginated response headers don't
// go over HTTP header size limits (4Kb)
exports.MAX_QUERY_LENGTH = 400;
// Webpack configures DEPLOY_PREVIEW_CONFIG for deploy preview builds.
exports.DEPLOY_PREVIEW_CONFIG = process.env.DEPLOY_PREVIEW_CONFIG;
// Webpack configures EXPERIMENTAL_SPA.
exports.EXPERIMENTAL_SPA = process.env.EXPERIMENTAL_SPA;
// so we don't use filtered values in certain display contexts
// TODO(kmclb): once relay is doing the scrubbing, the masking value will be dynamic,
// so this will have to change
exports.FILTER_MASK = '[Filtered]';
// Errors that may occur during the fetching of organization details
exports.ORGANIZATION_FETCH_ERROR_TYPES = {
    ORG_NOT_FOUND: 'ORG_NOT_FOUND',
    ORG_NO_ACCESS: 'ORG_NO_ACCESS',
};
exports.CONFIG_DOCS_URL = 'https://develop.sentry.dev/config/';
exports.DISCOVER2_DOCS_URL = 'https://docs.sentry.io/product/discover-queries/';
exports.IS_ACCEPTANCE_TEST = !!process.env.IS_ACCEPTANCE_TEST;
exports.NODE_ENV = process.env.NODE_ENV;
exports.DISABLE_RR_WEB = !!process.env.DISABLE_RR_WEB;
exports.SPA_DSN = process.env.SPA_DSN;
exports.SENTRY_RELEASE_VERSION = process.env.SENTRY_RELEASE_VERSION;
exports.DEFAULT_ERROR_JSON = {
    detail: (0, locale_1.t)('Unknown error. Please try again.'),
};
//# sourceMappingURL=index.jsx.map