Object.defineProperty(exports, "__esModule", { value: true });
exports.getInnerNameLabel = exports.LEGACY_BROWSER_LIST = exports.DYNAMIC_SAMPLING_DOC_LINK = void 0;
const tslib_1 = require("tslib");
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const locale_1 = require("app/locale");
const dynamicSampling_1 = require("app/types/dynamicSampling");
// TODO(PRISCILA): Update this link as soon as we have one for dynamic sampling
exports.DYNAMIC_SAMPLING_DOC_LINK = 'https://docs.sentry.io/product/data-management-settings/filtering/';
exports.LEGACY_BROWSER_LIST = {
    [dynamicSampling_1.LegacyBrowser.IE_PRE_9]: {
        icon: 'internet-explorer',
        title: (0, locale_1.t)('Internet Explorer version 8 and lower'),
    },
    [dynamicSampling_1.LegacyBrowser.IE9]: {
        icon: 'internet-explorer',
        title: (0, locale_1.t)('Internet Explorer version 9'),
    },
    [dynamicSampling_1.LegacyBrowser.IE10]: {
        icon: 'internet-explorer',
        title: (0, locale_1.t)('Internet Explorer version 10'),
    },
    [dynamicSampling_1.LegacyBrowser.IE11]: {
        icon: 'internet-explorer',
        title: (0, locale_1.t)('Internet Explorer version 11'),
    },
    [dynamicSampling_1.LegacyBrowser.SAFARI_PRE_6]: {
        icon: 'safari',
        title: (0, locale_1.t)('Safari version 5 and lower'),
    },
    [dynamicSampling_1.LegacyBrowser.OPERA_PRE_15]: {
        icon: 'opera',
        title: (0, locale_1.t)('Opera version 14 and lower'),
    },
    [dynamicSampling_1.LegacyBrowser.OPERA_MINI_PRE_8]: {
        icon: 'opera',
        title: (0, locale_1.t)('Opera Mini version 8 and lower'),
    },
    [dynamicSampling_1.LegacyBrowser.ANDROID_PRE_4]: {
        icon: 'android',
        title: (0, locale_1.t)('Android version 3 and lower'),
    },
};
function getInnerNameLabel(name) {
    switch (name) {
        case dynamicSampling_1.DynamicSamplingInnerName.TRACE_ENVIRONMENT:
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_ENVIRONMENT:
            return (0, locale_1.t)('Environment');
        case dynamicSampling_1.DynamicSamplingInnerName.TRACE_RELEASE:
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_RELEASE:
            return (0, locale_1.t)('Release');
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_USER_ID:
        case dynamicSampling_1.DynamicSamplingInnerName.TRACE_USER_ID:
            return (0, locale_1.t)('User Id');
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_USER_SEGMENT:
        case dynamicSampling_1.DynamicSamplingInnerName.TRACE_USER_SEGMENT:
            return (0, locale_1.t)('User Segment');
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_BROWSER_EXTENSIONS:
            return (0, locale_1.t)('Browser Extensions');
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_LOCALHOST:
            return (0, locale_1.t)('Localhost');
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_WEB_CRAWLERS:
            return (0, locale_1.t)('Web Crawlers');
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_LEGACY_BROWSER:
            return (0, locale_1.t)('Legacy Browser');
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_TRANSACTION:
        case dynamicSampling_1.DynamicSamplingInnerName.TRACE_TRANSACTION:
            return (0, locale_1.t)('Transaction');
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_ERROR_MESSAGES:
            return (0, locale_1.t)('Error Message');
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_CSP:
            return (0, locale_1.t)('Content Security Policy');
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_IP_ADDRESSES:
            return (0, locale_1.t)('IP Address');
        default: {
            Sentry.captureException(new Error('Unknown dynamic sampling condition inner name'));
            return null; // this shall never happen
        }
    }
}
exports.getInnerNameLabel = getInnerNameLabel;
//# sourceMappingURL=utils.jsx.map