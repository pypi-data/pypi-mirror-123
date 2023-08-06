Object.defineProperty(exports, "__esModule", { value: true });
exports.route = void 0;
const locale_1 = require("app/locale");
const utils_1 = require("app/utils");
const crashReports_1 = require("app/utils/crashReports");
// Export route to make these forms searchable by label/help
exports.route = '/settings/:orgId/security-and-privacy/';
exports.default = [
    {
        title: (0, locale_1.t)('Security & Privacy'),
        fields: [
            {
                name: 'require2FA',
                type: 'boolean',
                label: (0, locale_1.t)('Require Two-Factor Authentication'),
                help: (0, locale_1.t)('Require and enforce two-factor authentication for all members'),
                confirm: {
                    true: (0, locale_1.t)('This will remove all members without two-factor authentication' +
                        ' from your organization. It will also send them an email to setup 2FA' +
                        ' and reinstate their access and settings. Do you want to continue?'),
                    false: (0, locale_1.t)('Are you sure you want to allow users to access your organization without having two-factor authentication enabled?'),
                },
            },
            {
                name: 'requireEmailVerification',
                type: 'boolean',
                label: (0, locale_1.t)('Require Email Verification'),
                help: (0, locale_1.t)('Require and enforce email address verification for all members'),
                visible: ({ features }) => features.has('required-email-verification'),
                confirm: {
                    true: (0, locale_1.t)('This will remove all members whose email addresses are not verified' +
                        ' from your organization. It will also send them an email to verify their address' +
                        ' and reinstate their access and settings. Do you want to continue?'),
                    false: (0, locale_1.t)('Are you sure you want to allow users to access your organization without verifying their email address?'),
                },
            },
            {
                name: 'allowSharedIssues',
                type: 'boolean',
                label: (0, locale_1.t)('Allow Shared Issues'),
                help: (0, locale_1.t)('Enable sharing of limited details on issues to anonymous users'),
                confirm: {
                    true: (0, locale_1.t)('Are you sure you want to allow sharing issues to anonymous users?'),
                },
            },
            {
                name: 'enhancedPrivacy',
                type: 'boolean',
                label: (0, locale_1.t)('Enhanced Privacy'),
                help: (0, locale_1.t)('Enable enhanced privacy controls to limit personally identifiable information (PII) as well as source code in things like notifications'),
                confirm: {
                    false: (0, locale_1.t)('Disabling this can have privacy implications for ALL projects, are you sure you want to continue?'),
                },
            },
            {
                name: 'scrapeJavaScript',
                type: 'boolean',
                confirm: {
                    false: (0, locale_1.t)("Are you sure you want to disable sourcecode fetching for JavaScript events? This will affect Sentry's ability to aggregate issues if you're not already uploading sourcemaps as artifacts."),
                },
                label: (0, locale_1.t)('Allow JavaScript Source Fetching'),
                help: (0, locale_1.t)('Allow Sentry to scrape missing JavaScript source context when possible'),
            },
            {
                name: 'storeCrashReports',
                type: 'select',
                label: (0, locale_1.t)('Store Native Crash Reports'),
                help: (0, locale_1.t)('Store native crash reports such as Minidumps for improved processing and download in issue details'),
                visible: ({ features }) => features.has('event-attachments'),
                // HACK: some organization can have limit of stored crash reports a number that's not in the options (legacy reasons),
                // we therefore display it in a placeholder
                placeholder: ({ value }) => (0, crashReports_1.formatStoreCrashReports)(value),
                choices: () => (0, crashReports_1.getStoreCrashReportsValues)(crashReports_1.SettingScope.Organization).map(value => [
                    value,
                    (0, crashReports_1.formatStoreCrashReports)(value),
                ]),
            },
            {
                name: 'allowJoinRequests',
                type: 'boolean',
                label: (0, locale_1.t)('Allow Join Requests'),
                help: (0, locale_1.t)('Allow users to request to join your organization'),
                confirm: {
                    true: (0, locale_1.t)('Are you sure you want to allow users to request to join your organization?'),
                },
                visible: ({ hasSsoEnabled }) => !hasSsoEnabled,
            },
        ],
    },
    {
        title: (0, locale_1.t)('Data Scrubbing'),
        fields: [
            {
                name: 'dataScrubber',
                type: 'boolean',
                label: (0, locale_1.t)('Require Data Scrubber'),
                help: (0, locale_1.t)('Require server-side data scrubbing be enabled for all projects'),
                confirm: {
                    false: (0, locale_1.t)('Disabling this can have privacy implications for ALL projects, are you sure you want to continue?'),
                },
            },
            {
                name: 'dataScrubberDefaults',
                type: 'boolean',
                label: (0, locale_1.t)('Require Using Default Scrubbers'),
                help: (0, locale_1.t)('Require the default scrubbers be applied to prevent things like passwords and credit cards from being stored for all projects'),
                confirm: {
                    false: (0, locale_1.t)('Disabling this can have privacy implications for ALL projects, are you sure you want to continue?'),
                },
            },
            {
                name: 'sensitiveFields',
                type: 'string',
                multiline: true,
                autosize: true,
                maxRows: 10,
                rows: 1,
                placeholder: 'e.g. email',
                label: (0, locale_1.t)('Global Sensitive Fields'),
                help: (0, locale_1.t)('Additional field names to match against when scrubbing data for all projects. Separate multiple entries with a newline.'),
                extraHelp: (0, locale_1.t)('Note: These fields will be used in addition to project specific fields.'),
                getValue: val => (0, utils_1.extractMultilineFields)(val),
                setValue: val => (0, utils_1.convertMultilineFieldValue)(val),
            },
            {
                name: 'safeFields',
                type: 'string',
                multiline: true,
                autosize: true,
                maxRows: 10,
                rows: 1,
                placeholder: (0, locale_1.t)('e.g. business-email'),
                label: (0, locale_1.t)('Global Safe Fields'),
                help: (0, locale_1.t)('Field names which data scrubbers should ignore. Separate multiple entries with a newline.'),
                extraHelp: (0, locale_1.t)('Note: These fields will be used in addition to project specific fields'),
                getValue: val => (0, utils_1.extractMultilineFields)(val),
                setValue: val => (0, utils_1.convertMultilineFieldValue)(val),
            },
            {
                name: 'scrubIPAddresses',
                type: 'boolean',
                label: (0, locale_1.t)('Prevent Storing of IP Addresses'),
                help: (0, locale_1.t)('Preventing IP addresses from being stored for new events on all projects'),
                confirm: {
                    false: (0, locale_1.t)('Disabling this can have privacy implications for ALL projects, are you sure you want to continue?'),
                },
            },
        ],
    },
];
//# sourceMappingURL=organizationSecurityAndPrivacyGroups.jsx.map