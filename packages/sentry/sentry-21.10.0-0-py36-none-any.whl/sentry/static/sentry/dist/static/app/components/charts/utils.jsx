Object.defineProperty(exports, "__esModule", { value: true });
exports.lightenHexToRgb = exports.getDimensionValue = exports.isMultiSeriesStats = exports.getSeriesSelection = exports.canIncludePreviousPeriod = exports.getDiffInMinutes = exports.getSeriesApiInterval = exports.getInterval = exports.useShortInterval = exports.truncationFormatter = exports.RELEASE_LINES_THRESHOLD = exports.ONE_HOUR = exports.TWENTY_FOUR_HOURS = exports.ONE_WEEK = exports.TWO_WEEKS = exports.THIRTY_DAYS = exports.SIXTY_DAYS = void 0;
const tslib_1 = require("tslib");
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const constants_1 = require("app/constants");
const utils_1 = require("app/utils");
const dates_1 = require("app/utils/dates");
const queryString_1 = require("app/utils/queryString");
const DEFAULT_TRUNCATE_LENGTH = 80;
// In minutes
exports.SIXTY_DAYS = 86400;
exports.THIRTY_DAYS = 43200;
exports.TWO_WEEKS = 20160;
exports.ONE_WEEK = 10080;
exports.TWENTY_FOUR_HOURS = 1440;
exports.ONE_HOUR = 60;
/**
 * If there are more releases than this number we hide "Releases" series by default
 */
exports.RELEASE_LINES_THRESHOLD = 50;
function truncationFormatter(value, truncate) {
    if (!truncate) {
        return (0, utils_1.escape)(value);
    }
    const truncationLength = truncate && typeof truncate === 'number' ? truncate : DEFAULT_TRUNCATE_LENGTH;
    const truncated = value.length > truncationLength ? value.substring(0, truncationLength) + '…' : value;
    return (0, utils_1.escape)(truncated);
}
exports.truncationFormatter = truncationFormatter;
/**
 * Use a shorter interval if the time difference is <= 24 hours.
 */
function useShortInterval(datetimeObj) {
    const diffInMinutes = getDiffInMinutes(datetimeObj);
    return diffInMinutes <= exports.TWENTY_FOUR_HOURS;
}
exports.useShortInterval = useShortInterval;
function getInterval(datetimeObj, fidelity = 'medium') {
    const diffInMinutes = getDiffInMinutes(datetimeObj);
    if (diffInMinutes >= exports.SIXTY_DAYS) {
        // Greater than or equal to 60 days
        if (fidelity === 'high') {
            return '4h';
        }
        else if (fidelity === 'medium') {
            return '1d';
        }
        return '2d';
    }
    if (diffInMinutes >= exports.THIRTY_DAYS) {
        // Greater than or equal to 30 days
        if (fidelity === 'high') {
            return '1h';
        }
        else if (fidelity === 'medium') {
            return '4h';
        }
        return '1d';
    }
    if (diffInMinutes >= exports.TWO_WEEKS) {
        if (fidelity === 'high') {
            return '30m';
        }
        else if (fidelity === 'medium') {
            return '1h';
        }
        return '12h';
    }
    if (diffInMinutes > exports.TWENTY_FOUR_HOURS) {
        // Greater than 24 hours
        if (fidelity === 'high') {
            return '30m';
        }
        else if (fidelity === 'medium') {
            return '1h';
        }
        return '6h';
    }
    if (diffInMinutes > exports.ONE_HOUR) {
        // Between 1 hour and 24 hours
        if (fidelity === 'high') {
            return '5m';
        }
        else if (fidelity === 'medium') {
            return '15m';
        }
        else {
            return '1h';
        }
    }
    // Less than or equal to 1 hour
    if (fidelity === 'high') {
        return '1m';
    }
    else if (fidelity === 'medium') {
        return '5m';
    }
    else {
        return '10m';
    }
}
exports.getInterval = getInterval;
/**
 * Duplicate of getInterval, except that we do not support <1h granularity
 * Used by SessionsV2 and OrgStatsV2 API
 */
function getSeriesApiInterval(datetimeObj) {
    const diffInMinutes = getDiffInMinutes(datetimeObj);
    if (diffInMinutes >= exports.SIXTY_DAYS) {
        // Greater than or equal to 60 days
        return '1d';
    }
    if (diffInMinutes >= exports.THIRTY_DAYS) {
        // Greater than or equal to 30 days
        return '4h';
    }
    return '1h';
}
exports.getSeriesApiInterval = getSeriesApiInterval;
function getDiffInMinutes(datetimeObj) {
    const { period, start, end } = datetimeObj;
    if (start && end) {
        return (0, moment_1.default)(end).diff(start, 'minutes');
    }
    return ((0, dates_1.parsePeriodToHours)(typeof period === 'string' ? period : constants_1.DEFAULT_STATS_PERIOD) * 60);
}
exports.getDiffInMinutes = getDiffInMinutes;
// Max period (in hours) before we can no long include previous period
const MAX_PERIOD_HOURS_INCLUDE_PREVIOUS = 45 * 24;
function canIncludePreviousPeriod(includePrevious, period) {
    if (!includePrevious) {
        return false;
    }
    if (period && (0, dates_1.parsePeriodToHours)(period) > MAX_PERIOD_HOURS_INCLUDE_PREVIOUS) {
        return false;
    }
    // otherwise true
    return !!includePrevious;
}
exports.canIncludePreviousPeriod = canIncludePreviousPeriod;
/**
 * Generates a series selection based on the query parameters defined by the location.
 */
function getSeriesSelection(location, parameter = 'unselectedSeries') {
    const unselectedSeries = (0, queryString_1.decodeList)(location === null || location === void 0 ? void 0 : location.query[parameter]);
    return unselectedSeries.reduce((selection, series) => {
        selection[series] = false;
        return selection;
    }, {});
}
exports.getSeriesSelection = getSeriesSelection;
function isMultiSeriesStats(data) {
    return (0, utils_1.defined)(data) && data.data === undefined && data.totals === undefined;
}
exports.isMultiSeriesStats = isMultiSeriesStats;
// If dimension is a number convert it to pixels, otherwise use dimension
// without transform
const getDimensionValue = (dimension) => {
    if (typeof dimension === 'number') {
        return `${dimension}px`;
    }
    if (dimension === null) {
        return undefined;
    }
    return dimension;
};
exports.getDimensionValue = getDimensionValue;
const RGB_LIGHTEN_VALUE = 30;
const lightenHexToRgb = (colors) => colors.map(hex => {
    const rgb = [
        Math.min(parseInt(hex.slice(1, 3), 16) + RGB_LIGHTEN_VALUE, 255),
        Math.min(parseInt(hex.slice(3, 5), 16) + RGB_LIGHTEN_VALUE, 255),
        Math.min(parseInt(hex.slice(5, 7), 16) + RGB_LIGHTEN_VALUE, 255),
    ];
    return `rgb(${rgb[0]}, ${rgb[1]}, ${rgb[2]})`;
});
exports.lightenHexToRgb = lightenHexToRgb;
//# sourceMappingURL=utils.jsx.map