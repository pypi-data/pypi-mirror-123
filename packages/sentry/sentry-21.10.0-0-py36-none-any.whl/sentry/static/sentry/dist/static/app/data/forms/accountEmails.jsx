Object.defineProperty(exports, "__esModule", { value: true });
exports.route = void 0;
// Export route to make these forms searchable by label/help
exports.route = '/settings/account/emails/';
const formGroups = [
    {
        // Form "section"/"panel"
        title: 'Add Secondary Emails',
        fields: [
            {
                name: 'email',
                type: 'string',
                // additional data/props that is related to rendering of form field rather than data
                label: 'Additional Email',
                placeholder: 'e.g. secondary@example.com',
                help: 'Designate an alternative email for this account',
                showReturnButton: true,
            },
        ],
    },
];
exports.default = formGroups;
//# sourceMappingURL=accountEmails.jsx.map