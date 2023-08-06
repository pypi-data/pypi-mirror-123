Object.defineProperty(exports, "__esModule", { value: true });
exports.WIDGET_DEFINITIONS = exports.PerformanceWidgetSetting = void 0;
const tslib_1 = require("tslib");
const chartPalette_1 = (0, tslib_1.__importDefault)(require("app/constants/chartPalette"));
const locale_1 = require("app/locale");
const data_1 = require("../../data");
const types_1 = require("./types");
var PerformanceWidgetSetting;
(function (PerformanceWidgetSetting) {
    PerformanceWidgetSetting["LCP_HISTOGRAM"] = "lcp_histogram";
    PerformanceWidgetSetting["FCP_HISTOGRAM"] = "fcp_histogram";
    PerformanceWidgetSetting["FID_HISTOGRAM"] = "fid_histogram";
    PerformanceWidgetSetting["APDEX_AREA"] = "apdex_area";
    PerformanceWidgetSetting["P50_DURATION_AREA"] = "p50_duration_area";
    PerformanceWidgetSetting["P95_DURATION_AREA"] = "p95_duration_area";
    PerformanceWidgetSetting["P99_DURATION_AREA"] = "p99_duration_area";
    PerformanceWidgetSetting["TPM_AREA"] = "tpm_area";
    PerformanceWidgetSetting["FAILURE_RATE_AREA"] = "failure_rate_area";
    PerformanceWidgetSetting["USER_MISERY_AREA"] = "user_misery_area";
    PerformanceWidgetSetting["WORST_LCP_VITALS"] = "worst_lcp_vitals";
    PerformanceWidgetSetting["MOST_IMPROVED"] = "most_improved";
    PerformanceWidgetSetting["MOST_REGRESSED"] = "most_regressed";
})(PerformanceWidgetSetting = exports.PerformanceWidgetSetting || (exports.PerformanceWidgetSetting = {}));
const WIDGET_PALETTE = chartPalette_1.default[5];
const WIDGET_DEFINITIONS = ({ organization, }) => {
    var _a;
    return ({
        [PerformanceWidgetSetting.LCP_HISTOGRAM]: {
            title: (0, locale_1.t)('LCP Distribution'),
            titleTooltip: (0, data_1.getTermHelp)(organization, data_1.PERFORMANCE_TERM.DURATION_DISTRIBUTION),
            fields: ['measurements.lcp'],
            dataType: types_1.GenericPerformanceWidgetDataType.histogram,
            chartColor: WIDGET_PALETTE[5],
        },
        [PerformanceWidgetSetting.FCP_HISTOGRAM]: {
            title: (0, locale_1.t)('FCP Distribution'),
            titleTooltip: (0, data_1.getTermHelp)(organization, data_1.PERFORMANCE_TERM.DURATION_DISTRIBUTION),
            fields: ['measurements.fcp'],
            dataType: types_1.GenericPerformanceWidgetDataType.histogram,
            chartColor: WIDGET_PALETTE[5],
        },
        [PerformanceWidgetSetting.FID_HISTOGRAM]: {
            title: (0, locale_1.t)('FID Distribution'),
            titleTooltip: (0, data_1.getTermHelp)(organization, data_1.PERFORMANCE_TERM.DURATION_DISTRIBUTION),
            fields: ['measurements.fid'],
            dataType: types_1.GenericPerformanceWidgetDataType.histogram,
            chartColor: WIDGET_PALETTE[5],
        },
        [PerformanceWidgetSetting.WORST_LCP_VITALS]: {
            title: (0, locale_1.t)('Worst LCP Web Vitals'),
            titleTooltip: (0, data_1.getTermHelp)(organization, data_1.PERFORMANCE_TERM.LCP),
            fields: [
                'count_if(measurements.lcp,greaterOrEquals,4000)',
                'count_if(measurements.lcp,greaterOrEquals,2500)',
                'count_if(measurements.lcp,greaterOrEquals,0)',
                'equation|count_if(measurements.lcp,greaterOrEquals,2500) - count_if(measurements.lcp,greaterOrEquals,4000)',
                'equation|count_if(measurements.lcp,greaterOrEquals,0) - count_if(measurements.lcp,greaterOrEquals,2500)',
            ],
            dataType: types_1.GenericPerformanceWidgetDataType.vitals,
        },
        [PerformanceWidgetSetting.TPM_AREA]: {
            title: (0, locale_1.t)('Transactions Per Minute'),
            titleTooltip: (0, data_1.getTermHelp)(organization, data_1.PERFORMANCE_TERM.TPM),
            fields: ['tpm()'],
            dataType: types_1.GenericPerformanceWidgetDataType.area,
            chartColor: WIDGET_PALETTE[1],
        },
        [PerformanceWidgetSetting.APDEX_AREA]: {
            title: (0, locale_1.t)('Apdex'),
            titleTooltip: (0, data_1.getTermHelp)(organization, data_1.PERFORMANCE_TERM.APDEX_NEW),
            fields: ['apdex()'],
            dataType: types_1.GenericPerformanceWidgetDataType.area,
            chartColor: WIDGET_PALETTE[4],
        },
        [PerformanceWidgetSetting.P50_DURATION_AREA]: {
            title: (0, locale_1.t)('p50 Duration'),
            titleTooltip: (0, data_1.getTermHelp)(organization, data_1.PERFORMANCE_TERM.P50),
            fields: ['p50(transaction.duration)'],
            dataType: types_1.GenericPerformanceWidgetDataType.area,
            chartColor: WIDGET_PALETTE[3],
        },
        [PerformanceWidgetSetting.P95_DURATION_AREA]: {
            title: (0, locale_1.t)('p95 Duration'),
            titleTooltip: (0, data_1.getTermHelp)(organization, data_1.PERFORMANCE_TERM.P95),
            fields: ['p95(transaction.duration)'],
            dataType: types_1.GenericPerformanceWidgetDataType.area,
            chartColor: WIDGET_PALETTE[3],
        },
        [PerformanceWidgetSetting.P99_DURATION_AREA]: {
            title: (0, locale_1.t)('p99 Duration'),
            titleTooltip: (0, data_1.getTermHelp)(organization, data_1.PERFORMANCE_TERM.P99),
            fields: ['p99(transaction.duration)'],
            dataType: types_1.GenericPerformanceWidgetDataType.area,
            chartColor: WIDGET_PALETTE[3],
        },
        [PerformanceWidgetSetting.FAILURE_RATE_AREA]: {
            title: (0, locale_1.t)('Failure Rate'),
            titleTooltip: (0, data_1.getTermHelp)(organization, data_1.PERFORMANCE_TERM.FAILURE_RATE),
            fields: ['failure_rate()'],
            dataType: types_1.GenericPerformanceWidgetDataType.area,
            chartColor: WIDGET_PALETTE[2],
        },
        [PerformanceWidgetSetting.USER_MISERY_AREA]: {
            title: (0, locale_1.t)('User Misery'),
            titleTooltip: (0, data_1.getTermHelp)(organization, data_1.PERFORMANCE_TERM.USER_MISERY),
            fields: [`user_misery(${(_a = organization.apdexThreshold) !== null && _a !== void 0 ? _a : ''})`],
            dataType: types_1.GenericPerformanceWidgetDataType.area,
            chartColor: WIDGET_PALETTE[0],
        },
        [PerformanceWidgetSetting.MOST_IMPROVED]: {
            title: (0, locale_1.t)('Most Improved'),
            titleTooltip: (0, locale_1.t)('This compares the baseline (%s) of the past with the present.', 'improved'),
            fields: [],
            dataType: types_1.GenericPerformanceWidgetDataType.trends,
        },
        [PerformanceWidgetSetting.MOST_REGRESSED]: {
            title: (0, locale_1.t)('Most Regressed'),
            titleTooltip: (0, locale_1.t)('This compares the baseline (%s) of the past with the present.', 'regressed'),
            fields: [],
            dataType: types_1.GenericPerformanceWidgetDataType.trends,
        },
    });
};
exports.WIDGET_DEFINITIONS = WIDGET_DEFINITIONS;
//# sourceMappingURL=widgetDefinitions.jsx.map