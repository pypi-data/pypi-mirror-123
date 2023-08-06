Object.defineProperty(exports, "__esModule", { value: true });
exports.NOTIFICATION_SETTING_FIELDS = void 0;
const locale_1 = require("app/locale");
exports.NOTIFICATION_SETTING_FIELDS = {
    alerts: {
        name: 'alerts',
        type: 'select',
        label: (0, locale_1.t)('Issue Alerts'),
        choices: [
            ['always', (0, locale_1.t)('On')],
            ['never', (0, locale_1.t)('Off')],
        ],
        help: (0, locale_1.t)('Notifications sent from Alert rules that your team has set up.'),
    },
    workflow: {
        name: 'workflow',
        type: 'select',
        label: (0, locale_1.t)('Issue Workflow'),
        choices: [
            ['always', (0, locale_1.t)('On')],
            ['subscribe_only', (0, locale_1.t)('Only Subscribed Issues')],
            ['never', (0, locale_1.t)('Off')],
        ],
        help: (0, locale_1.t)('Changes in issue assignment, resolution status, and comments.'),
    },
    deploy: {
        name: 'deploy',
        type: 'select',
        label: (0, locale_1.t)('Deploys'),
        choices: [
            ['always', (0, locale_1.t)('On')],
            ['committed_only', (0, locale_1.t)('Only Committed Issues')],
            ['never', (0, locale_1.t)('Off')],
        ],
        help: (0, locale_1.t)('Release, environment, and commit overviews.'),
    },
    provider: {
        name: 'provider',
        type: 'select',
        label: (0, locale_1.t)('Delivery Method'),
        choices: [
            ['email', (0, locale_1.t)('Send to Email')],
            ['slack', (0, locale_1.t)('Send to Slack')],
            ['email+slack', (0, locale_1.t)('Send to Email and Slack')],
        ],
    },
    reports: {
        name: 'weekly reports',
        type: 'blank',
        label: (0, locale_1.t)('Weekly Reports'),
        help: (0, locale_1.t)('A summary of the past week for an organization.'),
    },
    email: {
        name: 'email routing',
        type: 'blank',
        label: (0, locale_1.t)('Email Routing'),
        help: (0, locale_1.t)('Change the email address that receives notifications.'),
    },
    personalActivityNotifications: {
        name: 'personalActivityNotifications',
        type: 'boolean',
        label: (0, locale_1.t)('My Own Activity'),
        help: (0, locale_1.t)('Notifications about your own actions on Sentry.'),
    },
    selfAssignOnResolve: {
        name: 'selfAssignOnResolve',
        type: 'boolean',
        label: (0, locale_1.t)('Claim Unassigned Issues I’ve Resolved'),
        help: (0, locale_1.t)('You’ll receive notifications about any changes that happen afterwards.'),
    },
};
//# sourceMappingURL=fields2.jsx.map