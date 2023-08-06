Object.defineProperty(exports, "__esModule", { value: true });
exports.getFieldOrBackup = exports.getBackupField = exports.getBackupAxes = exports.getBackupAxisOption = exports.getAxisOrBackupAxis = void 0;
function getAxisOrBackupAxis(axis, usingBackupAxis) {
    var _a;
    const displayedAxis = usingBackupAxis ? (_a = getBackupAxisOption(axis)) !== null && _a !== void 0 ? _a : axis : axis;
    return displayedAxis;
}
exports.getAxisOrBackupAxis = getAxisOrBackupAxis;
function getBackupAxisOption(axis) {
    return axis.backupOption;
}
exports.getBackupAxisOption = getBackupAxisOption;
function getBackupAxes(axes, usingBackupAxis) {
    return usingBackupAxis ? axes.map(axis => { var _a; return (_a = getBackupAxisOption(axis)) !== null && _a !== void 0 ? _a : axis; }) : axes;
}
exports.getBackupAxes = getBackupAxes;
function getBackupField(axis) {
    const backupOption = getBackupAxisOption(axis);
    if (!backupOption) {
        return undefined;
    }
    return backupOption.field;
}
exports.getBackupField = getBackupField;
function getFieldOrBackup(field, backupField) {
    return backupField !== null && backupField !== void 0 ? backupField : field;
}
exports.getFieldOrBackup = getFieldOrBackup;
//# sourceMappingURL=utils.jsx.map