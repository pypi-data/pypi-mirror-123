Object.defineProperty(exports, "__esModule", { value: true });
exports.getImageAddress = exports.shouldSkipSection = exports.normalizeId = exports.getFileName = exports.combineStatus = exports.getStatusWeight = exports.IMAGE_AND_CANDIDATE_LIST_MAX_HEIGHT = void 0;
const react_1 = require("react");
const utils_1 = require("app/components/events/interfaces/utils");
const debugImage_1 = require("app/types/debugImage");
const utils_2 = require("app/utils");
const IMAGE_ADDR_LEN = 12;
exports.IMAGE_AND_CANDIDATE_LIST_MAX_HEIGHT = 400;
function getStatusWeight(status) {
    switch (status) {
        case null:
        case undefined:
        case debugImage_1.ImageStatus.UNUSED:
            return 0;
        case debugImage_1.ImageStatus.FOUND:
            return 1;
        default:
            return 2;
    }
}
exports.getStatusWeight = getStatusWeight;
function combineStatus(debugStatus, unwindStatus) {
    const debugWeight = getStatusWeight(debugStatus);
    const unwindWeight = getStatusWeight(unwindStatus);
    const combined = debugWeight >= unwindWeight ? debugStatus : unwindStatus;
    return combined || debugImage_1.ImageStatus.UNUSED;
}
exports.combineStatus = combineStatus;
function getFileName(path) {
    if (!path) {
        return undefined;
    }
    const directorySeparator = /^([a-z]:\\|\\\\)/i.test(path) ? '\\' : '/';
    return path.split(directorySeparator).pop();
}
exports.getFileName = getFileName;
function normalizeId(id) {
    var _a;
    return (_a = id === null || id === void 0 ? void 0 : id.trim().toLowerCase().replace(/[- ]/g, '')) !== null && _a !== void 0 ? _a : '';
}
exports.normalizeId = normalizeId;
// TODO(ts): When replacing debugMeta with debugMetaV2, also replace {type: string} with the Image type defined in 'app/types/debugImage'
function shouldSkipSection(filteredImages, images) {
    if (!!filteredImages.length) {
        return false;
    }
    const definedImages = images.filter(image => (0, utils_2.defined)(image));
    if (!definedImages.length) {
        return true;
    }
    if (definedImages.every(image => image.type === 'proguard')) {
        return true;
    }
    return false;
}
exports.shouldSkipSection = shouldSkipSection;
function getImageAddress(image) {
    const [startAddress, endAddress] = (0, utils_1.getImageRange)(image);
    if (startAddress && endAddress) {
        return (<react_1.Fragment>
        <span>{(0, utils_1.formatAddress)(startAddress, IMAGE_ADDR_LEN)}</span>
        {' \u2013 '}
        <span>{(0, utils_1.formatAddress)(endAddress, IMAGE_ADDR_LEN)}</span>
      </react_1.Fragment>);
    }
    return undefined;
}
exports.getImageAddress = getImageAddress;
//# sourceMappingURL=utils.jsx.map