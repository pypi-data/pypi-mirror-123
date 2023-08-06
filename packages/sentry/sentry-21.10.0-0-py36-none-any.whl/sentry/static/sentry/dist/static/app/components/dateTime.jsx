Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const moment_timezone_1 = (0, tslib_1.__importDefault)(require("moment-timezone"));
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
class DateTime extends react_1.Component {
    constructor() {
        super(...arguments);
        this.getFormat = ({ clock24Hours }) => {
            const { dateOnly, timeOnly, seconds, shortDate, timeAndDate, format } = this.props;
            if (format) {
                return format;
            }
            // October 26, 2017
            if (dateOnly) {
                return 'LL';
            }
            // Oct 26, 11:30 AM
            if (timeAndDate) {
                if (clock24Hours) {
                    return 'MMM DD, HH:mm';
                }
                return 'MMM DD, LT';
            }
            // 4:57 PM
            if (timeOnly) {
                if (clock24Hours) {
                    return 'HH:mm';
                }
                return 'LT';
            }
            if (shortDate) {
                return 'MM/DD/YYYY';
            }
            // Oct 26, 2017 11:30
            if (clock24Hours) {
                return 'MMM D, YYYY HH:mm';
            }
            // Oct 26, 2017 11:30:30 AM
            if (seconds) {
                return 'll LTS z';
            }
            // Default is Oct 26, 2017 11:30 AM
            return 'lll';
        };
    }
    render() {
        var _a;
        const _b = this.props, { date, utc, seconds: _seconds, shortDate: _shortDate, dateOnly: _dateOnly, timeOnly: _timeOnly, timeAndDate: _timeAndDate } = _b, carriedProps = (0, tslib_1.__rest)(_b, ["date", "utc", "seconds", "shortDate", "dateOnly", "timeOnly", "timeAndDate"]);
        const user = configStore_1.default.get('user');
        const options = user === null || user === void 0 ? void 0 : user.options;
        const format = this.getFormat(options);
        return (<time {...carriedProps}>
        {utc
                ? moment_1.default.utc(date).format(format)
                : moment_timezone_1.default.tz(date, (_a = options === null || options === void 0 ? void 0 : options.timezone) !== null && _a !== void 0 ? _a : '').format(format)}
      </time>);
    }
}
DateTime.defaultProps = {
    seconds: true,
};
exports.default = DateTime;
//# sourceMappingURL=dateTime.jsx.map