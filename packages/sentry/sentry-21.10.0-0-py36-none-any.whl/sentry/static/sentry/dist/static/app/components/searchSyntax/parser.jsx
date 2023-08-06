Object.defineProperty(exports, "__esModule", { value: true });
exports.parseSearch = exports.TokenConverter = exports.filterTypeConfig = exports.interchangeableFilterOperators = exports.FilterType = exports.BooleanOperator = exports.TermOperator = exports.Token = void 0;
const tslib_1 = require("tslib");
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const locale_1 = require("app/locale");
const fields_1 = require("app/utils/discover/fields");
const grammar_pegjs_1 = (0, tslib_1.__importDefault)(require("./grammar.pegjs"));
const utils_1 = require("./utils");
const listJoiner = ([s1, comma, s2, _, value]) => ({
    separator: [s1.value, comma, s2.value].join(''),
    value,
});
/**
 * A token represents a node in the syntax tree. These are all extrapolated
 * from the grammar and may not be named exactly the same.
 */
var Token;
(function (Token) {
    Token["Spaces"] = "spaces";
    Token["Filter"] = "filter";
    Token["FreeText"] = "freeText";
    Token["LogicGroup"] = "logicGroup";
    Token["LogicBoolean"] = "logicBoolean";
    Token["KeySimple"] = "keySimple";
    Token["KeyExplicitTag"] = "keyExplicitTag";
    Token["KeyAggregate"] = "keyAggregate";
    Token["KeyAggregateArgs"] = "keyAggregateArgs";
    Token["KeyAggregateParam"] = "keyAggregateParam";
    Token["ValueIso8601Date"] = "valueIso8601Date";
    Token["ValueRelativeDate"] = "valueRelativeDate";
    Token["ValueDuration"] = "valueDuration";
    Token["ValuePercentage"] = "valuePercentage";
    Token["ValueBoolean"] = "valueBoolean";
    Token["ValueNumber"] = "valueNumber";
    Token["ValueText"] = "valueText";
    Token["ValueNumberList"] = "valueNumberList";
    Token["ValueTextList"] = "valueTextList";
})(Token = exports.Token || (exports.Token = {}));
/**
 * An operator in a key value term
 */
var TermOperator;
(function (TermOperator) {
    TermOperator["Default"] = "";
    TermOperator["GreaterThanEqual"] = ">=";
    TermOperator["LessThanEqual"] = "<=";
    TermOperator["GreaterThan"] = ">";
    TermOperator["LessThan"] = "<";
    TermOperator["Equal"] = "=";
    TermOperator["NotEqual"] = "!=";
})(TermOperator = exports.TermOperator || (exports.TermOperator = {}));
/**
 * Logic operators
 */
var BooleanOperator;
(function (BooleanOperator) {
    BooleanOperator["And"] = "AND";
    BooleanOperator["Or"] = "OR";
})(BooleanOperator = exports.BooleanOperator || (exports.BooleanOperator = {}));
/**
 * The Token.Filter may be one of many types of filters. This enum declares the
 * each variant filter type.
 */
var FilterType;
(function (FilterType) {
    FilterType["Text"] = "text";
    FilterType["TextIn"] = "textIn";
    FilterType["Date"] = "date";
    FilterType["SpecificDate"] = "specificDate";
    FilterType["RelativeDate"] = "relativeDate";
    FilterType["Duration"] = "duration";
    FilterType["Numeric"] = "numeric";
    FilterType["NumericIn"] = "numericIn";
    FilterType["Boolean"] = "boolean";
    FilterType["AggregateDuration"] = "aggregateDuration";
    FilterType["AggregatePercentage"] = "aggregatePercentage";
    FilterType["AggregateNumeric"] = "aggregateNumeric";
    FilterType["AggregateDate"] = "aggregateDate";
    FilterType["AggregateRelativeDate"] = "aggregateRelativeDate";
    FilterType["Has"] = "has";
    FilterType["Is"] = "is";
})(FilterType = exports.FilterType || (exports.FilterType = {}));
const allOperators = [
    TermOperator.Default,
    TermOperator.GreaterThanEqual,
    TermOperator.LessThanEqual,
    TermOperator.GreaterThan,
    TermOperator.LessThan,
    TermOperator.Equal,
    TermOperator.NotEqual,
];
const basicOperators = [TermOperator.Default, TermOperator.NotEqual];
/**
 * Map of certain filter types to other filter types with applicable operators
 * e.g. SpecificDate can use the operators from Date to become a Date filter.
 */
