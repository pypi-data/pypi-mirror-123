Object.defineProperty(exports, "__esModule", { value: true });
exports.fields = exports.route = void 0;
const locale_1 = require("app/locale");
// Export route to make these forms searchable by label/help
exports.route = '/settings/:orgId/projects/:projectId/alerts/';
const formatMinutes = (value) => {
    value = Number(value) / 60;
    return (0, locale_1.tn)('%s minute', '%s minutes', value);
};
exports.fields = {
    subjectTemplate: {
        name: 'subjectTemplate',
        type: 'string',
        // additional data/props that is related to rendering of form field rather than data
        label: (0, locale_1.t)('Subject Template'),
        placeholder: 'e.g. $shortID - $title',
        help: (0, locale_1.t)('The email subject to use (excluding the prefix) for individual alerts. Usable variables include: $title, $shortID, $projectID, $orgID, and ${tag:key}, such as ${tag:environment} or ${tag:release}.'),
    },
    digestsMinDelay: {
        name: 'digestsMinDelay',
        type: 'range',
        min: 60,
        max: 3600,
        step: 60,
        defaultValue: 300,
        label: (0, locale_1.t)('Minimum delivery interval'),
        help: (0, locale_1.t)('Notifications will be delivered at most this often.'),
        formatLabel: formatMinutes,
    },
    digestsMaxDelay: {
        name: 'digestsMaxDelay',
        type: 'range',
        min: 60,
        max: 3600,
        step: 60,
        defaultValue: 300,
        label: (0, locale_1.t)('Maximum delivery interval'),
        help: (0, locale_1.t)('Notifications will be delivered at least this often.'),
        formatLabel: formatMinutes,
    },
};
//# sourceMappingURL=projectAlerts.jsx.map