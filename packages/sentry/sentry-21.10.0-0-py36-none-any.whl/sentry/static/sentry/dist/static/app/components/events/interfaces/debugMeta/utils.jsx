Object.defineProperty(exports, "__esModule", { value: true });
exports.getFileName = exports.combineStatus = void 0;
function getStatusWeight(status) {
    switch (status) {
        case null:
        case undefined:
        case 'unused':
            return 0;
        case 'found':
            return 1;
        default:
            return 2;
    }
}
function combineStatus(debugStatus, unwindStatus) {
    const debugWeight = getStatusWeight(debugStatus);
    const unwindWeight = getStatusWeight(unwindStatus);
    const combined = debugWeight >= unwindWeight ? debugStatus : unwindStatus;
    return combined || 'unused';
}
exports.combineStatus = combineStatus;
function getFileName(path) {
    const directorySeparator = /^([a-z]:\\|\\\\)/i.test(path) ? '\\' : '/';
    return path.split(directorySeparator).pop();
}
exports.getFileName = getFileName;
//# sourceMappingURL=utils.jsx.map