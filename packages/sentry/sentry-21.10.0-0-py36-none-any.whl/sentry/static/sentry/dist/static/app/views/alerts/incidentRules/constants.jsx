Object.defineProperty(exports, "__esModule", { value: true });
exports.createRuleFromWizardTemplate = exports.createRuleFromEventView = exports.createDefaultRule = exports.createDefaultTrigger = exports.transactionFieldConfig = exports.wizardAlertFieldConfig = exports.getWizardAlertFieldConfig = exports.COMPARISON_DELTA_OPTIONS = exports.errorFieldConfig = exports.DATASOURCE_EVENT_TYPE_FILTERS = exports.DATASET_EVENT_TYPE_FILTERS = exports.DEFAULT_TRANSACTION_AGGREGATE = exports.DEFAULT_AGGREGATE = void 0;
const locale_1 = require("app/locale");
const constants_1 = require("app/utils/performance/vitals/constants");
const types_1 = require("app/views/alerts/incidentRules/types");
const utils_1 = require("app/views/alerts/utils");
exports.DEFAULT_AGGREGATE = 'count()';
exports.DEFAULT_TRANSACTION_AGGREGATE = 'p95(transaction.duration)';
exports.DATASET_EVENT_TYPE_FILTERS = {
    [types_1.Dataset.ERRORS]: 'event.type:error',
    [types_1.Dataset.TRANSACTIONS]: 'event.type:transaction',
};
exports.DATASOURCE_EVENT_TYPE_FILTERS = {
    [types_1.Datasource.ERROR_DEFAULT]: '(event.type:error OR event.type:default)',
    [types_1.Datasource.ERROR]: 'event.type:error',
    [types_1.Datasource.DEFAULT]: 'event.type:default',
    [types_1.Datasource.TRANSACTION]: 'event.type:transaction',
};
/**
 * Allowed error aggregations for alerts
 */
exports.errorFieldConfig = {
    aggregations: ['count', 'count_unique'],
    fields: ['user'],
};
const commonAggregations = [
    'avg',
    'percentile',
    'p50',
    'p75',
    'p95',
    'p99',
    'p100',
];
const allAggregations = [
    ...commonAggregations,
    'failure_rate',
    'apdex',
    'count',
];
exports.COMPARISON_DELTA_OPTIONS = [
    { value: 5, label: (0, locale_1.t)('same time 5 minutes ago') },
    { value: 15, label: (0, locale_1.t)('same time 15 minutes ago') },
    { value: 60, label: (0, locale_1.t)('same time one hour ago') },
    { value: 1440, label: (0, locale_1.t)('same time one day ago') },
    { value: 10080, label: (0, locale_1.t)('same time one week ago') },
    { value: 43200, label: (0, locale_1.t)('same time one month ago') }, // 30 days
];
function getWizardAlertFieldConfig(alertType, dataset) {
    if (alertType === 'custom' && dataset === types_1.Dataset.ERRORS) {
        return exports.errorFieldConfig;
    }
    // If user selected apdex we must include that in the OptionConfig as it has a user specified column
    const aggregations = alertType === 'apdex' || alertType === 'custom'
        ? allAggregations
        : commonAggregations;
    return {
        aggregations,
        fields: ['transaction.duration'],
        measurementKeys: Object.keys(constants_1.WEB_VITAL_DETAILS),
    };
}
exports.getWizardAlertFieldConfig = getWizardAlertFieldConfig;
/**
 * Allowed aggregations for alerts created from wizard
 */
exports.wizardAlertFieldConfig = {
    aggregations: commonAggregations,
    fields: ['transaction.duration'],
    measurementKeys: Object.keys(constants_1.WEB_VITAL_DETAILS),
};
/**
 * Allowed transaction aggregations for alerts
 */
exports.transactionFieldConfig = {
    aggregations: allAggregations,
    fields: ['transaction.duration'],
    measurementKeys: Object.keys(constants_1.WEB_VITAL_DETAILS),
};
function createDefaultTrigger(label) {
    return {
        label,
        alertThreshold: '',
        actions: [],
    };
}
exports.createDefaultTrigger = createDefaultTrigger;
function createDefaultRule(defaultRuleOptions = {}) {
    return Object.assign({ dataset: types_1.Dataset.ERRORS, eventTypes: [types_1.EventTypes.ERROR], aggregate: exports.DEFAULT_AGGREGATE, query: '', timeWindow: 1, triggers: [createDefaultTrigger('critical'), createDefaultTrigger('warning')], projects: [], environment: null, resolveThreshold: '', thresholdType: types_1.AlertRuleThresholdType.ABOVE }, defaultRuleOptions);
}
exports.createDefaultRule = createDefaultRule;
/**
 * Create an unsaved alert from a discover EventView object
 */
function createRuleFromEventView(eventView) {
    var _a;
    const parsedQuery = (0, utils_1.getQueryDatasource)(eventView.query);
    const datasetAndEventtypes = parsedQuery
        ? utils_1.DATA_SOURCE_TO_SET_AND_EVENT_TYPES[parsedQuery.source]
        : utils_1.DATA_SOURCE_TO_SET_AND_EVENT_TYPES.error;
    return Object.assign(Object.assign(Object.assign({}, createDefaultRule()), datasetAndEventtypes), { query: (_a = parsedQuery === null || parsedQuery === void 0 ? void 0 : parsedQuery.query) !== null && _a !== void 0 ? _a : eventView.query, 
        // If creating a metric alert for transactions, default to the p95 metric
        aggregate: datasetAndEventtypes.dataset === 'transactions'
            ? 'p95(transaction.duration)'
            : eventView.getYAxis(), environment: eventView.environment.length ? eventView.environment[0] : null });
}
exports.createRuleFromEventView = createRuleFromEventView;
function createRuleFromWizardTemplate(wizardTemplate) {
    const { eventTypes, aggregate, dataset } = wizardTemplate;
    const defaultRuleOptions = {};
    if ((0, utils_1.isSessionAggregate)(aggregate)) {
        defaultRuleOptions.thresholdType = types_1.AlertRuleThresholdType.BELOW;
        defaultRuleOptions.timeWindow = types_1.TimeWindow.ONE_HOUR;
    }
    return Object.assign(Object.assign({}, createDefaultRule(defaultRuleOptions)), { eventTypes: [eventTypes], aggregate,
        dataset });
}
exports.createRuleFromWizardTemplate = createRuleFromWizardTemplate;
//# sourceMappingURL=constants.jsx.map