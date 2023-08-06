Object.defineProperty(exports, "__esModule", { value: true });
exports.getParams = exports.parseStatsPeriod = void 0;
const tslib_1 = require("tslib");
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const constants_1 = require("app/constants");
const utils_1 = require("app/utils");
const STATS_PERIOD_PATTERN = '^(\\d+)([hdmsw])?$';
function parseStatsPeriod(input) {
    const result = input.match(STATS_PERIOD_PATTERN);
    if (!result) {
        return undefined;
    }
    const period = result[1];
    let periodLength = result[2];
    if (!periodLength) {
        // default to seconds.
        // this behaviour is based on src/sentry/utils/dates.py
        periodLength = 's';
    }
    return {
        period,
        periodLength,
    };
}
exports.parseStatsPeriod = parseStatsPeriod;
function coerceStatsPeriod(input) {
    const result = parseStatsPeriod(input);
    if (!result) {
        return undefined;
    }
    const { period, periodLength } = result;
    return `${period}${periodLength}`;
}
function getStatsPeriodValue(maybe) {
    if (Array.isArray(maybe)) {
        if (maybe.length <= 0) {
            return undefined;
        }
        const result = maybe.find(coerceStatsPeriod);
        if (!result) {
            return undefined;
        }
        return coerceStatsPeriod(result);
    }
    if (typeof maybe === 'string') {
        return coerceStatsPeriod(maybe);
    }
    return undefined;
}
// We normalize potential datetime strings into the form that would be valid
// if it were to be parsed by datetime.strptime using the format %Y-%m-%dT%H:%M:%S.%f
// This format was transformed to the form that moment.js understands using
// https://gist.github.com/asafge/0b13c5066d06ae9a4446
const normalizeDateTimeString = (input) => {
    if (!input) {
        return undefined;
    }
    const parsed = moment_1.default.utc(input);
    if (!parsed.isValid()) {
        return undefined;
    }
    return parsed.format('YYYY-MM-DDTHH:mm:ss.SSS');
};
const getDateTimeString = (maybe) => {
    if (Array.isArray(maybe)) {
        if (maybe.length <= 0) {
            return undefined;
        }
        const result = maybe.find(needle => moment_1.default.utc(needle).isValid());
        return normalizeDateTimeString(result);
    }
    return normalizeDateTimeString(maybe);
};
const parseUtcValue = (utc) => {
    if ((0, utils_1.defined)(utc)) {
        return utc === true || utc === 'true' ? 'true' : 'false';
    }
    return undefined;
};
const getUtcValue = (maybe) => {
    if (Array.isArray(maybe)) {
        if (maybe.length <= 0) {
            return undefined;
        }
        return maybe.find(needle => !!parseUtcValue(needle));
    }
    return parseUtcValue(maybe);
};
function getParams(params, { allowEmptyPeriod = false, allowAbsoluteDatetime = true, allowAbsolutePageDatetime = false, defaultStatsPeriod = constants_1.DEFAULT_STATS_PERIOD, } = {}) {
    var _a, _b;
    const { pageStatsPeriod, pageStart, pageEnd, pageUtc, start, end, period, statsPeriod, utc } = params, otherParams = (0, tslib_1.__rest)(params, ["pageStatsPeriod", "pageStart", "pageEnd", "pageUtc", "start", "end", "period", "statsPeriod", "utc"]);
    // `statsPeriod` takes precedence for now
    let coercedPeriod = getStatsPeriodValue(pageStatsPeriod) ||
        getStatsPeriodValue(statsPeriod) ||
        getStatsPeriodValue(period);
    const dateTimeStart = allowAbsoluteDatetime
        ? allowAbsolutePageDatetime
            ? (_a = getDateTimeString(pageStart)) !== null && _a !== void 0 ? _a : getDateTimeString(start)
            : getDateTimeString(start)
        : null;
    const dateTimeEnd = allowAbsoluteDatetime
        ? allowAbsolutePageDatetime
            ? (_b = getDateTimeString(pageEnd)) !== null && _b !== void 0 ? _b : getDateTimeString(end)
            : getDateTimeString(end)
        : null;
    if (!(dateTimeStart && dateTimeEnd)) {
        if (!coercedPeriod && !allowEmptyPeriod) {
            coercedPeriod = defaultStatsPeriod;
        }
    }
    return Object.fromEntries(Object.entries(Object.assign({ statsPeriod: coercedPeriod, start: coercedPeriod ? null : dateTimeStart, end: coercedPeriod ? null : dateTimeEnd, 
        // coerce utc into a string (it can be both: a string representation from router,
        // or a boolean from time range picker)
        utc: getUtcValue(pageUtc !== null && pageUtc !== void 0 ? pageUtc : utc) }, otherParams))
        // Filter null values
        .filter(([_key, value]) => (0, utils_1.defined)(value)));
}
exports.getParams = getParams;
//# sourceMappingURL=getParams.jsx.map