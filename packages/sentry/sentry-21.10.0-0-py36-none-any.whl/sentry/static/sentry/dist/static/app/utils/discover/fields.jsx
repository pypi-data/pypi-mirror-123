Object.defineProperty(exports, "__esModule", { value: true });
exports.hasDuplicate = exports.getColumnType = exports.getSpanOperationName = exports.isLegalYAxisType = exports.fieldAlignment = exports.aggregateMultiPlotType = exports.aggregateFunctionOutputType = exports.aggregateOutputType = exports.getAggregateFields = exports.isAggregateFieldOrEquation = exports.isAggregateField = exports.getAggregateAlias = exports.explodeField = exports.generateFieldAsString = exports.explodeFieldString = exports.generateAggregateFields = exports.isLegalEquationColumn = exports.isAggregateEquation = exports.getEquation = exports.getEquationAliasIndex = exports.stripEquationPrefix = exports.maybeEquationAlias = exports.isEquationAlias = exports.isEquation = exports.parseArguments = exports.parseFunction = exports.getAggregateArg = exports.getMeasurementSlug = exports.measurementType = exports.isMeasurement = exports.SPAN_OP_BREAKDOWN_PATTERN = exports.MEASUREMENT_PATTERN = exports.TRACING_FIELDS = exports.SPAN_OP_BREAKDOWN_FIELDS = exports.isRelativeSpanOperationBreakdownField = exports.SPAN_OP_RELATIVE_BREAKDOWN_FIELD = exports.isSpanOperationBreakdownField = exports.MobileVital = exports.WebVital = exports.SEMVER_TAGS = exports.FIELD_TAGS = exports.DEPRECATED_FIELDS = exports.FIELDS = exports.ALIASES = exports.AGGREGATIONS = void 0;
const tslib_1 = require("tslib");
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const constants_1 = require("app/constants");
const utils_1 = require("app/types/utils");
const CONDITIONS_ARGUMENTS = [
    {
        label: 'is equal to',
        value: 'equals',
    },
    {
        label: 'is not equal to',
        value: 'notEquals',
    },
    {
        label: 'is less than',
        value: 'less',
    },
    {
        label: 'is greater than',
        value: 'greater',
    },
    {
        label: 'is less than or equal to',
        value: 'lessOrEquals',
    },
    {
        label: 'is greater than or equal to',
        value: 'greaterOrEquals',
    },
];
// Refer to src/sentry/search/events/fields.py
// Try to keep functions logically sorted, ie. all the count functions are grouped together
exports.AGGREGATIONS = {
    count: {
        parameters: [],
        outputType: 'number',
        isSortable: true,
        multiPlotType: 'area',
    },
    count_unique: {
        parameters: [
            {
                kind: 'column',
                columnTypes: ['string', 'integer', 'number', 'duration', 'date', 'boolean'],
                defaultValue: 'user',
                required: true,
            },
        ],
        outputType: 'number',
        isSortable: true,
        multiPlotType: 'line',
    },
    count_miserable: {
        getFieldOverrides({ parameter, organization }) {
            var _a, _b;
            if (parameter.kind === 'column') {
                return { defaultValue: 'user' };
            }
            return {
                defaultValue: (_b = (_a = organization.apdexThreshold) === null || _a === void 0 ? void 0 : _a.toString()) !== null && _b !== void 0 ? _b : parameter.defaultValue,
            };
        },
        parameters: [
            {
                kind: 'column',
                columnTypes: validateAllowedColumns(['user']),
                defaultValue: 'user',
                required: true,
            },
            {
                kind: 'value',
                dataType: 'number',
                defaultValue: '300',
                required: true,
            },
        ],
        outputType: 'number',
        isSortable: true,
        multiPlotType: 'area',
    },
    count_if: {
        parameters: [
            {
                kind: 'column',
                columnTypes: validateDenyListColumns(['string', 'duration'], ['id', 'issue', 'user.display']),
                defaultValue: 'transaction.duration',
                required: true,
            },
            {
                kind: 'dropdown',
                options: CONDITIONS_ARGUMENTS,
                dataType: 'string',
                defaultValue: CONDITIONS_ARGUMENTS[0].value,
                required: true,
            },
            {
                kind: 'value',
                dataType: 'string',
                defaultValue: '300',
                required: true,
            },
        ],
        outputType: 'number',
        isSortable: true,
        multiPlotType: 'area',
    },
    eps: {
        parameters: [],
        outputType: 'number',
        isSortable: true,
        multiPlotType: 'area',
    },
    epm: {
        parameters: [],
        outputType: 'number',
        isSortable: true,
        multiPlotType: 'area',
    },
    failure_count: {
        parameters: [],
        outputType: 'number',
        isSortable: true,
        multiPlotType: 'line',
    },
    min: {
        parameters: [
            {
                kind: 'column',
                columnTypes: validateForNumericAggregate([
                    'integer',
                    'number',
                    'duration',
                    'date',
                    'percentage',
                ]),
                defaultValue: 'transaction.duration',
                required: true,
            },
        ],
        outputType: null,
        isSortable: true,
        multiPlotType: 'line',
    },
    max: {
        parameters: [
            {
                kind: 'column',
                columnTypes: validateForNumericAggregate([
                    'integer',
                    'number',
                    'duration',
                    'date',
                    'percentage',
                ]),
                defaultValue: 'transaction.duration',
                required: true,
            },
        ],
        outputType: null,
        isSortable: true,
        multiPlotType: 'line',
    },
    sum: {
        parameters: [
            {
                kind: 'column',
                columnTypes: validateForNumericAggregate(['duration', 'number', 'percentage']),
                required: true,
                defaultValue: 'transaction.duration',
            },
        ],
        outputType: null,
        isSortable: true,
        multiPlotType: 'area',
    },
    any: {
        parameters: [
            {
                kind: 'column',
                columnTypes: ['string', 'integer', 'number', 'duration', 'date', 'boolean'],
                required: true,
                defaultValue: 'transaction.duration',
            },
        ],
        outputType: null,
        isSortable: true,
    },
    p50: {
        parameters: [
            {
                kind: 'column',
                columnTypes: validateForNumericAggregate(['duration', 'number', 'percentage']),
                defaultValue: 'transaction.duration',
                required: false,
            },
        ],
        outputType: null,
        isSortable: true,
        multiPlotType: 'line',
    },
    p75: {
        parameters: [
            {
                kind: 'column',
                columnTypes: validateForNumericAggregate(['duration', 'number', 'percentage']),
                defaultValue: 'transaction.duration',
                required: false,
            },
        ],
        outputType: null,
        isSortable: true,
        multiPlotType: 'line',
    },
    p95: {
        parameters: [
            {
                kind: 'column',
                columnTypes: validateForNumericAggregate(['duration', 'number', 'percentage']),
                defaultValue: 'transaction.duration',
                required: false,
            },
        ],
        outputType: null,
        type: [],
        isSortable: true,
        multiPlotType: 'line',
    },
    p99: {
        parameters: [
            {
                kind: 'column',
                columnTypes: validateForNumericAggregate(['duration', 'number', 'percentage']),
                defaultValue: 'transaction.duration',
                required: false,
            },
        ],
        outputType: null,
        isSortable: true,
        multiPlotType: 'line',
    },
    p100: {
        parameters: [
            {
                kind: 'column',
                columnTypes: validateForNumericAggregate(['duration', 'number', 'percentage']),
                defaultValue: 'transaction.duration',
                required: false,
            },
        ],
        outputType: null,
        isSortable: true,
        multiPlotType: 'line',
    },
    percentile: {
        parameters: [
            {
                kind: 'column',
                columnTypes: validateForNumericAggregate(['duration', 'number', 'percentage']),
                defaultValue: 'transaction.duration',
                required: true,
            },
            {
                kind: 'value',
                dataType: 'number',
                defaultValue: '0.5',
                required: true,
            },
        ],
        outputType: null,
        isSortable: true,
        multiPlotType: 'line',
    },
    avg: {
        parameters: [
            {
                kind: 'column',
                columnTypes: validateForNumericAggregate(['duration', 'number', 'percentage']),
                defaultValue: 'transaction.duration',
                required: true,
            },
        ],
        outputType: null,
        isSortable: true,
        multiPlotType: 'line',
    },
    apdex: {
        getFieldOverrides({ parameter, organization }) {
            var _a, _b;
            return {
                defaultValue: (_b = (_a = organization.apdexThreshold) === null || _a === void 0 ? void 0 : _a.toString()) !== null && _b !== void 0 ? _b : parameter.defaultValue,
            };
        },
        parameters: [
            {
                kind: 'value',
                dataType: 'number',
                defaultValue: '300',
                required: true,
            },
        ],
        outputType: 'number',
        isSortable: true,
        multiPlotType: 'line',
    },
    user_misery: {
        getFieldOverrides({ parameter, organization }) {
            var _a, _b;
            return {
                defaultValue: (_b = (_a = organization.apdexThreshold) === null || _a === void 0 ? void 0 : _a.toString()) !== null && _b !== void 0 ? _b : parameter.defaultValue,
            };
        },
        parameters: [
            {
                kind: 'value',
                dataType: 'number',
                defaultValue: '300',
                required: true,
            },
        ],
        outputType: 'number',
        isSortable: true,
        multiPlotType: 'area',
    },
    failure_rate: {
        parameters: [],
        outputType: 'percentage',
        isSortable: true,
        multiPlotType: 'line',
    },
    last_seen: {
        parameters: [],
        outputType: 'date',
        isSortable: true,
    },
};
// TPM and TPS are aliases that are only used in Performance
exports.ALIASES = {
    tpm: 'epm',
    tps: 'eps',
};
(0, utils_1.assert)(exports.AGGREGATIONS);
var FieldKey;
(function (FieldKey) {
    FieldKey["CULPRIT"] = "culprit";
    FieldKey["DEVICE_ARCH"] = "device.arch";
    FieldKey["DEVICE_BATTERY_LEVEL"] = "device.battery_level";
    FieldKey["DEVICE_BRAND"] = "device.brand";
    FieldKey["DEVICE_CHARGING"] = "device.charging";
    FieldKey["DEVICE_LOCALE"] = "device.locale";
    FieldKey["DEVICE_NAME"] = "device.name";
    FieldKey["DEVICE_ONLINE"] = "device.online";
    FieldKey["DEVICE_ORIENTATION"] = "device.orientation";
    FieldKey["DEVICE_SIMULATOR"] = "device.simulator";
    FieldKey["DEVICE_UUID"] = "device.uuid";
    FieldKey["DIST"] = "dist";
    FieldKey["ENVIRONMENT"] = "environment";
    FieldKey["ERROR_HANDLED"] = "error.handled";
    FieldKey["ERROR_UNHANDLED"] = "error.unhandled";
    FieldKey["ERROR_MECHANISM"] = "error.mechanism";
    FieldKey["ERROR_TYPE"] = "error.type";
    FieldKey["ERROR_VALUE"] = "error.value";
    FieldKey["EVENT_TYPE"] = "event.type";
    FieldKey["GEO_CITY"] = "geo.city";
    FieldKey["GEO_COUNTRY_CODE"] = "geo.country_code";
    FieldKey["GEO_REGION"] = "geo.region";
    FieldKey["HTTP_METHOD"] = "http.method";
    FieldKey["HTTP_REFERER"] = "http.referer";
    FieldKey["HTTP_URL"] = "http.url";
    FieldKey["ID"] = "id";
    FieldKey["ISSUE"] = "issue";
    FieldKey["LOCATION"] = "location";
    FieldKey["MESSAGE"] = "message";
    FieldKey["OS_BUILD"] = "os.build";
    FieldKey["OS_KERNEL_VERSION"] = "os.kernel_version";
    FieldKey["PLATFORM_NAME"] = "platform.name";
    FieldKey["PROJECT"] = "project";
    FieldKey["RELEASE"] = "release";
    FieldKey["SDK_NAME"] = "sdk.name";
    FieldKey["SDK_VERSION"] = "sdk.version";
    FieldKey["STACK_ABS_PATH"] = "stack.abs_path";
    FieldKey["STACK_COLNO"] = "stack.colno";
    FieldKey["STACK_FILENAME"] = "stack.filename";
    FieldKey["STACK_FUNCTION"] = "stack.function";
    FieldKey["STACK_IN_APP"] = "stack.in_app";
    FieldKey["STACK_LINENO"] = "stack.lineno";
    FieldKey["STACK_MODULE"] = "stack.module";
    FieldKey["STACK_PACKAGE"] = "stack.package";
    FieldKey["STACK_STACK_LEVEL"] = "stack.stack_level";
    FieldKey["TIMESTAMP"] = "timestamp";
    FieldKey["TIMESTAMP_TO_HOUR"] = "timestamp.to_hour";
    FieldKey["TIMESTAMP_TO_DAY"] = "timestamp.to_day";
    FieldKey["TITLE"] = "title";
    FieldKey["TRACE"] = "trace";
    FieldKey["TRACE_PARENT_SPAN"] = "trace.parent_span";
    FieldKey["TRACE_SPAN"] = "trace.span";
    FieldKey["TRANSACTION"] = "transaction";
    FieldKey["TRANSACTION_DURATION"] = "transaction.duration";
    FieldKey["TRANSACTION_OP"] = "transaction.op";
    FieldKey["TRANSACTION_STATUS"] = "transaction.status";
    FieldKey["USER_EMAIL"] = "user.email";
    FieldKey["USER_ID"] = "user.id";
    FieldKey["USER_IP"] = "user.ip";
    FieldKey["USER_USERNAME"] = "user.username";
    FieldKey["USER_DISPLAY"] = "user.display";
})(FieldKey || (FieldKey = {}));
/**
 * Refer to src/sentry/snuba/events.py, search for Columns
 */
