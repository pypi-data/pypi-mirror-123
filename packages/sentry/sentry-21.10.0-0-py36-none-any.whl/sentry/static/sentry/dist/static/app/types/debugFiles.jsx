Object.defineProperty(exports, "__esModule", { value: true });
exports.CustomRepoType = exports.DebugFileFeature = exports.DebugFileType = void 0;
var DebugFileType;
(function (DebugFileType) {
    DebugFileType["EXE"] = "exe";
    DebugFileType["DBG"] = "dbg";
    DebugFileType["LIB"] = "lib";
})(DebugFileType = exports.DebugFileType || (exports.DebugFileType = {}));
var DebugFileFeature;
(function (DebugFileFeature) {
    DebugFileFeature["SYMTAB"] = "symtab";
    DebugFileFeature["DEBUG"] = "debug";
    DebugFileFeature["UNWIND"] = "unwind";
    DebugFileFeature["SOURCES"] = "sources";
})(DebugFileFeature = exports.DebugFileFeature || (exports.DebugFileFeature = {}));
// Custom Repositories
var CustomRepoType;
(function (CustomRepoType) {
    CustomRepoType["HTTP"] = "http";
    CustomRepoType["S3"] = "s3";
    CustomRepoType["GCS"] = "gcs";
    CustomRepoType["APP_STORE_CONNECT"] = "appStoreConnect";
})(CustomRepoType = exports.CustomRepoType || (exports.CustomRepoType = {}));
//# sourceMappingURL=debugFiles.jsx.map