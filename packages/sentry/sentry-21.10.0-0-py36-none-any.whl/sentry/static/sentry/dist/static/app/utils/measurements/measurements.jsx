Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const constants_1 = require("app/utils/performance/vitals/constants");
function measurementsFromDetails(details) {
    return Object.fromEntries(Object.entries(details).map(([key, value]) => {
        const newValue = {
            name: value.name,
            key,
        };
        return [key, newValue];
    }));
}
const MOBILE_MEASUREMENTS = measurementsFromDetails(constants_1.MOBILE_VITAL_DETAILS);
const WEB_MEASUREMENTS = measurementsFromDetails(constants_1.WEB_VITAL_DETAILS);
function Measurements({ organization, children }) {
    const measurements = organization.features.includes('performance-mobile-vitals')
        ? Object.assign(Object.assign({}, WEB_MEASUREMENTS), MOBILE_MEASUREMENTS) : WEB_MEASUREMENTS;
    return <React.Fragment>{children({ measurements })}</React.Fragment>;
}
exports.default = Measurements;
//# sourceMappingURL=measurements.jsx.map