Object.defineProperty(exports, "__esModule", { value: true });
exports.ImageStatus = exports.CandidateDownloadStatus = exports.ImageFeature = exports.SymbolType = exports.CandidateProcessingStatus = void 0;
// Candidate Processing Info
var CandidateProcessingStatus;
(function (CandidateProcessingStatus) {
    CandidateProcessingStatus["OK"] = "ok";
    CandidateProcessingStatus["MALFORMED"] = "malformed";
    CandidateProcessingStatus["ERROR"] = "error";
})(CandidateProcessingStatus = exports.CandidateProcessingStatus || (exports.CandidateProcessingStatus = {}));
var SymbolType;
(function (SymbolType) {
    SymbolType["UNKNOWN"] = "unknown";
    SymbolType["BREAKPAD"] = "breakpad";
    SymbolType["ELF"] = "elf";
    SymbolType["MACHO"] = "macho";
    SymbolType["PDB"] = "pdb";
    SymbolType["PE"] = "pe";
    SymbolType["SOURCEBUNDLE"] = "sourcebundle";
    SymbolType["WASM"] = "wasm";
    SymbolType["PROGUARD"] = "proguard";
})(SymbolType = exports.SymbolType || (exports.SymbolType = {}));
var ImageFeature;
(function (ImageFeature) {
    ImageFeature["has_sources"] = "has_sources";
    ImageFeature["has_debug_info"] = "has_debug_info";
    ImageFeature["has_unwind_info"] = "has_unwind_info";
    ImageFeature["has_symbols"] = "has_symbols";
})(ImageFeature = exports.ImageFeature || (exports.ImageFeature = {}));
// Candidate Download Status
var CandidateDownloadStatus;
(function (CandidateDownloadStatus) {
    CandidateDownloadStatus["OK"] = "ok";
    CandidateDownloadStatus["MALFORMED"] = "malformed";
    CandidateDownloadStatus["NOT_FOUND"] = "notfound";
    CandidateDownloadStatus["ERROR"] = "error";
    CandidateDownloadStatus["NO_PERMISSION"] = "noperm";
    CandidateDownloadStatus["DELETED"] = "deleted";
    CandidateDownloadStatus["UNAPPLIED"] = "unapplied";
})(CandidateDownloadStatus = exports.CandidateDownloadStatus || (exports.CandidateDownloadStatus = {}));
// Debug Status
var ImageStatus;
(function (ImageStatus) {
    ImageStatus["FOUND"] = "found";
    ImageStatus["UNUSED"] = "unused";
    ImageStatus["MISSING"] = "missing";
    ImageStatus["MALFORMED"] = "malformed";
    ImageStatus["FETCHING_FAILED"] = "fetching_failed";
    ImageStatus["TIMEOUT"] = "timeout";
    ImageStatus["OTHER"] = "other";
})(ImageStatus = exports.ImageStatus || (exports.ImageStatus = {}));
//# sourceMappingURL=debugImage.jsx.map