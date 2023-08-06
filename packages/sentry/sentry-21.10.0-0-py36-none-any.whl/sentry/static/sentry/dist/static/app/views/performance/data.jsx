Object.defineProperty(exports, "__esModule", { value: true });
exports.generatePerformanceVitalDetailView = exports.generatePerformanceEventView = exports.getTermHelp = exports.PERFORMANCE_TERMS = exports.getMobileAxisOptions = exports.getBackendAxisOptions = exports.getFrontendOtherAxisOptions = exports.getFrontendAxisOptions = exports.getAxisOptions = exports.PERFORMANCE_TERM = exports.COLUMN_TITLES = exports.DEFAULT_STATS_PERIOD = void 0;
const tslib_1 = require("tslib");
const gridEditable_1 = require("app/components/gridEditable");
const globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
const locale_1 = require("app/locale");
const eventView_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/eventView"));
const queryString_1 = require("app/utils/queryString");
const tokenizeSearch_1 = require("app/utils/tokenizeSearch");
const utils_1 = require("./landing/utils");
const utils_2 = require("./vitalDetail/utils");
exports.DEFAULT_STATS_PERIOD = '24h';
exports.COLUMN_TITLES = [
    'transaction',
    'project',
    'tpm',
    'p50',
    'p95',
    'failure rate',
    'apdex',
    'users',
    'user misery',
];
var PERFORMANCE_TERM;
(function (PERFORMANCE_TERM) {
    PERFORMANCE_TERM["APDEX"] = "apdex";
    PERFORMANCE_TERM["TPM"] = "tpm";
    PERFORMANCE_TERM["THROUGHPUT"] = "throughput";
    PERFORMANCE_TERM["FAILURE_RATE"] = "failureRate";
    PERFORMANCE_TERM["P50"] = "p50";
    PERFORMANCE_TERM["P75"] = "p75";
    PERFORMANCE_TERM["P95"] = "p95";
    PERFORMANCE_TERM["P99"] = "p99";
    PERFORMANCE_TERM["LCP"] = "lcp";
    PERFORMANCE_TERM["FCP"] = "fcp";
    PERFORMANCE_TERM["USER_MISERY"] = "userMisery";
    PERFORMANCE_TERM["STATUS_BREAKDOWN"] = "statusBreakdown";
    PERFORMANCE_TERM["DURATION_DISTRIBUTION"] = "durationDistribution";
    PERFORMANCE_TERM["USER_MISERY_NEW"] = "userMiseryNew";
    PERFORMANCE_TERM["APDEX_NEW"] = "apdexNew";
    PERFORMANCE_TERM["APP_START_COLD"] = "appStartCold";
    PERFORMANCE_TERM["APP_START_WARM"] = "appStartWarm";
    PERFORMANCE_TERM["SLOW_FRAMES"] = "slowFrames";
    PERFORMANCE_TERM["FROZEN_FRAMES"] = "frozenFrames";
    PERFORMANCE_TERM["STALL_PERCENTAGE"] = "stallPercentage";
})(PERFORMANCE_TERM = exports.PERFORMANCE_TERM || (exports.PERFORMANCE_TERM = {}));
function getAxisOptions(organization) {
    return [
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.APDEX_NEW),
            value: 'apdex()',
            label: (0, locale_1.t)('Apdex'),
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.TPM),
            value: 'tpm()',
            label: (0, locale_1.t)('Transactions Per Minute'),
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.FAILURE_RATE),
            value: 'failure_rate()',
            label: (0, locale_1.t)('Failure Rate'),
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.P50),
            value: 'p50()',
            label: (0, locale_1.t)('p50 Duration'),
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.P95),
            value: 'p95()',
            label: (0, locale_1.t)('p95 Duration'),
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.P99),
            value: 'p99()',
            label: (0, locale_1.t)('p99 Duration'),
        },
    ];
}
exports.getAxisOptions = getAxisOptions;
function getFrontendAxisOptions(organization) {
    return [
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.LCP),
            value: `p75(lcp)`,
            label: (0, locale_1.t)('LCP p75'),
            field: 'p75(measurements.lcp)',
            isLeftDefault: true,
            backupOption: {
                tooltip: getTermHelp(organization, PERFORMANCE_TERM.FCP),
                value: `p75(fcp)`,
                label: (0, locale_1.t)('FCP p75'),
                field: 'p75(measurements.fcp)',
            },
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.DURATION_DISTRIBUTION),
            value: 'lcp_distribution',
            label: (0, locale_1.t)('LCP Distribution'),
            field: 'measurements.lcp',
            isDistribution: true,
            isRightDefault: true,
            backupOption: {
                tooltip: getTermHelp(organization, PERFORMANCE_TERM.DURATION_DISTRIBUTION),
                value: 'fcp_distribution',
                label: (0, locale_1.t)('FCP Distribution'),
                field: 'measurements.fcp',
                isDistribution: true,
            },
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.TPM),
            value: 'tpm()',
            label: (0, locale_1.t)('Transactions Per Minute'),
            field: 'tpm()',
        },
    ];
}
exports.getFrontendAxisOptions = getFrontendAxisOptions;
function getFrontendOtherAxisOptions(organization) {
    return [
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.P50),
            value: `p50()`,
            label: (0, locale_1.t)('Duration p50'),
            field: 'p50(transaction.duration)',
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.P75),
            value: `p75()`,
            label: (0, locale_1.t)('Duration p75'),
            field: 'p75(transaction.duration)',
            isLeftDefault: true,
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.P95),
            value: `p95()`,
            label: (0, locale_1.t)('Duration p95'),
            field: 'p95(transaction.duration)',
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.DURATION_DISTRIBUTION),
            value: 'duration_distribution',
            label: (0, locale_1.t)('Duration Distribution'),
            field: 'transaction.duration',
            isDistribution: true,
            isRightDefault: true,
        },
    ];
}
exports.getFrontendOtherAxisOptions = getFrontendOtherAxisOptions;
function getBackendAxisOptions(organization) {
    return [
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.P50),
            value: `p50()`,
            label: (0, locale_1.t)('Duration p50'),
            field: 'p50(transaction.duration)',
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.P75),
            value: `p75()`,
            label: (0, locale_1.t)('Duration p75'),
            field: 'p75(transaction.duration)',
            isLeftDefault: true,
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.P95),
            value: `p95()`,
            label: (0, locale_1.t)('Duration p95'),
            field: 'p95(transaction.duration)',
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.P99),
            value: `p99()`,
            label: (0, locale_1.t)('Duration p99'),
            field: 'p99(transaction.duration)',
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.TPM),
            value: 'tpm()',
            label: (0, locale_1.t)('Transactions Per Minute'),
            field: 'tpm()',
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.FAILURE_RATE),
            value: 'failure_rate()',
            label: (0, locale_1.t)('Failure Rate'),
            field: 'failure_rate()',
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.DURATION_DISTRIBUTION),
            value: 'duration_distribution',
            label: (0, locale_1.t)('Duration Distribution'),
            field: 'transaction.duration',
            isDistribution: true,
            isRightDefault: true,
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.APDEX),
            value: 'apdex()',
            label: (0, locale_1.t)('Apdex'),
            field: 'apdex()',
        },
    ];
}
exports.getBackendAxisOptions = getBackendAxisOptions;
function getMobileAxisOptions(organization) {
    return [
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.APP_START_COLD),
            value: `p50(measurements.app_start_cold)`,
            label: (0, locale_1.t)('Cold Start Duration p50'),
            field: 'p50(measurements.app_start_cold)',
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.APP_START_COLD),
            value: `p75(measurements.app_start_cold)`,
            label: (0, locale_1.t)('Cold Start Duration p75'),
            field: 'p75(measurements.app_start_cold)',
            isLeftDefault: true,
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.APP_START_COLD),
            value: `p95(measurements.app_start_cold)`,
            label: (0, locale_1.t)('Cold Start Duration p95'),
            field: 'p95(measurements.app_start_cold)',
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.APP_START_COLD),
            value: `p99(measurements.app_start_cold)`,
            label: (0, locale_1.t)('Cold Start Duration p99'),
            field: 'p99(measurements.app_start_cold)',
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.DURATION_DISTRIBUTION),
            value: 'app_start_cold_distribution',
            label: (0, locale_1.t)('Cold Start Distribution'),
            field: 'measurements.app_start_cold',
            isDistribution: true,
            isRightDefault: true,
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.APP_START_WARM),
            value: `p50(measurements.app_start_warm)`,
            label: (0, locale_1.t)('Warm Start Duration p50'),
            field: 'p50(measurements.app_start_warm)',
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.APP_START_WARM),
            value: `p75(measurements.app_start_warm)`,
            label: (0, locale_1.t)('Warm Start Duration p75'),
            field: 'p75(measurements.app_start_warm)',
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.APP_START_WARM),
            value: `p95(measurements.app_start_warm)`,
            label: (0, locale_1.t)('Warm Start Duration p95'),
            field: 'p95(measurements.app_start_warm)',
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.APP_START_WARM),
            value: `p99(measurements.app_start_warm)`,
            label: (0, locale_1.t)('Warm Start Duration p99'),
            field: 'p99(measurements.app_start_warm)',
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.DURATION_DISTRIBUTION),
            value: 'app_start_warm_distribution',
            label: (0, locale_1.t)('Warm Start Distribution'),
            field: 'measurements.app_start_warm',
            isDistribution: true,
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.TPM),
            value: 'tpm()',
            label: (0, locale_1.t)('Transactions Per Minute'),
            field: 'tpm()',
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.FAILURE_RATE),
            value: 'failure_rate()',
            label: (0, locale_1.t)('Failure Rate'),
            field: 'failure_rate()',
        },
    ];
}
exports.getMobileAxisOptions = getMobileAxisOptions;
exports.PERFORMANCE_TERMS = {
    apdex: () => (0, locale_1.t)('Apdex is the ratio of both satisfactory and tolerable response times to all response times. To adjust the tolerable threshold, go to performance settings.'),
    tpm: () => (0, locale_1.t)('TPM is the number of recorded transaction events per minute.'),
    throughput: () => (0, locale_1.t)('Throughput is the number of recorded transaction events per minute.'),
    failureRate: () => (0, locale_1.t)('Failure rate is the percentage of recorded transactions that had a known and unsuccessful status.'),
    p50: () => (0, locale_1.t)('p50 indicates the duration that 50% of transactions are faster than.'),
    p75: () => (0, locale_1.t)('p75 indicates the duration that 75% of transactions are faster than.'),
    p95: () => (0, locale_1.t)('p95 indicates the duration that 95% of transactions are faster than.'),
    p99: () => (0, locale_1.t)('p99 indicates the duration that 99% of transactions are faster than.'),
    lcp: () => (0, locale_1.t)('Largest contentful paint (LCP) is a web vital meant to represent user load times'),
    fcp: () => (0, locale_1.t)('First contentful paint (FCP) is a web vital meant to represent user load times'),
    userMisery: organization => (0, locale_1.t)("User Misery is a score that represents the number of unique users who have experienced load times 4x your organization's apdex threshold of %sms.", organization.apdexThreshold),
    statusBreakdown: () => (0, locale_1.t)('The breakdown of transaction statuses. This may indicate what type of failure it is.'),
    durationDistribution: () => (0, locale_1.t)('Distribution buckets counts of transactions at specifics times for your current date range'),
    userMiseryNew: () => (0, locale_1.t)("User Misery is a score that represents the number of unique users who have experienced load times 4x the project's configured threshold. Adjust project threshold in project performance settings."),
    apdexNew: () => (0, locale_1.t)('Apdex is the ratio of both satisfactory and tolerable response times to all response times. To adjust the tolerable threshold, go to project performance settings.'),
    appStartCold: () => (0, locale_1.t)('Cold start is a measure of the application start up time from scratch.'),
    appStartWarm: () => (0, locale_1.t)('Warm start is a measure of the application start up time while still in memory.'),
    slowFrames: () => (0, locale_1.t)('The count of the number of slow frames in the transaction.'),
    frozenFrames: () => (0, locale_1.t)('The count of the number of frozen frames in the transaction.'),
    stallPercentage: () => (0, locale_1.t)('The percentage of the transaction duration in which the application is in a stalled state.'),
};
function getTermHelp(organization, term) {
    if (!exports.PERFORMANCE_TERMS.hasOwnProperty(term)) {
        return '';
    }
    return exports.PERFORMANCE_TERMS[term](organization);
}
exports.getTermHelp = getTermHelp;
function generateGenericPerformanceEventView(_organization, location) {
    const { query } = location;
    const fields = [
        'team_key_transaction',
        'transaction',
        'project',
        'tpm()',
        'p50()',
        'p95()',
        'failure_rate()',
        'apdex()',
        'count_unique(user)',
        'count_miserable(user)',
        'user_misery()',
    ];
    const hasStartAndEnd = query.start && query.end;
    const savedQuery = {
        id: undefined,
        name: (0, locale_1.t)('Performance'),
        query: 'event.type:transaction',
        projects: [],
        fields,
        version: 2,
    };
    const widths = Array(savedQuery.fields.length).fill(gridEditable_1.COL_WIDTH_UNDEFINED);
    widths[savedQuery.fields.length - 1] = '110';
    savedQuery.widths = widths;
    if (!query.statsPeriod && !hasStartAndEnd) {
        savedQuery.range = exports.DEFAULT_STATS_PERIOD;
    }
    savedQuery.orderby = (0, queryString_1.decodeScalar)(query.sort, '-tpm');
    const searchQuery = (0, queryString_1.decodeScalar)(query.query, '');
    const conditions = new tokenizeSearch_1.MutableSearch(searchQuery);
    // This is not an override condition since we want the duration to appear in the search bar as a default.
    if (!conditions.hasFilter('transaction.duration')) {
        conditions.setFilterValues('transaction.duration', ['<15m']);
    }
    // If there is a bare text search, we want to treat it as a search
    // on the transaction name.
    if (conditions.freeText.length > 0) {
        // the query here is a user entered condition, no need to escape it
        conditions.setFilterValues('transaction', [`*${conditions.freeText.join(' ')}*`], false);
        conditions.freeText = [];
    }
    savedQuery.query = conditions.formatString();
    const eventView = eventView_1.default.fromNewQueryWithLocation(savedQuery, location);
    eventView.additionalConditions.addFilterValues('event.type', ['transaction']);
    return eventView;
}
function generateBackendPerformanceEventView(_organization, location) {
    const { query } = location;
    const fields = [
        'team_key_transaction',
        'transaction',
        'project',
        'transaction.op',
        'http.method',
        'tpm()',
        'p50()',
        'p95()',
        'failure_rate()',
        'apdex()',
        'count_unique(user)',
        'count_miserable(user)',
        'user_misery()',
    ];
    const hasStartAndEnd = query.start && query.end;
    const savedQuery = {
        id: undefined,
        name: (0, locale_1.t)('Performance'),
        query: 'event.type:transaction',
        projects: [],
        fields,
        version: 2,
    };
    const widths = Array(savedQuery.fields.length).fill(gridEditable_1.COL_WIDTH_UNDEFINED);
    widths[savedQuery.fields.length - 1] = '110';
    savedQuery.widths = widths;
    if (!query.statsPeriod && !hasStartAndEnd) {
        savedQuery.range = exports.DEFAULT_STATS_PERIOD;
    }
    savedQuery.orderby = (0, queryString_1.decodeScalar)(query.sort, '-tpm');
    const searchQuery = (0, queryString_1.decodeScalar)(query.query, '');
    const conditions = new tokenizeSearch_1.MutableSearch(searchQuery);
    // This is not an override condition since we want the duration to appear in the search bar as a default.
    if (!conditions.hasFilter('transaction.duration')) {
        conditions.setFilterValues('transaction.duration', ['<15m']);
    }
    // If there is a bare text search, we want to treat it as a search
    // on the transaction name.
    if (conditions.freeText.length > 0) {
        // the query here is a user entered condition, no need to escape it
        conditions.setFilterValues('transaction', [`*${conditions.freeText.join(' ')}*`], false);
        conditions.freeText = [];
    }
    savedQuery.query = conditions.formatString();
    const eventView = eventView_1.default.fromNewQueryWithLocation(savedQuery, location);
    eventView.additionalConditions.addFilterValues('event.type', ['transaction']);
    return eventView;
}
function generateMobilePerformanceEventView(_organization, location, projects, genericEventView) {
    const { query } = location;
    const fields = [
        'team_key_transaction',
        'transaction',
        'project',
        'transaction.op',
        'tpm()',
        'p75(measurements.app_start_cold)',
        'p75(measurements.app_start_warm)',
        'p75(measurements.frames_slow_rate)',
        'p75(measurements.frames_frozen_rate)',
    ];
    // At this point, all projects are mobile projects.
    // If in addition to that, all projects are react-native projects,
    // then show the stall percentage as well.
    const projectIds = genericEventView.project;
    if (projectIds.length > 0 && projectIds[0] !== globalSelectionHeader_1.ALL_ACCESS_PROJECTS) {
        const selectedProjects = projects.filter(p => projectIds.includes(parseInt(p.id, 10)));
        if (selectedProjects.length > 0 &&
            selectedProjects.every(project => project.platform === 'react-native')) {
            // TODO(tonyx): remove these once the SDKs are ready
            fields.pop();
            fields.pop();
            fields.push('p75(measurements.stall_percentage)');
        }
    }
    const hasStartAndEnd = query.start && query.end;
    const savedQuery = {
        id: undefined,
        name: (0, locale_1.t)('Performance'),
        query: 'event.type:transaction',
        projects: [],
        fields: [...fields, 'count_unique(user)', 'count_miserable(user)', 'user_misery()'],
        version: 2,
    };
    const widths = Array(savedQuery.fields.length).fill(gridEditable_1.COL_WIDTH_UNDEFINED);
    widths[savedQuery.fields.length - 1] = '110';
    savedQuery.widths = widths;
    if (!query.statsPeriod && !hasStartAndEnd) {
        savedQuery.range = exports.DEFAULT_STATS_PERIOD;
    }
    savedQuery.orderby = (0, queryString_1.decodeScalar)(query.sort, '-tpm');
    const searchQuery = (0, queryString_1.decodeScalar)(query.query, '');
    const conditions = new tokenizeSearch_1.MutableSearch(searchQuery);
    // This is not an override condition since we want the duration to appear in the search bar as a default.
    if (!conditions.hasFilter('transaction.duration')) {
        conditions.setFilterValues('transaction.duration', ['<15m']);
    }
    // If there is a bare text search, we want to treat it as a search
    // on the transaction name.
    if (conditions.freeText.length > 0) {
        // the query here is a user entered condition, no need to escape it
        conditions.setFilterValues('transaction', [`*${conditions.freeText.join(' ')}*`], false);
        conditions.freeText = [];
    }
    savedQuery.query = conditions.formatString();
    const eventView = eventView_1.default.fromNewQueryWithLocation(savedQuery, location);
    eventView.additionalConditions.addFilterValues('event.type', ['transaction']);
    return eventView;
}
function generateFrontendPageloadPerformanceEventView(_organization, location) {
    const { query } = location;
    const fields = [
        'team_key_transaction',
        'transaction',
        'project',
        'tpm()',
        'p75(measurements.fcp)',
        'p75(measurements.lcp)',
        'p75(measurements.fid)',
        'p75(measurements.cls)',
        'count_unique(user)',
        'count_miserable(user)',
        'user_misery()',
    ];
    const hasStartAndEnd = query.start && query.end;
    const savedQuery = {
        id: undefined,
        name: (0, locale_1.t)('Performance'),
        query: 'event.type:transaction',
        projects: [],
        fields,
        version: 2,
    };
    const widths = Array(savedQuery.fields.length).fill(gridEditable_1.COL_WIDTH_UNDEFINED);
    widths[savedQuery.fields.length - 1] = '110';
    savedQuery.widths = widths;
    if (!query.statsPeriod && !hasStartAndEnd) {
        savedQuery.range = exports.DEFAULT_STATS_PERIOD;
    }
    savedQuery.orderby = (0, queryString_1.decodeScalar)(query.sort, '-tpm');
    const searchQuery = (0, queryString_1.decodeScalar)(query.query, '');
    const conditions = new tokenizeSearch_1.MutableSearch(searchQuery);
    // This is not an override condition since we want the duration to appear in the search bar as a default.
    if (!conditions.hasFilter('transaction.duration')) {
        conditions.setFilterValues('transaction.duration', ['<15m']);
    }
    // If there is a bare text search, we want to treat it as a search
    // on the transaction name.
    if (conditions.freeText.length > 0) {
        // the query here is a user entered condition, no need to escape it
        conditions.setFilterValues('transaction', [`*${conditions.freeText.join(' ')}*`], false);
        conditions.freeText = [];
    }
    savedQuery.query = conditions.formatString();
    const eventView = eventView_1.default.fromNewQueryWithLocation(savedQuery, location);
    eventView.additionalConditions
        .addFilterValues('event.type', ['transaction'])
        .addFilterValues('transaction.op', ['pageload']);
    return eventView;
}
function generateFrontendOtherPerformanceEventView(_organization, location) {
    const { query } = location;
    const fields = [
        'team_key_transaction',
        'transaction',
        'project',
        'transaction.op',
        'tpm()',
        'p50(transaction.duration)',
        'p75(transaction.duration)',
        'p95(transaction.duration)',
        'count_unique(user)',
        'count_miserable(user)',
        'user_misery()',
    ];
    const hasStartAndEnd = query.start && query.end;
    const savedQuery = {
        id: undefined,
        name: (0, locale_1.t)('Performance'),
        query: 'event.type:transaction',
        projects: [],
        fields,
        version: 2,
    };
    const widths = Array(savedQuery.fields.length).fill(gridEditable_1.COL_WIDTH_UNDEFINED);
    widths[savedQuery.fields.length - 1] = '110';
    savedQuery.widths = widths;
    if (!query.statsPeriod && !hasStartAndEnd) {
        savedQuery.range = exports.DEFAULT_STATS_PERIOD;
    }
    savedQuery.orderby = (0, queryString_1.decodeScalar)(query.sort, '-tpm');
    const searchQuery = (0, queryString_1.decodeScalar)(query.query, '');
    const conditions = new tokenizeSearch_1.MutableSearch(searchQuery);
    // This is not an override condition since we want the duration to appear in the search bar as a default.
    if (!conditions.hasFilter('transaction.duration')) {
        conditions.setFilterValues('transaction.duration', ['<15m']);
    }
    // If there is a bare text search, we want to treat it as a search
    // on the transaction name.
    if (conditions.freeText.length > 0) {
        // the query here is a user entered condition, no need to escape it
        conditions.setFilterValues('transaction', [`*${conditions.freeText.join(' ')}*`], false);
        conditions.freeText = [];
    }
    savedQuery.query = conditions.formatString();
    const eventView = eventView_1.default.fromNewQueryWithLocation(savedQuery, location);
    eventView.additionalConditions
        .addFilterValues('event.type', ['transaction'])
        .addFilterValues('!transaction.op', ['pageload']);
    return eventView;
}
function generatePerformanceEventView(organization, location, projects, isTrends = false) {
    const eventView = generateGenericPerformanceEventView(organization, location);
    if (isTrends) {
        return eventView;
    }
    const display = (0, utils_1.getCurrentLandingDisplay)(location, projects, eventView);
    switch (display === null || display === void 0 ? void 0 : display.field) {
        case utils_1.LandingDisplayField.FRONTEND_PAGELOAD:
            return generateFrontendPageloadPerformanceEventView(organization, location);
        case utils_1.LandingDisplayField.FRONTEND_OTHER:
            return generateFrontendOtherPerformanceEventView(organization, location);
        case utils_1.LandingDisplayField.BACKEND:
            return generateBackendPerformanceEventView(organization, location);
        case utils_1.LandingDisplayField.MOBILE:
            return generateMobilePerformanceEventView(organization, location, projects, eventView);
        default:
            return eventView;
    }
}
exports.generatePerformanceEventView = generatePerformanceEventView;
function generatePerformanceVitalDetailView(_organization, location) {
    const { query } = location;
    const vitalName = (0, utils_2.vitalNameFromLocation)(location);
    const hasStartAndEnd = query.start && query.end;
    const savedQuery = {
        id: undefined,
        name: (0, locale_1.t)('Vitals Performance Details'),
        query: 'event.type:transaction',
        projects: [],
        fields: [
            'team_key_transaction',
            'transaction',
            'project',
            'count_unique(user)',
            'count()',
            `p50(${vitalName})`,
            `p75(${vitalName})`,
            `p95(${vitalName})`,
            (0, utils_2.getVitalDetailTablePoorStatusFunction)(vitalName),
            (0, utils_2.getVitalDetailTableMehStatusFunction)(vitalName),
        ],
        version: 2,
    };
    if (!query.statsPeriod && !hasStartAndEnd) {
        savedQuery.range = exports.DEFAULT_STATS_PERIOD;
    }
    savedQuery.orderby = (0, queryString_1.decodeScalar)(query.sort, '-count');
    const searchQuery = (0, queryString_1.decodeScalar)(query.query, '');
    const conditions = new tokenizeSearch_1.MutableSearch(searchQuery);
    // If there is a bare text search, we want to treat it as a search
    // on the transaction name.
    if (conditions.freeText.length > 0) {
        // the query here is a user entered condition, no need to escape it
        conditions.setFilterValues('transaction', [`*${conditions.freeText.join(' ')}*`], false);
        conditions.freeText = [];
    }
    savedQuery.query = conditions.formatString();
    const eventView = eventView_1.default.fromNewQueryWithLocation(savedQuery, location);
    eventView.additionalConditions
        .addFilterValues('event.type', ['transaction'])
        .addFilterValues('has', [vitalName]);
    return eventView;
}
exports.generatePerformanceVitalDetailView = generatePerformanceVitalDetailView;
//# sourceMappingURL=data.jsx.map