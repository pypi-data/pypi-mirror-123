Object.defineProperty(exports, "__esModule", { value: true });
exports.makeDefaultCta = exports.PRESET_AGGREGATES = void 0;
const locale_1 = require("app/locale");
const types_1 = require("app/utils/discover/types");
const tokenizeSearch_1 = require("app/utils/tokenizeSearch");
const utils_1 = require("app/views/alerts/utils");
const getIncidentDiscoverUrl_1 = require("app/views/alerts/utils/getIncidentDiscoverUrl");
const utils_2 = require("app/views/performance/transactionSummary/utils");
const types_2 = require("./types");
exports.PRESET_AGGREGATES = [
    {
        name: (0, locale_1.t)('Error count'),
        match: /^count\(\)/,
        validDataset: [types_2.Dataset.ERRORS],
        default: 'count()',
        /**
         * Simple "Open in Discover" button
         */
        makeCtaParams: makeDefaultCta,
    },
    {
        name: (0, locale_1.t)('Users affected'),
        match: /^count_unique\(tags\[sentry:user\]\)/,
        validDataset: [types_2.Dataset.ERRORS],
        default: 'count_unique(tags[sentry:user])',
        /**
         * Simple "Open in Discover" button
         */
        makeCtaParams: makeDefaultCta,
    },
    {
        name: (0, locale_1.t)('Latency'),
        match: /^(p[0-9]{2,3}|percentile\(transaction\.duration,[^)]+\)|avg\([^)]+\))/,
        validDataset: [types_2.Dataset.TRANSACTIONS],
        default: 'percentile(transaction.duration, 0.95)',
        /**
         * see: makeGenericTransactionCta
         */
        makeCtaParams: opts => makeGenericTransactionCta({
            opts,
            tooltip: (0, locale_1.t)('Latency by Transaction'),
        }),
    },
    {
        name: (0, locale_1.t)('Apdex'),
        match: /^apdex\([0-9.]+\)/,
        validDataset: [types_2.Dataset.TRANSACTIONS],
        default: 'apdex(300)',
        /**
         * see: makeGenericTransactionCta
         */
        makeCtaParams: opts => makeGenericTransactionCta({
            opts,
            tooltip: (0, locale_1.t)('Apdex by Transaction'),
        }),
    },
    {
        name: (0, locale_1.t)('Transaction Count'),
        match: /^count\(\)/,
        validDataset: [types_2.Dataset.TRANSACTIONS],
        default: 'count()',
        /**
         * see: makeGenericTransactionCta
         */
        makeCtaParams: opts => makeGenericTransactionCta({ opts }),
    },
    {
        name: (0, locale_1.t)('Failure rate'),
        match: /^failure_rate\(\)/,
        validDataset: [types_2.Dataset.TRANSACTIONS],
        default: 'failure_rate()',
        /**
         * See makeFailureRateCta
         */
        makeCtaParams: makeFailureRateCta,
    },
];
/**
 * - CASE 1: If has a specific transaction filter
 *   - CTA is: "View Transaction Summary"
 *   - Tooltip is the transaction name
 *   - the same period as the alert graph (i.e. with alert start time in the middle)
 *
 * - CASE 2: If transaction is NOT filtered, or has a * filter:
 *   - "Open in Discover" button with optional tooltip which opens a discover view with...
 *      - fields {transaction, count(), <metric>} sorted by count()
 *      - top-5 activated
 */
function makeGenericTransactionCta(opts) {
    var _a, _b;
    const { opts: { orgSlug, projects, incident, stats }, tooltip, } = opts;
    if (!incident || !stats) {
        return { to: '', buttonText: (0, locale_1.t)('Incident details') };
    }
    const query = new tokenizeSearch_1.MutableSearch((_a = incident.discoverQuery) !== null && _a !== void 0 ? _a : '');
    const transaction = (_b = query
        .getFilterValues('transaction')) === null || _b === void 0 ? void 0 : _b.find(filter => !filter.includes('*'));
    // CASE 1
    if (transaction !== undefined) {
        const period = (0, utils_1.getStartEndFromStats)(stats);
        const summaryUrl = (0, utils_2.transactionSummaryRouteWithQuery)({
            orgSlug,
            transaction,
            projectID: projects
                .filter(({ slug }) => incident.projects.includes(slug))
                .map(({ id }) => id),
            query: Object.assign({}, period),
        });
        return {
            to: summaryUrl,
            buttonText: (0, locale_1.t)('View Transaction Summary'),
            title: transaction,
        };
    }
    // CASE 2
    const extraQueryParams = {
        fields: [...new Set(['transaction', 'count()', incident.alertRule.aggregate])],
        orderby: '-count',
        display: types_1.DisplayModes.TOP5,
    };
    const discoverUrl = (0, getIncidentDiscoverUrl_1.getIncidentDiscoverUrl)({
        orgSlug,
        projects,
        incident,
        stats,
        extraQueryParams,
    });
    return {
        to: discoverUrl,
        buttonText: (0, locale_1.t)('Open in Discover'),
        title: tooltip,
    };
}
/**
 * - CASE 1: Filtered to a specific transaction, "Open in Discover" with...
 *   - fields [transaction.status, count()] sorted by count(),
 *   - "Top 5 period" activated.
 *
 * - CASE 2: If filtered on multiple transactions, "Open in Discover" button
 *   with tooltip "Failure rate by transaction" which opens a discover view
 *   - fields [transaction, failure_rate()] sorted by failure_rate
 *   - top 5 activated
 */
function makeFailureRateCta({ orgSlug, incident, projects, stats }) {
    var _a, _b;
    if (!incident || !stats) {
        return { to: '', buttonText: (0, locale_1.t)('Incident details') };
    }
    const query = new tokenizeSearch_1.MutableSearch((_a = incident.discoverQuery) !== null && _a !== void 0 ? _a : '');
    const transaction = (_b = query
        .getFilterValues('transaction')) === null || _b === void 0 ? void 0 : _b.find(filter => !filter.includes('*'));
    const extraQueryParams = transaction !== undefined
        ? // CASE 1
            {
                fields: ['transaction.status', 'count()'],
                orderby: '-count',
                display: types_1.DisplayModes.TOP5,
            }
        : // Case 2
            {
                fields: ['transaction', 'failure_rate()'],
                orderby: '-failure_rate',
                display: types_1.DisplayModes.TOP5,
            };
    const discoverUrl = (0, getIncidentDiscoverUrl_1.getIncidentDiscoverUrl)({
        orgSlug,
        projects,
        incident,
        stats,
        extraQueryParams,
    });
    return {
        to: discoverUrl,
        buttonText: (0, locale_1.t)('Open in Discover'),
        title: transaction === undefined ? (0, locale_1.t)('Failure rate by transaction') : undefined,
    };
}
/**
 * Get the CTA used for alerts that do not have a preset
 */
function makeDefaultCta({ orgSlug, projects, incident, stats, }) {
    if (!incident) {
        return {
            buttonText: (0, locale_1.t)('Open in Discover'),
            to: '',
        };
    }
    const extraQueryParams = {
        display: types_1.DisplayModes.TOP5,
    };
    return {
        buttonText: (0, locale_1.t)('Open in Discover'),
        to: (0, getIncidentDiscoverUrl_1.getIncidentDiscoverUrl)({ orgSlug, projects, incident, stats, extraQueryParams }),
    };
}
exports.makeDefaultCta = makeDefaultCta;
//# sourceMappingURL=presets.jsx.map