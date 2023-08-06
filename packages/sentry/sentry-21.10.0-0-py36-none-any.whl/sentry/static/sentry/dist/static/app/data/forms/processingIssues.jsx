Object.defineProperty(exports, "__esModule", { value: true });
exports.route = void 0;
// Export route to make these forms searchable by label/help
const locale_1 = require("app/locale");
exports.route = '/settings/:orgId/projects/:projectId/processing-issues/';
const formGroups = [
    {
        // Form "section"/"panel"
        title: 'Settings',
        fields: [
            {
                name: 'sentry:reprocessing_active',
                type: 'boolean',
                label: (0, locale_1.t)('Reprocessing active'),
                disabled: ({ access }) => !access.has('project:write'),
                disabledReason: (0, locale_1.t)('Only admins may change reprocessing settings'),
                help: (0, locale_1.t)(`If reprocessing is enabled, Events with fixable issues will be
                held back until you resolve them. Processing issues will then
                show up in the list above with hints how to fix them.
                If reprocessing is disabled, Events with unresolved issues will
                also show up in the stream.
                `),
                saveOnBlur: false,
                saveMessage: ({ value }) => value
                    ? (0, locale_1.t)('Reprocessing applies to future events only.')
                    : (0, locale_1.t)(`All events with errors will be flushed into your issues stream.
                Beware that this process may take some time and cannot be undone.`),
                getData: form => ({ options: form }),
            },
        ],
    },
];
exports.default = formGroups;
//# sourceMappingURL=processingIssues.jsx.map