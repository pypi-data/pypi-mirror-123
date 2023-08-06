Object.defineProperty(exports, "__esModule", { value: true });
exports.isMobilePlatform = exports.isNativePlatform = void 0;
const platformCategories_1 = require("app/data/platformCategories");
function isNativePlatform(platform) {
    switch (platform) {
        case 'cocoa':
        case 'objc':
        case 'native':
        case 'swift':
        case 'c':
            return true;
        default:
            return false;
    }
}
exports.isNativePlatform = isNativePlatform;
function isMobilePlatform(platform) {
    if (!platform) {
        return false;
    }
    return [...platformCategories_1.mobile].includes(platform);
}
exports.isMobilePlatform = isMobilePlatform;
//# sourceMappingURL=platform.jsx.map