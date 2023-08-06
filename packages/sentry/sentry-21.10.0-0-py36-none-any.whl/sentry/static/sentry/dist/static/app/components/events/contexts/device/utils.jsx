Object.defineProperty(exports, "__esModule", { value: true });
exports.getInferredData = exports.commonDisplayResolutions = exports.formatStorage = exports.formatMemory = void 0;
const utils_1 = require("app/utils");
const types_1 = require("./types");
function formatMemory(memory_size, free_memory, usable_memory) {
    if (!Number.isInteger(memory_size) ||
        memory_size <= 0 ||
        !Number.isInteger(free_memory) ||
        free_memory <= 0) {
        return null;
    }
    let memory = `Total: ${(0, utils_1.formatBytesBase2)(memory_size)} / Free: ${(0, utils_1.formatBytesBase2)(free_memory)}`;
    if (Number.isInteger(usable_memory) && usable_memory > 0) {
        memory = `${memory} / Usable: ${(0, utils_1.formatBytesBase2)(usable_memory)}`;
    }
    return memory;
}
exports.formatMemory = formatMemory;
function formatStorage(storage_size, free_storage, external_storage_size, external_free_storage) {
    if (!Number.isInteger(storage_size) || storage_size <= 0) {
        return null;
    }
    let storage = `Total: ${(0, utils_1.formatBytesBase2)(storage_size)}`;
    if (Number.isInteger(free_storage) && free_storage > 0) {
        storage = `${storage} / Free: ${(0, utils_1.formatBytesBase2)(free_storage)}`;
    }
    if (Number.isInteger(external_storage_size) &&
        external_storage_size > 0 &&
        Number.isInteger(external_free_storage) &&
        external_free_storage > 0) {
        storage = `${storage} (External Total: ${(0, utils_1.formatBytesBase2)(external_storage_size)} / Free: ${(0, utils_1.formatBytesBase2)(external_free_storage)})`;
    }
    return storage;
}
exports.formatStorage = formatStorage;
// List of common display resolutions taken from the source: https://en.wikipedia.org/wiki/Display_resolution#Common_display_resolutions
exports.commonDisplayResolutions = {
    '640x360': 'nHD',
    '800x600': 'SVGA',
    '1024x768': 'XGA',
    '1280x720': 'WXGA',
    '1280x800': 'WXGA',
    '1280x1024': 'SXGA',
    '1360x768': 'HD',
    '1366x768': 'HD',
    '1440x900': 'WXGA+',
    '1536x864': 'NA',
    '1600x900': 'HD+',
    '1680x1050': 'WSXGA+',
    '1920x1080': 'FHD',
    '1920x1200': 'WUXGA',
    '2048x1152': 'QWXGA',
    '2560x1080': 'N/A',
    '2560x1440': 'QHD',
    '3440x1440': 'N/A',
    '3840x2160': '4K UHD',
};
function getInferredData(data) {
    const screenResolution = data[types_1.DeviceKnownDataType.SCREEN_RESOLUTION];
    const screenWidth = data[types_1.DeviceKnownDataType.SCREEN_WIDTH_PIXELS];
    const screenHeight = data[types_1.DeviceKnownDataType.SCREEN_HEIGHT_PIXELS];
    if (screenResolution) {
        const displayResolutionDescription = exports.commonDisplayResolutions[screenResolution];
        const commonData = Object.assign(Object.assign({}, data), { [types_1.DeviceKnownDataType.SCREEN_RESOLUTION]: displayResolutionDescription
                ? `${screenResolution} (${displayResolutionDescription})`
                : screenResolution });
        if (!(0, utils_1.defined)(screenWidth) && !(0, utils_1.defined)(screenHeight)) {
            const [width, height] = screenResolution.split('x');
            if (width && height) {
                return Object.assign(Object.assign({}, commonData), { [types_1.DeviceKnownDataType.SCREEN_WIDTH_PIXELS]: Number(width), [types_1.DeviceKnownDataType.SCREEN_HEIGHT_PIXELS]: Number(height) });
            }
        }
        return commonData;
    }
    if ((0, utils_1.defined)(screenWidth) && (0, utils_1.defined)(screenHeight)) {
        const displayResolution = `${screenWidth}x${screenHeight}`;
        const displayResolutionDescription = exports.commonDisplayResolutions[displayResolution];
        return Object.assign(Object.assign({}, data), { [types_1.DeviceKnownDataType.SCREEN_RESOLUTION]: displayResolutionDescription
                ? `${displayResolution} (${displayResolutionDescription})`
                : displayResolution });
    }
    return data;
}
exports.getInferredData = getInferredData;
//# sourceMappingURL=utils.jsx.map