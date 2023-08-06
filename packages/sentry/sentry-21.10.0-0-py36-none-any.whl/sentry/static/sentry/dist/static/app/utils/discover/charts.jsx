Object.defineProperty(exports, "__esModule", { value: true });
exports.axisDuration = exports.axisLabelFormatter = exports.tooltipFormatter = void 0;
const locale_1 = require("app/locale");
const fields_1 = require("app/utils/discover/fields");
const formatters_1 = require("app/utils/formatters");
/**
 * Formatter for chart tooltips that handle a variety of discover result values
 */
function tooltipFormatter(value, seriesName = '') {
    switch ((0, fields_1.aggregateOutputType)(seriesName)) {
        case 'integer':
        case 'number':
            return value.toLocaleString();
        case 'percentage':
            return (0, formatters_1.formatPercentage)(value, 2);
        case 'duration':
            return (0, formatters_1.getDuration)(value / 1000, 2, true);
        default:
            return value.toString();
    }
}
exports.tooltipFormatter = tooltipFormatter;
/**
 * Formatter for chart axis labels that handle a variety of discover result values
 * This function is *very similar* to tooltipFormatter but outputs data with less precision.
 */
function axisLabelFormatter(value, seriesName, abbreviation = false) {
    switch ((0, fields_1.aggregateOutputType)(seriesName)) {
        case 'integer':
        case 'number':
            return abbreviation ? (0, formatters_1.formatAbbreviatedNumber)(value) : value.toLocaleString();
        case 'percentage':
            return (0, formatters_1.formatPercentage)(value, 0);
        case 'duration':
            return axisDuration(value);
        default:
            return value.toString();
    }
}
exports.axisLabelFormatter = axisLabelFormatter;
/**
 * Specialized duration formatting for axis labels.
 * In that context we are ok sacrificing accuracy for more
 * consistent sizing.
 *
 * @param value Number of milliseconds to format.
 */
function axisDuration(value) {
    if (value === 0) {
        return '0';
    }
    if (value >= formatters_1.WEEK) {
        const label = (value / formatters_1.WEEK).toFixed(0);
        return (0, locale_1.t)('%swk', label);
    }
    if (value >= formatters_1.DAY) {
        const label = (value / formatters_1.DAY).toFixed(0);
        return (0, locale_1.t)('%sd', label);
    }
    if (value >= formatters_1.HOUR) {
        const label = (value / formatters_1.HOUR).toFixed(0);
        return (0, locale_1.t)('%shr', label);
    }
    if (value >= formatters_1.MINUTE) {
        const label = (value / formatters_1.MINUTE).toFixed(0);
        return (0, locale_1.t)('%smin', label);
    }
    if (value >= formatters_1.SECOND) {
        const label = (value / formatters_1.SECOND).toFixed(0);
        return (0, locale_1.t)('%ss', label);
    }
    const label = value.toFixed(0);
    return (0, locale_1.t)('%sms', label);
}
exports.axisDuration = axisDuration;
//# sourceMappingURL=charts.jsx.map