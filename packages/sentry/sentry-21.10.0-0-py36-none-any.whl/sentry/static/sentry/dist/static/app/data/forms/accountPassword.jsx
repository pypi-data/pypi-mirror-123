Object.defineProperty(exports, "__esModule", { value: true });
exports.route = void 0;
const getUserIsNotManaged = ({ user }) => !user.isManaged;
const formGroups = [
    {
        // Form "section"/"panel"
        title: 'Password',
        fields: [
            {
                name: 'password',
                type: 'secret',
                autoComplete: 'current-password',
                label: 'Current Password',
                placeholder: '',
                help: 'Your current password',
                visible: getUserIsNotManaged,
                required: true,
            },
            {
                name: 'passwordNew',
                type: 'secret',
                autoComplete: 'new-password',
                label: 'New Password',
                placeholder: '',
                help: '',
                required: true,
                visible: getUserIsNotManaged,
                validate: ({ id, form }) => (form[id] !== form.passwordVerify ? [[id, '']] : []),
            },
            {
                name: 'passwordVerify',
                type: 'secret',
                autoComplete: 'new-password',
                label: 'Verify New Password',
                placeholder: '',
                help: 'Verify your new password',
                required: true,
                visible: getUserIsNotManaged,
                validate: ({ id, form }) => {
                    // If password is set, and passwords don't match, then return an error
                    if (form.passwordNew && form.passwordNew !== form[id]) {
                        return [[id, 'Passwords do not match']];
                    }
                    return [];
                },
            },
        ],
    },
];
exports.route = '/settings/account/security/';
exports.default = formGroups;
//# sourceMappingURL=accountPassword.jsx.map