exports.interchangeableFilterOperators = {
    [FilterType.SpecificDate]: [FilterType.Date],
    [FilterType.Date]: [FilterType.SpecificDate],
};
const textKeys = [Token.KeySimple, Token.KeyExplicitTag];
const numberUnits = {
    b: 1000000000,
    m: 1000000,
    k: 1000,
};
/**
 * This constant-type configuration object declares how each filter type
 * operates. Including what types of keys, operators, and values it may
 * receive.
 *
 * This configuration is used to generate the discriminate Filter type that is
 * returned from the tokenFilter converter.
 */
exports.filterTypeConfig = {
    [FilterType.Text]: {
        validKeys: textKeys,
        validOps: basicOperators,
        validValues: [Token.ValueText],
        canNegate: true,
    },
    [FilterType.TextIn]: {
        validKeys: textKeys,
        validOps: [],
        validValues: [Token.ValueTextList],
        canNegate: true,
    },
    [FilterType.Date]: {
        validKeys: [Token.KeySimple],
        validOps: allOperators,
        validValues: [Token.ValueIso8601Date],
        canNegate: false,
    },
    [FilterType.SpecificDate]: {
        validKeys: [Token.KeySimple],
        validOps: [],
        validValues: [Token.ValueIso8601Date],
        canNegate: false,
    },
    [FilterType.RelativeDate]: {
        validKeys: [Token.KeySimple],
        validOps: [],
        validValues: [Token.ValueRelativeDate],
        canNegate: false,
    },
    [FilterType.Duration]: {
        validKeys: [Token.KeySimple],
        validOps: allOperators,
        validValues: [Token.ValueDuration],
        canNegate: false,
    },
    [FilterType.Numeric]: {
        validKeys: [Token.KeySimple],
        validOps: allOperators,
        validValues: [Token.ValueNumber],
        canNegate: false,
    },
    [FilterType.NumericIn]: {
        validKeys: [Token.KeySimple],
        validOps: [],
        validValues: [Token.ValueNumberList],
        canNegate: false,
    },
    [FilterType.Boolean]: {
        validKeys: [Token.KeySimple],
        validOps: basicOperators,
        validValues: [Token.ValueBoolean],
        canNegate: true,
    },
    [FilterType.AggregateDuration]: {
        validKeys: [Token.KeyAggregate],
        validOps: allOperators,
        validValues: [Token.ValueDuration],
        canNegate: true,
    },
    [FilterType.AggregateNumeric]: {
        validKeys: [Token.KeyAggregate],
        validOps: allOperators,
        validValues: [Token.ValueNumber],
        canNegate: true,
    },
    [FilterType.AggregatePercentage]: {
        validKeys: [Token.KeyAggregate],
        validOps: allOperators,
        validValues: [Token.ValuePercentage],
        canNegate: true,
    },
    [FilterType.AggregateDate]: {
        validKeys: [Token.KeyAggregate],
        validOps: allOperators,
        validValues: [Token.ValueIso8601Date],
        canNegate: true,
    },
    [FilterType.AggregateRelativeDate]: {
        validKeys: [Token.KeyAggregate],
        validOps: allOperators,
        validValues: [Token.ValueRelativeDate],
        canNegate: true,
    },
    [FilterType.Has]: {
        validKeys: [Token.KeySimple],
        validOps: basicOperators,
        validValues: [],
        canNegate: true,
    },
    [FilterType.Is]: {
        validKeys: [Token.KeySimple],
        validOps: basicOperators,
        validValues: [Token.ValueText],
        canNegate: true,
    },
};
/**
 * Used to construct token results via the token grammar
 */
