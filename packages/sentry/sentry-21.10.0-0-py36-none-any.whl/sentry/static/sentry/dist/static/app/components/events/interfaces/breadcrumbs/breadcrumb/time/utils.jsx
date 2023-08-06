Object.defineProperty(exports, "__esModule", { value: true });
exports.getFormattedTimestamp = void 0;
const tslib_1 = require("tslib");
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const locale_1 = require("app/locale");
const utils_1 = require("app/utils");
const dates_1 = require("app/utils/dates");
const formatters_1 = require("app/utils/formatters");
const timeFormat = 'HH:mm:ss';
const timeDateFormat = `ll ${timeFormat}`;
const getRelativeTime = (parsedTime, parsedTimeToCompareWith, displayRelativeTime) => {
    // ll is necessary here, otherwise moment(x).from will throw an error
    const formattedTime = (0, moment_1.default)(parsedTime.format(timeDateFormat));
    const formattedTimeToCompareWith = parsedTimeToCompareWith.format(timeDateFormat);
    const timeDiff = Math.abs(formattedTime.diff(formattedTimeToCompareWith));
    const shortRelativeTime = (0, formatters_1.getDuration)(Math.round(timeDiff / 1000), 0, true).replace(/\s/g, '');
    if (timeDiff !== 0) {
        return displayRelativeTime
            ? `-${shortRelativeTime}`
            : (0, locale_1.t)('%s before', shortRelativeTime);
    }
    return `\xA0${shortRelativeTime}`;
};
const getAbsoluteTimeFormat = (format) => {
    if ((0, dates_1.use24Hours)()) {
        return format;
    }
    return `${format} A`;
};
const getFormattedTimestamp = (timestamp, relativeTimestamp, displayRelativeTime) => {
    const parsedTimestamp = (0, moment_1.default)(timestamp);
    const date = parsedTimestamp.format('ll');
    const displayMilliSeconds = (0, utils_1.defined)(parsedTimestamp.milliseconds());
    const relativeTime = getRelativeTime(parsedTimestamp, (0, moment_1.default)(relativeTimestamp), displayRelativeTime);
    if (!displayRelativeTime) {
        return {
            date: `${date} ${parsedTimestamp.format(getAbsoluteTimeFormat('HH:mm'))}`,
            time: relativeTime,
            displayTime: parsedTimestamp.format(timeFormat),
        };
    }
    return {
        date,
        time: parsedTimestamp.format(getAbsoluteTimeFormat(displayMilliSeconds ? `${timeFormat}.SSS` : timeFormat)),
        displayTime: relativeTime,
    };
};
exports.getFormattedTimestamp = getFormattedTimestamp;
//# sourceMappingURL=utils.jsx.map