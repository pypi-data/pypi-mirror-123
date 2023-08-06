Object.defineProperty(exports, "__esModule", { value: true });
exports.getRelativeSummary = exports.parseStatsPeriod = void 0;
const tslib_1 = require("tslib");
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const constants_1 = require("app/constants");
const locale_1 = require("app/locale");
const DATE_TIME_FORMAT = 'YYYY-MM-DDTHH:mm:ss';
/**
 * Converts a relative stats period, e.g. `1h` to an object containing a start
 * and end date, with the end date as the current time and the start date as the
 * time that is the current time less the statsPeriod.
 *
 * @param statsPeriod Relative stats period
 * @param outputFormat Format of outputed start/end date
 * @return Object containing start and end date as YYYY-MM-DDTHH:mm:ss
 *
 */
function parseStatsPeriod(statsPeriod, outputFormat = DATE_TIME_FORMAT) {
    const statsPeriodRegex = /^(\d+)([smhd]{1})$/;
    const result = statsPeriodRegex.exec(statsPeriod);
    if (result === null) {
        throw new Error('Invalid stats period');
    }
    const value = parseInt(result[1], 10);
    const unit = {
        d: 'days',
        h: 'hours',
        s: 'seconds',
        m: 'minutes',
    }[result[2]];
    const format = outputFormat === null ? undefined : outputFormat;
    return {
        start: (0, moment_1.default)().subtract(value, unit).format(format),
        end: (0, moment_1.default)().format(format),
    };
}
exports.parseStatsPeriod = parseStatsPeriod;
/**
 * Given a relative stats period, e.g. `1h`, return a pretty string if it
 * is a default stats period. Otherwise if it's a valid period (can be any number
 * followed by a single character s|m|h|d) display "Other" or "Invalid period" if invalid
 *
 * @param relative Relative stats period
 * @return either one of the default "Last x days" string, "Other" if period is valid on the backend, or "Invalid period" otherwise
 */
function getRelativeSummary(relative, relativeOptions) {
    var _a;
    const defaultRelativePeriodString = (_a = relativeOptions === null || relativeOptions === void 0 ? void 0 : relativeOptions[relative]) !== null && _a !== void 0 ? _a : constants_1.DEFAULT_RELATIVE_PERIODS[relative];
    if (!defaultRelativePeriodString) {
        try {
            parseStatsPeriod(relative);
            return (0, locale_1.t)('Other');
        }
        catch (err) {
            return 'Invalid period';
        }
    }
    return defaultRelativePeriodString;
}
exports.getRelativeSummary = getRelativeSummary;
//# sourceMappingURL=utils.jsx.map