exports.FIELDS = {
    [FieldKey.ID]: 'string',
    // issue.id and project.id are omitted on purpose.
    // Customers should use `issue` and `project` instead.
    [FieldKey.TIMESTAMP]: 'date',
    // time is omitted on purpose.
    // Customers should use `timestamp` or `timestamp.to_hour`.
    [FieldKey.TIMESTAMP_TO_HOUR]: 'date',
    [FieldKey.TIMESTAMP_TO_DAY]: 'date',
    [FieldKey.CULPRIT]: 'string',
    [FieldKey.LOCATION]: 'string',
    [FieldKey.MESSAGE]: 'string',
    [FieldKey.PLATFORM_NAME]: 'string',
    [FieldKey.ENVIRONMENT]: 'string',
    [FieldKey.RELEASE]: 'string',
    [FieldKey.DIST]: 'string',
    [FieldKey.TITLE]: 'string',
    [FieldKey.EVENT_TYPE]: 'string',
    // tags.key and tags.value are omitted on purpose as well.
    [FieldKey.TRANSACTION]: 'string',
    [FieldKey.USER_ID]: 'string',
    [FieldKey.USER_EMAIL]: 'string',
    [FieldKey.USER_USERNAME]: 'string',
    [FieldKey.USER_IP]: 'string',
    [FieldKey.SDK_NAME]: 'string',
    [FieldKey.SDK_VERSION]: 'string',
    [FieldKey.HTTP_METHOD]: 'string',
    [FieldKey.HTTP_REFERER]: 'string',
    [FieldKey.HTTP_URL]: 'string',
    [FieldKey.OS_BUILD]: 'string',
    [FieldKey.OS_KERNEL_VERSION]: 'string',
    [FieldKey.DEVICE_NAME]: 'string',
    [FieldKey.DEVICE_BRAND]: 'string',
    [FieldKey.DEVICE_LOCALE]: 'string',
    [FieldKey.DEVICE_UUID]: 'string',
    [FieldKey.DEVICE_ARCH]: 'string',
    [FieldKey.DEVICE_BATTERY_LEVEL]: 'number',
    [FieldKey.DEVICE_ORIENTATION]: 'string',
    [FieldKey.DEVICE_SIMULATOR]: 'boolean',
    [FieldKey.DEVICE_ONLINE]: 'boolean',
    [FieldKey.DEVICE_CHARGING]: 'boolean',
    [FieldKey.GEO_COUNTRY_CODE]: 'string',
    [FieldKey.GEO_REGION]: 'string',
    [FieldKey.GEO_CITY]: 'string',
    [FieldKey.ERROR_TYPE]: 'string',
    [FieldKey.ERROR_VALUE]: 'string',
    [FieldKey.ERROR_MECHANISM]: 'string',
    [FieldKey.ERROR_HANDLED]: 'boolean',
    [FieldKey.ERROR_UNHANDLED]: 'boolean',
    [FieldKey.STACK_ABS_PATH]: 'string',
    [FieldKey.STACK_FILENAME]: 'string',
    [FieldKey.STACK_PACKAGE]: 'string',
    [FieldKey.STACK_MODULE]: 'string',
    [FieldKey.STACK_FUNCTION]: 'string',
    [FieldKey.STACK_IN_APP]: 'boolean',
    [FieldKey.STACK_COLNO]: 'number',
    [FieldKey.STACK_LINENO]: 'number',
    [FieldKey.STACK_STACK_LEVEL]: 'number',
    // contexts.key and contexts.value omitted on purpose.
    // Transaction event fields.
    [FieldKey.TRANSACTION_DURATION]: 'duration',
    [FieldKey.TRANSACTION_OP]: 'string',
    [FieldKey.TRANSACTION_STATUS]: 'string',
    [FieldKey.TRACE]: 'string',
    [FieldKey.TRACE_SPAN]: 'string',
    [FieldKey.TRACE_PARENT_SPAN]: 'string',
    // Field alises defined in src/sentry/api/event_search.py
    [FieldKey.PROJECT]: 'string',
    [FieldKey.ISSUE]: 'string',
    [FieldKey.USER_DISPLAY]: 'string',
};
exports.DEPRECATED_FIELDS = [FieldKey.CULPRIT];
exports.FIELD_TAGS = Object.freeze(Object.fromEntries(Object.keys(exports.FIELDS).map(item => [item, { key: item, name: item }])));
exports.SEMVER_TAGS = {
    'release.version': {
        key: 'release.version',
        name: 'release.version',
    },
    'release.build': {
        key: 'release.build',
        name: 'release.build',
    },
    'release.package': {
        key: 'release.package',
        name: 'release.package',
    },
    'release.stage': {
        key: 'release.stage',
        name: 'release.stage',
        predefined: true,
        values: constants_1.RELEASE_ADOPTION_STAGES,
    },
};
var WebVital;
(function (WebVital) {
    WebVital["FP"] = "measurements.fp";
    WebVital["FCP"] = "measurements.fcp";
    WebVital["LCP"] = "measurements.lcp";
    WebVital["FID"] = "measurements.fid";
    WebVital["CLS"] = "measurements.cls";
    WebVital["TTFB"] = "measurements.ttfb";
    WebVital["RequestTime"] = "measurements.ttfb.requesttime";
})(WebVital = exports.WebVital || (exports.WebVital = {}));
var MobileVital;
(function (MobileVital) {
    MobileVital["AppStartCold"] = "measurements.app_start_cold";
    MobileVital["AppStartWarm"] = "measurements.app_start_warm";
    MobileVital["FramesTotal"] = "measurements.frames_total";
    MobileVital["FramesSlow"] = "measurements.frames_slow";
    MobileVital["FramesFrozen"] = "measurements.frames_frozen";
    MobileVital["FramesSlowRate"] = "measurements.frames_slow_rate";
    MobileVital["FramesFrozenRate"] = "measurements.frames_frozen_rate";
    MobileVital["StallCount"] = "measurements.stall_count";
    MobileVital["StallTotalTime"] = "measurements.stall_total_time";
    MobileVital["StallLongestTime"] = "measurements.stall_longest_time";
    MobileVital["StallPercentage"] = "measurements.stall_percentage";
})(MobileVital = exports.MobileVital || (exports.MobileVital = {}));
const MEASUREMENTS = {
    [WebVital.FP]: 'duration',
    [WebVital.FCP]: 'duration',
    [WebVital.LCP]: 'duration',
    [WebVital.FID]: 'duration',
    [WebVital.CLS]: 'number',
    [WebVital.TTFB]: 'duration',
    [WebVital.RequestTime]: 'duration',
    [MobileVital.AppStartCold]: 'duration',
    [MobileVital.AppStartWarm]: 'duration',
    [MobileVital.FramesTotal]: 'integer',
    [MobileVital.FramesSlow]: 'integer',
    [MobileVital.FramesFrozen]: 'integer',
    [MobileVital.FramesSlowRate]: 'percentage',
    [MobileVital.FramesFrozenRate]: 'percentage',
    [MobileVital.StallCount]: 'integer',
    [MobileVital.StallTotalTime]: 'duration',
    [MobileVital.StallLongestTime]: 'duration',
    [MobileVital.StallPercentage]: 'percentage',
};
function isSpanOperationBreakdownField(field) {
    return field.startsWith('spans.');
}
exports.isSpanOperationBreakdownField = isSpanOperationBreakdownField;
exports.SPAN_OP_RELATIVE_BREAKDOWN_FIELD = 'span_ops_breakdown.relative';
function isRelativeSpanOperationBreakdownField(field) {
    return field === exports.SPAN_OP_RELATIVE_BREAKDOWN_FIELD;
}
exports.isRelativeSpanOperationBreakdownField = isRelativeSpanOperationBreakdownField;
exports.SPAN_OP_BREAKDOWN_FIELDS = [
    'spans.http',
    'spans.db',
    'spans.browser',
    'spans.resource',
];
// This list contains fields/functions that are available with performance-view feature.
exports.TRACING_FIELDS = [
    'avg',
    'sum',
    'transaction.duration',
    'transaction.op',
    'transaction.status',
    'p50',
    'p75',
    'p95',
    'p99',
    'p100',
    'percentile',
    'failure_rate',
    'apdex',
    'count_miserable',
    'user_misery',
    'eps',
    'epm',
    'team_key_transaction',
    ...Object.keys(MEASUREMENTS),
    ...exports.SPAN_OP_BREAKDOWN_FIELDS,
    exports.SPAN_OP_RELATIVE_BREAKDOWN_FIELD,
];
exports.MEASUREMENT_PATTERN = /^measurements\.([a-zA-Z0-9-_.]+)$/;
exports.SPAN_OP_BREAKDOWN_PATTERN = /^spans\.([a-zA-Z0-9-_.]+)$/;
function isMeasurement(field) {
    const results = field.match(exports.MEASUREMENT_PATTERN);
    return !!results;
}
exports.isMeasurement = isMeasurement;
function measurementType(field) {
    if (MEASUREMENTS.hasOwnProperty(field)) {
        return MEASUREMENTS[field];
    }
    return 'number';
}
exports.measurementType = measurementType;
function getMeasurementSlug(field) {
    const results = field.match(exports.MEASUREMENT_PATTERN);
    if (results && results.length >= 2) {
        return results[1];
    }
    return null;
}
exports.getMeasurementSlug = getMeasurementSlug;
const AGGREGATE_PATTERN = /^(\w+)\((.*)?\)$/;
// Identical to AGGREGATE_PATTERN, but without the $ for newline, or ^ for start of line
const AGGREGATE_BASE = /(\w+)\((.*)?\)/g;
function getAggregateArg(field) {
    // only returns the first argument if field is an aggregate
    const result = parseFunction(field);
    if (result && result.arguments.length > 0) {
        return result.arguments[0];
    }
    return null;
}
exports.getAggregateArg = getAggregateArg;
function parseFunction(field) {
    const results = field.match(AGGREGATE_PATTERN);
    if (results && results.length === 3) {
        return {
            name: results[1],
            arguments: parseArguments(results[1], results[2]),
        };
    }
    return null;
}
exports.parseFunction = parseFunction;
function parseArguments(functionText, columnText) {
    // Some functions take a quoted string for their arguments that may contain commas
    // This function attempts to be identical with the similarly named parse_arguments
    // found in src/sentry/search/events/fields.py
    if ((functionText !== 'to_other' && functionText !== 'count_if') ||
        columnText.length === 0) {
        return columnText ? columnText.split(',').map(result => result.trim()) : [];
    }
    const args = [];
    let quoted = false;
    let escaped = false;
    let i = 0;
    let j = 0;
    while (j < columnText.length) {
        if (i === j && columnText[j] === '"') {
            // when we see a quote at the beginning of
            // an argument, then this is a quoted string
            quoted = true;
        }
        else if (i === j && columnText[j] === ' ') {
            // argument has leading spaces, skip over them
            i += 1;
        }
        else if (quoted && !escaped && columnText[j] === '\\') {
            // when we see a slash inside a quoted string,
            // the next character is an escape character
            escaped = true;
        }
        else if (quoted && !escaped && columnText[j] === '"') {
            // when we see a non-escaped quote while inside
            // of a quoted string, we should end it
            quoted = false;
        }
        else if (quoted && escaped) {
            // when we are inside a quoted string and have
            // begun an escape character, we should end it
            escaped = false;
        }
        else if (quoted && columnText[j] === ',') {
            // when we are inside a quoted string and see
            // a comma, it should not be considered an
            // argument separator
        }
        else if (columnText[j] === ',') {
            // when we see a comma outside of a quoted string
            // it is an argument separator
            args.push(columnText.substring(i, j).trim());
            i = j + 1;
        }
        j += 1;
    }
    if (i !== j) {
        // add in the last argument if any
        args.push(columnText.substring(i).trim());
    }
    return args;
}
exports.parseArguments = parseArguments;
// `|` is an invalid field character, so it is used to determine whether a field is an equation or not
const EQUATION_PREFIX = 'equation|';
const EQUATION_ALIAS_PATTERN = /^equation\[(\d+)\]$/;
function isEquation(field) {
    return field.startsWith(EQUATION_PREFIX);
}
exports.isEquation = isEquation;
function isEquationAlias(field) {
    return EQUATION_ALIAS_PATTERN.test(field);
}
exports.isEquationAlias = isEquationAlias;
function maybeEquationAlias(field) {
    return field.includes(EQUATION_PREFIX);
}
exports.maybeEquationAlias = maybeEquationAlias;
function stripEquationPrefix(field) {
    return field.replace(EQUATION_PREFIX, '');
}
exports.stripEquationPrefix = stripEquationPrefix;
function getEquationAliasIndex(field) {
    const results = field.match(EQUATION_ALIAS_PATTERN);
    if (results && results.length === 2) {
        return parseInt(results[1], 10);
    }
    return -1;
}
exports.getEquationAliasIndex = getEquationAliasIndex;
function getEquation(field) {
    return field.slice(EQUATION_PREFIX.length);
}
exports.getEquation = getEquation;
function isAggregateEquation(field) {
    const results = field.match(AGGREGATE_BASE);
    return isEquation(field) && results !== null && results.length > 0;
}
exports.isAggregateEquation = isAggregateEquation;
function isLegalEquationColumn(column) {
    // Any isn't allowed in arithmetic
    if (column.kind === 'function' && column.function[0] === 'any') {
        return false;
    }
    const columnType = getColumnType(column);
    return columnType === 'number' || columnType === 'integer' || columnType === 'duration';
}
exports.isLegalEquationColumn = isLegalEquationColumn;
function generateAggregateFields(organization, eventFields, excludeFields = []) {
    const functions = Object.keys(exports.AGGREGATIONS);
    const fields = Object.values(eventFields).map(field => field.field);
    functions.forEach(func => {
        const parameters = exports.AGGREGATIONS[func].parameters.map(param => {
            const overrides = exports.AGGREGATIONS[func].getFieldOverrides;
            if (typeof overrides === 'undefined') {
                return param;
            }
            return Object.assign(Object.assign({}, param), overrides({ parameter: param, organization }));
        });
        if (parameters.every(param => typeof param.defaultValue !== 'undefined')) {
            const newField = `${func}(${parameters
                .map(param => param.defaultValue)
                .join(',')})`;
            if (fields.indexOf(newField) === -1 && excludeFields.indexOf(newField) === -1) {
                fields.push(newField);
            }
        }
    });
    return fields.map(field => ({ field }));
}
exports.generateAggregateFields = generateAggregateFields;
function explodeFieldString(field) {
    var _a;
    if (isEquation(field)) {
        return { kind: 'equation', field: getEquation(field) };
    }
    const results = parseFunction(field);
    if (results) {
        return {
            kind: 'function',
            function: [
                results.name,
                (_a = results.arguments[0]) !== null && _a !== void 0 ? _a : '',
                results.arguments[1],
                results.arguments[2],
            ],
        };
    }
    return { kind: 'field', field };
}
exports.explodeFieldString = explodeFieldString;
function generateFieldAsString(value) {
    if (value.kind === 'field') {
        return value.field;
    }
    else if (value.kind === 'equation') {
        return `${EQUATION_PREFIX}${value.field}`;
    }
    const aggregation = value.function[0];
    const parameters = value.function.slice(1).filter(i => i);
    return `${aggregation}(${parameters.join(',')})`;
}
exports.generateFieldAsString = generateFieldAsString;
function explodeField(field) {
    const results = explodeFieldString(field.field);
    return results;
}
exports.explodeField = explodeField;
/**
 * Get the alias that the API results will have for a given aggregate function name
 */
