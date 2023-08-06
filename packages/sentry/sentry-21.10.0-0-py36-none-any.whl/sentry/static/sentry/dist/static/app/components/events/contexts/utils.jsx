Object.defineProperty(exports, "__esModule", { value: true });
exports.getFullLanguageDescription = exports.getRelativeTimeFromEventDateCreated = exports.getSourcePlugin = exports.getContextComponent = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const moment_timezone_1 = (0, tslib_1.__importDefault)(require("moment-timezone"));
const locale_1 = require("app/locale");
const plugins_1 = (0, tslib_1.__importDefault)(require("app/plugins"));
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const CONTEXT_TYPES = {
    default: require('app/components/events/contexts/default').default,
    app: require('app/components/events/contexts/app/app').default,
    device: require('app/components/events/contexts/device/device').default,
    os: require('app/components/events/contexts/operatingSystem/operatingSystem').default,
    runtime: require('app/components/events/contexts/runtime/runtime').default,
    user: require('app/components/events/contexts/user/user').default,
    gpu: require('app/components/events/contexts/gpu/gpu').default,
    trace: require('app/components/events/contexts/trace/trace').default,
    // 'redux.state' will be replaced with more generic context called 'state'
    'redux.state': require('app/components/events/contexts/redux').default,
    state: require('app/components/events/contexts/state').default,
};
function getContextComponent(type) {
    return CONTEXT_TYPES[type] || plugins_1.default.contexts[type] || CONTEXT_TYPES.default;
}
exports.getContextComponent = getContextComponent;
function getSourcePlugin(pluginContexts, contextType) {
    if (CONTEXT_TYPES[contextType]) {
        return null;
    }
    for (const plugin of pluginContexts) {
        if (plugin.contexts.indexOf(contextType) >= 0) {
            return plugin;
        }
    }
    return null;
}
exports.getSourcePlugin = getSourcePlugin;
function getRelativeTimeFromEventDateCreated(eventDateCreated, timestamp, showTimestamp = true) {
    if (!(0, utils_1.defined)(timestamp)) {
        return timestamp;
    }
    const dateTime = (0, moment_timezone_1.default)(timestamp);
    if (!dateTime.isValid()) {
        return timestamp;
    }
    const relativeTime = `(${dateTime.from(eventDateCreated, true)} ${(0, locale_1.t)('before this event')})`;
    if (!showTimestamp) {
        return <RelativeTime>{relativeTime}</RelativeTime>;
    }
    return (<react_1.Fragment>
      {timestamp}
      <RelativeTime>{relativeTime}</RelativeTime>
    </react_1.Fragment>);
}
exports.getRelativeTimeFromEventDateCreated = getRelativeTimeFromEventDateCreated;
// Typescript doesn't have types for DisplayNames yet and that's why the type assertion "any" is needed below.
// There is currently an open PR that intends to introduce the types https://github.com/microsoft/TypeScript/pull/44022
function getFullLanguageDescription(locale) {
    const sentryAppLanguageCode = configStore_1.default.get('languageCode');
    const [languageAbbreviation, countryAbbreviation] = locale.includes('_')
        ? locale.split('_')
        : locale.split('-');
    try {
        const languageNames = new Intl.DisplayNames(sentryAppLanguageCode, {
            type: 'language',
        });
        const languageName = languageNames.of(languageAbbreviation);
        if (countryAbbreviation) {
            const regionNames = new Intl.DisplayNames(sentryAppLanguageCode, {
                type: 'region',
            });
            const countryName = regionNames.of(countryAbbreviation.toUpperCase());
            return `${languageName} (${countryName})`;
        }
        return languageName;
    }
    catch (_a) {
        return locale;
    }
}
exports.getFullLanguageDescription = getFullLanguageDescription;
const RelativeTime = (0, styled_1.default)('span') `
  color: ${p => p.theme.subText};
  margin-left: ${(0, space_1.default)(0.5)};
`;
//# sourceMappingURL=utils.jsx.map