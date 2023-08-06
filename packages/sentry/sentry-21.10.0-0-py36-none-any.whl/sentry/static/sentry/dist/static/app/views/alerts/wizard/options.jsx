Object.defineProperty(exports, "__esModule", { value: true });
exports.getFunctionHelpText = exports.hideParameterSelectorSet = exports.hidePrimarySelectorSet = exports.AlertWizardRuleTemplates = exports.AlertWizardPanelContent = exports.getAlertWizardCategories = exports.AlertWizardAlertNames = exports.WebVitalAlertTypes = void 0;
const tslib_1 = require("tslib");
const alerts_wizard_apdex_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/spot/alerts-wizard-apdex.svg"));
const alerts_wizard_cls_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/spot/alerts-wizard-cls.svg"));
const alerts_wizard_crash_free_sessions_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/spot/alerts-wizard-crash-free-sessions.svg"));
const alerts_wizard_crash_free_users_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/spot/alerts-wizard-crash-free-users.svg"));
const alerts_wizard_custom_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/spot/alerts-wizard-custom.svg"));
const alerts_wizard_errors_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/spot/alerts-wizard-errors.svg"));
const alerts_wizard_failure_rate_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/spot/alerts-wizard-failure-rate.svg"));
const alerts_wizard_fid_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/spot/alerts-wizard-fid.svg"));
const alerts_wizard_issues_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/spot/alerts-wizard-issues.svg"));
const alerts_wizard_lcp_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/spot/alerts-wizard-lcp.svg"));
const alerts_wizard_throughput_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/spot/alerts-wizard-throughput.svg"));
const alerts_wizard_transaction_duration_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/spot/alerts-wizard-transaction-duration.svg"));
const alerts_wizard_users_experiencing_errors_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/spot/alerts-wizard-users-experiencing-errors.svg"));
const locale_1 = require("app/locale");
const types_1 = require("app/views/alerts/incidentRules/types");
exports.WebVitalAlertTypes = new Set(['lcp', 'fid', 'cls', 'fcp']);
exports.AlertWizardAlertNames = {
    issues: (0, locale_1.t)('Issues'),
    num_errors: (0, locale_1.t)('Number of Errors'),
    users_experiencing_errors: (0, locale_1.t)('Users Experiencing Errors'),
    throughput: (0, locale_1.t)('Throughput'),
    trans_duration: (0, locale_1.t)('Transaction Duration'),
    apdex: (0, locale_1.t)('Apdex'),
    failure_rate: (0, locale_1.t)('Failure Rate'),
    lcp: (0, locale_1.t)('Largest Contentful Paint'),
    fid: (0, locale_1.t)('First Input Delay'),
    cls: (0, locale_1.t)('Cumulative Layout Shift'),
    custom: (0, locale_1.t)('Custom Metric'),
    crash_free_sessions: (0, locale_1.t)('Crash Free Session Rate'),
    crash_free_users: (0, locale_1.t)('Crash Free User Rate'),
};
const getAlertWizardCategories = (org) => [
    {
        categoryHeading: (0, locale_1.t)('Errors'),
        options: ['issues', 'num_errors', 'users_experiencing_errors'],
    },
    ...(org.features.includes('crash-rate-alerts')
        ? [
            {
                categoryHeading: (0, locale_1.t)('Sessions'),
                options: ['crash_free_sessions', 'crash_free_users'],
            },
        ]
        : []),
    {
        categoryHeading: (0, locale_1.t)('Performance'),
        options: [
            'throughput',
            'trans_duration',
            'apdex',
            'failure_rate',
            'lcp',
            'fid',
            'cls',
        ],
    },
    {
        categoryHeading: (0, locale_1.t)('Other'),
        options: ['custom'],
    },
];
exports.getAlertWizardCategories = getAlertWizardCategories;
exports.AlertWizardPanelContent = {
    issues: {
        description: (0, locale_1.t)('Issues are groups of errors that have a similar stacktrace. Set an alert for new issues, when an issue changes state, frequency of errors, or users affected by an issue.'),
        examples: [
            (0, locale_1.t)("When the triggering event's level is fatal."),
            (0, locale_1.t)('When an issue was seen 100 times in the last 2 days.'),
            (0, locale_1.t)('Create a JIRA ticket when an issue changes state from resolved to unresolved and is unassigned.'),
        ],
        illustration: alerts_wizard_issues_svg_1.default,
    },
    num_errors: {
        description: (0, locale_1.t)('Alert when the number of errors in a project matching your filters crosses a threshold. This is useful for monitoring the overall level or errors in your project or errors occurring in specific parts of your app.'),
        examples: [
            (0, locale_1.t)('When the signup page has more than 10k errors in 5 minutes.'),
            (0, locale_1.t)('When there are more than 500k errors in 10 minutes from a specific file.'),
        ],
        illustration: alerts_wizard_errors_svg_1.default,
    },
    users_experiencing_errors: {
        description: (0, locale_1.t)('Alert when the number of users affected by errors in your project crosses a threshold.'),
        examples: [
            (0, locale_1.t)('When 100k users experience an error in 1 hour.'),
            (0, locale_1.t)('When 100 users experience a problem on the Checkout page.'),
        ],
        illustration: alerts_wizard_users_experiencing_errors_svg_1.default,
    },
    throughput: {
        description: (0, locale_1.t)('Throughput is the total number of transactions in a project and you can alert when it reaches a threshold within a period of time.'),
        examples: [
            (0, locale_1.t)('When number of transactions on a key page exceeds 100k per minute.'),
            (0, locale_1.t)('When number of transactions drops below a threshold.'),
        ],
        illustration: alerts_wizard_throughput_svg_1.default,
    },
    trans_duration: {
        description: (0, locale_1.t)('Monitor how long it takes for transactions to complete. Use flexible aggregates like percentiles, averages, and min/max.'),
        examples: [
            (0, locale_1.t)('When any transaction is slower than 3 seconds.'),
            (0, locale_1.t)('When the 75th percentile response time is higher than 250 milliseconds.'),
        ],
        illustration: alerts_wizard_transaction_duration_svg_1.default,
    },
    apdex: {
        description: (0, locale_1.t)('Apdex is a metric used to track and measure user satisfaction based on your application response times. The Apdex score provides the ratio of satisfactory, tolerable, and frustrated requests in a specific transaction or endpoint.'),
        examples: [(0, locale_1.t)('When apdex is below 300.')],
        docsLink: 'https://docs.sentry.io/product/performance/metrics/#apdex',
        illustration: alerts_wizard_apdex_svg_1.default,
    },
    failure_rate: {
        description: (0, locale_1.t)('Failure rate is the percentage of unsuccessful transactions. Sentry treats transactions with a status other than “ok,” “canceled,” and “unknown” as failures.'),
        examples: [(0, locale_1.t)('When the failure rate for an important endpoint reaches 10%.')],
        docsLink: 'https://docs.sentry.io/product/performance/metrics/#failure-rate',
        illustration: alerts_wizard_failure_rate_svg_1.default,
    },
    lcp: {
        description: (0, locale_1.t)('Largest Contentful Paint (LCP) measures loading performance. It marks the point when the largest image or text block is visible within the viewport. A fast LCP helps reassure the user that the page is useful, and so we recommend an LCP of less than 2.5 seconds.'),
        examples: [
            (0, locale_1.t)('When the 75th percentile LCP of your homepage is longer than 2.5 seconds.'),
        ],
        docsLink: 'https://docs.sentry.io/product/performance/web-vitals',
        illustration: alerts_wizard_lcp_svg_1.default,
    },
    fid: {
        description: (0, locale_1.t)('First Input Delay (FID) measures interactivity as the response time when the user tries to interact with the viewport. A low FID helps ensure that a page is useful, and we recommend a FID of less than 100 milliseconds.'),
        examples: [(0, locale_1.t)('When the average FID of a page is longer than 4 seconds.')],
        docsLink: 'https://docs.sentry.io/product/performance/web-vitals',
        illustration: alerts_wizard_fid_svg_1.default,
    },
    cls: {
        description: (0, locale_1.t)('Cumulative Layout Shift (CLS) measures visual stability by quantifying unexpected layout shifts that occur during the entire lifespan of the page. A CLS of less than 0.1 is a good user experience, while anything greater than 0.25 is poor.'),
        examples: [(0, locale_1.t)('When the CLS of a page is more than 0.5.')],
        docsLink: 'https://docs.sentry.io/product/performance/web-vitals',
        illustration: alerts_wizard_cls_svg_1.default,
    },
    custom: {
        description: (0, locale_1.t)('Alert on metrics which are not listed above, such as first paint (FP), first contentful paint (FCP), and time to first byte (TTFB).'),
        examples: [
            (0, locale_1.t)('When the 95th percentile FP of a page is longer than 250 milliseconds.'),
            (0, locale_1.t)('When the average TTFB of a page is longer than 600 millliseconds.'),
        ],
        illustration: alerts_wizard_custom_svg_1.default,
    },
    crash_free_sessions: {
        description: (0, locale_1.t)('A session begins when a user starts the application and ends when it’s closed or sent to the background. A crash is when a session ends due to an error and this type of alert lets you monitor when those crashed sessions exceed a threshold. This lets you get a better picture of the health of your app.'),
        examples: [
            (0, locale_1.t)('When the Crash Free Rate is below 98%, send a Slack notification to the team.'),
        ],
        illustration: alerts_wizard_crash_free_sessions_svg_1.default,
    },
    crash_free_users: {
        description: (0, locale_1.t)('Crash Free Users is the percentage of distinct users that haven’t experienced a crash and so this type of alert tells you when the overall user experience dips below a certain unacceptable threshold.'),
        examples: [
            (0, locale_1.t)('When the Crash Free Rate is below 97%, send an email notification to yourself.'),
        ],
        illustration: alerts_wizard_crash_free_users_svg_1.default,
    },
};
exports.AlertWizardRuleTemplates = {
    num_errors: {
        aggregate: 'count()',
        dataset: types_1.Dataset.ERRORS,
        eventTypes: types_1.EventTypes.ERROR,
    },
    users_experiencing_errors: {
        aggregate: 'count_unique(tags[sentry:user])',
        dataset: types_1.Dataset.ERRORS,
        eventTypes: types_1.EventTypes.ERROR,
    },
    throughput: {
        aggregate: 'count()',
        dataset: types_1.Dataset.TRANSACTIONS,
        eventTypes: types_1.EventTypes.TRANSACTION,
    },
    trans_duration: {
        aggregate: 'p95(transaction.duration)',
        dataset: types_1.Dataset.TRANSACTIONS,
        eventTypes: types_1.EventTypes.TRANSACTION,
    },
    apdex: {
        aggregate: 'apdex(300)',
        dataset: types_1.Dataset.TRANSACTIONS,
        eventTypes: types_1.EventTypes.TRANSACTION,
    },
    failure_rate: {
        aggregate: 'failure_rate()',
        dataset: types_1.Dataset.TRANSACTIONS,
        eventTypes: types_1.EventTypes.TRANSACTION,
    },
    lcp: {
        aggregate: 'p95(measurements.lcp)',
        dataset: types_1.Dataset.TRANSACTIONS,
        eventTypes: types_1.EventTypes.TRANSACTION,
    },
    fid: {
        aggregate: 'p95(measurements.fid)',
        dataset: types_1.Dataset.TRANSACTIONS,
        eventTypes: types_1.EventTypes.TRANSACTION,
    },
    cls: {
        aggregate: 'p95(measurements.cls)',
        dataset: types_1.Dataset.TRANSACTIONS,
        eventTypes: types_1.EventTypes.TRANSACTION,
    },
    custom: {
        aggregate: 'p95(measurements.fp)',
        dataset: types_1.Dataset.TRANSACTIONS,
        eventTypes: types_1.EventTypes.TRANSACTION,
    },
    crash_free_sessions: {
        aggregate: types_1.SessionsAggregate.CRASH_FREE_SESSIONS,
        dataset: types_1.Dataset.SESSIONS,
        eventTypes: types_1.EventTypes.SESSION,
    },
    crash_free_users: {
        aggregate: types_1.SessionsAggregate.CRASH_FREE_USERS,
        dataset: types_1.Dataset.SESSIONS,
        eventTypes: types_1.EventTypes.USER,
    },
};
exports.hidePrimarySelectorSet = new Set([
    'num_errors',
    'users_experiencing_errors',
    'throughput',
    'apdex',
    'failure_rate',
    'crash_free_sessions',
    'crash_free_users',
]);
exports.hideParameterSelectorSet = new Set([
    'trans_duration',
    'lcp',
    'fid',
    'cls',
]);
function getFunctionHelpText(alertType) {
    const timeWindowText = (0, locale_1.t)('over');
    if (alertType === 'apdex') {
        return {
            labelText: (0, locale_1.t)('Select apdex value and time interval'),
            timeWindowText,
        };
    }
    else if (exports.hidePrimarySelectorSet.has(alertType)) {
        return {
            labelText: (0, locale_1.t)('Select time interval'),
        };
    }
    else {
        return {
            labelText: (0, locale_1.t)('Select function and time interval'),
            timeWindowText,
        };
    }
}
exports.getFunctionHelpText = getFunctionHelpText;
//# sourceMappingURL=options.jsx.map