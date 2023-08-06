Object.defineProperty(exports, "__esModule", { value: true });
exports.getFeatureTooltip = exports.getFileType = void 0;
const locale_1 = require("app/locale");
const debugFiles_1 = require("app/types/debugFiles");
function getFileType(dsym) {
    var _a;
    switch ((_a = dsym.data) === null || _a === void 0 ? void 0 : _a.type) {
        case debugFiles_1.DebugFileType.EXE:
            return (0, locale_1.t)('executable');
        case debugFiles_1.DebugFileType.DBG:
            return (0, locale_1.t)('debug companion');
        case debugFiles_1.DebugFileType.LIB:
            return (0, locale_1.t)('dynamic library');
        default:
            return null;
    }
}
exports.getFileType = getFileType;
function getFeatureTooltip(feature) {
    switch (feature) {
        case debugFiles_1.DebugFileFeature.SYMTAB:
            return (0, locale_1.t)('Symbol tables are used as a fallback when full debug information is not available');
        case debugFiles_1.DebugFileFeature.DEBUG:
            return (0, locale_1.t)('Debug information provides function names and resolves inlined frames during symbolication');
        case debugFiles_1.DebugFileFeature.UNWIND:
            return (0, locale_1.t)('Stack unwinding information improves the quality of stack traces extracted from minidumps');
        case debugFiles_1.DebugFileFeature.SOURCES:
            return (0, locale_1.t)('Source code information allows Sentry to display source code context for stack frames');
        default:
            return null;
    }
}
exports.getFeatureTooltip = getFeatureTooltip;
//# sourceMappingURL=utils.jsx.map