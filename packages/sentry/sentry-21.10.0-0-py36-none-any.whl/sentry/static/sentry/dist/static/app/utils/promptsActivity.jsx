Object.defineProperty(exports, "__esModule", { value: true });
exports.snoozedDays = void 0;
const tslib_1 = require("tslib");
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
/**
 * Given a snoozed unix timestamp in seconds, returns the number of days since
 * the prompt was snoozed.
 *
 * @param snoozedTs Snoozed timestamp
 */
function snoozedDays(snoozedTs) {
    const now = moment_1.default.utc();
    const snoozedDay = moment_1.default.unix(snoozedTs).utc();
    return now.diff(snoozedDay, 'days');
}
exports.snoozedDays = snoozedDays;
//# sourceMappingURL=promptsActivity.jsx.map