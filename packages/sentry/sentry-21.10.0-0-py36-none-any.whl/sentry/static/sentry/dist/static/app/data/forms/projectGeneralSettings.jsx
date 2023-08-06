Object.defineProperty(exports, "__esModule", { value: true });
exports.fields = exports.route = void 0;
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const platformicons_1 = require("platformicons");
const platforms_1 = (0, tslib_1.__importDefault)(require("app/data/platforms"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const slugify_1 = (0, tslib_1.__importDefault)(require("app/utils/slugify"));
// Export route to make these forms searchable by label/help
exports.route = '/settings/:orgId/projects/:projectId/';
const getResolveAgeAllowedValues = () => {
    let i = 0;
    const values = [];
    while (i <= 720) {
        values.push(i);
        if (i < 12) {
            i += 1;
        }
        else if (i < 24) {
            i += 3;
        }
        else if (i < 36) {
            i += 6;
        }
        else if (i < 48) {
            i += 12;
        }
        else {
            i += 24;
        }
    }
    return values;
};
const RESOLVE_AGE_ALLOWED_VALUES = getResolveAgeAllowedValues();
const ORG_DISABLED_REASON = (0, locale_1.t)("This option is enforced by your organization's settings and cannot be customized per-project.");
exports.fields = {
    slug: {
        name: 'slug',
        type: 'string',
        required: true,
        label: (0, locale_1.t)('Name'),
        placeholder: (0, locale_1.t)('my-service-name'),
        help: (0, locale_1.t)('A unique ID used to identify this project'),
        transformInput: slugify_1.default,
        saveOnBlur: false,
        saveMessageAlertType: 'info',
        saveMessage: (0, locale_1.t)('You will be redirected to the new project slug after saving'),
    },
    platform: {
        name: 'platform',
        type: 'select',
        label: (0, locale_1.t)('Platform'),
        choices: () => platforms_1.default.map(({ id, name }) => [
            id,
            <PlatformWrapper key={id}>
          <StyledPlatformIcon platform={id}/>
          {name}
        </PlatformWrapper>,
        ]),
        help: (0, locale_1.t)('The primary platform for this project'),
    },
    subjectPrefix: {
        name: 'subjectPrefix',
        type: 'string',
        label: (0, locale_1.t)('Subject Prefix'),
        placeholder: (0, locale_1.t)('e.g. [my-org]'),
        help: (0, locale_1.t)('Choose a custom prefix for emails from this project'),
    },
    resolveAge: {
        name: 'resolveAge',
        type: 'range',
        allowedValues: RESOLVE_AGE_ALLOWED_VALUES,
        label: (0, locale_1.t)('Auto Resolve'),
        help: (0, locale_1.t)("Automatically resolve an issue if it hasn't been seen for this amount of time"),
        formatLabel: val => {
            val = Number(val);
            if (val === 0) {
                return (0, locale_1.t)('Disabled');
            }
            if (val > 23 && val % 24 === 0) {
                // Based on allowed values, val % 24 should always be true
                val = val / 24;
                return (0, locale_1.tn)('%s day', '%s days', val);
            }
            return (0, locale_1.tn)('%s hour', '%s hours', val);
        },
        saveOnBlur: false,
        saveMessage: (0, locale_1.tct)('[Caution]: Enabling auto resolve will immediately resolve anything that has ' +
            'not been seen within this period of time. There is no undo!', {
            Caution: <strong>Caution</strong>,
        }),
        saveMessageAlertType: 'warning',
    },
    allowedDomains: {
        name: 'allowedDomains',
        type: 'string',
        multiline: true,
        autosize: true,
        maxRows: 10,
        rows: 1,
        placeholder: (0, locale_1.t)('https://example.com or example.com'),
        label: (0, locale_1.t)('Allowed Domains'),
        help: (0, locale_1.t)('Separate multiple entries with a newline'),
        getValue: val => (0, utils_1.extractMultilineFields)(val),
        setValue: val => (0, utils_1.convertMultilineFieldValue)(val),
    },
    scrapeJavaScript: {
        name: 'scrapeJavaScript',
        type: 'boolean',
        // if this is off for the organization, it cannot be enabled for the project
        disabled: ({ organization, name }) => !organization[name],
        disabledReason: ORG_DISABLED_REASON,
        // `props` are the props given to FormField
        setValue: (val, props) => props.organization && props.organization[props.name] && val,
        label: (0, locale_1.t)('Enable JavaScript source fetching'),
        help: (0, locale_1.t)('Allow Sentry to scrape missing JavaScript source context when possible'),
    },
    securityToken: {
        name: 'securityToken',
        type: 'string',
        label: (0, locale_1.t)('Security Token'),
        help: (0, locale_1.t)('Outbound requests matching Allowed Domains will have the header "{token_header}: {token}" appended'),
        setValue: value => (0, getDynamicText_1.default)({ value, fixed: '__SECURITY_TOKEN__' }),
    },
    securityTokenHeader: {
        name: 'securityTokenHeader',
        type: 'string',
        placeholder: (0, locale_1.t)('X-Sentry-Token'),
        label: (0, locale_1.t)('Security Token Header'),
        help: (0, locale_1.t)('Outbound requests matching Allowed Domains will have the header "{token_header}: {token}" appended'),
    },
    verifySSL: {
        name: 'verifySSL',
        type: 'boolean',
        label: (0, locale_1.t)('Verify TLS/SSL'),
        help: (0, locale_1.t)('Outbound requests will verify TLS (sometimes known as SSL) connections'),
    },
};
const PlatformWrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
`;
const StyledPlatformIcon = (0, styled_1.default)(platformicons_1.PlatformIcon) `
  margin-right: ${(0, space_1.default)(1)};
`;
//# sourceMappingURL=projectGeneralSettings.jsx.map