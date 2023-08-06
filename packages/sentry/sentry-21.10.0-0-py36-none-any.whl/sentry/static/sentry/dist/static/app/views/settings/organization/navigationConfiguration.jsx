Object.defineProperty(exports, "__esModule", { value: true });
const locale_1 = require("app/locale");
const pathPrefix = '/settings/:orgId';
const organizationNavigation = [
    {
        name: (0, locale_1.t)('Organization'),
        items: [
            {
                path: `${pathPrefix}/`,
                title: (0, locale_1.t)('General Settings'),
                index: true,
                description: (0, locale_1.t)('Configure general settings for an organization'),
                id: 'general',
            },
            {
                path: `${pathPrefix}/projects/`,
                title: (0, locale_1.t)('Projects'),
                description: (0, locale_1.t)("View and manage an organization's projects"),
                id: 'projects',
            },
            {
                path: `${pathPrefix}/teams/`,
                title: (0, locale_1.t)('Teams'),
                description: (0, locale_1.t)("Manage an organization's teams"),
                id: 'teams',
            },
            {
                path: `${pathPrefix}/members/`,
                title: (0, locale_1.t)('Members'),
                show: ({ access }) => access.has('member:read'),
                description: (0, locale_1.t)('Manage user membership for an organization'),
                id: 'members',
            },
            {
                path: `${pathPrefix}/performance/`,
                title: (0, locale_1.t)('Performance'),
                show: ({ features }) => features.has('performance-view'),
                description: (0, locale_1.t)('Manage performance settings'),
                id: 'performance',
            },
            {
                path: `${pathPrefix}/security-and-privacy/`,
                title: (0, locale_1.t)('Security & Privacy'),
                description: (0, locale_1.t)('Configuration related to dealing with sensitive data and other security settings. (Data Scrubbing, Data Privacy, Data Scrubbing)'),
                id: 'security-and-privacy',
            },
            {
                path: `${pathPrefix}/auth/`,
                title: (0, locale_1.t)('Auth'),
                description: (0, locale_1.t)('Configure single sign-on'),
                id: 'sso',
            },
            {
                path: `${pathPrefix}/api-keys/`,
                title: (0, locale_1.t)('API Keys'),
                show: ({ access, features }) => features.has('api-keys') && access.has('org:admin'),
                id: 'api-keys',
            },
            {
                path: `${pathPrefix}/audit-log/`,
                title: (0, locale_1.t)('Audit Log'),
                show: ({ access }) => access.has('org:write'),
                description: (0, locale_1.t)('View the audit log for an organization'),
                id: 'audit-log',
            },
            {
                path: `${pathPrefix}/rate-limits/`,
                title: (0, locale_1.t)('Rate Limits'),
                show: ({ access, features }) => features.has('legacy-rate-limits') && access.has('org:write'),
                description: (0, locale_1.t)('Configure rate limits for all projects in the organization'),
                id: 'rate-limits',
            },
            {
                path: `${pathPrefix}/relay/`,
                title: (0, locale_1.t)('Relay'),
                description: (0, locale_1.t)('Manage relays connected to the organization'),
                id: 'relay',
            },
            {
                path: `${pathPrefix}/repos/`,
                title: (0, locale_1.t)('Repositories'),
                description: (0, locale_1.t)('Manage repositories connected to the organization'),
                id: 'repos',
            },
            {
                path: `${pathPrefix}/integrations/`,
                title: (0, locale_1.t)('Integrations'),
                description: (0, locale_1.t)('Manage organization-level integrations, including: Slack, Github, Bitbucket, Jira, and Azure DevOps'),
                id: 'integrations',
                recordAnalytics: true,
            },
            {
                path: `${pathPrefix}/developer-settings/`,
                title: (0, locale_1.t)('Developer Settings'),
                description: (0, locale_1.t)('Manage developer applications'),
                id: 'developer-settings',
            },
        ],
    },
];
exports.default = organizationNavigation;
//# sourceMappingURL=navigationConfiguration.jsx.map