function getAggregateAlias(field) {
    const result = parseFunction(field);
    if (!result) {
        return field;
    }
    let alias = result.name;
    if (result.arguments.length > 0) {
        alias += '_' + result.arguments.join('_');
    }
    return alias.replace(/[^\w]/g, '_').replace(/^_+/g, '').replace(/_+$/, '');
}
exports.getAggregateAlias = getAggregateAlias;
/**
 * Check if a field name looks like an aggregate function or known aggregate alias.
 */
function isAggregateField(field) {
    return parseFunction(field) !== null;
}
exports.isAggregateField = isAggregateField;
function isAggregateFieldOrEquation(field) {
    return isAggregateField(field) || isAggregateEquation(field);
}
exports.isAggregateFieldOrEquation = isAggregateFieldOrEquation;
function getAggregateFields(fields) {
    return fields.filter(field => isAggregateField(field) || isAggregateEquation(field));
}
exports.getAggregateFields = getAggregateFields;
/**
 * Convert a function string into type it will output.
 * This is useful when you need to format values in tooltips,
 * or in series markers.
 */
function aggregateOutputType(field) {
    const result = parseFunction(field);
    if (!result) {
        return 'number';
    }
    const outputType = aggregateFunctionOutputType(result.name, result.arguments[0]);
    if (outputType === null) {
        return 'number';
    }
    return outputType;
}
exports.aggregateOutputType = aggregateOutputType;
/**
 * Converts a function string and its first argument into its output type.
 * - If the function has a fixed output type, that will be the result.
 * - If the function does not define an output type, the output type will be equal to
 *   the type of its first argument.
 * - If the function has an optional first argument, and it was not defined, make sure
 *   to use the default argument as the first argument.
 * - If the type could not be determined, return null.
 */
