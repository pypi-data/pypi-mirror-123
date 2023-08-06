Object.defineProperty(exports, "__esModule", { value: true });
exports.isDisplayUtc = exports.abbreviateUsageNumber = exports.getFormatUsageOptions = exports.formatUsageWithUnits = exports.GIGABYTE = exports.BILLION = exports.MILLION = void 0;
const utils_1 = require("app/components/charts/utils");
const types_1 = require("app/types");
const utils_2 = require("app/utils");
const dates_1 = require("app/utils/dates");
exports.MILLION = Math.pow(10, 6);
exports.BILLION = Math.pow(10, 9);
exports.GIGABYTE = Math.pow(10, 9);
/**
 * This expects usage values/quantities for the data categories that we sell.
 *
 * Note: usageQuantity for Attachments should be in BYTES
 */
function formatUsageWithUnits(usageQuantity = 0, dataCategory, options = { isAbbreviated: false, useUnitScaling: false }) {
    if (dataCategory !== types_1.DataCategory.ATTACHMENTS) {
        return options.isAbbreviated
            ? abbreviateUsageNumber(usageQuantity)
            : usageQuantity.toLocaleString();
    }
    if (options.useUnitScaling) {
        return (0, utils_2.formatBytesBase10)(usageQuantity);
    }
    const usageGb = usageQuantity / exports.GIGABYTE;
    return options.isAbbreviated
        ? `${abbreviateUsageNumber(usageGb)} GB`
        : `${usageGb.toLocaleString(undefined, { maximumFractionDigits: 2 })} GB`;
}
exports.formatUsageWithUnits = formatUsageWithUnits;
/**
 * Good default for "formatUsageWithUnits"
 */
function getFormatUsageOptions(dataCategory) {
    return {
        isAbbreviated: dataCategory !== types_1.DataCategory.ATTACHMENTS,
        useUnitScaling: dataCategory === types_1.DataCategory.ATTACHMENTS,
    };
}
exports.getFormatUsageOptions = getFormatUsageOptions;
/**
 * Instead of using this function directly, use formatReservedWithUnits or
 * formatUsageWithUnits with options.isAbbreviated to true instead.
 *
 * This function display different precision for billion/million/thousand to
 * provide clarity on usage of errors/transactions/attachments to the user.
 *
 * If you are not displaying usage numbers, it might be better to use
 * `formatAbbreviatedNumber` in 'app/utils/formatters'
 */
function abbreviateUsageNumber(n) {
    if (n >= exports.BILLION) {
        return (n / exports.BILLION).toLocaleString(undefined, { maximumFractionDigits: 2 }) + 'B';
    }
    if (n >= exports.MILLION) {
        return (n / exports.MILLION).toLocaleString(undefined, { maximumFractionDigits: 1 }) + 'M';
    }
    if (n >= 1000) {
        return (n / 1000).toFixed().toLocaleString() + 'K';
    }
    // Do not show decimals
    return n.toFixed().toLocaleString();
}
exports.abbreviateUsageNumber = abbreviateUsageNumber;
/**
 * We want to display datetime in UTC in the following situations:
 *
 * 1) The user selected an absolute date range with UTC
 * 2) The user selected a wide date range with 1d interval
 *
 * When the interval is 1d, we need to use UTC because the 24 hour range might
 * shift forward/backward depending on the user's timezone, or it might be
 * displayed as a day earlier/later
 */
function isDisplayUtc(datetime) {
    if (datetime.utc) {
        return true;
    }
    const interval = (0, utils_1.getSeriesApiInterval)(datetime);
    const hours = (0, dates_1.parsePeriodToHours)(interval);
    return hours >= 24;
}
exports.isDisplayUtc = isDisplayUtc;
//# sourceMappingURL=utils.jsx.map