Object.defineProperty(exports, "__esModule", { value: true });
const locale_1 = require("app/locale");
const pathPrefix = '/settings/:orgId/projects/:projectId';
// Object with the pluginId as the key, and enablingFeature as the value
const SHADOW_DEPRECATED_PLUGINS = {
    teamwork: 'integrations-ignore-teamwork-deprecation',
    clubhouse: 'integrations-ignore-clubhouse-deprecation',
    vsts: 'integrations-ignore-vsts-deprecation',
};
const canViewPlugin = (pluginId, organization) => {
    var _a;
    const isDeprecated = SHADOW_DEPRECATED_PLUGINS.hasOwnProperty(pluginId);
    const hasFeature = (_a = organization === null || organization === void 0 ? void 0 : organization.features) === null || _a === void 0 ? void 0 : _a.includes(SHADOW_DEPRECATED_PLUGINS[pluginId]);
    return isDeprecated ? hasFeature : true;
};
function getConfiguration({ project, organization, debugFilesNeedsReview, }) {
    const plugins = ((project && project.plugins) || []).filter(plugin => plugin.enabled);
    return [
        {
            name: (0, locale_1.t)('Project'),
            items: [
                {
                    path: `${pathPrefix}/`,
                    index: true,
                    title: (0, locale_1.t)('General Settings'),
                    description: (0, locale_1.t)('Configure general settings for a project'),
                },
                {
                    path: `${pathPrefix}/teams/`,
                    title: (0, locale_1.t)('Project Teams'),
                    description: (0, locale_1.t)('Manage team access for a project'),
                },
                {
                    path: `${pathPrefix}/alerts/`,
                    title: (0, locale_1.t)('Alerts'),
                    description: (0, locale_1.t)('Manage alert rules for a project'),
                },
                {
                    path: `${pathPrefix}/tags/`,
                    title: (0, locale_1.t)('Tags'),
                    description: (0, locale_1.t)("View and manage a  project's tags"),
                },
                {
                    path: `${pathPrefix}/environments/`,
                    title: (0, locale_1.t)('Environments'),
                    description: (0, locale_1.t)('Manage environments in a project'),
                },
                {
                    path: `${pathPrefix}/ownership/`,
                    title: (0, locale_1.t)('Issue Owners'),
                    description: (0, locale_1.t)('Manage issue ownership rules for a project'),
                    badge: () => 'new',
                },
                {
                    path: `${pathPrefix}/data-forwarding/`,
                    title: (0, locale_1.t)('Data Forwarding'),
                },
            ],
        },
        {
            name: (0, locale_1.t)('Processing'),
            items: [
                {
                    path: `${pathPrefix}/filters/`,
                    title: (0, locale_1.t)('Inbound Filters'),
                    description: (0, locale_1.t)("Configure a project's inbound filters (e.g. browsers, messages)"),
                },
                {
                    path: `${pathPrefix}/filters-and-sampling/`,
                    title: (0, locale_1.t)('Filters & Sampling'),
                    show: () => { var _a; return !!((_a = organization === null || organization === void 0 ? void 0 : organization.features) === null || _a === void 0 ? void 0 : _a.includes('filters-and-sampling')); },
                    description: (0, locale_1.t)("Manage an organization's inbound data"),
                    badge: () => 'new',
                },
                {
                    path: `${pathPrefix}/security-and-privacy/`,
                    title: (0, locale_1.t)('Security & Privacy'),
                    description: (0, locale_1.t)('Configuration related to dealing with sensitive data and other security settings. (Data Scrubbing, Data Privacy, Data Scrubbing) for a project'),
                },
                {
                    path: `${pathPrefix}/issue-grouping/`,
                    title: (0, locale_1.t)('Issue Grouping'),
                },
                {
                    path: `${pathPrefix}/processing-issues/`,
                    title: (0, locale_1.t)('Processing Issues'),
                    // eslint-disable-next-line @typescript-eslint/no-shadow
                    badge: ({ project }) => {
                        if (!project) {
                            return null;
                        }
                        if (project.processingIssues <= 0) {
                            return null;
                        }
                        return project.processingIssues > 99 ? '99+' : project.processingIssues;
                    },
                },
                {
                    path: `${pathPrefix}/debug-symbols/`,
                    title: (0, locale_1.t)('Debug Files'),
                    badge: debugFilesNeedsReview ? () => 'warning' : undefined,
                },
                {
                    path: `${pathPrefix}/proguard/`,
                    title: (0, locale_1.t)('ProGuard'),
                },
                {
                    path: `${pathPrefix}/source-maps/`,
                    title: (0, locale_1.t)('Source Maps'),
                },
                {
                    path: `${pathPrefix}/performance/`,
                    title: (0, locale_1.t)('Performance'),
                    show: () => { var _a; return !!((_a = organization === null || organization === void 0 ? void 0 : organization.features) === null || _a === void 0 ? void 0 : _a.includes('performance-view')); },
                },
            ],
        },
        {
            name: (0, locale_1.t)('SDK Setup'),
            items: [
                {
                    path: `${pathPrefix}/install/`,
                    title: (0, locale_1.t)('Instrumentation'),
                },
                {
                    path: `${pathPrefix}/keys/`,
                    title: (0, locale_1.t)('Client Keys (DSN)'),
                    description: (0, locale_1.t)("View and manage the project's client keys (DSN)"),
                },
                {
                    path: `${pathPrefix}/release-tracking/`,
                    title: (0, locale_1.t)('Releases'),
                },
                {
                    path: `${pathPrefix}/security-headers/`,
                    title: (0, locale_1.t)('Security Headers'),
                },
                {
                    path: `${pathPrefix}/user-feedback/`,
                    title: (0, locale_1.t)('User Feedback'),
                    description: (0, locale_1.t)('Configure user feedback reporting feature'),
                },
            ],
        },
        {
            name: (0, locale_1.t)('Legacy Integrations'),
            items: [
                {
                    path: `${pathPrefix}/plugins/`,
                    title: (0, locale_1.t)('Legacy Integrations'),
                    description: (0, locale_1.t)('View, enable, and disable all integrations for a project'),
                    id: 'legacy_integrations',
                    recordAnalytics: true,
                },
                ...plugins.map(plugin => ({
                    path: `${pathPrefix}/plugins/${plugin.id}/`,
                    title: plugin.name,
                    show: opts => { var _a; return ((_a = opts === null || opts === void 0 ? void 0 : opts.access) === null || _a === void 0 ? void 0 : _a.has('project:write')) && canViewPlugin(plugin.id, organization); },
                    id: 'plugin_details',
                    recordAnalytics: true,
                })),
            ],
        },
    ];
}
exports.default = getConfiguration;
//# sourceMappingURL=navigationConfiguration.jsx.map