class TokenConverter {
    constructor({ text, location, config }) {
        /**
         * Validates various types of keys
         */
        this.keyValidation = {
            isNumeric: (key) => this.config.numericKeys.has(key) ||
                (0, fields_1.isMeasurement)(key) ||
                (0, fields_1.isSpanOperationBreakdownField)(key),
            isBoolean: (key) => this.config.booleanKeys.has(key),
            isPercentage: (key) => this.config.percentageKeys.has(key),
            isDate: (key) => this.config.dateKeys.has(key),
            isDuration: (key) => this.config.durationKeys.has(key) ||
                (0, fields_1.isSpanOperationBreakdownField)(key) ||
                (0, fields_1.measurementType)(key) === 'duration',
        };
        this.tokenSpaces = (value) => (Object.assign(Object.assign({}, this.defaultTokenFields), { type: Token.Spaces, value }));
        this.tokenFilter = (filter, key, value, operator, negated) => {
            const filterToken = {
                type: Token.Filter,
                filter,
                key,
                value,
                negated,
                operator: operator !== null && operator !== void 0 ? operator : TermOperator.Default,
                invalid: this.checkInvalidFilter(filter, key, value),
            };
            return Object.assign(Object.assign({}, this.defaultTokenFields), filterToken);
        };
        this.tokenFreeText = (value, quoted) => (Object.assign(Object.assign({}, this.defaultTokenFields), { type: Token.FreeText, value,
            quoted }));
        this.tokenLogicGroup = (inner) => (Object.assign(Object.assign({}, this.defaultTokenFields), { type: Token.LogicGroup, inner }));
        this.tokenLogicBoolean = (bool) => (Object.assign(Object.assign({}, this.defaultTokenFields), { type: Token.LogicBoolean, value: bool }));
        this.tokenKeySimple = (value, quoted) => (Object.assign(Object.assign({}, this.defaultTokenFields), { type: Token.KeySimple, value,
            quoted }));
        this.tokenKeyExplicitTag = (prefix, key) => (Object.assign(Object.assign({}, this.defaultTokenFields), { type: Token.KeyExplicitTag, prefix,
            key }));
        this.tokenKeyAggregateParam = (value, quoted) => (Object.assign(Object.assign({}, this.defaultTokenFields), { type: Token.KeyAggregateParam, value,
            quoted }));
        this.tokenKeyAggregate = (name, args, argsSpaceBefore, argsSpaceAfter) => (Object.assign(Object.assign({}, this.defaultTokenFields), { type: Token.KeyAggregate, name,
            args,
            argsSpaceBefore,
            argsSpaceAfter }));
        this.tokenKeyAggregateArgs = (arg1, args) => (Object.assign(Object.assign({}, this.defaultTokenFields), { type: Token.KeyAggregateArgs, args: [{ separator: '', value: arg1 }, ...args.map(listJoiner)] }));
        this.tokenValueIso8601Date = (value) => (Object.assign(Object.assign({}, this.defaultTokenFields), { type: Token.ValueIso8601Date, value: (0, moment_1.default)(value) }));
        this.tokenValueRelativeDate = (value, sign, unit) => (Object.assign(Object.assign({}, this.defaultTokenFields), { type: Token.ValueRelativeDate, value: Number(value), sign,
            unit }));
        this.tokenValueDuration = (value, unit) => (Object.assign(Object.assign({}, this.defaultTokenFields), { type: Token.ValueDuration, value: Number(value), unit }));
        this.tokenValuePercentage = (value) => (Object.assign(Object.assign({}, this.defaultTokenFields), { type: Token.ValuePercentage, value: Number(value) }));
        this.tokenValueBoolean = (value) => (Object.assign(Object.assign({}, this.defaultTokenFields), { type: Token.ValueBoolean, value: ['1', 'true'].includes(value.toLowerCase()) }));
        this.tokenValueNumber = (value, unit) => {
            var _a;
            return (Object.assign(Object.assign({}, this.defaultTokenFields), { type: Token.ValueNumber, value, rawValue: Number(value) * ((_a = numberUnits[unit]) !== null && _a !== void 0 ? _a : 1), unit }));
        };
        this.tokenValueNumberList = (item1, items) => (Object.assign(Object.assign({}, this.defaultTokenFields), { type: Token.ValueNumberList, items: [{ separator: '', value: item1 }, ...items.map(listJoiner)] }));
        this.tokenValueTextList = (item1, items) => (Object.assign(Object.assign({}, this.defaultTokenFields), { type: Token.ValueTextList, items: [{ separator: '', value: item1 }, ...items.map(listJoiner)] }));
        this.tokenValueText = (value, quoted) => (Object.assign(Object.assign({}, this.defaultTokenFields), { type: Token.ValueText, value,
            quoted }));
        /**
         * This method is used while tokenizing to predicate whether a filter should
         * match or not. We do this because not all keys are valid for specific
         * filter types. For example, boolean filters should only match for keys
         * which can be filtered as booleans.
         *
         * See [0] and look for &{ predicate } to understand how predicates are
         * declared in the grammar
         *
         * [0]:https://pegjs.org/documentation
         */
        this.predicateFilter = (type, key) => {
            const keyName = (0, utils_1.getKeyName)(key);
            const aggregateKey = key;
            const { isNumeric, isDuration, isBoolean, isDate, isPercentage } = this.keyValidation;
            const checkAggregate = (check) => { var _a; return (_a = aggregateKey.args) === null || _a === void 0 ? void 0 : _a.args.some(arg => { var _a, _b; return check((_b = (_a = arg === null || arg === void 0 ? void 0 : arg.value) === null || _a === void 0 ? void 0 : _a.value) !== null && _b !== void 0 ? _b : ''); }); };
            switch (type) {
                case FilterType.Numeric:
                case FilterType.NumericIn:
                    return isNumeric(keyName);
                case FilterType.Duration:
                    return isDuration(keyName);
                case FilterType.Boolean:
                    return isBoolean(keyName);
                case FilterType.Date:
                case FilterType.RelativeDate:
                case FilterType.SpecificDate:
                    return isDate(keyName);
                case FilterType.AggregateDuration:
                    return checkAggregate(isDuration);
                case FilterType.AggregateDate:
                    return checkAggregate(isDate);
                case FilterType.AggregatePercentage:
                    return checkAggregate(isPercentage);
                default:
                    return true;
            }
        };
        /**
         * Predicates weather a text filter have operators for specific keys.
         */
        this.predicateTextOperator = (key) => this.config.textOperatorKeys.has((0, utils_1.getKeyName)(key));
        /**
         * Checks a filter against some non-grammar validation rules
         */
        this.checkInvalidFilter = (filter, key, value) => {
            // Text filter is the "fall through" filter that will match when other
            // filter predicates fail.
            if (filter === FilterType.Text) {
                return this.checkInvalidTextFilter(key, value);
            }
            if (filter === FilterType.Is || filter === FilterType.Has) {
                return this.checkInvalidTextValue(value);
            }
            if ([FilterType.TextIn, FilterType.NumericIn].includes(filter)) {
                return this.checkInvalidInFilter(value);
            }
            return null;
        };
        /**
         * Validates text filters which may have failed predication
         */
        this.checkInvalidTextFilter = (key, value) => {
            // Explicit tag keys will always be treated as text filters
            if (key.type === Token.KeyExplicitTag) {
                return this.checkInvalidTextValue(value);
            }
            const keyName = (0, utils_1.getKeyName)(key);
            if (this.keyValidation.isDuration(keyName)) {
                return {
                    reason: (0, locale_1.t)('Invalid duration. Expected number followed by duration unit suffix'),
                    expectedType: [FilterType.Duration],
                };
            }
            if (this.keyValidation.isDate(keyName)) {
                const date = new Date();
                date.setSeconds(0);
                date.setMilliseconds(0);
                const example = date.toISOString();
                return {
                    reason: (0, locale_1.t)('Invalid date format. Expected +/-duration (e.g. +1h) or ISO 8601-like (e.g. %s or %s)', example.slice(0, 10), example),
                    expectedType: [FilterType.Date, FilterType.SpecificDate, FilterType.RelativeDate],
                };
            }
            if (this.keyValidation.isBoolean(keyName)) {
                return {
                    reason: (0, locale_1.t)('Invalid boolean. Expected true, 1, false, or 0.'),
                    expectedType: [FilterType.Boolean],
                };
            }
            if (this.keyValidation.isNumeric(keyName)) {
                return {
                    reason: (0, locale_1.t)('Invalid number. Expected number then optional k, m, or b suffix (e.g. 500k)'),
                    expectedType: [FilterType.Numeric, FilterType.NumericIn],
                };
            }
            return this.checkInvalidTextValue(value);
        };
        /**
         * Validates the value of a text filter
         */
        this.checkInvalidTextValue = (value) => {
            if (!value.quoted && /(^|[^\\])"/.test(value.value)) {
                return { reason: (0, locale_1.t)('Quotes must enclose text or be escaped') };
            }
            if (!value.quoted && value.value === '') {
                return { reason: (0, locale_1.t)('Filter must have a value') };
            }
            return null;
        };
        /**
         * Validates IN filter values do not have an missing elements
         */
        this.checkInvalidInFilter = ({ items }) => {
            const hasEmptyValue = items.some(item => item.value === null);
            if (hasEmptyValue) {
                return { reason: (0, locale_1.t)('Lists should not have empty values') };
            }
            return null;
        };
        this.text = text;
        this.location = location;
        this.config = config;
    }
    /**
     * Creates shared `text` and `location` keys.
     */
    get defaultTokenFields() {
        return {
            text: this.text(),
            location: this.location(),
        };
    }
}
exports.TokenConverter = TokenConverter;
const defaultConfig = {
    textOperatorKeys: new Set([
        'release.version',
        'release.build',
        'release.package',
        'release.stage',
    ]),
    durationKeys: new Set(['transaction.duration']),
    percentageKeys: new Set(['percentage']),
    numericKeys: new Set([
        'project_id',
        'project.id',
        'issue.id',
        'stack.colno',
        'stack.lineno',
        'stack.stack_level',
        'transaction.duration',
        'apdex',
        'p75',
        'p95',
        'p99',
        'failure_rate',
        'count_miserable',
        'user_misery',
        'count_miserable_new',
        'user_miser_new',
    ]),
    dateKeys: new Set([
        'start',
        'end',
        'first_seen',
        'last_seen',
        'time',
        'event.timestamp',
        'timestamp',
        'timestamp.to_hour',
        'timestamp.to_day',
        'transaction.start_time',
        'transaction.end_time',
    ]),
    booleanKeys: new Set([
        'error.handled',
        'error.unhandled',
        'stack.in_app',
        'team_key_transaction',
    ]),
    allowBoolean: true,
};
const options = {
    TokenConverter,
    TermOperator,
    FilterType,
    config: defaultConfig,
};
/**
 * Parse a search query into a ParseResult. Failing to parse the search query
 * will result in null.
 */
function parseSearch(query) {
    try {
        return grammar_pegjs_1.default.parse(query, options);
    }
    catch (e) {
        // TODO(epurkhiser): Should we capture these errors somewhere?
    }
    return null;
}
exports.parseSearch = parseSearch;
//# sourceMappingURL=parser.jsx.map