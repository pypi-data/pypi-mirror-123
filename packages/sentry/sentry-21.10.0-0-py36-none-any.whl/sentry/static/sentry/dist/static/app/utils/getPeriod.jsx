Object.defineProperty(exports, "__esModule", { value: true });
exports.getPeriod = void 0;
const tslib_1 = require("tslib");
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const constants_1 = require("app/constants");
const dates_1 = require("app/utils/dates");
/**
 * Gets the period to query with if we need to double the initial period in order
 * to get data for the previous period
 *
 * Returns an object with either a period or start/end dates ({statsPeriod: string} or {start: string, end: string})
 */
const getPeriod = ({ period, start, end }, { shouldDoublePeriod } = {}) => {
    if (!period && !start && !end) {
        period = constants_1.DEFAULT_STATS_PERIOD;
    }
    // you can not specify both relative and absolute periods
    // relative period takes precedence
    if (period) {
        if (!shouldDoublePeriod) {
            return { statsPeriod: period };
        }
        const [, periodNumber, periodLength] = period.match(/([0-9]+)([mhdw])/);
        return { statsPeriod: `${parseInt(periodNumber, 10) * 2}${periodLength}` };
    }
    if (!start || !end) {
        throw new Error('start and end required');
    }
    const formattedStart = (0, dates_1.getUtcDateString)(start);
    const formattedEnd = (0, dates_1.getUtcDateString)(end);
    if (shouldDoublePeriod) {
        // get duration of end - start and double
        const diff = (0, moment_1.default)(end).diff((0, moment_1.default)(start));
        const previousPeriodStart = (0, moment_1.default)(start).subtract(diff);
        // This is not as accurate as having 2 start/end objs
        return {
            start: (0, dates_1.getUtcDateString)(previousPeriodStart),
            end: formattedEnd,
        };
    }
    return {
        start: formattedStart,
        end: formattedEnd,
    };
};
exports.getPeriod = getPeriod;
//# sourceMappingURL=getPeriod.jsx.map