function aggregateFunctionOutputType(funcName, firstArg) {
    var _a;
    const aggregate = exports.AGGREGATIONS[exports.ALIASES[funcName] || funcName];
    // Attempt to use the function's outputType.
    if (aggregate === null || aggregate === void 0 ? void 0 : aggregate.outputType) {
        return aggregate.outputType;
    }
    // If the first argument is undefined and it is not required,
    // then we attempt to get the default value.
    if (!firstArg && ((_a = aggregate === null || aggregate === void 0 ? void 0 : aggregate.parameters) === null || _a === void 0 ? void 0 : _a[0])) {
        if (aggregate.parameters[0].required === false) {
            firstArg = aggregate.parameters[0].defaultValue;
        }
    }
    // If the function is an inherit type it will have a field as
    // the first parameter and we can use that to get the type.
    if (firstArg && exports.FIELDS.hasOwnProperty(firstArg)) {
        return exports.FIELDS[firstArg];
    }
    else if (firstArg && isMeasurement(firstArg)) {
        return measurementType(firstArg);
    }
    else if (firstArg && isSpanOperationBreakdownField(firstArg)) {
        return 'duration';
    }
    return null;
}
exports.aggregateFunctionOutputType = aggregateFunctionOutputType;
/**
 * Get the multi-series chart type for an aggregate function.
 */
