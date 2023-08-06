Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const locale_1 = require("app/locale");
const hookStore_1 = (0, tslib_1.__importDefault)(require("app/stores/hookStore"));
const pathPrefix = '/settings/account';
function getConfiguration({ organization }) {
    return [
        {
            name: (0, locale_1.t)('Account'),
            items: [
                {
                    path: `${pathPrefix}/details/`,
                    title: (0, locale_1.t)('Account Details'),
                    description: (0, locale_1.t)('Change your account details and preferences (e.g. timezone/clock, avatar, language)'),
                },
                {
                    path: `${pathPrefix}/security/`,
                    title: (0, locale_1.t)('Security'),
                    description: (0, locale_1.t)('Change your account password and/or two factor authentication'),
                },
                {
                    path: `${pathPrefix}/notifications/`,
                    title: (0, locale_1.t)('Notifications'),
                    description: (0, locale_1.t)('Configure what email notifications to receive'),
                },
                {
                    path: `${pathPrefix}/emails/`,
                    title: (0, locale_1.t)('Email Addresses'),
                    description: (0, locale_1.t)('Add or remove secondary emails, change your primary email, verify your emails'),
                },
                {
                    path: `${pathPrefix}/subscriptions/`,
                    title: (0, locale_1.t)('Subscriptions'),
                    description: (0, locale_1.t)('Change Sentry marketing subscriptions you are subscribed to (GDPR)'),
                },
                {
                    path: `${pathPrefix}/authorizations/`,
                    title: (0, locale_1.t)('Authorized Applications'),
                    description: (0, locale_1.t)('Manage third-party applications that have access to your Sentry account'),
                },
                {
                    path: `${pathPrefix}/identities/`,
                    title: (0, locale_1.t)('Identities'),
                    description: (0, locale_1.t)('Manage your third-party identities that are associated to Sentry'),
                },
                {
                    path: `${pathPrefix}/close-account/`,
                    title: (0, locale_1.t)('Close Account'),
                    description: (0, locale_1.t)('Permanently close your Sentry account'),
                },
            ],
        },
        {
            name: (0, locale_1.t)('API'),
            items: [
                {
                    path: `${pathPrefix}/api/applications/`,
                    title: (0, locale_1.t)('Applications'),
                    description: (0, locale_1.t)('Add and configure OAuth2 applications'),
                },
                {
                    path: `${pathPrefix}/api/auth-tokens/`,
                    title: (0, locale_1.t)('Auth Tokens'),
                    description: (0, locale_1.t)("Authentication tokens allow you to perform actions against the Sentry API on behalf of your account. They're the easiest way to get started using the API."),
                },
                ...hookStore_1.default.get('settings:api-navigation-config').flatMap(cb => cb(organization)),
            ],
        },
    ];
}
exports.default = getConfiguration;
//# sourceMappingURL=navigationConfiguration.jsx.map