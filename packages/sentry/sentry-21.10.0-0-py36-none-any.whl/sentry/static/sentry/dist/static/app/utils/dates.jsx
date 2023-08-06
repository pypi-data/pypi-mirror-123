Object.defineProperty(exports, "__esModule", { value: true });
exports.getTimeFormat = exports.use24Hours = exports.statsPeriodToDays = exports.parsePeriodToHours = exports.intervalToMilliseconds = exports.getStartOfPeriodAgo = exports.getPeriodAgo = exports.getEndOfDay = exports.getStartOfDay = exports.getLocalToSystem = exports.getUtcToSystem = exports.setDateToTime = exports.getUtcToLocalDateObject = exports.getUserTimezone = exports.getFormattedDate = exports.getUtcDateString = exports.isValidTime = exports.DEFAULT_DAY_END_TIME = exports.DEFAULT_DAY_START_TIME = void 0;
const tslib_1 = require("tslib");
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
// TODO(billy): Move to TimeRangeSelector specific utils
exports.DEFAULT_DAY_START_TIME = '00:00:00';
exports.DEFAULT_DAY_END_TIME = '23:59:59';
const DATE_FORMAT_NO_TIMEZONE = 'YYYY/MM/DD HH:mm:ss';
function getParser(local = false) {
    return local ? moment_1.default : moment_1.default.utc;
}
/**
 * Checks if string is valid time. Only accepts 24 hour format.
 *
 * Chrome's time input will (at least for US locale), allow you to input 12
 * hour format with AM/PM but the raw value is in 24 hour.
 *
 * Safari does not do any validation so you could get a value of > 24 hours
 */
function isValidTime(str) {
    return (0, moment_1.default)(str, 'HH:mm', true).isValid();
}
exports.isValidTime = isValidTime;
/**
 * Given a date object, format in datetime in UTC
 * given: Tue Oct 09 2018 00:00:00 GMT-0700 (Pacific Daylight Time)
 * returns: "2018-10-09T07:00:00.000"
 */
function getUtcDateString(dateObj) {
    return moment_1.default.utc(dateObj).format(moment_1.default.HTML5_FMT.DATETIME_LOCAL_SECONDS);
}
exports.getUtcDateString = getUtcDateString;
function getFormattedDate(dateObj, format, { local } = {}) {
    return getParser(local)(dateObj).format(format);
}
exports.getFormattedDate = getFormattedDate;
/**
 * Returns user timezone from their account preferences
 */
function getUserTimezone() {
    const user = configStore_1.default.get('user');
    return user && user.options && user.options.timezone;
}
exports.getUserTimezone = getUserTimezone;
/**
 * Given a UTC date, return a Date object in local time
 */
function getUtcToLocalDateObject(date) {
    return moment_1.default.utc(date).local().toDate();
}
exports.getUtcToLocalDateObject = getUtcToLocalDateObject;
/**
 * Sets time (hours + minutes) of the current date object
 *
 * @param {String} timeStr Time in 24hr format (HH:mm)
 */
function setDateToTime(dateObj, timeStr, { local } = {}) {
    const [hours, minutes, seconds] = timeStr.split(':').map(t => parseInt(t, 10));
    const date = new Date(+dateObj);
    if (local) {
        date.setHours(hours, minutes);
    }
    else {
        date.setUTCHours(hours, minutes);
    }
    if (typeof seconds !== 'undefined') {
        date.setSeconds(seconds);
    }
    return date;
}
exports.setDateToTime = setDateToTime;
/**
 * Given a UTC timestamp, return a system date object with the same date
 * e.g. given: system is -0700 (PST),
 * 1/1/2001 @ 22:00 UTC, return:  1/1/2001 @ 22:00 -0700 (PST)
 */
function getUtcToSystem(dateObj) {
    // This is required because if your system timezone !== user configured timezone
    // then there will be a mismatch of dates with `react-date-picker`
    //
    // We purposely strip the timezone when formatting from the utc timezone
    return new Date(moment_1.default.utc(dateObj).format(DATE_FORMAT_NO_TIMEZONE));
}
exports.getUtcToSystem = getUtcToSystem;
/**
 * Given a timestamp, format to user preference timezone, and strip timezone to
 * return a system date object with the same date
 *
 * e.g. given: system is -0700 (PST) and user preference is -0400 (EST),
 * 1/1/2001 @ 22:00 UTC --> 1/1/2001 @ 18:00 -0400 (EST) -->
 * return:  1/1/2001 @ 18:00 -0700 (PST)
 */
