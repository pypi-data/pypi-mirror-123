Object.defineProperty(exports, "__esModule", { value: true });
const locale_1 = require("app/locale");
const utils_1 = require("app/utils");
const types_1 = require("./types");
function getOperatingSystemKnownDataDetails(data, type) {
    switch (type) {
        case types_1.OperatingSystemKnownDataType.NAME:
            return {
                subject: (0, locale_1.t)('Name'),
                value: data.name,
            };
        case types_1.OperatingSystemKnownDataType.VERSION:
            return {
                subject: (0, locale_1.t)('Version'),
                value: `${data.version}${data.build ? `(${data.build})` : ''}`,
            };
        case types_1.OperatingSystemKnownDataType.KERNEL_VERSION:
            return {
                subject: (0, locale_1.t)('Kernel Version'),
                value: data.kernel_version,
            };
        case types_1.OperatingSystemKnownDataType.ROOTED:
            return {
                subject: (0, locale_1.t)('Rooted'),
                value: (0, utils_1.defined)(data.rooted) ? (data.rooted ? (0, locale_1.t)('yes') : (0, locale_1.t)('no')) : null,
            };
        default:
            return {
                subject: type,
                value: data[type] || null,
            };
    }
}
exports.default = getOperatingSystemKnownDataDetails;
//# sourceMappingURL=getOperatingSystemKnownDataDetails.jsx.map