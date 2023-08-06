Object.defineProperty(exports, "__esModule", { value: true });
exports.convertDayValueObjectToSeries = exports.convertDaySeriesToWeeks = void 0;
const tslib_1 = require("tslib");
const chunk_1 = (0, tslib_1.__importDefault)(require("lodash/chunk"));
/**
 * Buckets a week of sequential days into one data unit
 */
function convertDaySeriesToWeeks(data) {
    const sortedData = data.sort((a, b) => new Date(a.name).getTime() - new Date(b.name).getTime());
    return (0, chunk_1.default)(sortedData, 7).map(week => {
        return {
            name: week[0].name,
            value: week.reduce((total, currentData) => total + currentData.value, 0),
        };
    });
}
exports.convertDaySeriesToWeeks = convertDaySeriesToWeeks;
/**
 * Convert an object with date as the key to a series
 */
function convertDayValueObjectToSeries(data) {
    return Object.entries(data).map(([bucket, count]) => ({
        value: count,
        name: new Date(bucket).getTime(),
    }));
}
exports.convertDayValueObjectToSeries = convertDayValueObjectToSeries;
//# sourceMappingURL=utils.jsx.map