Object.defineProperty(exports, "__esModule", { value: true });
exports.ACCOUNT_NOTIFICATION_FIELDS = void 0;
const locale_1 = require("app/locale");
exports.ACCOUNT_NOTIFICATION_FIELDS = {
    alerts: {
        title: 'Project Alerts',
        description: (0, locale_1.t)('Notifications from Alert Rules that your team has setup. You’ll always receive notifications from Alerts configured to be sent directly to you.'),
        type: 'select',
        options: [
            { value: '-1', label: (0, locale_1.t)('Default') },
            { value: '1', label: (0, locale_1.t)('On') },
            { value: '0', label: (0, locale_1.t)('Off') },
        ],
        defaultValue: '-1',
        defaultFieldName: 'subscribeByDefault',
    },
    workflow: {
        title: 'Workflow Notifications',
        description: (0, locale_1.t)('Control workflow notifications, e.g. changes in issue assignment, resolution status, and comments.'),
        type: 'select',
        options: [
            { value: '-1', label: (0, locale_1.t)('Default') },
            { value: '0', label: (0, locale_1.t)('Always') },
            { value: '1', label: (0, locale_1.t)('Only on issues I subscribe to') },
            { value: '2', label: (0, locale_1.t)('Never') },
        ],
        defaultValue: '-1',
        defaultFieldName: 'workflowNotifications',
    },
    deploy: {
        title: (0, locale_1.t)('Deploy Notifications'),
        description: (0, locale_1.t)('Control deploy notifications that include release, environment, and commit overviews.'),
        type: 'select',
        options: [
            { value: '-1', label: (0, locale_1.t)('Default') },
            { value: '2', label: (0, locale_1.t)('Always') },
            { value: '3', label: (0, locale_1.t)('Only on deploys with my commits') },
            { value: '4', label: (0, locale_1.t)('Never') },
        ],
        defaultValue: '-1',
        defaultFieldName: 'deployNotifications',
    },
    reports: {
        title: (0, locale_1.t)('Weekly Reports'),
        description: (0, locale_1.t)("Reports contain a summary of what's happened within the organization."),
        type: 'select',
        // API only saves organizations that have this disabled, so we should default to "On"
        defaultValue: '1',
        options: [
            { value: '1', label: (0, locale_1.t)('On') },
            { value: '0', label: (0, locale_1.t)('Off') },
        ],
        defaultFieldName: 'weeklyReports',
    },
    email: {
        title: (0, locale_1.t)('Email Routing'),
        description: (0, locale_1.t)('On a per project basis, route emails to an alternative email address.'),
        type: 'select',
        // No choices here because it's going to have dynamic content
        // Component will create choices
    },
};
//# sourceMappingURL=fields.jsx.map