function aggregateMultiPlotType(field) {
    if (isEquation(field)) {
        return 'line';
    }
    const result = parseFunction(field);
    // Handle invalid data.
    if (!result) {
        return 'area';
    }
    if (!exports.AGGREGATIONS.hasOwnProperty(result.name)) {
        return 'area';
    }
    return exports.AGGREGATIONS[result.name].multiPlotType;
}
exports.aggregateMultiPlotType = aggregateMultiPlotType;
function validateForNumericAggregate(validColumnTypes) {
    return function ({ name, dataType }) {
        // these built-in columns cannot be applied to numeric aggregates such as percentile(...)
        if ([
            FieldKey.DEVICE_BATTERY_LEVEL,
            FieldKey.STACK_COLNO,
            FieldKey.STACK_LINENO,
            FieldKey.STACK_STACK_LEVEL,
        ].includes(name)) {
            return false;
        }
        return validColumnTypes.includes(dataType);
    };
}
function validateDenyListColumns(validColumnTypes, deniedColumns) {
    return function ({ name, dataType }) {
        return validColumnTypes.includes(dataType) && !deniedColumns.includes(name);
    };
}
function validateAllowedColumns(validColumns) {
    return function ({ name }) {
        return validColumns.includes(name);
    };
}
const alignedTypes = ['number', 'duration', 'integer', 'percentage'];
function fieldAlignment(columnName, columnType, metadata) {
    let align = 'left';
    if (columnType) {
        align = alignedTypes.includes(columnType) ? 'right' : 'left';
    }
    if (columnType === undefined || columnType === 'never') {
        // fallback to align the column based on the table metadata
        const maybeType = metadata ? metadata[getAggregateAlias(columnName)] : undefined;
        if (maybeType !== undefined && alignedTypes.includes(maybeType)) {
            align = 'right';
        }
    }
    return align;
}
exports.fieldAlignment = fieldAlignment;
/**
 * Match on types that are legal to show on a timeseries chart.
 */
