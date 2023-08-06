Object.defineProperty(exports, "__esModule", { value: true });
exports.fields = exports.route = void 0;
const locale_1 = require("app/locale");
// Export route to make these forms searchable by label/help
exports.route = '/settings/account/notifications/';
exports.fields = {
    subscribeByDefault: {
        name: 'subscribeByDefault',
        type: 'boolean',
        label: (0, locale_1.t)('Send Me Alerts'),
        // TODO(billy): Make this a real link
        help: (0, locale_1.t)('Enable this to receive notifications for Alerts sent to your teams. You will always receive alerts configured to be sent directly to you.'),
    },
    workflowNotifications: {
        name: 'workflowNotifications',
        type: 'radio',
        label: (0, locale_1.t)('Send Me Workflow Notifications'),
        choices: [
            [0, (0, locale_1.t)('Always')],
            [1, (0, locale_1.t)('Only On Issues I Subscribe To')],
            [2, (0, locale_1.t)('Never')],
        ],
        help: (0, locale_1.t)('E.g. changes in issue assignment, resolution status, and comments.'),
    },
    weeklyReports: {
        // Form is not visible because currently not implemented
        name: 'weeklyReports',
        type: 'boolean',
        label: (0, locale_1.t)('Send Me Weekly Reports'),
        help: (0, locale_1.t)("Reports contain a summary of what's happened within your organization."),
        disabled: true,
    },
    deployNotifications: {
        name: 'deployNotifications',
        type: 'radio',
        label: (0, locale_1.t)('Send Me Deploy Notifications'),
        choices: [
            [2, (0, locale_1.t)('Always')],
            [3, (0, locale_1.t)('Only On Deploys With My Commits')],
            [4, (0, locale_1.t)('Never')],
        ],
        help: (0, locale_1.t)('Deploy emails include release, environment and commit overviews.'),
    },
    personalActivityNotifications: {
        name: 'personalActivityNotifications',
        type: 'boolean',
        label: (0, locale_1.t)('Notify Me About My Own Activity'),
        help: (0, locale_1.t)('Enable this to receive notifications about your own actions on Sentry.'),
    },
    selfAssignOnResolve: {
        name: 'selfAssignOnResolve',
        type: 'boolean',
        label: (0, locale_1.t)("Claim Unassigned Issues I've Resolved"),
        help: (0, locale_1.t)("You'll receive notifications about any changes that happen afterwards."),
    },
};
const formGroups = [
    {
        title: (0, locale_1.t)('Alerts'),
        fields: [exports.fields.subscribeByDefault],
    },
    {
        title: (0, locale_1.t)('Workflow Notifications'),
        fields: [exports.fields.workflowNotifications],
    },
    {
        title: (0, locale_1.t)('Email Routing'),
        fields: [],
    },
    {
        title: (0, locale_1.t)('Weekly Reports'),
        fields: [],
    },
    {
        title: (0, locale_1.t)('Deploy Notifications'),
        fields: [exports.fields.deployNotifications],
    },
    {
        title: (0, locale_1.t)('My Activity'),
        fields: [exports.fields.personalActivityNotifications, exports.fields.selfAssignOnResolve],
    },
];
exports.default = formGroups;
//# sourceMappingURL=accountNotificationSettings.jsx.map