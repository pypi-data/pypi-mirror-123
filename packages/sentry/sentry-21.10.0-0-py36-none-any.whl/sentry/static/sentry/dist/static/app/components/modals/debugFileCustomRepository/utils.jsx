Object.defineProperty(exports, "__esModule", { value: true });
exports.getFinalData = exports.getFormFieldsAndInitialData = void 0;
const tslib_1 = require("tslib");
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const debugFileSources_1 = require("app/data/debugFileSources");
const locale_1 = require("app/locale");
const debugFiles_1 = require("app/types/debugFiles");
function objectToChoices(obj) {
    return Object.entries(obj).map(([key, value]) => [key, (0, locale_1.t)(value)]);
}
const commonFields = {
    id: {
        name: 'id',
        type: 'hidden',
        required: true,
        defaultValue: () => Math.random().toString(36).substring(2),
    },
    name: {
        name: 'name',
        type: 'string',
        required: true,
        label: (0, locale_1.t)('Name'),
        placeholder: (0, locale_1.t)('New Repository'),
        help: (0, locale_1.t)('A display name for this repository'),
    },
    // filters are explicitly not exposed to the UI
    layoutType: {
        name: 'layout.type',
        type: 'select',
        label: (0, locale_1.t)('Directory Layout'),
        help: (0, locale_1.t)('The layout of the folder structure.'),
        defaultValue: 'native',
        choices: objectToChoices(debugFileSources_1.DEBUG_SOURCE_LAYOUTS),
    },
    layoutCasing: {
        name: 'layout.casing',
        type: 'select',
        label: (0, locale_1.t)('Path Casing'),
        help: (0, locale_1.t)('The case of files and folders.'),
        defaultValue: 'default',
        choices: objectToChoices(debugFileSources_1.DEBUG_SOURCE_CASINGS),
    },
    prefix: {
        name: 'prefix',
        type: 'string',
        label: 'Root Path',
        placeholder: '/',
        help: (0, locale_1.t)('The path at which files are located within this repository.'),
    },
    separator: {
        name: '',
        type: 'separator',
    },
};
function getFormFieldsAndInitialData(type, sourceConfig) {
    if (type === debugFiles_1.CustomRepoType.HTTP || type === debugFiles_1.CustomRepoType.APP_STORE_CONNECT) {
        return {};
    }
    const _a = sourceConfig !== null && sourceConfig !== void 0 ? sourceConfig : {}, { secret_key, layout, private_key } = _a, config = (0, tslib_1.__rest)(_a, ["secret_key", "layout", "private_key"]);
    const initialData = layout
        ? Object.assign(Object.assign({}, config), { 'layout.casing': layout.casing, 'layout.type': layout.type }) : config;
    switch (type) {
        case 's3':
            return {
                fields: [
                    commonFields.id,
                    commonFields.name,
                    commonFields.separator,
                    {
                        name: 'bucket',
                        type: 'string',
                        required: true,
                        label: (0, locale_1.t)('Bucket'),
                        placeholder: 's3-bucket-name',
                        help: (0, locale_1.t)('Name of the S3 bucket. Read permissions are required to download symbols.'),
                    },
                    {
                        name: 'region',
                        type: 'select',
                        required: true,
                        label: (0, locale_1.t)('Region'),
                        help: (0, locale_1.t)('The AWS region and availability zone of the bucket.'),
                        choices: debugFileSources_1.AWS_REGIONS.map(([k, v]) => [
                            k,
                            <span key={k}>
                <code>{k}</code> {v}
              </span>,
                        ]),
                    },
                    {
                        name: 'access_key',
                        type: 'string',
                        required: true,
                        label: (0, locale_1.t)('Access Key ID'),
                        placeholder: 'AKIAIOSFODNN7EXAMPLE',
                        help: (0, locale_1.tct)('Access key to the AWS account. Credentials can be managed in the [link].', {
                            link: (<externalLink_1.default href="https://console.aws.amazon.com/iam/">
                    IAM console
                  </externalLink_1.default>),
                        }),
                    },
                    {
                        name: 'secret_key',
                        type: 'string',
                        required: true,
                        label: (0, locale_1.t)('Secret Access Key'),
                        placeholder: typeof secret_key === 'object'
                            ? (0, locale_1.t)('(Secret Access Key unchanged)')
                            : 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
                    },
                    commonFields.separator,
                    commonFields.prefix,
                    commonFields.layoutType,
                    commonFields.layoutCasing,
                ],
                initialData: !initialData
                    ? undefined
                    : Object.assign(Object.assign({}, initialData), { secret_key: undefined }),
            };
        case 'gcs':
            return {
                fields: [
                    commonFields.id,
                    commonFields.name,
                    commonFields.separator,
                    {
                        name: 'bucket',
                        type: 'string',
                        required: true,
                        label: (0, locale_1.t)('Bucket'),
                        placeholder: 'gcs-bucket-name',
                        help: (0, locale_1.t)('Name of the GCS bucket. Read permissions are required to download symbols.'),
                    },
                    {
                        name: 'client_email',
                        type: 'email',
                        required: true,
                        label: (0, locale_1.t)('Client Email'),
                        placeholder: 'user@project.iam.gserviceaccount.com',
                        help: (0, locale_1.t)('Email address of the GCS service account.'),
                    },
                    {
                        name: 'private_key',
                        type: 'string',
                        required: true,
                        multiline: true,
                        autosize: true,
                        maxRows: 5,
                        rows: 3,
                        label: (0, locale_1.t)('Private Key'),
                        placeholder: typeof private_key === 'object'
                            ? (0, locale_1.t)('(Private Key unchanged)')
                            : '-----BEGIN PRIVATE KEY-----\n[PRIVATE-KEY]\n-----END PRIVATE KEY-----',
                        help: (0, locale_1.tct)('The service account key. Credentials can be managed on the [link].', {
                            link: (<externalLink_1.default href="https://console.cloud.google.com/project/_/iam-admin">
                    IAM &amp; Admin Page
                  </externalLink_1.default>),
                        }),
                    },
                    commonFields.separator,
                    commonFields.prefix,
                    commonFields.layoutType,
                    commonFields.layoutCasing,
                ],
                initialData: !initialData
                    ? undefined
                    : Object.assign(Object.assign({}, initialData), { private_key: undefined }),
            };
        default: {
            Sentry.captureException(new Error('Unknown custom repository type'));
            return {}; // this shall never happen
        }
    }
}
exports.getFormFieldsAndInitialData = getFormFieldsAndInitialData;
function getFinalData(type, data) {
    var _a, _b;
    if (type === debugFiles_1.CustomRepoType.HTTP || type === debugFiles_1.CustomRepoType.APP_STORE_CONNECT) {
        return data;
    }
    switch (type) {
        case 's3':
            return Object.assign(Object.assign({}, data), { secret_key: (_a = data.secret_key) !== null && _a !== void 0 ? _a : {
                    'hidden-secret': true,
                } });
        case 'gcs':
            return Object.assign(Object.assign({}, data), { private_key: (_b = data.private_key) !== null && _b !== void 0 ? _b : {
                    'hidden-secret': true,
                } });
        default: {
            Sentry.captureException(new Error('Unknown custom repository type'));
            return {}; // this shall never happen
        }
    }
}
exports.getFinalData = getFinalData;
//# sourceMappingURL=utils.jsx.map