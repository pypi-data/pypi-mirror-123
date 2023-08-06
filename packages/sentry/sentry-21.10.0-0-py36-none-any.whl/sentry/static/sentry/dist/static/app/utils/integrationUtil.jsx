Object.defineProperty(exports, "__esModule", { value: true });
exports.getAlertText = exports.isSlackIntegrationUpToDate = exports.platformToIntegrationMap = exports.getIntegrationIcon = exports.safeGetQsParam = exports.convertIntegrationTypeToSnakeCase = exports.getIntegrationType = exports.isDocumentIntegration = exports.isPlugin = exports.isSentryApp = exports.getCategoriesForIntegration = exports.getCategories = exports.getSentryAppInstallStatus = exports.getIntegrationFeatureGate = exports.trackIntegrationAnalytics = void 0;
const tslib_1 = require("tslib");
const capitalize_1 = (0, tslib_1.__importDefault)(require("lodash/capitalize"));
const qs = (0, tslib_1.__importStar)(require("query-string"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const hookStore_1 = (0, tslib_1.__importDefault)(require("app/stores/hookStore"));
const integrationAnalyticsEvents_1 = require("app/utils/analytics/integrationAnalyticsEvents");
const makeAnalyticsFunction_1 = (0, tslib_1.__importDefault)(require("app/utils/analytics/makeAnalyticsFunction"));
const mapIntegrationParams = analyticsParams => {
    // Reload expects integration_status even though it's not relevant for non-sentry apps
    // Passing in a dummy value of published in those cases
    const fullParams = Object.assign({}, analyticsParams);
    if (analyticsParams.integration && analyticsParams.integration_type !== 'sentry_app') {
        fullParams.integration_status = 'published';
    }
    return fullParams;
};
exports.trackIntegrationAnalytics = (0, makeAnalyticsFunction_1.default)(integrationAnalyticsEvents_1.integrationEventMap, {
    mapValuesFn: mapIntegrationParams,
});
/**
 * In sentry.io the features list supports rendering plan details. If the hook
 * is not registered for rendering the features list like this simply show the
 * features as a normal list.
 */
const generateFeaturesList = p => (<ul>
    {p.features.map((f, i) => (<li key={i}>{f.description}</li>))}
  </ul>);
const generateIntegrationFeatures = p => p.children({
    disabled: false,
    disabledReason: null,
    ungatedFeatures: p.features,
    gatedFeatureGroups: [],
});
const defaultFeatureGateComponents = {
    IntegrationFeatures: generateIntegrationFeatures,
    IntegrationDirectoryFeatures: generateIntegrationFeatures,
    FeatureList: generateFeaturesList,
    IntegrationDirectoryFeatureList: generateFeaturesList,
};
const getIntegrationFeatureGate = () => {
    const defaultHook = () => defaultFeatureGateComponents;
    const featureHook = hookStore_1.default.get('integrations:feature-gates')[0] || defaultHook;
    return featureHook();
};
exports.getIntegrationFeatureGate = getIntegrationFeatureGate;
const getSentryAppInstallStatus = (install) => {
    if (install) {
        return (0, capitalize_1.default)(install.status);
    }
    return 'Not Installed';
};
exports.getSentryAppInstallStatus = getSentryAppInstallStatus;
const getCategories = (features) => {
    const transform = features.map(({ featureGate }) => {
        const feature = featureGate
            .replace(/integrations/g, '')
            .replace(/-/g, ' ')
            .trim();
        switch (feature) {
            case 'actionable notification':
                return 'notification action';
            case 'issue basic':
            case 'issue link':
            case 'issue sync':
                return 'project management';
            case 'commits':
                return 'source code management';
            case 'chat unfurl':
                return 'chat';
            default:
                return feature;
        }
    });
    return [...new Set(transform)];
};
exports.getCategories = getCategories;
const getCategoriesForIntegration = (integration) => {
    if (isSentryApp(integration)) {
        return ['internal', 'unpublished'].includes(integration.status)
            ? [integration.status]
            : (0, exports.getCategories)(integration.featureData);
    }
    if (isPlugin(integration)) {
        return (0, exports.getCategories)(integration.featureDescriptions);
    }
    if (isDocumentIntegration(integration)) {
        return (0, exports.getCategories)(integration.features);
    }
    return (0, exports.getCategories)(integration.metadata.features);
};
exports.getCategoriesForIntegration = getCategoriesForIntegration;
function isSentryApp(integration) {
    return !!integration.uuid;
}
exports.isSentryApp = isSentryApp;
function isPlugin(integration) {
    return integration.hasOwnProperty('shortName');
}
exports.isPlugin = isPlugin;
function isDocumentIntegration(integration) {
    return integration.hasOwnProperty('docUrl');
}
exports.isDocumentIntegration = isDocumentIntegration;
const getIntegrationType = (integration) => {
    if (isSentryApp(integration)) {
        return 'sentry_app';
    }
    if (isPlugin(integration)) {
        return 'plugin';
    }
    if (isDocumentIntegration(integration)) {
        return 'document';
    }
    return 'first_party';
};
exports.getIntegrationType = getIntegrationType;
const convertIntegrationTypeToSnakeCase = (type) => {
    switch (type) {
        case 'firstParty':
            return 'first_party';
        case 'sentryApp':
            return 'sentry_app';
        case 'documentIntegration':
            return 'document';
        default:
            return type;
    }
};
exports.convertIntegrationTypeToSnakeCase = convertIntegrationTypeToSnakeCase;
const safeGetQsParam = (param) => {
    try {
        const query = qs.parse(window.location.search) || {};
        return query[param];
    }
    catch (_a) {
        return undefined;
    }
};
exports.safeGetQsParam = safeGetQsParam;
const getIntegrationIcon = (integrationType, size) => {
    const iconSize = size || 'md';
    switch (integrationType) {
        case 'bitbucket':
            return <icons_1.IconBitbucket size={iconSize}/>;
        case 'gitlab':
            return <icons_1.IconGitlab size={iconSize}/>;
        case 'github':
        case 'github_enterprise':
            return <icons_1.IconGithub size={iconSize}/>;
        case 'jira':
        case 'jira_server':
            return <icons_1.IconJira size={iconSize}/>;
        case 'vsts':
            return <icons_1.IconVsts size={iconSize}/>;
        default:
            return <icons_1.IconGeneric size={iconSize}/>;
    }
};
exports.getIntegrationIcon = getIntegrationIcon;
// used for project creation and onboarding
// determines what integration maps to what project platform
exports.platformToIntegrationMap = {
    'node-awslambda': 'aws_lambda',
    'python-awslambda': 'aws_lambda',
};
const isSlackIntegrationUpToDate = (integrations) => {
    return integrations.every(integration => { var _a; return integration.provider.key !== 'slack' || ((_a = integration.scopes) === null || _a === void 0 ? void 0 : _a.includes('commands')); });
};
exports.isSlackIntegrationUpToDate = isSlackIntegrationUpToDate;
const getAlertText = (integrations) => {
    return (0, exports.isSlackIntegrationUpToDate)(integrations || [])
        ? undefined
        : (0, locale_1.t)('Update to the latest version of our Slack app to get access to personal and team notifications.');
};
exports.getAlertText = getAlertText;
//# sourceMappingURL=integrationUtil.jsx.map