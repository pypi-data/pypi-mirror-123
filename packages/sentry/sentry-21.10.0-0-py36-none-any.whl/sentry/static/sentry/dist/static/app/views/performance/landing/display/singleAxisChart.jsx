Object.defineProperty(exports, "__esModule", { value: true });
exports.SingleAxisChart = void 0;
const tslib_1 = require("tslib");
const durationChart_1 = (0, tslib_1.__importDefault)(require("../chart/durationChart"));
const histogramChart_1 = (0, tslib_1.__importDefault)(require("../chart/histogramChart"));
const utils_1 = require("./utils");
function SingleAxisChart(props) {
    const { axis, onFilterChange, eventView, organization, location, didReceiveMultiAxis, usingBackupAxis, } = props;
    const backupField = (0, utils_1.getBackupField)(axis);
    function didReceiveMulti(dataCounts) {
        if (!didReceiveMultiAxis) {
            return;
        }
        if (dataCounts[axis.field]) {
            didReceiveMultiAxis(false);
            return;
        }
        if (backupField && dataCounts[backupField]) {
            didReceiveMultiAxis(true);
            return;
        }
    }
    const axisOrBackup = (0, utils_1.getAxisOrBackupAxis)(axis, usingBackupAxis);
    return axis.isDistribution ? (<histogramChart_1.default field={axis.field} eventView={eventView} organization={organization} location={location} onFilterChange={onFilterChange} title={axisOrBackup.label} titleTooltip={axisOrBackup.tooltip} didReceiveMultiAxis={didReceiveMulti} usingBackupAxis={usingBackupAxis} backupField={backupField}/>) : (<durationChart_1.default field={axis.field} eventView={eventView} organization={organization} title={axisOrBackup.label} titleTooltip={axisOrBackup.tooltip} usingBackupAxis={usingBackupAxis} backupField={backupField}/>);
}
exports.SingleAxisChart = SingleAxisChart;
//# sourceMappingURL=singleAxisChart.jsx.map