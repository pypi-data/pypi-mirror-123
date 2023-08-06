Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const locale_1 = require("app/locale");
const formatMemory_1 = (0, tslib_1.__importDefault)(require("./formatMemory"));
const types_1 = require("./types");
function getGPUKnownDataDetails(data, type) {
    switch (type) {
        case types_1.GPUKnownDataType.NAME:
            return {
                subject: (0, locale_1.t)('Name'),
                value: data.name,
            };
        case types_1.GPUKnownDataType.VERSION:
            return {
                subject: (0, locale_1.t)('Version'),
                value: data.version,
            };
        case types_1.GPUKnownDataType.MEMORY:
            return {
                subject: (0, locale_1.t)('Memory'),
                value: data.memory_size ? (0, formatMemory_1.default)(data.memory_size) : undefined,
            };
        case types_1.GPUKnownDataType.NPOT_SUPPORT:
            return {
                subject: (0, locale_1.t)('NPOT Support'),
                value: data.npot_support,
            };
        case types_1.GPUKnownDataType.MULTI_THREAD_RENDERING:
            return {
                subject: (0, locale_1.t)('Multi-Thread rendering'),
                value: data.multi_threaded_rendering,
            };
        case types_1.GPUKnownDataType.API_TYPE:
            return {
                subject: (0, locale_1.t)('API Type'),
                value: data.api_type,
            };
        case types_1.GPUKnownDataType.VENDOR_ID:
            return {
                subject: (0, locale_1.t)('Vendor ID'),
                value: data.vendor_id,
            };
        case types_1.GPUKnownDataType.ID:
            return {
                subject: (0, locale_1.t)('GPU ID'),
                value: data.id,
            };
        default:
            return {
                subject: type,
                value: data[type],
            };
    }
}
exports.default = getGPUKnownDataDetails;
//# sourceMappingURL=getGPUKnownDataDetails.jsx.map