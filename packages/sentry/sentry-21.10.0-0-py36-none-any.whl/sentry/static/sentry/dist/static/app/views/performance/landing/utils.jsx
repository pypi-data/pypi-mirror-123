Object.defineProperty(exports, "__esModule", { value: true });
exports.getDisplayAxes = exports.vitalCardDetails = exports.getDefaultDisplayFieldForPlatform = exports.getChartWidth = exports.handleLandingDisplayChange = exports.getCurrentLandingDisplay = exports.LANDING_DISPLAYS = exports.LandingDisplayField = exports.RIGHT_AXIS_QUERY_KEY = exports.LEFT_AXIS_QUERY_KEY = void 0;
const react_router_1 = require("react-router");
const locale_1 = require("app/locale");
const formatters_1 = require("app/utils/formatters");
const queryString_1 = require("app/utils/queryString");
const tokenizeSearch_1 = require("app/utils/tokenizeSearch");
const data_1 = require("../data");
const utils_1 = require("../utils");
exports.LEFT_AXIS_QUERY_KEY = 'left';
exports.RIGHT_AXIS_QUERY_KEY = 'right';
var LandingDisplayField;
(function (LandingDisplayField) {
    LandingDisplayField["ALL"] = "all";
    LandingDisplayField["FRONTEND_PAGELOAD"] = "frontend_pageload";
    LandingDisplayField["FRONTEND_OTHER"] = "frontend_other";
    LandingDisplayField["BACKEND"] = "backend";
    LandingDisplayField["MOBILE"] = "mobile";
})(LandingDisplayField = exports.LandingDisplayField || (exports.LandingDisplayField = {}));
exports.LANDING_DISPLAYS = [
    {
        label: 'All Transactions',
        field: LandingDisplayField.ALL,
    },
    {
        label: 'Frontend (Pageload)',
        field: LandingDisplayField.FRONTEND_PAGELOAD,
    },
    {
        label: 'Frontend (Other)',
        field: LandingDisplayField.FRONTEND_OTHER,
    },
    {
        label: 'Backend',
        field: LandingDisplayField.BACKEND,
    },
    {
        label: 'Mobile',
        field: LandingDisplayField.MOBILE,
        isShown: (organization) => organization.features.includes('performance-mobile-vitals'),
        badge: 'new',
    },
];
function getCurrentLandingDisplay(location, projects, eventView) {
    var _a;
    const landingField = (0, queryString_1.decodeScalar)((_a = location === null || location === void 0 ? void 0 : location.query) === null || _a === void 0 ? void 0 : _a.landingDisplay);
    const display = exports.LANDING_DISPLAYS.find(({ field }) => field === landingField);
    if (display) {
        return display;
    }
    const defaultDisplayField = getDefaultDisplayFieldForPlatform(projects, eventView);
    const defaultDisplay = exports.LANDING_DISPLAYS.find(({ field }) => field === defaultDisplayField);
    return defaultDisplay || exports.LANDING_DISPLAYS[0];
}
exports.getCurrentLandingDisplay = getCurrentLandingDisplay;
function handleLandingDisplayChange(field, location) {
    const newQuery = Object.assign({}, location.query);
    delete newQuery[exports.LEFT_AXIS_QUERY_KEY];
    delete newQuery[exports.RIGHT_AXIS_QUERY_KEY];
    // Transaction op can affect the display and show no results if it is explicitly set.
    const query = (0, queryString_1.decodeScalar)(location.query.query, '');
    const searchConditions = new tokenizeSearch_1.MutableSearch(query);
    searchConditions.removeFilter('transaction.op');
    react_router_1.browserHistory.push({
        pathname: location.pathname,
        query: Object.assign(Object.assign({}, newQuery), { query: searchConditions.formatString(), landingDisplay: field }),
    });
}
exports.handleLandingDisplayChange = handleLandingDisplayChange;
function getChartWidth(chartData, refPixelRect) {
    const distance = refPixelRect ? refPixelRect.point2.x - refPixelRect.point1.x : 0;
    const chartWidth = chartData.length * distance;
    return {
        chartWidth,
    };
}
exports.getChartWidth = getChartWidth;
function getDefaultDisplayFieldForPlatform(projects, eventView) {
    var _a;
    if (!eventView) {
        return LandingDisplayField.ALL;
    }
    const projectIds = eventView.project;
    const performanceTypeToDisplay = {
        [utils_1.PROJECT_PERFORMANCE_TYPE.ANY]: LandingDisplayField.ALL,
        [utils_1.PROJECT_PERFORMANCE_TYPE.FRONTEND]: LandingDisplayField.FRONTEND_PAGELOAD,
        [utils_1.PROJECT_PERFORMANCE_TYPE.BACKEND]: LandingDisplayField.BACKEND,
        [utils_1.PROJECT_PERFORMANCE_TYPE.MOBILE]: LandingDisplayField.MOBILE,
    };
    const performanceType = (0, utils_1.platformToPerformanceType)(projects, projectIds);
    const landingField = (_a = performanceTypeToDisplay[performanceType]) !== null && _a !== void 0 ? _a : LandingDisplayField.ALL;
    return landingField;
}
exports.getDefaultDisplayFieldForPlatform = getDefaultDisplayFieldForPlatform;
const vitalCardDetails = (organization) => {
    return {
        'p75(transaction.duration)': {
            title: (0, locale_1.t)('Duration (p75)'),
            tooltip: (0, data_1.getTermHelp)(organization, data_1.PERFORMANCE_TERM.P75),
            formatter: value => (0, formatters_1.getDuration)(value / 1000, value >= 1000 ? 3 : 0, true),
        },
        'tpm()': {
            title: (0, locale_1.t)('Throughput'),
            tooltip: (0, data_1.getTermHelp)(organization, data_1.PERFORMANCE_TERM.THROUGHPUT),
            formatter: formatters_1.formatAbbreviatedNumber,
        },
        'failure_rate()': {
            title: (0, locale_1.t)('Failure Rate'),
            tooltip: (0, data_1.getTermHelp)(organization, data_1.PERFORMANCE_TERM.FAILURE_RATE),
            formatter: value => (0, formatters_1.formatPercentage)(value, 2),
        },
        'apdex()': {
            title: (0, locale_1.t)('Apdex'),
            tooltip: (0, data_1.getTermHelp)(organization, data_1.PERFORMANCE_TERM.APDEX_NEW),
            formatter: value => (0, formatters_1.formatFloat)(value, 4),
        },
        'p75(measurements.frames_slow_rate)': {
            title: (0, locale_1.t)('Slow Frames (p75)'),
            tooltip: (0, data_1.getTermHelp)(organization, data_1.PERFORMANCE_TERM.SLOW_FRAMES),
            formatter: value => (0, formatters_1.formatPercentage)(value, 2),
        },
        'p75(measurements.frames_frozen_rate)': {
            title: (0, locale_1.t)('Frozen Frames (p75)'),
            tooltip: (0, data_1.getTermHelp)(organization, data_1.PERFORMANCE_TERM.FROZEN_FRAMES),
            formatter: value => (0, formatters_1.formatPercentage)(value, 2),
        },
        'p75(measurements.app_start_cold)': {
            title: (0, locale_1.t)('Cold Start (p75)'),
            tooltip: (0, data_1.getTermHelp)(organization, data_1.PERFORMANCE_TERM.APP_START_COLD),
            formatter: value => (0, formatters_1.getDuration)(value / 1000, value >= 1000 ? 3 : 0, true),
        },
        'p75(measurements.app_start_warm)': {
            title: (0, locale_1.t)('Warm Start (p75)'),
            tooltip: (0, data_1.getTermHelp)(organization, data_1.PERFORMANCE_TERM.APP_START_WARM),
            formatter: value => (0, formatters_1.getDuration)(value / 1000, value >= 1000 ? 3 : 0, true),
        },
        'p75(measurements.stall_percentage)': {
            title: (0, locale_1.t)('Stall Percentage (p75)'),
            tooltip: (0, data_1.getTermHelp)(organization, data_1.PERFORMANCE_TERM.STALL_PERCENTAGE),
            formatter: value => (0, formatters_1.formatPercentage)(value, 2),
        },
    };
};
exports.vitalCardDetails = vitalCardDetails;
function getDisplayAxes(options, location) {
    const leftDefault = options.find(opt => opt.isLeftDefault) || options[0];
    const rightDefault = options.find(opt => opt.isRightDefault) || options[1];
    const leftAxis = options.find(opt => opt.value === location.query[exports.LEFT_AXIS_QUERY_KEY]) || leftDefault;
    const rightAxis = options.find(opt => opt.value === location.query[exports.RIGHT_AXIS_QUERY_KEY]) ||
        rightDefault;
    return {
        leftAxis,
        rightAxis,
    };
}
exports.getDisplayAxes = getDisplayAxes;
//# sourceMappingURL=utils.jsx.map