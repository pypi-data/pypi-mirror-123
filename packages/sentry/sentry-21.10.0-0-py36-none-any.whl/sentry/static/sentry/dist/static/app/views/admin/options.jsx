Object.defineProperty(exports, "__esModule", { value: true });
exports.getForm = exports.getOptionField = exports.getOptionDefault = exports.getOption = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const keyBy_1 = (0, tslib_1.__importDefault)(require("lodash/keyBy"));
const locale_1 = require("app/locale");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const forms_1 = require("app/views/settings/components/forms");
// This are ordered based on their display order visually
const sections = [
    {
        key: 'system',
    },
    {
        key: 'mail',
        heading: (0, locale_1.t)('Outbound email'),
    },
    {
        key: 'auth',
        heading: (0, locale_1.t)('Authentication'),
    },
    {
        key: 'beacon',
        heading: (0, locale_1.t)('Beacon'),
    },
];
// This are ordered based on their display order visually
const definitions = [
    {
        key: 'system.url-prefix',
        label: (0, locale_1.t)('Root URL'),
        placeholder: 'https://sentry.example.com',
        help: (0, locale_1.t)('The root web address which is used to communicate with the Sentry backend.'),
        defaultValue: () => `${document.location.protocol}//${document.location.host}`,
    },
    {
        key: 'system.admin-email',
        label: (0, locale_1.t)('Admin Email'),
        placeholder: 'admin@example.com',
        help: (0, locale_1.t)('The technical contact for this Sentry installation.'),
        // TODO(dcramer): this should not be hardcoded to a component
        component: forms_1.EmailField,
        defaultValue: () => configStore_1.default.get('user').email,
    },
    {
        key: 'system.support-email',
        label: (0, locale_1.t)('Support Email'),
        placeholder: 'support@example.com',
        help: (0, locale_1.t)('The support contact for this Sentry installation.'),
        // TODO(dcramer): this should not be hardcoded to a component
        component: forms_1.EmailField,
        defaultValue: () => configStore_1.default.get('user').email,
    },
    {
        key: 'system.security-email',
        label: (0, locale_1.t)('Security Email'),
        placeholder: 'security@example.com',
        help: (0, locale_1.t)('The security contact for this Sentry installation.'),
        // TODO(dcramer): this should not be hardcoded to a component
        component: forms_1.EmailField,
        defaultValue: () => configStore_1.default.get('user').email,
    },
    {
        key: 'system.rate-limit',
        label: (0, locale_1.t)('Rate Limit'),
        placeholder: 'e.g. 500',
        help: (0, locale_1.t)('The maximum number of events the system should accept per minute. A value of 0 will disable the default rate limit.'),
    },
    {
        key: 'auth.allow-registration',
        label: (0, locale_1.t)('Allow Registration'),
        help: (0, locale_1.t)('Allow anyone to create an account and access this Sentry installation.'),
        component: forms_1.BooleanField,
        defaultValue: () => false,
    },
    {
        key: 'auth.ip-rate-limit',
        label: (0, locale_1.t)('IP Rate Limit'),
        placeholder: 'e.g. 10',
        help: (0, locale_1.t)('The maximum number of times an authentication attempt may be made by a single IP address in a 60 second window.'),
    },
    {
        key: 'auth.user-rate-limit',
        label: (0, locale_1.t)('User Rate Limit'),
        placeholder: 'e.g. 10',
        help: (0, locale_1.t)('The maximum number of times an authentication attempt may be made against a single account in a 60 second window.'),
    },
    {
        key: 'api.rate-limit.org-create',
        label: 'Organization Creation Rate Limit',
        placeholder: 'e.g. 5',
        help: (0, locale_1.t)('The maximum number of organizations which may be created by a single account in a one hour window.'),
    },
    {
        key: 'beacon.anonymous',
        label: 'Usage Statistics',
        component: forms_1.RadioBooleanField,
        // yes and no are inverted here due to the nature of this configuration
        noLabel: 'Send my contact information along with usage statistics',
        yesLabel: 'Please keep my usage information anonymous',
        yesFirst: false,
        help: (0, locale_1.tct)('If enabled, any stats reported to sentry.io will exclude identifying information (such as your administrative email address). By anonymizing your installation the Sentry team will be unable to contact you about security updates. For more information on what data is sent to Sentry, see the [link:documentation].', {
            link: <a href="https://develop.sentry.dev/self-hosted/"/>,
        }),
    },
    {
        key: 'mail.from',
        label: (0, locale_1.t)('Email From'),
        component: forms_1.EmailField,
        defaultValue: () => `sentry@${document.location.hostname}`,
        help: (0, locale_1.t)('Email address to be used in From for all outbound email.'),
    },
    {
        key: 'mail.host',
        label: (0, locale_1.t)('SMTP Host'),
        placeholder: 'localhost',
        defaultValue: () => 'localhost',
    },
    {
        key: 'mail.port',
        label: (0, locale_1.t)('SMTP Port'),
        placeholder: '25',
        defaultValue: () => '25',
    },
    {
        key: 'mail.username',
        label: (0, locale_1.t)('SMTP Username'),
        defaultValue: () => '',
    },
    {
        key: 'mail.password',
        label: (0, locale_1.t)('SMTP Password'),
        // TODO(mattrobenolt): We don't want to use a real password field unless
        // there's a way to reveal it. Without being able to see the password, it's
        // impossible to confirm if it's right.
        // component: PasswordField,
        defaultValue: () => '',
    },
    {
        key: 'mail.use-tls',
        label: (0, locale_1.t)('Use STARTTLS? (exclusive with SSL)'),
        component: forms_1.BooleanField,
        defaultValue: () => false,
    },
    {
        key: 'mail.use-ssl',
        label: (0, locale_1.t)('Use SSL? (exclusive with STARTTLS)'),
        component: forms_1.BooleanField,
        defaultValue: () => false,
    },
];
const definitionsMap = (0, keyBy_1.default)(definitions, def => def.key);
const disabledReasons = {
    diskPriority: 'This setting is defined in config.yml and may not be changed via the web UI.',
    smtpDisabled: 'SMTP mail has been disabled, so this option is unavailable',
};
function getOption(option) {
    return definitionsMap[option];
}
exports.getOption = getOption;
function getOptionDefault(option) {
    const meta = getOption(option);
    return meta.defaultValue ? meta.defaultValue() : undefined;
}
exports.getOptionDefault = getOptionDefault;
function optionsForSection(section) {
    return definitions.filter(option => option.key.split('.')[0] === section.key);
}
function getOptionField(option, field) {
    const meta = Object.assign(Object.assign({}, getOption(option)), field);
    const Field = meta.component || forms_1.TextField;
    return (<Field {...meta} name={option} key={option} defaultValue={getOptionDefault(option)} required={meta.required && !meta.allowEmpty} disabledReason={meta.disabledReason && disabledReasons[meta.disabledReason]}/>);
}
exports.getOptionField = getOptionField;
function getSectionFieldSet(section, fields) {
    return (<fieldset key={section.key}>
      {section.heading && <legend>{section.heading}</legend>}
      {fields}
    </fieldset>);
}
function getForm(fieldMap) {
    const sets = [];
    for (const section of sections) {
        const set = [];
        for (const option of optionsForSection(section)) {
            if (fieldMap[option.key]) {
                set.push(fieldMap[option.key]);
            }
        }
        if (set.length) {
            sets.push(getSectionFieldSet(section, set));
        }
    }
    return sets;
}
exports.getForm = getForm;
//# sourceMappingURL=options.jsx.map