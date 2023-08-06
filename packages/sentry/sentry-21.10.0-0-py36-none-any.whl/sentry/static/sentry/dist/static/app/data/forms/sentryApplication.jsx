Object.defineProperty(exports, "__esModule", { value: true });
exports.internalIntegrationForms = exports.publicIntegrationForms = void 0;
const tslib_1 = require("tslib");
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const locale_1 = require("app/locale");
const utils_1 = require("app/utils");
const getPublicFormFields = () => [
    {
        name: 'name',
        type: 'string',
        required: true,
        placeholder: 'e.g. My Integration',
        label: 'Name',
        help: 'Human readable name of your Integration.',
    },
    {
        name: 'author',
        type: 'string',
        required: true,
        placeholder: 'e.g. Acme Software',
        label: 'Author',
        help: 'The company or person who built and maintains this Integration.',
    },
    {
        name: 'webhookUrl',
        type: 'string',
        required: true,
        label: 'Webhook URL',
        placeholder: 'e.g. https://example.com/sentry/webhook/',
        help: (0, locale_1.tct)('All webhook requests for your integration will be sent to this URL. Visit the [webhook_docs:documentation] to see the different types and payloads.', {
            webhook_docs: (<externalLink_1.default href="https://docs.sentry.io/product/integrations/integration-platform/webhooks/"/>),
        }),
    },
    {
        name: 'redirectUrl',
        type: 'string',
        label: 'Redirect URL',
        placeholder: 'e.g. https://example.com/sentry/setup/',
        help: 'The URL Sentry will redirect users to after installation.',
    },
    {
        name: 'verifyInstall',
        label: 'Verify Installation',
        type: 'boolean',
        help: 'If enabled, installations will need to be verified before becoming installed.',
    },
    {
        name: 'isAlertable',
        type: 'boolean',
        label: 'Alert Rule Action',
        disabled: ({ webhookDisabled }) => webhookDisabled,
        disabledReason: 'Cannot enable alert rule action without a webhook url',
        help: (0, locale_1.tct)('If enabled, this integration will be available in Issue Alert rules and Metric Alert rules in Sentry. The notification destination is the Webhook URL specified above. More on actions [learn_more:here].', {
            learn_more: (<externalLink_1.default href="https://docs.sentry.io/product/alerts-notifications/notifications/"/>),
        }),
    },
    {
        name: 'schema',
        type: 'textarea',
        label: 'Schema',
        autosize: true,
        rows: 1,
        help: (0, locale_1.tct)('Schema for your UI components. Click [schema_docs:here] for documentation.', {
            schema_docs: (<externalLink_1.default href="https://docs.sentry.io/product/integrations/integration-platform/ui-components/"/>),
        }),
        getValue: (val) => (val === '' ? {} : JSON.parse(val)),
        setValue: (val) => {
            const schema = JSON.stringify(val, null, 2);
            if (schema === '{}') {
                return '';
            }
            return schema;
        },
        validate: ({ id, form }) => {
            if (!form.schema) {
                return [];
            }
            try {
                JSON.parse(form.schema);
            }
            catch (e) {
                return [[id, 'Invalid JSON']];
            }
            return [];
        },
    },
    {
        name: 'overview',
        type: 'textarea',
        label: 'Overview',
        autosize: true,
        rows: 1,
        help: 'Description of your Integration and its functionality.',
    },
    {
        name: 'allowedOrigins',
        type: 'string',
        multiline: true,
        placeholder: 'e.g. example.com',
        label: 'Authorized JavaScript Origins',
        help: 'Separate multiple entries with a newline.',
        getValue: (val) => (0, utils_1.extractMultilineFields)(val),
        setValue: (val) => (val && typeof val.join === 'function' && val.join('\n')) || '',
    },
];
exports.publicIntegrationForms = [
    {
        title: 'Public Integration Details',
        fields: getPublicFormFields(),
    },
];
const getInternalFormFields = () => {
    // Generate internal form fields copy copying the public form fields and
    // making adjustments:
    //
    //   1. remove fields not needed for internal integrations
    //   2. make webhookUrl optional
    const internalFormFields = getPublicFormFields().filter(formField => !['redirectUrl', 'verifyInstall', 'author'].includes(formField.name || ''));
    const webhookField = internalFormFields.find(field => field.name === 'webhookUrl');
    if (webhookField) {
        webhookField.required = false;
    }
    return internalFormFields;
};
exports.internalIntegrationForms = [
    {
        title: 'Internal Integration Details',
        fields: getInternalFormFields(),
    },
];
//# sourceMappingURL=sentryApplication.jsx.map