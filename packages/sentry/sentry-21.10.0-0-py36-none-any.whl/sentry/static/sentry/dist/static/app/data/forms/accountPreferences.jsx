Object.defineProperty(exports, "__esModule", { value: true });
exports.route = void 0;
const tslib_1 = require("tslib");
const languages_1 = (0, tslib_1.__importDefault)(require("app/data/languages"));
const timezones_1 = (0, tslib_1.__importDefault)(require("app/data/timezones"));
const locale_1 = require("app/locale");
// Export route to make these forms searchable by label/help
exports.route = '/settings/account/details/';
// Called before sending API request, these fields need to be sent as an
// `options` object
const transformOptions = (data) => ({ options: data });
const formGroups = [
    {
        // Form "section"/"panel"
        title: 'Preferences',
        fields: [
            {
                name: 'theme',
                type: 'select',
                label: (0, locale_1.t)('Theme'),
                help: (0, locale_1.t)("Select your theme preference. It can be synced to your system's theme, always light mode, or always dark mode."),
                choices: [
                    ['light', (0, locale_1.t)('Light')],
                    ['dark', (0, locale_1.t)('Dark')],
                    ['system', (0, locale_1.t)('Default to system')],
                ],
                getData: transformOptions,
            },
            {
                name: 'language',
                type: 'select',
                label: (0, locale_1.t)('Language'),
                choices: languages_1.default,
                getData: transformOptions,
            },
            {
                name: 'timezone',
                type: 'select',
                label: (0, locale_1.t)('Timezone'),
                choices: timezones_1.default,
                getData: transformOptions,
            },
            {
                name: 'clock24Hours',
                type: 'boolean',
                label: (0, locale_1.t)('Use a 24-hour clock'),
                getData: transformOptions,
            },
            {
                name: 'stacktraceOrder',
                type: 'select',
                required: false,
                choices: [
                    [-1, (0, locale_1.t)('Default (let Sentry decide)')],
                    [1, (0, locale_1.t)('Most recent call last')],
                    [2, (0, locale_1.t)('Most recent call first')],
                ],
                label: (0, locale_1.t)('Stack Trace Order'),
                help: (0, locale_1.t)('Choose the default ordering of frames in stack traces'),
                getData: transformOptions,
            },
        ],
    },
];
exports.default = formGroups;
//# sourceMappingURL=accountPreferences.jsx.map