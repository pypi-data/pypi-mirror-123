Object.defineProperty(exports, "__esModule", { value: true });
exports.COMPARISON_INTERVAL_CHOICES = exports.COMPARISON_TYPE_CHOICES = exports.COMPARISON_TYPE_CHOICE_VALUES = exports.CHANGE_ALERT_PLACEHOLDERS_LABELS = exports.CHANGE_ALERT_CONDITION_IDS = void 0;
exports.CHANGE_ALERT_CONDITION_IDS = [
    'sentry.rules.conditions.event_frequency.EventFrequencyCondition',
    'sentry.rules.conditions.event_frequency.EventUniqueUserFrequencyCondition',
    'sentry.rules.conditions.event_frequency.EventFrequencyPercentCondition',
];
exports.CHANGE_ALERT_PLACEHOLDERS_LABELS = {
    'sentry.rules.conditions.event_frequency.EventFrequencyCondition': 'Number of errors in an issue is...',
    'sentry.rules.conditions.event_frequency.EventUniqueUserFrequencyCondition': 'Number of users affected by an issue is...',
    'sentry.rules.conditions.event_frequency.EventFrequencyPercentCondition': 'Percent of sessions affected by an issue is...',
};
exports.COMPARISON_TYPE_CHOICE_VALUES = {
    count: 'more than {value} in {interval}',
    percent: '{value}% higher in {interval} compared to {comparisonInterval} ago',
};
exports.COMPARISON_TYPE_CHOICES = [
    ['count', exports.COMPARISON_TYPE_CHOICE_VALUES.count],
    ['percent', exports.COMPARISON_TYPE_CHOICE_VALUES.percent],
];
exports.COMPARISON_INTERVAL_CHOICES = [
    ['5m', '5 minutes'],
    ['15m', '15 minutes'],
    ['1h', 'one hour'],
    ['1d', 'one day'],
    ['1w', 'one week'],
    ['30d', '30 days'],
];
//# sourceMappingURL=changeAlerts.jsx.map