function isLegalYAxisType(match) {
    return ['number', 'integer', 'duration', 'percentage'].includes(match);
}
exports.isLegalYAxisType = isLegalYAxisType;
function getSpanOperationName(field) {
    const results = field.match(exports.SPAN_OP_BREAKDOWN_PATTERN);
    if (results && results.length >= 2) {
        return results[1];
    }
    return null;
}
exports.getSpanOperationName = getSpanOperationName;
function getColumnType(column) {
    if (column.kind === 'function') {
        const outputType = aggregateFunctionOutputType(column.function[0], column.function[1]);
        if (outputType !== null) {
            return outputType;
        }
    }
    else if (column.kind === 'field') {
        if (exports.FIELDS.hasOwnProperty(column.field)) {
            return exports.FIELDS[column.field];
        }
        else if (isMeasurement(column.field)) {
            return measurementType(column.field);
        }
        else if (isSpanOperationBreakdownField(column.field)) {
            return 'duration';
        }
    }
    return 'string';
}
exports.getColumnType = getColumnType;
function hasDuplicate(columnList, column) {
    if (column.kind !== 'function' && column.kind !== 'field') {
        return false;
    }
    return columnList.filter(newColumn => (0, isEqual_1.default)(newColumn, column)).length > 1;
}
exports.hasDuplicate = hasDuplicate;
//# sourceMappingURL=fields.jsx.map