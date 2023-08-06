Object.defineProperty(exports, "__esModule", { value: true });
exports.didProjectOrEnvironmentChange = exports.shouldFetchPreviousPeriod = void 0;
const utils_1 = require("app/components/charts/utils");
function shouldFetchPreviousPeriod(datetime) {
    const { start, end, period } = datetime;
    return !start && !end && (0, utils_1.canIncludePreviousPeriod)(true, period);
}
exports.shouldFetchPreviousPeriod = shouldFetchPreviousPeriod;
function didProjectOrEnvironmentChange(location1, location2) {
    return (location1.query.environment !== location2.query.environment ||
        location1.query.project !== location2.query.project);
}
exports.didProjectOrEnvironmentChange = didProjectOrEnvironmentChange;
//# sourceMappingURL=utils.jsx.map