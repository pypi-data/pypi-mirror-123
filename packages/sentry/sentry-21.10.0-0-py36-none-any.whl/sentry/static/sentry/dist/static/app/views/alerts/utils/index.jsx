Object.defineProperty(exports, "__esModule", { value: true });
exports.shouldScaleAlertChart = exports.ALERT_CHART_MIN_MAX_BUFFER = exports.alertTooltipValueFormatter = exports.alertAxisFormatter = exports.SESSION_AGGREGATE_TO_FIELD = exports.isSessionAggregate = exports.getQueryDatasource = exports.convertDatasetEventTypesToSource = exports.DATA_SOURCE_TO_SET_AND_EVENT_TYPES = exports.DATA_SOURCE_LABELS = exports.isIssueAlert = exports.getStartEndFromStats = exports.getIncidentMetricPreset = exports.updateStatus = exports.updateSubscription = exports.fetchIncident = exports.fetchIncidentsForRule = exports.fetchAlertRule = void 0;
const tslib_1 = require("tslib");
const round_1 = (0, tslib_1.__importDefault)(require("lodash/round"));
const api_1 = require("app/api");
const locale_1 = require("app/locale");
const types_1 = require("app/types");
const utils_1 = require("app/utils");
const dates_1 = require("app/utils/dates");
const charts_1 = require("app/utils/discover/charts");
const presets_1 = require("app/views/alerts/incidentRules/presets");
const types_2 = require("app/views/alerts/incidentRules/types");
// Use this api for requests that are getting cancelled
const uncancellableApi = new api_1.Client();
function fetchAlertRule(orgId, ruleId) {
    return uncancellableApi.requestPromise(`/organizations/${orgId}/alert-rules/${ruleId}/`);
}
exports.fetchAlertRule = fetchAlertRule;
function fetchIncidentsForRule(orgId, alertRule, start, end) {
    return uncancellableApi.requestPromise(`/organizations/${orgId}/incidents/`, {
        query: {
            alertRule,
            includeSnapshots: true,
            start,
            end,
            expand: ['activities', 'seen_by', 'original_alert_rule'],
        },
    });
}
exports.fetchIncidentsForRule = fetchIncidentsForRule;
function fetchIncident(api, orgId, alertId) {
    return api.requestPromise(`/organizations/${orgId}/incidents/${alertId}/`);
}
exports.fetchIncident = fetchIncident;
function updateSubscription(api, orgId, alertId, isSubscribed) {
    const method = isSubscribed ? 'POST' : 'DELETE';
    return api.requestPromise(`/organizations/${orgId}/incidents/${alertId}/subscriptions/`, {
        method,
    });
}
exports.updateSubscription = updateSubscription;
function updateStatus(api, orgId, alertId, status) {
    return api.requestPromise(`/organizations/${orgId}/incidents/${alertId}/`, {
        method: 'PUT',
        data: {
            status,
        },
    });
}
exports.updateStatus = updateStatus;
function getIncidentMetricPreset(incident) {
    var _a, _b;
    const alertRule = incident === null || incident === void 0 ? void 0 : incident.alertRule;
    const aggregate = (_a = alertRule === null || alertRule === void 0 ? void 0 : alertRule.aggregate) !== null && _a !== void 0 ? _a : '';
    const dataset = (_b = alertRule === null || alertRule === void 0 ? void 0 : alertRule.dataset) !== null && _b !== void 0 ? _b : types_2.Dataset.ERRORS;
    return presets_1.PRESET_AGGREGATES.find(p => p.validDataset.includes(dataset) && p.match.test(aggregate));
}
exports.getIncidentMetricPreset = getIncidentMetricPreset;
/**
 * Gets start and end date query parameters from stats
 */
