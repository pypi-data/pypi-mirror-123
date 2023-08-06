Object.defineProperty(exports, "__esModule", { value: true });
exports.getStatusTooltipDescription = exports.getSourceTooltipDescription = exports.getImageFeatureDescription = void 0;
const tslib_1 = require("tslib");
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const locale_1 = require("app/locale");
const debugImage_1 = require("app/types/debugImage");
const utils_1 = require("../utils");
function getImageFeatureDescription(type) {
    switch (type) {
        case debugImage_1.ImageFeature.has_debug_info:
            return {
                label: (0, locale_1.t)('debug'),
                description: (0, locale_1.t)('Debug information provides function names and resolves inlined frames during symbolication'),
            };
        case debugImage_1.ImageFeature.has_sources:
            return {
                label: (0, locale_1.t)('sources'),
                description: (0, locale_1.t)('Source code information allows Sentry to display source code context for stack frames'),
            };
        case debugImage_1.ImageFeature.has_symbols:
            return {
                label: (0, locale_1.t)('symtab'),
                description: (0, locale_1.t)('Symbol tables are used as a fallback when full debug information is not available'),
            };
        case debugImage_1.ImageFeature.has_unwind_info:
            return {
                label: (0, locale_1.t)('unwind'),
                description: (0, locale_1.t)('Stack unwinding information improves the quality of stack traces extracted from minidumps'),
            };
        default: {
            Sentry.withScope(scope => {
                scope.setLevel(Sentry.Severity.Warning);
                Sentry.captureException(new Error('Unknown image candidate feature'));
            });
            return {}; // this shall not happen
        }
    }
}
exports.getImageFeatureDescription = getImageFeatureDescription;
function getSourceTooltipDescription(source, builtinSymbolSources) {
    if (source === utils_1.INTERNAL_SOURCE) {
        return (0, locale_1.t)("This debug information file is from Sentry's internal symbol server for this project");
    }
    if (builtinSymbolSources === null || builtinSymbolSources === void 0 ? void 0 : builtinSymbolSources.find(builtinSymbolSource => builtinSymbolSource.id === source)) {
        return (0, locale_1.t)('This debug information file is from a built-in symbol server');
    }
    return (0, locale_1.t)('This debug information file is from a custom symbol server');
}
exports.getSourceTooltipDescription = getSourceTooltipDescription;
function getStatusTooltipDescription(candidate, hasReprocessWarning) {
    const { download, location, source } = candidate;
    switch (download.status) {
        case debugImage_1.CandidateDownloadStatus.OK: {
            return {
                label: (0, locale_1.t)('Download Details'),
                description: location,
                disabled: !location || source === utils_1.INTERNAL_SOURCE,
            };
        }
        case debugImage_1.CandidateDownloadStatus.ERROR:
        case debugImage_1.CandidateDownloadStatus.MALFORMED: {
            const { details } = download;
            return {
                label: (0, locale_1.t)('Download Details'),
                description: details,
                disabled: !details,
            };
        }
        case debugImage_1.CandidateDownloadStatus.NOT_FOUND: {
            return {};
        }
        case debugImage_1.CandidateDownloadStatus.NO_PERMISSION: {
            const { details } = download;
            return {
                label: (0, locale_1.t)('Permission Error'),
                description: details,
                disabled: !details,
            };
        }
        case debugImage_1.CandidateDownloadStatus.DELETED: {
            return {
                label: (0, locale_1.t)('This file was deleted after the issue was processed.'),
            };
        }
        case debugImage_1.CandidateDownloadStatus.UNAPPLIED: {
            return {
                label: hasReprocessWarning
                    ? (0, locale_1.t)('This issue was processed before this debug information file was available. To apply new debug information, reprocess this issue.')
                    : (0, locale_1.t)('This issue was processed before this debug information file was available'),
            };
        }
        default: {
            Sentry.withScope(scope => {
                scope.setLevel(Sentry.Severity.Warning);
                Sentry.captureException(new Error('Unknown image candidate download status'));
            });
            return {}; // This shall not happen
        }
    }
}
exports.getStatusTooltipDescription = getStatusTooltipDescription;
//# sourceMappingURL=utils.jsx.map