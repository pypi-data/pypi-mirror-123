Object.defineProperty(exports, "__esModule", { value: true });
exports.route = void 0;
const tslib_1 = require("tslib");
const locale_1 = require("app/locale");
const slugify_1 = (0, tslib_1.__importDefault)(require("app/utils/slugify"));
// Export route to make these forms searchable by label/help
exports.route = '/settings/:orgId/teams/:teamId/settings/';
const formGroups = [
    {
        // Form "section"/"panel"
        title: 'Team Settings',
        fields: [
            {
                name: 'slug',
                type: 'string',
                required: true,
                label: (0, locale_1.t)('Name'),
                placeholder: 'e.g. api-team',
                help: (0, locale_1.t)('A unique ID used to identify the team'),
                disabled: ({ access }) => !access.has('team:write'),
                transformInput: slugify_1.default,
                saveOnBlur: false,
                saveMessageAlertType: 'info',
                saveMessage: (0, locale_1.t)('You will be redirected to the new team slug after saving'),
            },
        ],
    },
];
exports.default = formGroups;
//# sourceMappingURL=teamSettingsFields.jsx.map