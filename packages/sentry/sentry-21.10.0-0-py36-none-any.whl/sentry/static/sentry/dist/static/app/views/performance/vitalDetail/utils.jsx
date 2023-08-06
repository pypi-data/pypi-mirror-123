Object.defineProperty(exports, "__esModule", { value: true });
exports.getMaxOfSeries = exports.vitalAbbreviations = exports.vitalDescription = exports.vitalChartTitleMap = exports.vitalMap = exports.getVitalDetailTableMehStatusFunction = exports.getVitalDetailTablePoorStatusFunction = exports.vitalNameFromLocation = exports.vitalDetailRouteWithQuery = exports.vitalStateIcons = exports.vitalStateColors = exports.VitalState = exports.webVitalMeh = exports.webVitalPoor = exports.generateVitalDetailRoute = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const icons_1 = require("app/icons");
const fields_1 = require("app/utils/discover/fields");
const queryString_1 = require("app/utils/queryString");
function generateVitalDetailRoute({ orgSlug }) {
    return `/organizations/${orgSlug}/performance/vitaldetail/`;
}
exports.generateVitalDetailRoute = generateVitalDetailRoute;
exports.webVitalPoor = {
    [fields_1.WebVital.FP]: 3000,
    [fields_1.WebVital.FCP]: 3000,
    [fields_1.WebVital.LCP]: 4000,
    [fields_1.WebVital.FID]: 300,
    [fields_1.WebVital.CLS]: 0.25,
};
exports.webVitalMeh = {
    [fields_1.WebVital.FP]: 1000,
    [fields_1.WebVital.FCP]: 1000,
    [fields_1.WebVital.LCP]: 2500,
    [fields_1.WebVital.FID]: 100,
    [fields_1.WebVital.CLS]: 0.1,
};
var VitalState;
(function (VitalState) {
    VitalState["POOR"] = "Poor";
    VitalState["MEH"] = "Meh";
    VitalState["GOOD"] = "Good";
})(VitalState = exports.VitalState || (exports.VitalState = {}));
exports.vitalStateColors = {
    [VitalState.POOR]: 'red300',
    [VitalState.MEH]: 'yellow300',
    [VitalState.GOOD]: 'green300',
};
exports.vitalStateIcons = {
    [VitalState.POOR]: <icons_1.IconFire color={exports.vitalStateColors[VitalState.POOR]}/>,
    [VitalState.MEH]: <icons_1.IconWarning color={exports.vitalStateColors[VitalState.MEH]}/>,
    [VitalState.GOOD]: (<icons_1.IconCheckmark color={exports.vitalStateColors[VitalState.GOOD]} isCircled/>),
};
function vitalDetailRouteWithQuery({ orgSlug, vitalName, projectID, query, }) {
    const pathname = generateVitalDetailRoute({
        orgSlug,
    });
    return {
        pathname,
        query: {
            vitalName,
            project: projectID,
            environment: query.environment,
            statsPeriod: query.statsPeriod,
            start: query.start,
            end: query.end,
            query: query.query,
        },
    };
}
exports.vitalDetailRouteWithQuery = vitalDetailRouteWithQuery;
function vitalNameFromLocation(location) {
    const _vitalName = (0, queryString_1.decodeScalar)(location.query.vitalName);
    const vitalName = Object.values(fields_1.WebVital).find(v => v === _vitalName);
    if (vitalName) {
        return vitalName;
    }
    else {
        return fields_1.WebVital.LCP;
    }
}
exports.vitalNameFromLocation = vitalNameFromLocation;
function getVitalDetailTablePoorStatusFunction(vitalName) {
    const vitalThreshold = exports.webVitalPoor[vitalName];
    const statusFunction = `compare_numeric_aggregate(${(0, fields_1.getAggregateAlias)(`p75(${vitalName})`)},greater,${vitalThreshold})`;
    return statusFunction;
}
exports.getVitalDetailTablePoorStatusFunction = getVitalDetailTablePoorStatusFunction;
function getVitalDetailTableMehStatusFunction(vitalName) {
    const vitalThreshold = exports.webVitalMeh[vitalName];
    const statusFunction = `compare_numeric_aggregate(${(0, fields_1.getAggregateAlias)(`p75(${vitalName})`)},greater,${vitalThreshold})`;
    return statusFunction;
}
exports.getVitalDetailTableMehStatusFunction = getVitalDetailTableMehStatusFunction;
exports.vitalMap = {
    [fields_1.WebVital.FCP]: 'First Contentful Paint',
    [fields_1.WebVital.CLS]: 'Cumulative Layout Shift',
    [fields_1.WebVital.FID]: 'First Input Delay',
    [fields_1.WebVital.LCP]: 'Largest Contentful Paint',
};
exports.vitalChartTitleMap = exports.vitalMap;
exports.vitalDescription = {
    [fields_1.WebVital.FCP]: 'First Contentful Paint (FCP) measures the amount of time the first content takes to render in the viewport. Like FP, this could also show up in any form from the document object model (DOM), such as images, SVGs, or text blocks.',
    [fields_1.WebVital.CLS]: 'Cumulative Layout Shift (CLS) is the sum of individual layout shift scores for every unexpected element shift during the rendering process. Imagine navigating to an article and trying to click a link before the page finishes loading. Before your cursor even gets there, the link may have shifted down due to an image rendering. Rather than using duration for this Web Vital, the CLS score represents the degree of disruptive and visually unstable shifts.',
    [fields_1.WebVital.FID]: 'First Input Delay measures the response time when the user tries to interact with the viewport. Actions maybe include clicking a button, link or other custom Javascript controller. It is key in helping the user determine if a page is usable or not.',
    [fields_1.WebVital.LCP]: 'Largest Contentful Paint (LCP) measures the render time for the largest content to appear in the viewport. This may be in any form from the document object model (DOM), such as images, SVGs, or text blocks. It’s the largest pixel area in the viewport, thus most visually defining. LCP helps developers understand how long it takes to see the main content on the page.',
};
exports.vitalAbbreviations = {
    [fields_1.WebVital.FCP]: 'FCP',
    [fields_1.WebVital.CLS]: 'CLS',
    [fields_1.WebVital.FID]: 'FID',
    [fields_1.WebVital.LCP]: 'LCP',
};
function getMaxOfSeries(series) {
    let max = -Infinity;
    for (const { data } of series) {
        for (const point of data) {
            max = Math.max(max, point.value);
        }
    }
    return max;
}
exports.getMaxOfSeries = getMaxOfSeries;
//# sourceMappingURL=utils.jsx.map