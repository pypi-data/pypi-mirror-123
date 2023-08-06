Object.defineProperty(exports, "__esModule", { value: true });
exports.getXAxisLabelInterval = exports.getTooltipFormatter = exports.getXAxisDates = exports.getDateFromUnixTimestamp = exports.getDateFromMoment = exports.FORMAT_DATETIME_HOURLY = exports.FORMAT_DATETIME_DAILY = void 0;
const tslib_1 = require("tslib");
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const types_1 = require("app/types");
const dates_1 = require("app/utils/dates");
const utils_1 = require("../utils");
/**
 * Avoid changing "MMM D" format as X-axis labels on UsageChart are naively
 * truncated by date.slice(0, 6). This avoids "..." when truncating by ECharts.
 */
exports.FORMAT_DATETIME_DAILY = 'MMM D';
exports.FORMAT_DATETIME_HOURLY = 'MMM D LT';
/**
 * Used to generate X-axis data points and labels for UsageChart
 * Ensure that this method is idempotent and doesn't change the moment object
 * that is passed in
 *
 * If hours are not shown, this method will need to use UTC to avoid oddities
 * caused by the user being ahead/behind UTC.
 */
function getDateFromMoment(m, interval = '1d', useUtc = false) {
    const days = (0, dates_1.parsePeriodToHours)(interval) / 24;
    if (days >= 1) {
        return moment_1.default.utc(m).format(exports.FORMAT_DATETIME_DAILY);
    }
    const parsedInterval = (0, getParams_1.parseStatsPeriod)(interval);
    const datetime = useUtc ? (0, moment_1.default)(m).utc() : (0, moment_1.default)(m).local();
    return parsedInterval
        ? `${datetime.format(exports.FORMAT_DATETIME_HOURLY)} - ${datetime
            .add(parsedInterval.period, parsedInterval.periodLength)
            .format('LT (Z)')}`
        : datetime.format(exports.FORMAT_DATETIME_HOURLY);
}
exports.getDateFromMoment = getDateFromMoment;
function getDateFromUnixTimestamp(timestamp) {
    const date = moment_1.default.unix(timestamp);
    return getDateFromMoment(date);
}
exports.getDateFromUnixTimestamp = getDateFromUnixTimestamp;
function getXAxisDates(dateStart, dateEnd, dateUtc = true, interval = '1d') {
    var _a;
    const range = [];
    const start = (0, moment_1.default)(dateStart).utc().startOf('h');
    const end = (0, moment_1.default)(dateEnd).startOf('h');
    if (!start.isValid() || !end.isValid()) {
        return range;
    }
    const { period, periodLength } = (_a = (0, getParams_1.parseStatsPeriod)(interval)) !== null && _a !== void 0 ? _a : {
        period: 1,
        periodLength: 'd',
    };
    while (!start.isAfter(end)) {
        range.push(getDateFromMoment(start, interval, dateUtc));
        start.add(period, periodLength); // FIXME(ts): Something odd with momentjs types
    }
    return range;
}
exports.getXAxisDates = getXAxisDates;
function getTooltipFormatter(dataCategory) {
    if (dataCategory === types_1.DataCategory.ATTACHMENTS) {
        return (val = 0) => (0, utils_1.formatUsageWithUnits)(val, types_1.DataCategory.ATTACHMENTS, { useUnitScaling: true });
    }
    return (val = 0) => val.toLocaleString();
}
exports.getTooltipFormatter = getTooltipFormatter;
const MAX_NUMBER_OF_LABELS = 10;
/**
 *
 * @param dataPeriod - Quantity of hours covered by the data
 * @param numBars - Quantity of data points covered by the dataPeriod
 */
function getXAxisLabelInterval(dataPeriod, numBars) {
    return dataPeriod > 7 * 24
        ? getLabelIntervalLongPeriod(dataPeriod, numBars)
        : getLabelIntervalShortPeriod(dataPeriod, numBars);
}
exports.getXAxisLabelInterval = getXAxisLabelInterval;
/**
 * @param dataPeriod - Quantity of hours covered by data, expected 7+ days
 */
function getLabelIntervalLongPeriod(dataPeriod, numBars) {
    const days = dataPeriod / 24;
    if (days <= 7) {
        throw new Error('This method should be used for periods > 7 days');
    }
    // Use 1 tick per day
    let numTicks = days;
    let numLabels = numTicks;
    const daysBetweenLabels = [2, 4, 7, 14];
    const daysBetweenTicks = [1, 2, 7, 7];
    for (let i = 0; i < daysBetweenLabels.length && numLabels > MAX_NUMBER_OF_LABELS; i++) {
        numLabels = numTicks / daysBetweenLabels[i];
        numTicks = days / daysBetweenTicks[i];
    }
    return {
        xAxisTickInterval: numBars / numTicks - 1,
        xAxisLabelInterval: numBars / numLabels - 1,
    };
}
/**
 * @param dataPeriod - Quantity of hours covered by data, expected <7 days
 */
function getLabelIntervalShortPeriod(dataPeriod, numBars) {
    const days = dataPeriod / 24;
    if (days > 7) {
        throw new Error('This method should be used for periods <= 7 days');
    }
    // Use 1 tick/label per day, since it's guaranteed to be 7 or less
    const numTicks = days;
    const interval = numBars / numTicks;
    return {
        xAxisTickInterval: interval - 1,
        xAxisLabelInterval: interval - 1,
    };
}
//# sourceMappingURL=utils.jsx.map