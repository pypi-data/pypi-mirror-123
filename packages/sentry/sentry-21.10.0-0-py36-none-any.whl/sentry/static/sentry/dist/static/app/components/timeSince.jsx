Object.defineProperty(exports, "__esModule", { value: true });
exports.getRelativeDate = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const isNumber_1 = (0, tslib_1.__importDefault)(require("lodash/isNumber"));
const isString_1 = (0, tslib_1.__importDefault)(require("lodash/isString"));
const moment_timezone_1 = (0, tslib_1.__importDefault)(require("moment-timezone"));
const locale_1 = require("app/locale");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const formatters_1 = require("app/utils/formatters");
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("./tooltip"));
const ONE_MINUTE_IN_MS = 60000;
class TimeSince extends React.PureComponent {
    constructor() {
        super(...arguments);
        this.state = {
            relative: '',
        };
        this.ticker = null;
        this.setRelativeDateTicker = () => {
            this.ticker = window.setTimeout(() => {
                this.setState({
                    relative: getRelativeDate(this.props.date, this.props.suffix, this.props.shorten, this.props.extraShort),
                });
                this.setRelativeDateTicker();
            }, ONE_MINUTE_IN_MS);
        };
    }
    // TODO(ts) TODO(emotion): defining the props type breaks emotion's typings
    // See: https://github.com/emotion-js/emotion/pull/1514
    static getDerivedStateFromProps(props) {
        return {
            relative: getRelativeDate(props.date, props.suffix, props.shorten, props.extraShort),
        };
    }
    componentDidMount() {
        this.setRelativeDateTicker();
    }
    componentWillUnmount() {
        if (this.ticker) {
            window.clearTimeout(this.ticker);
            this.ticker = null;
        }
    }
    render() {
        var _a;
        const _b = this.props, { date, suffix: _suffix, disabledAbsoluteTooltip, className, tooltipTitle, shorten: _shorten, extraShort: _extraShort } = _b, props = (0, tslib_1.__rest)(_b, ["date", "suffix", "disabledAbsoluteTooltip", "className", "tooltipTitle", "shorten", "extraShort"]);
        const dateObj = getDateObj(date);
        const user = configStore_1.default.get('user');
        const options = user ? user.options : null;
        const format = (options === null || options === void 0 ? void 0 : options.clock24Hours) ? 'MMMM D, YYYY HH:mm z' : 'LLL z';
        const tooltip = (0, getDynamicText_1.default)({
            fixed: (options === null || options === void 0 ? void 0 : options.clock24Hours)
                ? 'November 3, 2020 08:57 UTC'
                : 'November 3, 2020 8:58 AM UTC',
            value: moment_timezone_1.default.tz(dateObj, (_a = options === null || options === void 0 ? void 0 : options.timezone) !== null && _a !== void 0 ? _a : '').format(format),
        });
        return (<tooltip_1.default disabled={disabledAbsoluteTooltip} title={<div>
            <div>{tooltipTitle}</div>
            {tooltip}
          </div>}>
        <time dateTime={dateObj.toISOString()} className={className} {...props}>
          {this.state.relative}
        </time>
      </tooltip_1.default>);
    }
}
TimeSince.defaultProps = {
    suffix: 'ago',
};
exports.default = TimeSince;
function getDateObj(date) {
    if ((0, isString_1.default)(date) || (0, isNumber_1.default)(date)) {
        date = new Date(date);
    }
    return date;
}
function getRelativeDate(currentDateTime, suffix, shorten, extraShort) {
    const date = getDateObj(currentDateTime);
    if ((shorten || extraShort) && suffix) {
        return (0, locale_1.t)('%(time)s %(suffix)s', {
            time: (0, formatters_1.getDuration)((0, moment_timezone_1.default)().diff((0, moment_timezone_1.default)(date), 'seconds'), 0, shorten, extraShort),
            suffix,
        });
    }
    else if ((shorten || extraShort) && !suffix) {
        return (0, formatters_1.getDuration)((0, moment_timezone_1.default)().diff((0, moment_timezone_1.default)(date), 'seconds'), 0, shorten, extraShort);
    }
    else if (!suffix) {
        return (0, moment_timezone_1.default)(date).fromNow(true);
    }
    else if (suffix === 'ago') {
        return (0, moment_timezone_1.default)(date).fromNow();
    }
    else if (suffix === 'old') {
        return (0, locale_1.t)('%(time)s old', { time: (0, moment_timezone_1.default)(date).fromNow(true) });
    }
    else {
        throw new Error('Unsupported time format suffix');
    }
}
exports.getRelativeDate = getRelativeDate;
//# sourceMappingURL=timeSince.jsx.map