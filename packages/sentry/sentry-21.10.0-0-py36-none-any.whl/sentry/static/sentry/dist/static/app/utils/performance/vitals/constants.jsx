Object.defineProperty(exports, "__esModule", { value: true });
exports.MOBILE_VITAL_DETAILS = exports.WEB_VITAL_DETAILS = void 0;
const locale_1 = require("app/locale");
const fields_1 = require("app/utils/discover/fields");
exports.WEB_VITAL_DETAILS = {
    [fields_1.WebVital.FP]: {
        slug: 'fp',
        name: (0, locale_1.t)('First Paint'),
        acronym: 'FP',
        description: (0, locale_1.t)('Render time of the first pixel loaded in the viewport (may overlap with FCP).'),
        poorThreshold: 3000,
        type: (0, fields_1.measurementType)(fields_1.WebVital.FP),
    },
    [fields_1.WebVital.FCP]: {
        slug: 'fcp',
        name: (0, locale_1.t)('First Contentful Paint'),
        acronym: 'FCP',
        description: (0, locale_1.t)('Render time of the first image, text or other DOM node in the viewport.'),
        poorThreshold: 3000,
        type: (0, fields_1.measurementType)(fields_1.WebVital.FCP),
    },
    [fields_1.WebVital.LCP]: {
        slug: 'lcp',
        name: (0, locale_1.t)('Largest Contentful Paint'),
        acronym: 'LCP',
        description: (0, locale_1.t)('Render time of the largest image, text or other DOM node in the viewport.'),
        poorThreshold: 4000,
        type: (0, fields_1.measurementType)(fields_1.WebVital.LCP),
    },
    [fields_1.WebVital.FID]: {
        slug: 'fid',
        name: (0, locale_1.t)('First Input Delay'),
        acronym: 'FID',
        description: (0, locale_1.t)('Response time of the browser to a user interaction (clicking, tapping, etc).'),
        poorThreshold: 300,
        type: (0, fields_1.measurementType)(fields_1.WebVital.FID),
    },
    [fields_1.WebVital.CLS]: {
        slug: 'cls',
        name: (0, locale_1.t)('Cumulative Layout Shift'),
        acronym: 'CLS',
        description: (0, locale_1.t)('Sum of layout shift scores that measure the visual stability of the page.'),
        poorThreshold: 0.25,
        type: (0, fields_1.measurementType)(fields_1.WebVital.CLS),
    },
    [fields_1.WebVital.TTFB]: {
        slug: 'ttfb',
        name: (0, locale_1.t)('Time to First Byte'),
        acronym: 'TTFB',
        description: (0, locale_1.t)("The time that it takes for a user's browser to receive the first byte of page content."),
        poorThreshold: 600,
        type: (0, fields_1.measurementType)(fields_1.WebVital.TTFB),
    },
    [fields_1.WebVital.RequestTime]: {
        slug: 'ttfb.requesttime',
        name: (0, locale_1.t)('Request Time'),
        acronym: 'RT',
        description: (0, locale_1.t)('Captures the time spent making the request and receiving the first byte of the response.'),
        poorThreshold: 600,
        type: (0, fields_1.measurementType)(fields_1.WebVital.RequestTime),
    },
};
exports.MOBILE_VITAL_DETAILS = {
    [fields_1.MobileVital.AppStartCold]: {
        slug: 'app_start_cold',
        name: (0, locale_1.t)('App Start Cold'),
        description: (0, locale_1.t)('Cold start is a measure of the application start up time from scratch.'),
        type: (0, fields_1.measurementType)(fields_1.MobileVital.AppStartCold),
    },
    [fields_1.MobileVital.AppStartWarm]: {
        slug: 'app_start_warm',
        name: (0, locale_1.t)('App Start Warm'),
        description: (0, locale_1.t)('Warm start is a measure of the application start up time while still in memory.'),
        type: (0, fields_1.measurementType)(fields_1.MobileVital.AppStartWarm),
    },
    [fields_1.MobileVital.FramesTotal]: {
        slug: 'frames_total',
        name: (0, locale_1.t)('Total Frames'),
        description: (0, locale_1.t)('Total frames is a count of the number of frames recorded within a transaction.'),
        type: (0, fields_1.measurementType)(fields_1.MobileVital.FramesTotal),
    },
    [fields_1.MobileVital.FramesSlow]: {
        slug: 'frames_slow',
        name: (0, locale_1.t)('Slow Frames'),
        description: (0, locale_1.t)('Slow frames is a count of the number of slow frames recorded within a transaction.'),
        type: (0, fields_1.measurementType)(fields_1.MobileVital.FramesSlow),
    },
    [fields_1.MobileVital.FramesFrozen]: {
        slug: 'frames_frozen',
        name: (0, locale_1.t)('Frozen Frames'),
        description: (0, locale_1.t)('Frozen frames is a count of the number of frozen frames recorded within a transaction.'),
        type: (0, fields_1.measurementType)(fields_1.MobileVital.FramesFrozen),
    },
    [fields_1.MobileVital.FramesSlowRate]: {
        slug: 'frames_slow_rate',
        name: (0, locale_1.t)('Slow Frames Rate'),
        description: (0, locale_1.t)('Slow Frames Rate is the percentage of frames recorded within a transaction that is considered slow.'),
        type: (0, fields_1.measurementType)(fields_1.MobileVital.FramesSlowRate),
    },
    [fields_1.MobileVital.FramesFrozenRate]: {
        slug: 'frames_frozen_rate',
        name: (0, locale_1.t)('Frozen Frames Rate'),
        description: (0, locale_1.t)('Frozen Frames Rate is the percentage of frames recorded within a transaction that is considered frozen.'),
        type: (0, fields_1.measurementType)(fields_1.MobileVital.FramesFrozenRate),
    },
    [fields_1.MobileVital.StallCount]: {
        slug: 'stall_count',
        name: (0, locale_1.t)('Stalls'),
        description: (0, locale_1.t)('Stalls is the number of times the application stalled within a transaction.'),
        type: (0, fields_1.measurementType)(fields_1.MobileVital.StallCount),
    },
    [fields_1.MobileVital.StallTotalTime]: {
        slug: 'stall_total_time',
        name: (0, locale_1.t)('Total Stall Time'),
        description: (0, locale_1.t)('Stall Total Time is the total amount of time the application is stalled within a transaction.'),
        type: (0, fields_1.measurementType)(fields_1.MobileVital.StallTotalTime),
    },
    [fields_1.MobileVital.StallLongestTime]: {
        slug: 'stall_longest_time',
        name: (0, locale_1.t)('Longest Stall Time'),
        description: (0, locale_1.t)('Stall Longest Time is the longest amount of time the application is stalled within a transaction.'),
        type: (0, fields_1.measurementType)(fields_1.MobileVital.StallLongestTime),
    },
    [fields_1.MobileVital.StallPercentage]: {
        slug: 'stall_percentage',
        name: (0, locale_1.t)('Stall Percentage'),
        description: (0, locale_1.t)('Stall Percentage is the percentage of the transaction duration the application was stalled.'),
        type: (0, fields_1.measurementType)(fields_1.MobileVital.StallPercentage),
    },
};
//# sourceMappingURL=constants.jsx.map