function getStartEndFromStats(stats) {
    const start = (0, dates_1.getUtcDateString)(stats.eventStats.data[0][0] * 1000);
    const end = (0, dates_1.getUtcDateString)(stats.eventStats.data[stats.eventStats.data.length - 1][0] * 1000);
    return { start, end };
}
exports.getStartEndFromStats = getStartEndFromStats;
function isIssueAlert(data) {
    return !data.hasOwnProperty('triggers');
}
exports.isIssueAlert = isIssueAlert;
exports.DATA_SOURCE_LABELS = {
    [types_2.Dataset.ERRORS]: (0, locale_1.t)('Errors'),
    [types_2.Dataset.TRANSACTIONS]: (0, locale_1.t)('Transactions'),
    [types_2.Datasource.ERROR_DEFAULT]: (0, locale_1.t)('event.type:error OR event.type:default'),
    [types_2.Datasource.ERROR]: (0, locale_1.t)('event.type:error'),
    [types_2.Datasource.DEFAULT]: (0, locale_1.t)('event.type:default'),
    [types_2.Datasource.TRANSACTION]: (0, locale_1.t)('event.type:transaction'),
};
// Maps a datasource to the relevant dataset and event_types for the backend to use
exports.DATA_SOURCE_TO_SET_AND_EVENT_TYPES = {
    [types_2.Datasource.ERROR_DEFAULT]: {
        dataset: types_2.Dataset.ERRORS,
        eventTypes: [types_2.EventTypes.ERROR, types_2.EventTypes.DEFAULT],
    },
    [types_2.Datasource.ERROR]: {
        dataset: types_2.Dataset.ERRORS,
        eventTypes: [types_2.EventTypes.ERROR],
    },
    [types_2.Datasource.DEFAULT]: {
        dataset: types_2.Dataset.ERRORS,
        eventTypes: [types_2.EventTypes.DEFAULT],
    },
    [types_2.Datasource.TRANSACTION]: {
        dataset: types_2.Dataset.TRANSACTIONS,
        eventTypes: [types_2.EventTypes.TRANSACTION],
    },
};
// Converts the given dataset and event types array to a datasource for the datasource dropdown
function convertDatasetEventTypesToSource(dataset, eventTypes) {
    // transactions only has one datasource option regardless of event type
    if (dataset === types_2.Dataset.TRANSACTIONS) {
        return types_2.Datasource.TRANSACTION;
    }
    // if no event type was provided use the default datasource
    if (!eventTypes) {
        return types_2.Datasource.ERROR;
    }
    if (eventTypes.includes(types_2.EventTypes.DEFAULT) && eventTypes.includes(types_2.EventTypes.ERROR)) {
        return types_2.Datasource.ERROR_DEFAULT;
    }
    else if (eventTypes.includes(types_2.EventTypes.DEFAULT)) {
        return types_2.Datasource.DEFAULT;
    }
    else {
        return types_2.Datasource.ERROR;
    }
}
exports.convertDatasetEventTypesToSource = convertDatasetEventTypesToSource;
/**
 * Attempt to guess the data source of a discover query
 *
 * @returns An object containing the datasource and new query without the datasource.
 * Returns null on no datasource.
 */
function getQueryDatasource(query) {
    let match = query.match(/\(?\bevent\.type:(error|default|transaction)\)?\WOR\W\(?event\.type:(error|default|transaction)\)?/i);
    if (match) {
        // should be [error, default] or [default, error]
        const eventTypes = match.slice(1, 3).sort().join(',');
        if (eventTypes !== 'default,error') {
            return null;
        }
        return { source: types_2.Datasource.ERROR_DEFAULT, query: query.replace(match[0], '').trim() };
    }
    match = query.match(/(^|\s)event\.type:(error|default|transaction)/i);
    if (match && types_2.Datasource[match[2].toUpperCase()]) {
        return {
            source: types_2.Datasource[match[2].toUpperCase()],
            query: query.replace(match[0], '').trim(),
        };
    }
    return null;
}
exports.getQueryDatasource = getQueryDatasource;
function isSessionAggregate(aggregate) {
    return Object.values(types_2.SessionsAggregate).includes(aggregate);
}
exports.isSessionAggregate = isSessionAggregate;
exports.SESSION_AGGREGATE_TO_FIELD = {
    [types_2.SessionsAggregate.CRASH_FREE_SESSIONS]: types_1.SessionField.SESSIONS,
    [types_2.SessionsAggregate.CRASH_FREE_USERS]: types_1.SessionField.USERS,
};
function alertAxisFormatter(value, seriesName, aggregate) {
    if (isSessionAggregate(aggregate)) {
        return (0, utils_1.defined)(value) ? `${(0, round_1.default)(value, 2)}%` : '\u2015';
    }
    return (0, charts_1.axisLabelFormatter)(value, seriesName);
}
exports.alertAxisFormatter = alertAxisFormatter;
function alertTooltipValueFormatter(value, seriesName, aggregate) {
    if (isSessionAggregate(aggregate)) {
        return (0, utils_1.defined)(value) ? `${value}%` : '\u2015';
    }
    return (0, charts_1.tooltipFormatter)(value, seriesName);
}
exports.alertTooltipValueFormatter = alertTooltipValueFormatter;
exports.ALERT_CHART_MIN_MAX_BUFFER = 1.03;
function shouldScaleAlertChart(aggregate) {
    // We want crash free rate charts to be scaled because they are usually too
    // close to 100% and therefore too fine to see the spikes on 0%-100% scale.
    return isSessionAggregate(aggregate);
}
exports.shouldScaleAlertChart = shouldScaleAlertChart;
//# sourceMappingURL=index.jsx.map