Object.defineProperty(exports, "__esModule", { value: true });
exports.formatAbbreviatedNumber = exports.formatPercentage = exports.formatFloat = exports.getExactDuration = exports.getDuration = exports.SECOND = exports.MINUTE = exports.HOUR = exports.DAY = exports.WEEK = exports.MONTH = exports.formatVersion = exports.userDisplayName = void 0;
const tslib_1 = require("tslib");
const release_parser_1 = require("@sentry/release-parser");
const round_1 = (0, tslib_1.__importDefault)(require("lodash/round"));
const locale_1 = require("app/locale");
function userDisplayName(user, includeEmail = true) {
    var _a, _b;
    let displayName = String((_a = user === null || user === void 0 ? void 0 : user.name) !== null && _a !== void 0 ? _a : (0, locale_1.t)('Unknown author')).trim();
    if (displayName.length <= 0) {
        displayName = (0, locale_1.t)('Unknown author');
    }
    const email = String((_b = user === null || user === void 0 ? void 0 : user.email) !== null && _b !== void 0 ? _b : '').trim();
    if (email.length > 0 && email !== displayName && includeEmail) {
        displayName += ' (' + email + ')';
    }
    return displayName;
}
exports.userDisplayName = userDisplayName;
const formatVersion = (rawVersion, withPackage = false) => {
    try {
        const parsedVersion = new release_parser_1.Release(rawVersion);
        const versionToDisplay = parsedVersion.describe();
        if (versionToDisplay.length) {
            return `${versionToDisplay}${withPackage && parsedVersion.package ? `, ${parsedVersion.package}` : ''}`;
        }
        return rawVersion;
    }
    catch (_a) {
        return rawVersion;
    }
};
exports.formatVersion = formatVersion;
function roundWithFixed(value, fixedDigits) {
    const label = value.toFixed(fixedDigits);
    const result = fixedDigits <= 0 ? Math.round(value) : value;
    return { label, result };
}
// in milliseconds
exports.MONTH = 2629800000;
exports.WEEK = 604800000;
exports.DAY = 86400000;
exports.HOUR = 3600000;
exports.MINUTE = 60000;
exports.SECOND = 1000;
function getDuration(seconds, fixedDigits = 0, abbreviation = false, extraShort = false) {
    // value in milliseconds
    const msValue = seconds * 1000;
    const value = Math.abs(msValue);
    if (value >= exports.MONTH && !extraShort) {
        const { label, result } = roundWithFixed(msValue / exports.MONTH, fixedDigits);
        return `${label}${abbreviation ? (0, locale_1.tn)('mo', 'mos', result) : ` ${(0, locale_1.tn)('month', 'months', result)}`}`;
    }
    if (value >= exports.WEEK) {
        const { label, result } = roundWithFixed(msValue / exports.WEEK, fixedDigits);
        if (extraShort) {
            return `${label}${(0, locale_1.t)('w')}`;
        }
        if (abbreviation) {
            return `${label}${(0, locale_1.t)('wk')}`;
        }
        return `${label} ${(0, locale_1.tn)('week', 'weeks', result)}`;
    }
    if (value >= 172800000) {
        const { label, result } = roundWithFixed(msValue / exports.DAY, fixedDigits);
        return `${label}${abbreviation || extraShort ? (0, locale_1.t)('d') : ` ${(0, locale_1.tn)('day', 'days', result)}`}`;
    }
    if (value >= 7200000) {
        const { label, result } = roundWithFixed(msValue / exports.HOUR, fixedDigits);
        if (extraShort) {
            return `${label}${(0, locale_1.t)('h')}`;
        }
        if (abbreviation) {
            return `${label}${(0, locale_1.t)('hr')}`;
        }
        return `${label} ${(0, locale_1.tn)('hour', 'hours', result)}`;
    }
    if (value >= 120000) {
        const { label, result } = roundWithFixed(msValue / exports.MINUTE, fixedDigits);
        if (extraShort) {
            return `${label}${(0, locale_1.t)('m')}`;
        }
        if (abbreviation) {
            return `${label}${(0, locale_1.t)('min')}`;
        }
        return `${label} ${(0, locale_1.tn)('minute', 'minutes', result)}`;
    }
    if (value >= exports.SECOND) {
        const { label, result } = roundWithFixed(msValue / exports.SECOND, fixedDigits);
        if (extraShort || abbreviation) {
            return `${label}${(0, locale_1.t)('s')}`;
        }
        return `${label} ${(0, locale_1.tn)('second', 'seconds', result)}`;
    }
    const { label } = roundWithFixed(msValue, fixedDigits);
    return label + (0, locale_1.t)('ms');
}
exports.getDuration = getDuration;
function getExactDuration(seconds, abbreviation = false) {
    const convertDuration = (secs, abbr) => {
        // value in milliseconds
        const msValue = (0, round_1.default)(secs * 1000);
        const value = (0, round_1.default)(Math.abs(secs * 1000));
        const divideBy = (time) => {
            return {
                quotient: msValue < 0 ? Math.ceil(msValue / time) : Math.floor(msValue / time),
                remainder: msValue % time,
            };
        };
        if (value >= exports.WEEK) {
            const { quotient, remainder } = divideBy(exports.WEEK);
            return `${quotient}${abbr ? (0, locale_1.t)('wk') : ` ${(0, locale_1.tn)('week', 'weeks', quotient)}`} ${convertDuration(remainder / 1000, abbr)}`;
        }
        if (value >= exports.DAY) {
            const { quotient, remainder } = divideBy(exports.DAY);
            return `${quotient}${abbr ? (0, locale_1.t)('d') : ` ${(0, locale_1.tn)('day', 'days', quotient)}`} ${convertDuration(remainder / 1000, abbr)}`;
        }
        if (value >= exports.HOUR) {
            const { quotient, remainder } = divideBy(exports.HOUR);
            return `${quotient}${abbr ? (0, locale_1.t)('hr') : ` ${(0, locale_1.tn)('hour', 'hours', quotient)}`} ${convertDuration(remainder / 1000, abbr)}`;
        }
        if (value >= exports.MINUTE) {
            const { quotient, remainder } = divideBy(exports.MINUTE);
            return `${quotient}${abbr ? (0, locale_1.t)('min') : ` ${(0, locale_1.tn)('minute', 'minutes', quotient)}`} ${convertDuration(remainder / 1000, abbr)}`;
        }
        if (value >= exports.SECOND) {
            const { quotient, remainder } = divideBy(exports.SECOND);
            return `${quotient}${abbr ? (0, locale_1.t)('s') : ` ${(0, locale_1.tn)('second', 'seconds', quotient)}`} ${convertDuration(remainder / 1000, abbr)}`;
        }
        if (value === 0) {
            return '';
        }
        return `${msValue}${abbr ? (0, locale_1.t)('ms') : ` ${(0, locale_1.tn)('millisecond', 'milliseconds', value)}`}`;
    };
    const result = convertDuration(seconds, abbreviation).trim();
    if (result.length) {
        return result;
    }
    return `0${abbreviation ? (0, locale_1.t)('ms') : ` ${(0, locale_1.t)('milliseconds')}`}`;
}
exports.getExactDuration = getExactDuration;
function formatFloat(number, places) {
    const multi = Math.pow(10, places);
    return parseInt((number * multi).toString(), 10) / multi;
}
exports.formatFloat = formatFloat;
/**
 * Format a value between 0 and 1 as a percentage
 */
function formatPercentage(value, places = 2) {
    if (value === 0) {
        return '0%';
    }
    return ((0, round_1.default)(value * 100, places).toLocaleString(undefined, {
        maximumFractionDigits: places,
    }) + '%');
}
exports.formatPercentage = formatPercentage;
const numberFormats = [
    [1000000000, 'b'],
    [1000000, 'm'],
    [1000, 'k'],
];
function formatAbbreviatedNumber(number) {
    number = Number(number);
    let lookup;
    // eslint-disable-next-line no-cond-assign
    for (let i = 0; (lookup = numberFormats[i]); i++) {
        const [suffixNum, suffix] = lookup;
        const shortValue = Math.floor(number / suffixNum);
        const fitsBound = number % suffixNum;
        if (shortValue <= 0) {
            continue;
        }
        return shortValue / 10 > 1 || !fitsBound
            ? `${shortValue}${suffix}`
            : `${formatFloat(number / suffixNum, 1)}${suffix}`;
    }
    return number.toLocaleString();
}
exports.formatAbbreviatedNumber = formatAbbreviatedNumber;
//# sourceMappingURL=formatters.jsx.map