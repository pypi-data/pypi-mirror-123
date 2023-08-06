Object.defineProperty(exports, "__esModule", { value: true });
exports.route = void 0;
const tslib_1 = require("tslib");
const locale_1 = require("app/locale");
const slugify_1 = (0, tslib_1.__importDefault)(require("app/utils/slugify"));
// Export route to make these forms searchable by label/help
exports.route = '/settings/:orgId/';
const formGroups = [
    {
        // Form "section"/"panel"
        title: (0, locale_1.t)('General'),
        fields: [
            {
                name: 'slug',
                type: 'string',
                required: true,
                label: (0, locale_1.t)('Organization Slug'),
                help: (0, locale_1.t)('A unique ID used to identify this organization'),
                transformInput: slugify_1.default,
                saveOnBlur: false,
                saveMessageAlertType: 'info',
                saveMessage: (0, locale_1.t)('You will be redirected to the new organization slug after saving'),
            },
            {
                name: 'name',
                type: 'string',
                required: true,
                label: (0, locale_1.t)('Display Name'),
                help: (0, locale_1.t)('A human-friendly name for the organization'),
            },
            {
                name: 'isEarlyAdopter',
                type: 'boolean',
                label: (0, locale_1.t)('Early Adopter'),
                help: (0, locale_1.t)("Opt-in to new features before they're released to the public"),
            },
        ],
    },
    {
        title: 'Membership',
        fields: [
            {
                name: 'defaultRole',
                type: 'select',
                required: true,
                label: (0, locale_1.t)('Default Role'),
                // seems weird to have choices in initial form data
                choices: ({ initialData } = {}) => { var _a, _b; return (_b = (_a = initialData === null || initialData === void 0 ? void 0 : initialData.availableRoles) === null || _a === void 0 ? void 0 : _a.map((r) => [r.id, r.name])) !== null && _b !== void 0 ? _b : []; },
                help: (0, locale_1.t)('The default role new members will receive'),
                disabled: ({ access }) => !access.has('org:admin'),
            },
            {
                name: 'openMembership',
                type: 'boolean',
                required: true,
                label: (0, locale_1.t)('Open Membership'),
                help: (0, locale_1.t)('Allow organization members to freely join or leave any team'),
            },
            {
                name: 'eventsMemberAdmin',
                type: 'boolean',
                label: (0, locale_1.t)('Let Members Delete Events'),
                help: (0, locale_1.t)('Allow members to delete events (including the delete & discard action) by granting them the `event:admin` scope.'),
            },
            {
                name: 'alertsMemberWrite',
                type: 'boolean',
                label: (0, locale_1.t)('Let Members Create and Edit Alerts'),
                help: (0, locale_1.t)('Allow members to create, edit, and delete alert rules by granting them the `alerts:write` scope.'),
            },
            {
                name: 'attachmentsRole',
                type: 'select',
                choices: ({ initialData = {} }) => { var _a, _b; return (_b = (_a = initialData === null || initialData === void 0 ? void 0 : initialData.availableRoles) === null || _a === void 0 ? void 0 : _a.map((r) => [r.id, r.name])) !== null && _b !== void 0 ? _b : []; },
                label: (0, locale_1.t)('Attachments Access'),
                help: (0, locale_1.t)('Role required to download event attachments, such as native crash reports or log files.'),
                visible: ({ features }) => features.has('event-attachments'),
            },
            {
                name: 'debugFilesRole',
                type: 'select',
                choices: ({ initialData = {} }) => { var _a, _b; return (_b = (_a = initialData === null || initialData === void 0 ? void 0 : initialData.availableRoles) === null || _a === void 0 ? void 0 : _a.map((r) => [r.id, r.name])) !== null && _b !== void 0 ? _b : []; },
                label: (0, locale_1.t)('Debug Files Access'),
                help: (0, locale_1.t)('Role required to download debug information files, proguard mappings and source maps.'),
            },
        ],
    },
];
exports.default = formGroups;
//# sourceMappingURL=organizationGeneralSettings.jsx.map