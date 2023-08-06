Object.defineProperty(exports, "__esModule", { value: true });
exports.getAlertTypeFromAggregateDataset = void 0;
const types_1 = require("app/views/alerts/incidentRules/types");
// A set of unique identifiers to be able to tie aggregate and dataset back to a wizard alert type
const alertTypeIdentifiers = {
    [types_1.Dataset.ERRORS]: {
        num_errors: 'count()',
        users_experiencing_errors: 'count_unique(tags[sentry:user])',
    },
    [types_1.Dataset.TRANSACTIONS]: {
        throughput: 'count()',
        trans_duration: 'transaction.duration',
        apdex: 'apdex',
        failure_rate: 'failure_rate()',
        lcp: 'measurements.lcp',
        fid: 'measurements.fid',
        cls: 'measurements.cls',
    },
    [types_1.Dataset.SESSIONS]: {
        crash_free_sessions: types_1.SessionsAggregate.CRASH_FREE_SESSIONS,
        crash_free_users: types_1.SessionsAggregate.CRASH_FREE_USERS,
    },
};
/**
 * Given an aggregate and dataset object, will return the corresponding wizard alert type
 * e.g. {aggregate: 'count()', dataset: 'events'} will yield 'num_errors'
 * @param template
 */
function getAlertTypeFromAggregateDataset({ aggregate, dataset, }) {
    const identifierForDataset = alertTypeIdentifiers[dataset];
    const matchingAlertTypeEntry = Object.entries(identifierForDataset).find(([_alertType, identifier]) => identifier && aggregate.includes(identifier));
    const alertType = matchingAlertTypeEntry && matchingAlertTypeEntry[0];
    return alertType ? alertType : 'custom';
}
exports.getAlertTypeFromAggregateDataset = getAlertTypeFromAggregateDataset;
//# sourceMappingURL=utils.jsx.map