Object.defineProperty(exports, "__esModule", { value: true });
exports.route = void 0;
const tslib_1 = require("tslib");
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const locale_1 = require("app/locale");
const utils_1 = require("app/utils");
const crashReports_1 = require("app/utils/crashReports");
// Export route to make these forms searchable by label/help
exports.route = '/settings/:orgId/projects/:projectId/security-and-privacy/';
const ORG_DISABLED_REASON = (0, locale_1.t)("This option is enforced by your organization's settings and cannot be customized per-project.");
// Check if a field has been set AND IS TRUTHY at the organization level.
const hasOrgOverride = ({ organization, name }) => organization[name];
exports.default = [
    {
        title: (0, locale_1.t)('Security & Privacy'),
        fields: [
            {
                name: 'storeCrashReports',
                type: 'select',
                label: (0, locale_1.t)('Store Native Crash Reports'),
                help: ({ organization }) => (0, locale_1.tct)('Store native crash reports such as Minidumps for improved processing and download in issue details. Overrides [organizationSettingsLink: organization settings].', {
                    organizationSettingsLink: (<link_1.default to={`/settings/${organization.slug}/security-and-privacy/`}/>),
                }),
                visible: ({ features }) => features.has('event-attachments'),
                placeholder: ({ organization, value }) => {
                    // empty value means that this project should inherit organization settings
                    if (value === '') {
                        return (0, locale_1.tct)('Inherit organization settings ([organizationValue])', {
                            organizationValue: (0, crashReports_1.formatStoreCrashReports)(organization.storeCrashReports),
                        });
                    }
                    // HACK: some organization can have limit of stored crash reports a number that's not in the options (legacy reasons),
                    // we therefore display it in a placeholder
                    return (0, crashReports_1.formatStoreCrashReports)(value);
                },
                choices: ({ organization }) => (0, crashReports_1.getStoreCrashReportsValues)(crashReports_1.SettingScope.Project).map(value => [
                    value,
                    (0, crashReports_1.formatStoreCrashReports)(value, organization.storeCrashReports),
                ]),
            },
        ],
    },
    {
        title: (0, locale_1.t)('Data Scrubbing'),
        fields: [
            {
                name: 'dataScrubber',
                type: 'boolean',
                label: (0, locale_1.t)('Data Scrubber'),
                disabled: hasOrgOverride,
                disabledReason: ORG_DISABLED_REASON,
                help: (0, locale_1.t)('Enable server-side data scrubbing'),
                // `props` are the props given to FormField
                setValue: (val, props) => (props.organization && props.organization[props.name]) || val,
                confirm: {
                    false: (0, locale_1.t)('Are you sure you want to disable server-side data scrubbing?'),
                },
            },
            {
                name: 'dataScrubberDefaults',
                type: 'boolean',
                disabled: hasOrgOverride,
                disabledReason: ORG_DISABLED_REASON,
                label: (0, locale_1.t)('Use Default Scrubbers'),
                help: (0, locale_1.t)('Apply default scrubbers to prevent things like passwords and credit cards from being stored'),
                // `props` are the props given to FormField
                setValue: (val, props) => (props.organization && props.organization[props.name]) || val,
                confirm: {
                    false: (0, locale_1.t)('Are you sure you want to disable using default scrubbers?'),
                },
            },
            {
                name: 'scrubIPAddresses',
                type: 'boolean',
                disabled: hasOrgOverride,
                disabledReason: ORG_DISABLED_REASON,
                // `props` are the props given to FormField
                setValue: (val, props) => (props.organization && props.organization[props.name]) || val,
                label: (0, locale_1.t)('Prevent Storing of IP Addresses'),
                help: (0, locale_1.t)('Preventing IP addresses from being stored for new events'),
                confirm: {
                    false: (0, locale_1.t)('Are you sure you want to disable scrubbing IP addresses?'),
                },
            },
            {
                name: 'sensitiveFields',
                type: 'string',
                multiline: true,
                autosize: true,
                maxRows: 10,
                rows: 1,
                placeholder: (0, locale_1.t)('email'),
                label: (0, locale_1.t)('Additional Sensitive Fields'),
                help: (0, locale_1.t)('Additional field names to match against when scrubbing data. Separate multiple entries with a newline'),
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
                placeholder: (0, locale_1.t)('business-email'),
                label: (0, locale_1.t)('Safe Fields'),
                help: (0, locale_1.t)('Field names which data scrubbers should ignore. Separate multiple entries with a newline'),
                getValue: val => (0, utils_1.extractMultilineFields)(val),
                setValue: val => (0, utils_1.convertMultilineFieldValue)(val),
            },
        ],
    },
];
//# sourceMappingURL=projectSecurityAndPrivacyGroups.jsx.map