function getLocalToSystem(dateObj) {
    // This is required because if your system timezone !== user configured timezone
    // then there will be a mismatch of dates with `react-date-picker`
    //
    // We purposely strip the timezone when formatting from the utc timezone
    return new Date((0, moment_1.default)(dateObj).format(DATE_FORMAT_NO_TIMEZONE));
}
exports.getLocalToSystem = getLocalToSystem;
// Get the beginning of day (e.g. midnight)
function getStartOfDay(date) {
    return (0, moment_1.default)(date)
        .startOf('day')
        .startOf('hour')
        .startOf('minute')
        .startOf('second')
        .local()
        .toDate();
}
exports.getStartOfDay = getStartOfDay;
// Get tomorrow at midnight so that default endtime
// is inclusive of today
function getEndOfDay(date) {
    return (0, moment_1.default)(date)
        .add(1, 'day')
        .startOf('hour')
        .startOf('minute')
        .startOf('second')
        .subtract(1, 'second')
        .local()
        .toDate();
}
exports.getEndOfDay = getEndOfDay;
function getPeriodAgo(period, unit) {
    return (0, moment_1.default)().local().subtract(unit, period);
}
exports.getPeriodAgo = getPeriodAgo;
// Get the start of the day (midnight) for a period ago
//
// e.g. 2 weeks ago at midnight
function getStartOfPeriodAgo(period, unit) {
    return getStartOfDay(getPeriodAgo(period, unit));
}
exports.getStartOfPeriodAgo = getStartOfPeriodAgo;
/**
 * Convert an interval string into a number of seconds.
 * This allows us to create end timestamps from starting ones
 * enabling us to find events in narrow windows.
 *
 * @param {String} interval The interval to convert.
 * @return {Integer}
 */
function intervalToMilliseconds(interval) {
    const pattern = /^(\d+)(d|h|m)$/;
    const matches = pattern.exec(interval);
    if (!matches) {
        return 0;
    }
    const [, value, unit] = matches;
    const multipliers = {
        d: 60 * 60 * 24,
        h: 60 * 60,
        m: 60,
    };
    return parseInt(value, 10) * multipliers[unit] * 1000;
}
exports.intervalToMilliseconds = intervalToMilliseconds;
/**
 * This parses our period shorthand strings (e.g. <int><unit>)
 * and converts it into hours
 */
function parsePeriodToHours(str) {
    const result = (0, getParams_1.parseStatsPeriod)(str);
    if (!result) {
        return -1;
    }
    const { period, periodLength } = result;
    const periodNumber = parseInt(period, 10);
    switch (periodLength) {
        case 's':
            return periodNumber / (60 * 60);
        case 'm':
            return periodNumber / 60;
        case 'h':
            return periodNumber;
        case 'd':
            return periodNumber * 24;
        case 'w':
            return periodNumber * 24 * 7;
        default:
            return -1;
    }
}
exports.parsePeriodToHours = parsePeriodToHours;
function statsPeriodToDays(statsPeriod, start, end) {
    if (statsPeriod && statsPeriod.endsWith('d')) {
        return parseInt(statsPeriod.slice(0, -1), 10);
    }
    else if (statsPeriod && statsPeriod.endsWith('h')) {
        return parseInt(statsPeriod.slice(0, -1), 10) / 24;
    }
    else if (start && end) {
        return (new Date(end).getTime() - new Date(start).getTime()) / (24 * 60 * 60 * 1000);
    }
    return 0;
}
exports.statsPeriodToDays = statsPeriodToDays;
const use24Hours = () => { var _a, _b; return (_b = (_a = configStore_1.default.get('user')) === null || _a === void 0 ? void 0 : _a.options) === null || _b === void 0 ? void 0 : _b.clock24Hours; };
exports.use24Hours = use24Hours;
const getTimeFormat = () => ((0, exports.use24Hours)() ? 'HH:mm' : 'LT');
exports.getTimeFormat = getTimeFormat;
//# sourceMappingURL=dates.jsx.map