Object.defineProperty(exports, "__esModule", { value: true });
exports.valueSuggestions = exports.unarySuggestions = exports.getRuleLabel = exports.getMethodLabel = exports.binarySuggestions = void 0;
const locale_1 = require("app/locale");
const types_1 = require("./types");
function getRuleLabel(type) {
    switch (type) {
        case types_1.RuleType.ANYTHING:
            return (0, locale_1.t)('Anything');
        case types_1.RuleType.IMEI:
            return (0, locale_1.t)('IMEI numbers');
        case types_1.RuleType.MAC:
            return (0, locale_1.t)('MAC addresses');
        case types_1.RuleType.EMAIL:
            return (0, locale_1.t)('Email addresses');
        case types_1.RuleType.PEMKEY:
            return (0, locale_1.t)('PEM keys');
        case types_1.RuleType.URLAUTH:
            return (0, locale_1.t)('Auth in URLs');
        case types_1.RuleType.USSSN:
            return (0, locale_1.t)('US social security numbers');
        case types_1.RuleType.USER_PATH:
            return (0, locale_1.t)('Usernames in filepaths');
        case types_1.RuleType.UUID:
            return (0, locale_1.t)('UUIDs');
        case types_1.RuleType.CREDITCARD:
            return (0, locale_1.t)('Credit card numbers');
        case types_1.RuleType.PASSWORD:
            return (0, locale_1.t)('Password fields');
        case types_1.RuleType.IP:
            return (0, locale_1.t)('IP addresses');
        case types_1.RuleType.PATTERN:
            return (0, locale_1.t)('Regex matches');
        default:
            return '';
    }
}
exports.getRuleLabel = getRuleLabel;
function getMethodLabel(type) {
    switch (type) {
        case types_1.MethodType.MASK:
            return {
                label: (0, locale_1.t)('Mask'),
                description: (0, locale_1.t)('Replace with ****'),
            };
        case types_1.MethodType.HASH:
            return {
                label: (0, locale_1.t)('Hash'),
                description: (0, locale_1.t)('Replace with DEADBEEF'),
            };
        case types_1.MethodType.REMOVE:
            return {
                label: (0, locale_1.t)('Remove'),
                description: (0, locale_1.t)('Replace with null'),
            };
        case types_1.MethodType.REPLACE:
            return {
                label: (0, locale_1.t)('Replace'),
                description: (0, locale_1.t)('Replace with Placeholder'),
            };
        default:
            return {
                label: '',
            };
    }
}
exports.getMethodLabel = getMethodLabel;
const binarySuggestions = [
    {
        type: types_1.SourceSuggestionType.BINARY,
        value: '&&',
    },
    {
        type: types_1.SourceSuggestionType.BINARY,
        value: '||',
    },
];
exports.binarySuggestions = binarySuggestions;
const unarySuggestions = [
    {
        type: types_1.SourceSuggestionType.UNARY,
        value: '!',
    },
];
exports.unarySuggestions = unarySuggestions;
const valueSuggestions = [
    { type: types_1.SourceSuggestionType.VALUE, value: '**', description: (0, locale_1.t)('everywhere') },
    {
        type: types_1.SourceSuggestionType.VALUE,
        value: 'password',
        description: (0, locale_1.t)('attributes named "password"'),
    },
    {
        type: types_1.SourceSuggestionType.VALUE,
        value: '$error.value',
        description: (0, locale_1.t)('the exception value'),
    },
    {
        type: types_1.SourceSuggestionType.VALUE,
        value: '$message',
        description: (0, locale_1.t)('the log message'),
    },
    {
        type: types_1.SourceSuggestionType.VALUE,
        value: 'extra.MyValue',
        description: (0, locale_1.t)('the key "MyValue" in "Additional Data"'),
    },
    {
        type: types_1.SourceSuggestionType.VALUE,
        value: 'extra.**',
        description: (0, locale_1.t)('everything in "Additional Data"'),
    },
    {
        type: types_1.SourceSuggestionType.VALUE,
        value: '$http.headers.x-custom-token',
        description: (0, locale_1.t)('the X-Custom-Token HTTP header'),
    },
    {
        type: types_1.SourceSuggestionType.VALUE,
        value: '$user.ip_address',
        description: (0, locale_1.t)('the user IP address'),
    },
    {
        type: types_1.SourceSuggestionType.VALUE,
        value: '$frame.vars.foo',
        description: (0, locale_1.t)('the local variable "foo"'),
    },
    {
        type: types_1.SourceSuggestionType.VALUE,
        value: 'contexts.device.timezone',
        description: (0, locale_1.t)('the timezone in the device context'),
    },
    {
        type: types_1.SourceSuggestionType.VALUE,
        value: 'tags.server_name',
        description: (0, locale_1.t)('the tag "server_name"'),
    },
    {
        type: types_1.SourceSuggestionType.VALUE,
        value: '$attachments.**',
        description: (0, locale_1.t)('all attachments'),
    },
    {
        type: types_1.SourceSuggestionType.VALUE,
        value: "$attachments.'logfile.txt'",
        description: (0, locale_1.t)('all attachments named "logfile.txt"'),
    },
    {
        type: types_1.SourceSuggestionType.VALUE,
        value: '$minidump',
        description: (0, locale_1.t)('the entire minidump of a native crash report'),
    },
    {
        type: types_1.SourceSuggestionType.VALUE,
        value: '$minidump.heap_memory',
        description: (0, locale_1.t)('the heap memory region in a native crash report'),
    },
    {
        type: types_1.SourceSuggestionType.VALUE,
        value: 'code_file',
        description: (0, locale_1.t)('the pathname of a code module in a native crash report'),
    },
    {
        type: types_1.SourceSuggestionType.VALUE,
        value: 'debug_file',
        description: (0, locale_1.t)('the pathname of a debug module in a native crash report'),
    },
];
exports.valueSuggestions = valueSuggestions;
//# sourceMappingURL=utils.jsx.map